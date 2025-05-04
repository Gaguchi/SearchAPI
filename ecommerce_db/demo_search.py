import sys
import time
import os
from ai_product_search import search_products
from check_ollama import check_ollama_status

def spinner_animation():
    """Display a simple spinner animation to show processing"""
    chars = ['|', '/', '-', '\\']
    for char in chars:
        sys.stdout.write('\r' + "Processing " + char)
        sys.stdout.flush()
        time.sleep(0.1)

def verbose_search_products(query, debug=False):
    """
    Perform product search with progress indicators at each step
    """
    print(f"🔍 Starting search for: \"{query}\"")
    
    # Enable debug mode in current environment if requested
    if debug:
        os.environ['DEBUG_SEARCH'] = "1"
        print("🐛 Debug mode enabled - showing detailed processing steps")
    
    print("🧠 Querying Ollama API with Gemma 3 model...")
    print("   This may take a moment - waiting for AI response...")
    
    # Use a simple animation to show that the process is running
    start_time = time.time()
    
    try:
        # Show spinner for up to 30 seconds or until search completes
        search_completed = False
        max_wait = 30  # Maximum wait time in seconds
        
        # Start the search in a more controlled way
        print("📊 Preparing product database...")
        
        # Perform the actual search with timeout handling
        import threading
        results = []
        
        def search_thread():
            nonlocal results, search_completed
            try:
                results = search_products(query)
                search_completed = True
            except Exception as e:
                print(f"❌ Error during search: {e}")
                search_completed = True
        
        # Start search in a separate thread
        thread = threading.Thread(target=search_thread)
        thread.daemon = True
        thread.start()
        
        # Display progress while waiting for search to complete
        elapsed = 0
        while not search_completed and elapsed < max_wait:
            spinner_animation()
            elapsed += 0.5
            if elapsed % 5 == 0:
                print(f"\r⏱️ Still processing... ({elapsed:.0f}s elapsed)")
        
        if not search_completed:
            print("\r❌ Search appears to be stuck or taking too long. You might want to check:")
            print("   - Is Ollama running? (try 'ollama serve' in a terminal)")
            print("   - Is the Gemma 3 model installed? (try 'ollama pull gemma:3')")
            print("   - Is there a network or server issue?")
            return []
            
        elapsed_time = time.time() - start_time
        print(f"\r✅ Search completed in {elapsed_time:.2f} seconds")
        
        if results:
            print(f"🎯 Found {len(results)} matching products")
        else:
            print("⚠️ No matching products found")
        
        return results
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\r❌ Search failed after {elapsed_time:.2f} seconds with error: {e}")
        return []

def run_demo_searches():
    """Run demo searches with example queries to test the AI search functionality"""
    
    # First check if Ollama is properly configured
    if not check_ollama_status():
        print("\n⚠️ Cannot proceed with demo - please set up Ollama with Gemma 3 first.")
        print("   Run the following commands:")
        print("   1. Start Ollama server: ollama serve")
        print("   2. Pull Gemma 3 model: ollama pull gemma:3")
        sys.exit(1)
    
    # Example search queries that showcase different search capabilities
    example_queries = [
        "I need a lightweight laptop for travel under $1000",
        "Comfortable running shoes with good arch support",
        "Waterproof bluetooth speaker for the beach",
        "Organic skincare products for sensitive skin",
        "Kitchen gadgets for small apartments"
    ]
    
    print("\n" + "="*80)
    print("DEMO: AI PRODUCT SEARCH WITH GEMMA 3".center(80))
    print("="*80 + "\n")
    
    # Modify to only run first example with debug enabled
    for i, query in enumerate(example_queries[:1], 1):
        print(f"\n--- Example {i}: \"{query}\" ---\n")
        
        # Perform the search with progress indicators and debug mode
        results = verbose_search_products(query, debug=True)
        
        # Display results summary
        if results:
            print(f"\n📋 Search Results Summary:")
            print(f"Found {len(results)} matching products:")
            for j, product in enumerate(results, 1):
                price_info = f"${product['price']:.2f}"
                if product.get('sale_price'):
                    price_info += f" (Sale: ${product['sale_price']:.2f})"
                
                print(f"  {j}. {product['name']} - {price_info}")
                print(f"     Category: {product.get('category_name', 'N/A')}")
                if product.get('short_description'):
                    print(f"     {product['short_description']}")
                print()
        else:
            print("No matching products found.")
    
    print("\nDemo completed. You can now try your own search queries using:")
    print("python ai_product_search.py \"your search query here\"")

if __name__ == "__main__":
    run_demo_searches()