import sqlite3
import json
import requests
import argparse
from typing import List, Dict, Any

# Database connection
DB_FILE = 'ecommerce.db'

# Ollama API config
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3"  # Updated to use the available Gemma 3 model

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

def ask_ai_for_product_recommendations(user_query: str, product_data: List[Dict]) -> List[int]:
    """
    Ask Ollama with Gemma 3 to recommend products based on the user query
    """
    # Create a prompt for the AI
    products_context = json.dumps(product_data, indent=2)
    
    prompt = f"""<start_of_turn>user
You are a precise product search assistant. I need you to find the most relevant products from our catalog based on this request:

"{user_query}"

Here is the product catalog in JSON format:
{products_context}

Analyze the user request and match it with the most suitable products. Consider categories, attributes, tags, price, and descriptions.
<end_of_turn>

<start_of_turn>assistant
I'll recommend the 5 most relevant products for this request. After careful analysis, here are the product IDs in JSON array format:
"""
    
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
        
        # Find and parse the JSON array of product IDs
        # Look for a pattern that resembles a JSON array
        import re
        json_pattern = r'\[\s*\d+\s*(?:,\s*\d+\s*)*\]'
        match = re.search(json_pattern, ai_response)
        
        if match:
            product_ids_json = match.group(0)
            product_ids = json.loads(product_ids_json)
            return product_ids[:5]  # Ensure we only return 5 products
        else:
            # Fallback: try to parse the entire response as JSON
            try:
                product_ids = json.loads(ai_response)
                if isinstance(product_ids, list) and all(isinstance(id, int) for id in product_ids):
                    return product_ids[:5]
            except:
                pass
            
            # Secondary fallback: Extract all numbers from the response
            numbers = re.findall(r'\d+', ai_response)
            if numbers:
                try:
                    product_ids = [int(num) for num in numbers[:5]]
                    return product_ids
                except:
                    pass
            
            print(f"Could not parse AI response as product IDs. Response: {ai_response}")
            return []
            
    except Exception as e:
        print(f"Error calling Ollama API: {e}")
        return []

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
    
    # Get all products in a simplified format for AI analysis
    all_products = get_all_products_for_ai_analysis()
    
    # Get AI recommendations
    recommended_product_ids = ask_ai_for_product_recommendations(query, all_products)
    
    # If we got no recommendations, return empty list
    if not recommended_product_ids:
        return []
    
    # Get full details for the recommended products
    recommended_products = get_product_details(recommended_product_ids)
    
    # Update the search log with the results count
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE search_logs SET results_count = ? WHERE search_query = ? ORDER BY id DESC LIMIT 1",
        (len(recommended_products), query)
    )
    conn.commit()
    conn.close()
    
    return recommended_products

def main():
    """
    Main entry point for the CLI application
    """
    parser = argparse.ArgumentParser(description='AI-powered product search')
    parser.add_argument('query', type=str, help='The search query or prompt')
    args = parser.parse_args()
    
    print(f"Searching for products matching: {args.query}")
    results = search_products(args.query)
    
    if results:
        print(f"\nFound {len(results)} matching products:")
        print(json.dumps(results, indent=2))
    else:
        print("No matching products found.")

if __name__ == "__main__":
    main()