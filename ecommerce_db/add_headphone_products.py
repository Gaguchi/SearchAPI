import sqlite3
import json
import random

DB_FILE = 'ecommerce.db'

def add_headphone_products():
    """
    Add specific headphone products including ones with noise cancellation
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get the next available product ID
    cursor.execute("SELECT MAX(id) FROM products")
    next_id = (cursor.fetchone()[0] or 0) + 1
    
    # Create audio headphone products
    headphone_products = [
        {
            "name": "NoiseShield Pro Wireless Headphones",
            "sku": "AUDIO-NSP-101",
            "description": "Experience premium sound quality with the NoiseShield Pro Wireless Headphones featuring industry-leading active noise cancellation technology. These over-ear headphones block out ambient noise so you can focus on your music or calls. With 30 hours of battery life, Bluetooth 5.2 connectivity, and plush memory foam ear cushions, the NoiseShield Pro delivers exceptional comfort for all-day listening. Touch controls allow easy adjustment of volume, tracks, and noise cancellation levels. Built-in microphones ensure crystal-clear calls even in noisy environments, while the foldable design makes these headphones perfect for travel.",
            "short_description": "Premium wireless headphones with advanced active noise cancellation.",
            "price": 249.99,
            "sale_price": 199.99,
            "category_id": 4,  # Audio category
            "brand": "AudioTech",
            "attributes": [
                {"name": "Type", "value": "Over-ear", "display_order": 1},
                {"name": "Noise Cancellation", "value": "Active Noise Cancelling", "display_order": 2},
                {"name": "Battery Life", "value": "Up to 30 hours", "display_order": 3},
                {"name": "Water Resistance", "value": "IPX4", "display_order": 4}
            ],
            "tags": ["Premium", "Wireless", "Noise Cancellation"]
        },
        {
            "name": "SoundFlow Wireless Earbuds",
            "sku": "AUDIO-SFW-202",
            "description": "The SoundFlow Wireless Earbuds deliver exceptional audio quality in a compact, lightweight design. These true wireless earbuds feature passive noise isolation that naturally blocks ambient sounds, allowing you to enjoy your music without distractions. With 8 hours of playback time and an additional 24 hours from the charging case, you'll have plenty of battery life for all-day listening. The earbuds are sweat and water-resistant, making them perfect for workouts. The intuitive touch controls and comfortable ergonomic design ensure these earbuds stay secure during any activity.",
            "short_description": "Compact wireless earbuds with passive noise isolation.",
            "price": 129.99,
            "sale_price": 99.99,
            "category_id": 4,  # Audio category
            "brand": "SoundWave",
            "attributes": [
                {"name": "Type", "value": "In-ear", "display_order": 1},
                {"name": "Noise Cancellation", "value": "Passive Isolation", "display_order": 2},
                {"name": "Battery Life", "value": "Up to 8 hours", "display_order": 3},
                {"name": "Water Resistance", "value": "IPX5", "display_order": 4}
            ],
            "tags": ["Wireless", "Compact", "Workout"]
        },
        {
            "name": "BassBoost Noise-Cancelling Headphones",
            "sku": "AUDIO-BB-303",
            "description": "The BassBoost Noise-Cancelling Headphones combine powerful bass response with advanced noise cancellation technology. These wireless headphones analyze and filter out background noise in real-time, creating a bubble of silence around you. The adaptive noise cancellation adjusts automatically based on your environment, providing the perfect level of noise reduction whether you're on a plane, commuting, or working in a noisy office. With 25 hours of battery life, fast charging that provides 5 hours of playback from just 10 minutes of charging, and premium audio drivers tuned for rich, detailed sound, these headphones deliver an immersive listening experience.",
            "short_description": "Wireless headphones with adaptive noise cancellation and enhanced bass.",
            "price": 199.99,
            "sale_price": 169.99,
            "category_id": 4,  # Audio category
            "brand": "BeatPro",
            "attributes": [
                {"name": "Type", "value": "Over-ear", "display_order": 1},
                {"name": "Noise Cancellation", "value": "Adaptive ANC", "display_order": 2},
                {"name": "Battery Life", "value": "Up to 25 hours", "display_order": 3},
                {"name": "Water Resistance", "value": "Not water resistant", "display_order": 4}
            ],
            "tags": ["Bass", "Wireless", "Noise Cancellation"]
        },
        {
            "name": "ProSound Studio Headphones",
            "sku": "AUDIO-PSS-404",
            "description": "The ProSound Studio Headphones deliver professional-grade audio quality for musicians, producers, and audiophiles. These wired headphones feature a flat frequency response for accurate sound reproduction, making them perfect for studio monitoring and mixing. The open-back design creates a wider soundstage for more natural audio imaging, while the premium materials ensure comfort during long recording or listening sessions. The detachable cable with industry-standard connections allows for easy replacement and customization.",
            "short_description": "Professional wired studio headphones with flat frequency response.",
            "price": 179.99,
            "sale_price": None,
            "category_id": 4,  # Audio category
            "brand": "AudioPhile",
            "attributes": [
                {"name": "Type", "value": "Open-back", "display_order": 1},
                {"name": "Noise Cancellation", "value": "None", "display_order": 2},
                {"name": "Connection", "value": "Wired (3.5mm/6.3mm)", "display_order": 3},
                {"name": "Impedance", "value": "250 Ohm", "display_order": 4}
            ],
            "tags": ["Studio", "Professional", "Hi-Fi"]
        }
    ]
    
    # Insert the products
    for product in headphone_products:
        # Insert basic product info
        cursor.execute('''
            INSERT INTO products (
                name, sku, description, short_description, price, sale_price, cost, 
                stock_quantity, category_id, brand, weight, dimensions, is_featured, is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product["name"], 
            product["sku"], 
            product["description"], 
            product["short_description"], 
            product["price"], 
            product["sale_price"], 
            product["price"] * 0.5,  # Cost is 50% of retail price
            random.randint(50, 200),  # Random stock quantity
            product["category_id"], 
            product["brand"], 
            round(random.uniform(0.1, 0.5), 2),  # Random weight
            json.dumps({"length": 20, "width": 15, "height": 8}),  # Dimensions
            1 if random.random() < 0.25 else 0,  # 25% chance of being featured
            1  # Always active
        ))
        
        product_id = cursor.lastrowid
        
        # Insert product attributes
        for attr in product["attributes"]:
            cursor.execute('''
                INSERT INTO product_attributes (
                    product_id, attribute_name, attribute_value, display_order, is_filterable, is_visible
                )
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                product_id, 
                attr["name"], 
                attr["value"], 
                attr["display_order"], 
                1,  # Is filterable
                1   # Is visible
            ))
        
        # Insert product images
        cursor.execute('''
            INSERT INTO product_images (
                product_id, image_url, is_primary, display_order, alt_text
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (
            product_id, 
            f"product_{product_id}_main.jpg", 
            1,  # Is primary
            1,  # Display order
            f"{product['name']} main view"
        ))
        
        # Add additional images
        angles = ["front", "side", "wearing", "detail"]
        for i, angle in enumerate(angles):
            cursor.execute('''
                INSERT INTO product_images (
                    product_id, image_url, is_primary, display_order, alt_text
                )
                VALUES (?, ?, ?, ?, ?)
            ''', (
                product_id, 
                f"product_{product_id}_{angle}.jpg", 
                0,  # Not primary
                i+2,  # Display order
                f"{product['name']} {angle} view"
            ))
        
        # Add tags
        for tag_name in product["tags"]:
            # Check if the tag exists
            cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_row = cursor.fetchone()
            
            if tag_row:
                tag_id = tag_row[0]
            else:
                # Create new tag
                cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
                tag_id = cursor.lastrowid
            
            # Link tag to product
            cursor.execute('''
                INSERT INTO product_tags (product_id, tag_id)
                VALUES (?, ?)
            ''', (product_id, tag_id))
    
    conn.commit()
    conn.close()
    
    print(f"Successfully added {len(headphone_products)} headphone products to the database.")

if __name__ == "__main__":
    add_headphone_products()