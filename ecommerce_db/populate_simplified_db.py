import sqlite3
import random
import json

# Database file path
DB_FILE = 'simplified_ecommerce.db'

def populate_database():
    """Populate the simplified e-commerce database with products and tags"""
    # Connect to the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Insert sample categories
    categories = [
        (None, "Electronics", "Electronic devices and gadgets"),
        (None, "Smartphones", "Mobile phones and accessories"),
        (None, "Laptops", "Notebook computers"),
        (None, "Audio", "Headphones, speakers and audio equipment"),
        (None, "Clothing", "Apparel and fashion items"),
        (None, "Home & Kitchen", "Home appliances and kitchenware"),
        (None, "Books", "Books and publications"),
        (None, "Sports & Outdoors", "Sporting goods and outdoor equipment"),
        (None, "Beauty", "Beauty products and cosmetics"),
        (None, "Toys & Games", "Toys and games for all ages")
    ]
    
    cursor.executemany('''
    INSERT INTO categories (id, name, description)
    VALUES (?, ?, ?)
    ''', categories)
    
    # Insert tags - a comprehensive set of tags to describe products
    tags = [
        # Product characteristics
        "Wireless", "Bluetooth", "Noise-cancelling", "Waterproof", "Portable", 
        "Rechargeable", "High-resolution", "Touchscreen", "Foldable", "Lightweight",
        "HD", "4K", "Ultra-HD", "Smart", "WiFi", "Premium", "Budget", "Compact",
        
        # Product types
        "Headphones", "Earbuds", "Laptop", "Smartphone", "Camera", "Speaker", "Tablet",
        "Monitor", "Keyboard", "Mouse", "Game", "Book", "Watch", "Fitness-tracker",
        
        # Features & capabilities
        "Fast-charging", "Long-battery", "Voice-control", "Surround-sound", 
        "Multi-device", "High-performance", "Gaming", "Professional", "Streaming",
        "Cloud-storage", "AI-powered", "Virtual-reality", "Augmented-reality",
        
        # Uses & activities
        "Outdoor", "Sports", "Travel", "Office", "School", "Entertainment", "Music",
        "Video", "Photography", "Cooking", "Exercise", "Meditation", "Reading",
        
        # Materials & design
        "Leather", "Metal", "Plastic", "Glass", "Wood", "Stainless-steel", "Aluminum",
        "Ergonomic", "Adjustable", "Customizable", "Slim", "Rugged", "Durable",
        
        # Technical specifications
        "USB-C", "HDMI", "Thunderbolt", "5G", "WiFi-6", "Gigabit", "LED", "OLED", 
        "QLED", "Retina", "Intel", "AMD", "NVIDIA", "SSD", "Memory-foam",
        
        # Groups & communities
        "Family", "Children", "Teens", "Adults", "Seniors", "Beginners", "Advanced",
        "Enthusiasts", "Professionals", "Students", "Travelers", "Commuters", "Gamers",
        
        # Price & value
        "Best-seller", "New-arrival", "Limited-edition", "Sale", "Exclusive",
        "Award-winning", "Top-rated", "Popular", "Trending", "Essential",
        
        # Brands & ecosystems
        "Apple", "Samsung", "Sony", "Bose", "Microsoft", "Google", "Amazon", "LG",
        "Dell", "Asus", "Logitech", "JBL", "Fitbit", "Nike", "Adidas"
    ]
    
    # Insert all tags
    for tag in tags:
        cursor.execute('INSERT INTO tags (name) VALUES (?)', (tag,))
    
    # Get tag IDs for later use
    cursor.execute('SELECT id, name FROM tags')
    tag_map = {name: tag_id for tag_id, name in cursor.fetchall()}
    
    # Product templates with appropriate tags
    product_templates = [
        # Headphones categories
        {
            "category": "Audio",
            "products": [
                {
                    "name": "TechSound Pro Wireless Headphones",
                    "description": "Experience premium sound quality with TechSound Pro Wireless Headphones featuring active noise cancellation technology that blocks out ambient noise so you can focus on your music or calls. With 30 hours of battery life, Bluetooth 5.2 connectivity, and memory foam ear cushions, these headphones deliver exceptional comfort for all-day listening.",
                    "short_description": "Premium wireless headphones with active noise cancellation",
                    "price": 249.99,
                    "sale_price": 199.99,
                    "image_url": "techsound_pro.jpg",
                    "tags": ["Headphones", "Wireless", "Bluetooth", "Noise-cancelling", "Premium", "Long-battery"]
                },
                {
                    "name": "AudioMax Studio Headphones",
                    "description": "The AudioMax Studio Headphones deliver professional-grade audio quality for musicians, producers, and audiophiles. These wired headphones feature a flat frequency response for accurate sound reproduction, making them perfect for studio monitoring and mixing.",
                    "short_description": "Professional wired studio headphones for audio production",
                    "price": 179.99,
                    "sale_price": None,
                    "image_url": "audiomax_studio.jpg",
                    "tags": ["Headphones", "Professional", "Studio", "Wired", "High-resolution"]
                },
                {
                    "name": "SoundFlex Wireless Earbuds",
                    "description": "SoundFlex Wireless Earbuds deliver exceptional audio quality in a compact, lightweight design. With passive noise isolation and 8 hours of playback time plus 24 more from the charging case, these earbuds are perfect for workouts or commuting.",
                    "short_description": "Compact wireless earbuds with long battery life",
                    "price": 129.99,
                    "sale_price": 99.99,
                    "image_url": "soundflex_earbuds.jpg",
                    "tags": ["Earbuds", "Wireless", "Bluetooth", "Portable", "Sports", "Waterproof"]
                }
            ]
        },
        
        # Smartphones category
        {
            "category": "Smartphones",
            "products": [
                {
                    "name": "GalaxyPro X5 Smartphone",
                    "description": "The GalaxyPro X5 features a stunning 6.7-inch AMOLED display, 108MP camera system, and the latest processor for exceptional performance. With 5G connectivity and all-day battery life, it's perfect for professionals and enthusiasts alike.",
                    "short_description": "Flagship smartphone with pro-grade camera system",
                    "price": 999.99,
                    "sale_price": 899.99,
                    "image_url": "galaxypro_x5.jpg",
                    "tags": ["Smartphone", "5G", "OLED", "High-resolution", "Fast-charging", "Samsung", "Premium"]
                },
                {
                    "name": "PixelView Lite Smartphone",
                    "description": "PixelView Lite offers the essential smartphone experience with a bright 6.2-inch display, reliable performance, and an exceptional camera that captures stunning photos even in low light. Its 5000mAh battery ensures you stay powered all day long.",
                    "short_description": "Budget-friendly smartphone with great camera",
                    "price": 399.99,
                    "sale_price": 349.99,
                    "image_url": "pixelview_lite.jpg",
                    "tags": ["Smartphone", "Budget", "Long-battery", "Google", "Camera", "AI-powered"]
                }
            ]
        },
        
        # Laptops category
        {
            "category": "Laptops",
            "products": [
                {
                    "name": "UltraBook Pro 16",
                    "description": "The UltraBook Pro 16 is designed for professionals who demand the best. Featuring a 16-inch Liquid Retina XDR display, powerful processor, and 32GB of unified memory, it handles intensive workflows with ease.",
                    "short_description": "Professional-grade laptop with stunning display",
                    "price": 2499.99,
                    "sale_price": None,
                    "image_url": "ultrabook_pro.jpg",
                    "tags": ["Laptop", "Professional", "High-performance", "Retina", "Thunderbolt", "Apple", "Premium"]
                },
                {
                    "name": "TechBook Gaming Laptop",
                    "description": "Engineered for gamers, the TechBook Gaming Laptop features a 15.6-inch 144Hz display, RGB keyboard, and dedicated graphics card to deliver smooth gameplay and immersive experiences for the most demanding games.",
                    "short_description": "High-performance gaming laptop with 144Hz display",
                    "price": 1299.99,
                    "sale_price": 1149.99,
                    "image_url": "techbook_gaming.jpg",
                    "tags": ["Laptop", "Gaming", "High-performance", "NVIDIA", "RGB", "Fast-charging", "HD"]
                },
                {
                    "name": "LightBook Air",
                    "description": "The LightBook Air weighs just 2.2 pounds but doesn't compromise on performance with its efficient processor and 13.3-inch display. Perfect for students and travelers who need reliable computing on the go.",
                    "short_description": "Ultra-lightweight laptop for productivity on the go",
                    "price": 899.99,
                    "sale_price": 799.99,
                    "image_url": "lightbook_air.jpg",
                    "tags": ["Laptop", "Lightweight", "Portable", "Travel", "Students", "Long-battery", "Budget"]
                }
            ]
        },
        
        # Electronics category
        {
            "category": "Electronics",
            "products": [
                {
                    "name": "SmartView 4K 55\" TV",
                    "description": "Experience stunning visuals with the SmartView 4K TV featuring Quantum Dot technology, HDR support, and a sleek design. Smart features give you access to all your favorite streaming services and apps.",
                    "short_description": "55-inch 4K smart TV with Quantum Dot technology",
                    "price": 799.99,
                    "sale_price": 699.99,
                    "image_url": "smartview_tv.jpg",
                    "tags": ["4K", "Ultra-HD", "Smart", "WiFi", "Entertainment", "Streaming", "QLED"]
                },
                {
                    "name": "SoundBase Wireless Speaker",
                    "description": "Fill your room with immersive sound from the SoundBase Wireless Speaker. This compact yet powerful speaker offers rich bass, clear treble, and connects via Bluetooth or WiFi for versatile audio streaming.",
                    "short_description": "Compact wireless speaker with room-filling sound",
                    "price": 199.99,
                    "sale_price": None,
                    "image_url": "soundbase_speaker.jpg",
                    "tags": ["Speaker", "Wireless", "Bluetooth", "WiFi", "Portable", "Music", "JBL"]
                },
                {
                    "name": "FitTrack Pro Smartwatch",
                    "description": "Track your health and fitness with the FitTrack Pro Smartwatch. Monitor heart rate, sleep quality, and activity levels while enjoying smart notifications and music control from your wrist.",
                    "short_description": "Advanced fitness tracking smartwatch with heart monitoring",
                    "price": 249.99,
                    "sale_price": 199.99,
                    "image_url": "fittrack_pro.jpg",
                    "tags": ["Watch", "Fitness-tracker", "Waterproof", "Smart", "Bluetooth", "Exercise", "Fitbit"]
                }
            ]
        }
    ]
    
    # Lists to collect all the products, product-tag relationships, and product images
    all_products = []
    all_product_tags = []
    all_product_images = []
    
    # Generate 200 products based on templates
    product_id = 1
    
    # First, insert the template products as-is
    for category_template in product_templates:
        category_name = category_template["category"]
        # Get category ID
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()[0]
        
        for product in category_template["products"]:
            # Add product (without image_url field)
            all_products.append((
                None,
                product["name"],
                product["description"],
                product["short_description"],
                product["price"],
                product["sale_price"],
                category_id,
                product.get("brand", "Generic Brand"),  # Add brand
                1  # is_active
            ))
            
            # Add product image separately
            all_product_images.append((
                product_id,
                product["image_url"],
                1  # is_primary
            ))
            
            # Add product-tag relationships
            for tag_name in product["tags"]:
                if tag_name in tag_map:
                    all_product_tags.append((product_id, tag_map[tag_name]))
            
            product_id += 1
    
    # Generate additional products with variations
    while len(all_products) < 200:
        # Pick a random template product
        category_template = random.choice(product_templates)
        template_product = random.choice(category_template["products"])
        
        # Get category ID
        category_name = category_template["category"]
        cursor.execute('SELECT id FROM categories WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()[0]
        
        # Create variations of the name
        adjectives = ["Premium", "Ultra", "Elite", "Pro", "Max", "Advanced", "Essential", "Classic", "Next-Gen", "Smart"]
        variants = ["Plus", "Lite", "Mini", "XL", "SE", "2.0", "3.0", "Air", "Neo", "Eco"]
        
        new_name = f"{random.choice(adjectives)} {template_product['name'].split(' ', 1)[0]} {random.choice(variants)}"
        
        # Adjust price (80% to 120% of original)
        price_factor = random.uniform(0.8, 1.2)
        new_price = round(template_product["price"] * price_factor, 2)
        
        # Decide if on sale (30% chance)
        if random.random() < 0.3:
            sale_price = round(new_price * 0.85, 2)
        else:
            sale_price = None
        
        # Create a new product based on the template (without image_url field)
        all_products.append((
            None,
            new_name,
            template_product["description"].replace(template_product["name"], new_name),
            f"Advanced version of {template_product['short_description']}",
            new_price,
            sale_price,
            category_id,
            template_product.get("brand", "Generic Brand"),  # Add brand
            1  # is_active
        ))
        
        # Add product image separately
        all_product_images.append((
            product_id,
            f"product_{product_id}.jpg",
            1  # is_primary
        ))
        
        # Select most of the original tags plus some random ones
        original_tags = template_product["tags"]
        # Keep 70% of original tags
        keep_tags = random.sample(original_tags, k=max(1, int(len(original_tags) * 0.7)))
        
        # Add 2-4 random tags not in the original tags
        available_tags = [tag for tag in tag_map.keys() if tag not in original_tags]
        if available_tags:
            random_tags = random.sample(available_tags, k=min(random.randint(2, 4), len(available_tags)))
            product_tags = keep_tags + random_tags
            
            # Add product-tag relationships
            for tag_name in product_tags:
                if tag_name in tag_map:
                    all_product_tags.append((product_id, tag_map[tag_name]))
        
        product_id += 1
    
    # Insert all products at once
    cursor.executemany('''
    INSERT INTO products (id, name, description, short_description, price, sale_price, category_id, brand, is_active)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', all_products)
    
    # Insert all product images
    cursor.executemany('''
    INSERT INTO product_images (product_id, image_url, is_primary)
    VALUES (?, ?, ?)
    ''', all_product_images)
    
    # Insert all product-tag relationships
    cursor.executemany('''
    INSERT INTO product_tags (product_id, tag_id)
    VALUES (?, ?)
    ''', all_product_tags)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database populated with {len(all_products)} products, {len(all_product_tags)} product-tag relationships, and {len(all_product_images)} product images.")

if __name__ == "__main__":
    populate_database()