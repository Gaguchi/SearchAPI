import sqlite3
import json
import requests
import argparse
import os
import re
import sys
from typing import List, Dict, Any, Tuple

# Database connection
DB_FILE = 'ecommerce.db'

# Ollama API config
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"  # Using Gemma 3 instead of DeepSeek

# Confidence threshold - products with lower confidence won't be displayed
CONFIDENCE_THRESHOLD = 0.75

# Debug mode flag - can be enabled with environment variable
DEBUG_MODE = os.environ.get('DEBUG_SEARCH', '0') == '1'

def debug_print(*args, **kwargs):
    """Print debug information if debug mode is enabled"""
    if DEBUG_MODE:
        # Ensure immediate output by flushing
        print("[DEBUG]", *args, **kwargs, flush=True)
        # Also log to a file for easier viewing
        with open("search_debug.log", "a", encoding="utf-8") as f:
            print("[DEBUG]", *args, **kwargs, file=f)

def get_product_details(product_ids: List[int]) -> List[Dict[str, Any]]:
    """
    Fetch complete details for the given product IDs
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    products_with_details = []
    
    for product_id in product_ids:
        # Get basic product info
        cursor.execute("""
            SELECT p.*, c.name as category_name 
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?
        """, (product_id,))
        product = dict(cursor.fetchone())
        
        # Get product attributes
        cursor.execute("""
            SELECT attribute_name, attribute_value
            FROM product_attributes
            WHERE product_id = ?
            ORDER BY display_order
        """, (product_id,))
        product['attributes'] = {row['attribute_name']: row['attribute_value'] for row in cursor.fetchall()}
        
        # Get product images
        cursor.execute("""
            SELECT image_url, alt_text
            FROM product_images
            WHERE product_id = ?
            ORDER BY is_primary DESC, display_order
        """, (product_id,))
        product['images'] = [dict(row) for row in cursor.fetchall()]
        
        # Get product tags
        cursor.execute("""
            SELECT t.name
            FROM product_tags pt
            JOIN tags t ON pt.tag_id = t.id
            WHERE pt.product_id = ?
        """, (product_id,))
        product['tags'] = [row['name'] for row in cursor.fetchall()]
        
        products_with_details.append(product)
    
    conn.close()
    return products_with_details

def get_all_products_for_ai_analysis() -> List[Dict[str, Any]]:
    """
    Fetch simplified product data for all products to send to AI
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all products with basic details
    cursor.execute("""
        SELECT p.id, p.name, p.short_description, p.price, p.sale_price, 
               c.name as category, p.brand
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = 1
    """)
    
    all_products = []
    for row in cursor.fetchall():
        product = dict(row)
        
        # Get product attributes
        cursor.execute("""
            SELECT attribute_name, attribute_value
            FROM product_attributes
            WHERE product_id = ? AND is_visible = 1
            ORDER BY display_order
            LIMIT 5
        """, (product['id'],))
        product['attributes'] = {row['attribute_name']: row['attribute_value'] for row in cursor.fetchall()}
        
        # Get product tags
        cursor.execute("""
            SELECT t.name
            FROM product_tags pt
            JOIN tags t ON pt.tag_id = t.id
            WHERE pt.product_id = ?
        """, (product['id'],))
        product['tags'] = [row['name'] for row in cursor.fetchall()]
        
        all_products.append(product)
    
    conn.close()
    return all_products

def ask_ai_for_product_recommendations(user_query: str, product_data: List[Dict]) -> List[Tuple[int, float]]:
    """
    Ask Ollama with Gemma 3 model to recommend products based on the user query
    Returns a list of tuples containing (product_id, confidence_score)
    """
    # Create a prompt for the AI
    products_context = json.dumps(product_data, indent=2)
    
    debug_print(f"Total products in catalog: {len(product_data)}")
    debug_print(f"User query: '{user_query}'")
    
    prompt = f"""<start_of_turn>user
You are a precise product search assistant for an e-commerce store. I need you to find products that match this specific search query:

SEARCH QUERY: "{user_query}"

When evaluating products, consider these guidelines:
1. For queries about specific product types (like "headphones" or "laptops"), only return products of that exact type
2. When specific features are mentioned (like "noise cancellation" or "wireless"), prioritize products with those exact features
3. Pay close attention to product categories, attributes, and descriptions

Here is the product catalog in JSON format:
{products_context}

For each product, evaluate how well it matches the query and assign a confidence score between 0.0 and 1.0, where:
- 1.0 = Perfect match to the query (exact product type with all requested features)
- 0.75 = Good match (right product type, most requested features)
- 0.5 = Moderate match (right product type, some features missing)
- 0.25 = Poor match (related category but wrong product type)
- 0.0 = Not relevant at all

Respond with a JSON array of objects containing product_id and confidence like this:
[
  {{"product_id": 3, "confidence": 0.95}},
  {{"product_id": 7, "confidence": 0.82}},
  {{"product_id": 12, "confidence": 0.76}}
]

Before providing the JSON, briefly explain your reasoning about how you evaluated the products.
<end_of_turn>

<start_of_turn>assistant
"""
    
    debug_print("Sending query to Ollama API with Gemma 3 model...")
    
    # Call Ollama API with Gemma 3
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower temperature for more deterministic results
                    "top_p": 0.9
                }
            }
        )
        response.raise_for_status()
        
        # Extract the response text
        result = response.json()
        ai_response = result.get('response', '')
        
        debug_print("\nAI response (raw):")
        debug_print("====================")
        debug_print(ai_response)
        debug_print("====================\n")
        
        # Try to find and parse a JSON array with product_id and confidence
        json_pattern = r'\[\s*\{.*?\}\s*(?:,\s*\{.*?\}\s*)*\]'
        match = re.search(json_pattern, ai_response, re.DOTALL)
        
        if match:
            products_json = match.group(0)
            debug_print(f"Found JSON array in response: {products_json}")
            try:
                products_with_confidence = json.loads(products_json)
                debug_print(f"Parsed products with confidence: {products_with_confidence}")
                
                # Convert to list of tuples (product_id, confidence)
                result = []
                for item in products_with_confidence:
                    if isinstance(item, dict) and 'product_id' in item and 'confidence' in item:
                        result.append((item['product_id'], item['confidence']))
                
                # Sort by confidence score (highest first)
                result.sort(key=lambda x: x[1], reverse=True)
                debug_print(f"Sorted result by confidence: {result}")
                return result
                
            except json.JSONDecodeError as e:
                debug_print(f"Failed to parse JSON: {e}")
        
        debug_print("No valid JSON found in the response or JSON format doesn't match expected structure.")
        debug_print("Trying fallback extraction methods...")
        
        # Try to extract product IDs and confidence scores using regex
        # Look for patterns like: {"product_id": 123, "confidence": 0.95}
        product_pattern = r'{"product_id":\s*(\d+),\s*"confidence":\s*(0\.\d+|1\.0|1)'
        matches = re.findall(product_pattern, ai_response)
        
        if matches:
            debug_print(f"Extracted product IDs and confidence scores using regex: {matches}")
            result = [(int(pid), float(conf)) for pid, conf in matches]
            # Sort by confidence score (highest first)
            result.sort(key=lambda x: x[1], reverse=True)
            debug_print(f"Sorted result by confidence: {result}")
            return result
        
        # Try a more flexible regex pattern as a last resort
        flexible_pattern = r'product(?:_|\s)?id["\s:]*(\d+).*?confidence["\s:]*(\d+\.\d+|\d+)'
        matches = re.findall(flexible_pattern, ai_response, re.IGNORECASE)
        if matches:
            debug_print(f"Extracted IDs and confidence with flexible regex: {matches}")
            result = [(int(pid), float(conf)) for pid, conf in matches]
            result.sort(key=lambda x: x[1], reverse=True)
            debug_print(f"Sorted result by confidence: {result}")
            return result
        
        # As a last resort, just extract product IDs and assign decreasing confidence
        numbers = re.findall(r'\d+', ai_response)
        if numbers:
            try:
                # Start with confidence of 1.0 and decrease by 0.1 for each subsequent product
                max_products = 10
                product_ids = [int(num) for num in numbers[:max_products]]
                confidences = [max(0.1, 1.0 - (i * 0.1)) for i in range(len(product_ids))]
                result = list(zip(product_ids, confidences))
                debug_print(f"Assigned decreasing confidence to product IDs: {result}")
                return result
            except Exception as e:
                debug_print(f"Failed to convert extracted numbers to product IDs: {e}")
        
        print(f"Could not parse AI response for product recommendations.")
        return []
            
    except Exception as e:
        print(f"Error calling Ollama API: {e}")
        debug_print(f"API error details: {str(e)}")
        return []

def search_products_directly(query: str) -> List[int]:
    """
    Perform direct keyword search in the database as a fallback for AI search
    Returns a list of product IDs matching the keywords in the query
    """
    # Break the query into keywords
    keywords = [k.strip().lower() for k in query.split() if len(k.strip()) > 3]
    
    if not keywords:
        return []
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Build the SQL query to search in product name, description, and attributes
    sql_conditions = []
    params = []
    
    for keyword in keywords:
        pattern = f"%{keyword}%"
        sql_conditions.append("""
            (LOWER(p.name) LIKE ? OR 
             LOWER(p.description) LIKE ? OR 
             LOWER(p.short_description) LIKE ? OR
             EXISTS (
                SELECT 1 FROM product_attributes pa 
                WHERE pa.product_id = p.id AND 
                (LOWER(pa.attribute_name) LIKE ? OR LOWER(pa.attribute_value) LIKE ?)
             ))
        """)
        params.extend([pattern, pattern, pattern, pattern, pattern])
    
    # Combine all conditions with AND (products must match all keywords)
    sql = f"""
        SELECT p.id, p.name, p.short_description
        FROM products p
        WHERE p.is_active = 1 AND {" AND ".join(sql_conditions)}
        ORDER BY 
            CASE 
                WHEN LOWER(p.name) LIKE ? THEN 3 
                WHEN LOWER(p.short_description) LIKE ? THEN 2 
                ELSE 1 
            END DESC,
            p.id
    """
    
    # Add the most important keyword for sorting
    primary_keyword = keywords[0] if keywords else ""
    primary_pattern = f"%{primary_keyword}%"
    params.extend([primary_pattern, primary_pattern])
    
    # Execute the search
    cursor.execute(sql, params)
    matching_products = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return matching_products

def search_products(query: str) -> List[Dict[str, Any]]:
    """
    Main function to search products based on user query
    """
    # Log the search query
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO search_logs (search_query, search_date) VALUES (?, datetime('now'))",
        (query,)
    )
    conn.commit()
    conn.close()
    
    # Extract key terms from the query for relevance checking
    query_terms = set([term.lower() for term in query.split() if len(term) > 3])
    
    # First try direct keyword search to see if we have exact matches
    print("Trying direct keyword search first...")
    direct_product_ids = search_products_directly(query)
    
    if direct_product_ids:
        print(f"Found {len(direct_product_ids)} products with direct keyword matching.")
        direct_products = get_product_details(direct_product_ids[:10])  # Limit to 10 results
        for product in direct_products:
            product['confidence_score'] = 1.0
        return direct_products
    
    # If direct search found nothing, try AI-based search
    print("No direct matches found. Trying AI-powered search...")
    
    # Get all products in a simplified format for AI analysis
    all_products = get_all_products_for_ai_analysis()
    
    # Get AI recommendations with confidence scores
    recommended_products_with_confidence = ask_ai_for_product_recommendations(query, all_products)
    
    # Filter products by confidence threshold
    filtered_recommendations = [
        (product_id, confidence) for product_id, confidence in recommended_products_with_confidence
        if confidence >= CONFIDENCE_THRESHOLD
    ]
    
    # If we got no recommendations after filtering, return empty list
    if not filtered_recommendations:
        print(f"No products met the confidence threshold of {CONFIDENCE_THRESHOLD}")
        
        # Show products that were below threshold for debugging
        if recommended_products_with_confidence and DEBUG_MODE:
            print("[DEBUG] Products below threshold:")
            for product_id, confidence in recommended_products_with_confidence:
                print(f"[DEBUG] Product ID {product_id} with confidence {confidence:.2f}")
        return []
    
    # Get product IDs from filtered recommendations
    product_ids = [product_id for product_id, _ in filtered_recommendations]
    
    # Get full details for the recommended products
    recommended_products = get_product_details(product_ids)
    
    # Add confidence scores to product details
    for product in recommended_products:
        for product_id, confidence in filtered_recommendations:
            if product['id'] == product_id:
                product['confidence_score'] = confidence
                break
    
    # Sort products by confidence score (highest first)
    recommended_products.sort(key=lambda p: p.get('confidence_score', 0), reverse=True)
    
    # Check if AI recommendations are relevant by looking for query terms in the top product
    if recommended_products and query_terms:
        top_product = recommended_products[0]
        product_text = (
            (top_product['name'] + ' ' + 
            top_product['short_description'] + ' ' + 
            ' '.join(str(v) for v in top_product['attributes'].values()) + ' ' +
            top_product['category_name']).lower()
        )
        
        # Count how many query terms appear in the product text
        matching_terms = sum(1 for term in query_terms if term in product_text)
        match_ratio = matching_terms / len(query_terms) if query_terms else 0
        
        if match_ratio < 0.5:  # If less than half of query terms match
            print(f"AI recommendations don't seem relevant (match ratio: {match_ratio:.2f})")
            print("No relevant products found for the query.")
            return []
    
    # Update the search log with the results count
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Get the ID of the most recent search log for this query
    cursor.execute(
        "SELECT id FROM search_logs WHERE search_query = ? ORDER BY id DESC LIMIT 1",
        (query,)
    )
    search_log_id = cursor.fetchone()[0]
    # Update the search log with the results count
    cursor.execute(
        "UPDATE search_logs SET results_count = ? WHERE id = ?",
        (len(recommended_products), search_log_id)
    )
    conn.commit()
    conn.close()
    
    return recommended_products

def main():
    """
    Main entry point for the CLI application
    """
    global DEBUG_MODE, CONFIDENCE_THRESHOLD
    
    parser = argparse.ArgumentParser(description='AI-powered product search')
    parser.add_argument('query', type=str, help='The search query or prompt')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--threshold', type=float, default=CONFIDENCE_THRESHOLD, 
                        help=f'Confidence threshold (default: {CONFIDENCE_THRESHOLD})')
    args = parser.parse_args()
    
    # Set debug mode if requested
    if args.debug:
        DEBUG_MODE = True
    
    # Set custom threshold if provided
    if args.threshold != CONFIDENCE_THRESHOLD:
        CONFIDENCE_THRESHOLD = args.threshold
    
    print(f"Searching for products matching: {args.query}")
    results = search_products(args.query)
    
    if results:
        print(f"\nFound {len(results)} matching products:")
        
        # Print results in a user-friendly format
        for i, product in enumerate(results, 1):
            confidence = product.get('confidence_score', 0)
            print(f"\n{i}. {product['name']} - ${product['price']:.2f}", end="")
            if product.get('sale_price'):
                print(f" (Sale: ${product['sale_price']:.2f})", end="")
            print(f" - Confidence: {confidence:.2f}")
            print(f"   Category: {product['category_name']}")
            print(f"   {product['short_description']}")
            
            # Print key attributes if available
            if product['attributes']:
                print("   Key features:", end=" ")
                print(", ".join([f"{k}: {v}" for k, v in list(product['attributes'].items())[:3]]))
            
            # Print tags if available
            if product['tags']:
                print("   Tags:", ", ".join(product['tags']))
        
        # Ask if user wants to see detailed JSON
        if input("\nShow detailed JSON? (y/n): ").lower().startswith('y'):
            print(json.dumps(results, indent=2))
    else:
        print("No matching products found.")
        
        # Offer to lower threshold if no results found
        if args.threshold >= 0.7:  # Only offer if threshold is reasonably high
            lower_threshold = 0.5
            if input(f"\nTry again with a lower confidence threshold ({lower_threshold})? (y/n): ").lower().startswith('y'):
                print(f"\nRerunning search with lower threshold ({lower_threshold})...")
                CONFIDENCE_THRESHOLD = lower_threshold
                results = search_products(args.query)
                if results:
                    print(f"\nFound {len(results)} matching products with lower threshold:")
                    # Print results in a user-friendly format
                    for i, product in enumerate(results, 1):
                        confidence = product.get('confidence_score', 0)
                        print(f"\n{i}. {product['name']} - ${product['price']:.2f}", end="")
                        if product.get('sale_price'):
                            print(f" (Sale: ${product['sale_price']:.2f})", end="")
                        print(f" - Confidence: {confidence:.2f}")
                        print(f"   Category: {product['category_name']}")
                        print(f"   {product['short_description']}")
                else:
                    print("Still no matching products found.")

if __name__ == "__main__":
    main()