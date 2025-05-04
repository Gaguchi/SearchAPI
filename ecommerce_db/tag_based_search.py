import sqlite3
import requests
import json
import argparse
import os
import sys
from typing import List, Dict, Any

# Database connection
DB_FILE = 'simplified_ecommerce.db'

# Ollama API config
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma:7b"  # Using Gemma as a default model

# Debug mode flag - can be enabled with environment variable
DEBUG_MODE = os.environ.get('DEBUG_SEARCH', '0') == '1'

def debug_print(*args, **kwargs):
    """Print debug information if debug mode is enabled"""
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs, flush=True)
        # Also log to a file for easier viewing
        with open("search_debug.log", "a", encoding="utf-8") as f:
            print("[DEBUG]", *args, **kwargs, file=f)

def get_all_tags():
    """Get all available tags from the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM tags ORDER BY name")
    tags = cursor.fetchall()
    conn.close()
    return tags

def get_tag_focused_products():
    """
    Get all products with their associated tags
    Returns a list of products with tags included
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cursor = conn.cursor()
    
    # Get all products with basic info
    cursor.execute("""
        SELECT p.id, p.name, p.short_description, p.price, p.sale_price, 
               c.name as category
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = 1
    """)
    
    products = []
    for row in cursor.fetchall():
        product = dict(row)
        
        # Get tags for this product
        cursor.execute("""
            SELECT t.name
            FROM product_tags pt
            JOIN tags t ON pt.tag_id = t.id
            WHERE pt.product_id = ?
        """, (product['id'],))
        
        product['tags'] = [tag[0] for tag in cursor.fetchall()]
        products.append(product)
    
    conn.close()
    return products

def select_relevant_tags(user_query: str, all_tags: List) -> List[str]:
    """
    Manually select relevant tags based on the search query 
    without requiring an AI API call.
    
    This function implements a simple rules-based approach that:
    1. Looks for direct matches between query words and tags
    2. Handles common synonyms and related concepts
    3. Returns a prioritized list of tags relevant to the query
    """
    query_words = user_query.lower().split()
    
    # Get all tag names from the all_tags list
    tag_names = [tag[1] for tag in all_tags]
    
    # Direct matches - look for tags directly mentioned in the query
    direct_matches = []
    for tag in tag_names:
        tag_lower = tag.lower()
        # Check if tag is directly mentioned in the query
        if tag_lower in user_query.lower():
            direct_matches.append(tag)
            continue
        
        # Check if any query word is in the tag (or vice versa)
        for word in query_words:
            if (word in tag_lower) or (tag_lower in word):
                if len(word) > 3:  # Only consider meaningful words
                    direct_matches.append(tag)
                    break
    
    # Known mappings for common search concepts to tags
    concept_to_tags = {
        "noise cancellation": ["Noise-cancelling", "Premium", "Headphones"],
        "wireless": ["Wireless", "Bluetooth"],
        "headphones": ["Headphones", "Earbuds", "Audio"],
        "earbuds": ["Earbuds", "Portable", "Wireless"],
        "bluetooth": ["Bluetooth", "Wireless"],
        "gaming": ["Gaming", "High-performance"],
        "cheap": ["Budget", "Sale"],
        "affordable": ["Budget", "Sale"],
        "budget": ["Budget"],
        "high quality": ["Premium", "High-resolution"],
        "premium": ["Premium"],
        "fast": ["Fast-charging", "High-performance"],
        "long battery": ["Long-battery", "Rechargeable"],
        "durable": ["Durable", "Rugged"],
        "sports": ["Sports", "Waterproof", "Portable"],
        "kids": ["Children", "Family"],
        "work": ["Professional", "Office"],
        "professional": ["Professional"],
        "travel": ["Travel", "Portable", "Lightweight"],
        "water resistant": ["Waterproof"],
        "waterproof": ["Waterproof"],
        "apple": ["Apple"],
        "samsung": ["Samsung"],
        "sony": ["Sony"],
        "bose": ["Bose"],
        "loud": ["Surround-sound", "High-performance"],
        "powerful": ["High-performance"],
        "4k": ["4K", "Ultra-HD"],
        "hd": ["HD", "4K", "Ultra-HD"],
        "tv": ["QLED", "OLED", "Smart", "Entertainment"],
        "phone": ["Smartphone", "5G"],
        "smartphone": ["Smartphone"],
        "laptop": ["Laptop"],
        "computer": ["Laptop"],
        "tablet": ["Tablet"],
        "camera": ["Camera", "High-resolution"],
        "speaker": ["Speaker"],
        "watch": ["Watch", "Fitness-tracker"],
        "fitness": ["Fitness-tracker", "Exercise"],
        "keyboard": ["Keyboard"],
        "mouse": ["Mouse"],
    }
    
    # Concept matches - check if any known concepts are in the query
    concept_matches = []
    for concept, related_tags in concept_to_tags.items():
        # Check if the concept appears in the query
        if concept in user_query.lower():
            concept_matches.extend(related_tags)
            continue
            
        # Check for partial word matches
        for word in query_words:
            if (word in concept) or (concept in word):
                if len(word) > 3:  # Only consider meaningful words
                    concept_matches.extend(related_tags)
                    break
    
    # Combine matches, prioritizing direct matches and removing duplicates
    all_matches = []
    
    # First add direct matches
    for tag in direct_matches:
        if tag not in all_matches and tag in tag_names:
            all_matches.append(tag)
    
    # Then add concept matches if not already included
    for tag in concept_matches:
        if tag not in all_matches and tag in tag_names:
            all_matches.append(tag)
    
    # Limit to maximum 10 tags
    return all_matches[:10]

def tag_based_search(user_query: str) -> List[Dict[str, Any]]:
    """
    Search for products based on user query, focusing primarily on tags
    """
    # Connect to the database and log the search
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO search_logs (search_query, search_date) VALUES (?, datetime('now'))",
            (user_query,)
        )
        conn.commit()
        
        # Get all products with their tags
        products = get_tag_focused_products()
        debug_print(f"Loaded {len(products)} products with tags")
        
        # Get all available tags for reference
        all_tags = get_all_tags()
        debug_print(f"Found {len(all_tags)} total tags in system")
        
        # First try our manual tag selection function
        relevant_tags = select_relevant_tags(user_query, all_tags)
        debug_print(f"Selected relevant tags: {relevant_tags}")
        
        # Only proceed with AI tag analysis if specifically requested with ENABLE_AI=1
        if os.environ.get('ENABLE_AI', '0') == '1':
            debug_print("AI tag analysis enabled, proceeding with API call...")
            
            # Create a prompt for the AI to analyze tags
            tag_analysis_prompt = f"""<start_of_turn>user
I need you to analyze a user's product search query and identify which product tags are most relevant to their search.

User search query: "{user_query}"

Here are all available product tags in our system:
{[tag[1] for tag in all_tags]}

Please identify the 5-10 most relevant tags from this list that match the user's search intent. Consider:
1. Direct mentions of product types (headphones, laptop, etc.)
2. Features or characteristics specifically mentioned (wireless, waterproof, etc.)
3. Use cases or activities mentioned (gaming, travel, etc.)
4. Technical specifications that might be relevant (5G, OLED, etc.)
5. Implied needs (e.g., "long lasting" might suggest "Long-battery" tag)

Respond with a JSON array of tag names, sorted by relevance:
["TagName1", "TagName2", "TagName3", ...]
<end_of_turn>

<start_of_turn>assistant
"""
            
            debug_print("Sending tag analysis query to AI model...")
            
            # Call the AI to analyze the tags
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": tag_analysis_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2  # Low temperature for more deterministic results
                    }
                }
            )
            response.raise_for_status()
            
            # Parse the AI response to get relevant tags
            ai_response = response.json().get('response', '')
            debug_print(f"AI response: {ai_response}")
            
            # Find JSON array in response
            start_idx = ai_response.find('[')
            end_idx = ai_response.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                tags_json = ai_response[start_idx:end_idx]
                try:
                    ai_relevant_tags = json.loads(tags_json)
                    debug_print(f"AI identified relevant tags: {ai_relevant_tags}")
                    # Combine with our manually selected tags, prioritizing AI selections
                    for tag in ai_relevant_tags:
                        if tag not in relevant_tags:
                            relevant_tags.insert(0, tag)
                    relevant_tags = relevant_tags[:10]  # Keep top 10
                except json.JSONDecodeError:
                    debug_print("Failed to parse JSON array of tags, using manually selected tags")
        else:
            debug_print("AI tag analysis disabled, using only manually selected tags")
            
        # Score products based on tag matches
        scored_products = []
        for product in products:
            # Calculate tag match score
            product_tags = [tag.lower() for tag in product['tags']]
            tag_matches = sum(1 for tag in relevant_tags if tag.lower() in product_tags)
            
            # Also check if any tags are found in name or description
            name_desc_matches = sum(1 for tag in relevant_tags 
                              if tag.lower() in product['name'].lower() or 
                                 tag.lower() in product['short_description'].lower())
            
            # Combined score with higher weight for tag matches
            match_score = (tag_matches * 2) + name_desc_matches
            
            if match_score > 0:
                product['match_score'] = match_score
                scored_products.append(product)
        
        # Sort products by match score (highest first)
        scored_products.sort(key=lambda p: p['match_score'], reverse=True)
        
        # Update search log with results count - Fix the SQL syntax error here
        cursor.execute(
            "UPDATE search_logs SET results_count = ? WHERE id = (SELECT MAX(id) FROM search_logs WHERE search_query = ?)",
            (len(scored_products), user_query)
        )
        conn.commit()
        
        conn.close()
        return scored_products[:10]  # Return top 10 results
        
    except Exception as e:
        debug_print(f"Error in tag_based_search: {str(e)}")
        conn.close()
        
        # Fall back to simple keyword search
        return keyword_search(user_query)

def keyword_search(query: str) -> List[Dict[str, Any]]:
    """
    Simple keyword-based search as a fallback
    """
    debug_print(f"Falling back to keyword search for: {query}")
    
    # Break the query into keywords
    keywords = [k.strip().lower() for k in query.split() if len(k.strip()) > 3]
    
    if not keywords:
        return []
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Build the SQL query with placeholders for each keyword
    placeholders = []
    params = []
    
    for keyword in keywords:
        placeholders.append("""
            (LOWER(p.name) LIKE ? OR 
             LOWER(p.description) LIKE ? OR 
             LOWER(p.short_description) LIKE ?)
        """)
        pattern = f"%{keyword}%"
        params.extend([pattern, pattern, pattern])
    
    sql = f"""
        SELECT p.id, p.name, p.short_description, p.price, p.sale_price, 
               c.name as category
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = 1 AND ({" OR ".join(placeholders)})
    """
    
    # Execute the search
    cursor.execute(sql, params)
    results = [dict(row) for row in cursor.fetchall()]
    
    # Get tags for each product
    for product in results:
        cursor.execute("""
            SELECT t.name
            FROM product_tags pt
            JOIN tags t ON pt.tag_id = t.id
            WHERE pt.product_id = ?
        """, (product['id'],))
        product['tags'] = [tag[0] for tag in cursor.fetchall()]
    
    conn.close()
    return results

def main():
    parser = argparse.ArgumentParser(description='Tag-focused product search')
    parser.add_argument('query', type=str, help='The search query')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--ai', action='store_true', help='Enable AI tag analysis')
    parser.add_argument('--tags-only', action='store_true', help='Only show selected tags without search results')
    args = parser.parse_args()
    
    # Set debug mode if requested
    if args.debug:
        os.environ['DEBUG_SEARCH'] = "1"
        global DEBUG_MODE
        DEBUG_MODE = True
    
    # Enable AI if requested
    if args.ai:
        os.environ['ENABLE_AI'] = "1"
    
    # If tags-only mode, just show the tags without search results
    if args.tags_only:
        # Get all available tags for reference
        all_tags = get_all_tags()
        selected_tags = select_relevant_tags(args.query, all_tags)
        print(f"\nQuery: {args.query}")
        print(f"Selected tags: {', '.join(selected_tags)}")
        return
    
    print(f"Searching for products matching: {args.query}")
    results = tag_based_search(args.query)
    
    if results:
        print(f"\nFound {len(results)} matching products:")
        
        # Print results in a user-friendly format
        for i, product in enumerate(results, 1):
            match_score = product.get('match_score', 0)
            print(f"\n{i}. {product['name']} - ${product['price']:.2f}", end="")
            if product.get('sale_price'):
                print(f" (Sale: ${product['sale_price']:.2f})", end="")
            if match_score:
                print(f" - Match score: {match_score}", end="")
            print(f"\n   Category: {product['category']}")
            print(f"   {product['short_description']}")
            print(f"   Tags: {', '.join(product['tags'])}")
    else:
        print("No matching products found.")

if __name__ == "__main__":
    main()