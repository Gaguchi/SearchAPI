import sqlite3
import datetime
import json
import random

# Database file path
DB_FILE = 'ecommerce.db'

def populate_database():
    """Populate the e-commerce database with sample data"""
    # Connect to the existing database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Insert sample data
    insert_sample_data(conn)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database '{DB_FILE}' populated successfully with sample data.")

def insert_sample_data(conn):
    """Insert sample data into all tables"""
    cursor = conn.cursor()
    
    # Insert categories
    categories = [
        (None, "Electronics", "Electronic devices and gadgets", None, "electronics.jpg"),
        (None, "Smartphones", "Mobile phones and accessories", 1, "smartphones.jpg"),
        (None, "Laptops", "Notebook computers", 1, "laptops.jpg"),
        (None, "Audio", "Headphones, speakers and audio equipment", 1, "audio.jpg"),
        (None, "Clothing", "Apparel and fashion items", None, "clothing.jpg"),
        (None, "Men's", "Men's clothing and accessories", 5, "mens.jpg"),
        (None, "Women's", "Women's clothing and accessories", 5, "womens.jpg"),
        (None, "Home & Kitchen", "Home appliances and kitchenware", None, "home.jpg"),
        (None, "Books", "Books and publications", None, "books.jpg"),
        (None, "Sports & Outdoors", "Sporting goods and outdoor equipment", None, "sports.jpg")
    ]
    
    cursor.executemany('''
    INSERT INTO categories (id, name, description, parent_id, image_url)
    VALUES (?, ?, ?, ?, ?)
    ''', categories)
    
    # Insert tags
    tags = [
        (None, "Best Seller", "Products that are selling well"),
        (None, "New Arrival", "Recently added products"),
        (None, "Sale", "Products on sale"),
        (None, "Limited Edition", "Products with limited availability"),
        (None, "Organic", "Organic products"),
        (None, "Eco-friendly", "Environmentally friendly products"),
        (None, "Handmade", "Handcrafted products"),
        (None, "Premium", "High-quality premium products"),
        (None, "Budget", "Affordable budget-friendly products"),
        (None, "Gift Idea", "Products suitable as gifts")
    ]
    
    cursor.executemany('''
    INSERT INTO tags (id, name, description)
    VALUES (?, ?, ?)
    ''', tags)
    
    # Insert products
    products = [
        # Electronics - Smartphones
        (None, "XPhone 15 Pro", "XP15PRO", 
         "The XPhone 15 Pro features a stunning 6.7-inch Super Retina XDR display with ProMotion technology for a responsive and fluid experience. Powered by the latest A17 Pro chip, it delivers exceptional performance for even the most demanding tasks. The pro camera system includes a 48MP main camera, capturing incredible detail and color, along with ultrawide and telephoto lenses for versatile photography. With up to 1TB of storage, you'll have plenty of space for photos, videos, and apps. The device boasts all-day battery life and is built with premium materials including surgical-grade stainless steel and Ceramic Shield front cover for enhanced durability.",
         "Flagship smartphone with pro-grade camera system and powerful performance.", 
         999.99, 949.99, 600.00, 150, 2, "XPhone", 0.24, 
         json.dumps({"length": 6.33, "width": 3.05, "height": 0.32}), 1, 1),
        
        # Electronics - Laptops
        (None, "UltraBook Pro 16", "UBPRO16", 
         "The UltraBook Pro 16 is designed for professionals who demand the best. Featuring a 16-inch Liquid Retina XDR display with mini-LED technology, it delivers exceptional brightness and contrast. Powered by the M2 Pro chip with a 12-core CPU and 19-core GPU, it handles intensive workflows with ease. The laptop includes 32GB of unified memory and a 1TB SSD for ample storage and rapid access to files. The Magic Keyboard provides a comfortable typing experience, and the advanced camera and studio-quality microphones make it perfect for video conferencing. Its all-day battery life and MagSafe charging add convenience to its impressive feature set.",
         "Professional-grade laptop with stunning display and powerful performance.", 
         2499.99, 2399.99, 1800.00, 75, 3, "UltraBook", 4.7, 
         json.dumps({"length": 14.01, "width": 9.77, "height": 0.66}), 1, 1),
        
        # Clothing - Men's
        (None, "Classic Fit Oxford Shirt", "MOS-CF-BLUE", 
         "This versatile Oxford shirt is crafted from premium 100% cotton fabric that's been pre-washed for exceptional softness. The classic fit provides a comfortable silhouette without being too loose or too tight. Features include a button-down collar, a single chest pocket, and a box pleat at the back for ease of movement. Perfect for both casual and semi-formal occasions, this shirt can be dressed up with chinos for the office or paired with jeans for a more relaxed look. The durable construction and timeless design ensure this will be a staple in your wardrobe for years to come.",
         "Premium cotton button-down shirt with a comfortable classic fit.", 
         59.99, 49.99, 20.00, 200, 6, "Fashion Basics", 0.3, 
         json.dumps({"length": 30, "width": 22, "height": 1}), 0, 1),
        
        # Clothing - Women's
        (None, "Merino Wool Cardigan", "WWC-MERINO-GRAY", 
         "This luxurious cardigan is crafted from 100% fine Merino wool, known for its exceptional softness, breathability, and natural temperature regulation. The relaxed fit and hip-length cut create a flattering silhouette, while the ribbed cuffs and hem add structure and durability. Five-button front closure with a subtle V-neck design makes this piece versatile for layering. The fine-gauge knit provides warmth without bulk, making it perfect for year-round wear. This cardigan transitions effortlessly from office to weekend, pairing beautifully with everything from tailored trousers to casual jeans.",
         "Soft, versatile Merino wool cardigan with a flattering relaxed fit.", 
         89.99, 79.99, 40.00, 120, 7, "Wool & Co", 0.4, 
         json.dumps({"length": 26, "width": 18, "height": 1}), 0, 1),
        
        # Home & Kitchen
        (None, "Pro Chef Kitchen Knife", "CHEFKNIFE-8", 
         "This professional 8-inch chef's knife is the ultimate kitchen essential, crafted with precision from high-carbon German stainless steel for exceptional durability and edge retention. The blade features a 15-degree cutting edge on each side, providing the perfect balance between sharpness and strength. The ergonomic handle is made from premium G10 material, offering a comfortable grip even during extended use and resistance to heat, cold, and moisture. The knife's full-tang construction ensures outstanding balance and stability. Perfect for chopping, slicing, dicing, and mincing, this versatile knife will elevate your cooking experience with its professional-grade performance and precision.",
         "Professional-grade 8-inch chef knife with German steel blade and ergonomic handle.", 
         129.99, None, 50.00, 85, 8, "Master Cutlery", 0.6, 
         json.dumps({"length": 13, "width": 1.8, "height": 0.1}), 0, 1),
        
        # Books
        (None, "The Art of Strategic Thinking", "BOOK-STRATEGY-101", 
         "This comprehensive guide to strategic thinking combines practical frameworks with real-world case studies to develop your analytical reasoning and decision-making capabilities. The author, Dr. Eleanor Hughes, draws on her 25 years of experience as a business consultant and academic to present a systematic approach to problem-solving that can be applied in both professional and personal contexts. The book is divided into three parts: fundamentals of strategic analysis, advanced decision frameworks, and implementation strategies. Each chapter includes exercises designed to reinforce key concepts and develop your strategic mindset. Whether you're a business leader, aspiring entrepreneur, or simply looking to make better decisions, this book provides valuable insights into the art and science of strategic thinking.",
         "Comprehensive guide to developing strategic thinking skills with practical frameworks and case studies.", 
         24.99, 19.99, 8.00, 250, 9, "Pinnacle Publishing", 0.9, 
         json.dumps({"length": 9, "width": 6, "height": 1.2}), 0, 1),
        
        # Sports & Outdoors
        (None, "Ultra Trail Running Shoes", "TRAIL-X5-10", 
         "Designed for serious trail runners, these shoes feature a responsive cushioning system that provides exceptional impact absorption and energy return on varied terrain. The Vibram Megagrip outsole delivers superior traction on both wet and dry surfaces, while the rock plate protects your feet from sharp objects without sacrificing ground feel. The breathable mesh upper is reinforced with TPU overlays for durability and support, while remaining lightweight and quick-drying. The padded collar and gusseted tongue prevent debris from entering the shoe, and the quick-lace system allows for easy adjustment even with gloved hands. With a 5mm drop, these shoes promote a natural stride while still offering protection for long-distance trail adventures.",
         "High-performance trail running shoes with exceptional grip and cushioning for varied terrain.", 
         149.99, 129.99, 70.00, 90, 10, "Alpine Athletics", 0.62, 
         json.dumps({"length": 12, "width": 4.5, "height": 5}), 0, 1)
    ]
    
    cursor.executemany('''
    INSERT INTO products (
        id, name, sku, description, short_description, price, sale_price, cost, 
        stock_quantity, category_id, brand, weight, dimensions, is_featured, is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Insert product images
    product_images = [
        (None, 1, "xphone_15_pro_main.jpg", 1, 1, "XPhone 15 Pro in Deep Blue"),
        (None, 1, "xphone_15_pro_back.jpg", 0, 2, "XPhone 15 Pro rear view showing camera system"),
        (None, 1, "xphone_15_pro_side.jpg", 0, 3, "XPhone 15 Pro side profile"),
        (None, 2, "ultrabook_pro_main.jpg", 1, 1, "UltraBook Pro 16 front view"),
        (None, 2, "ultrabook_pro_open.jpg", 0, 2, "UltraBook Pro 16 open at 45 degrees"),
        (None, 2, "ultrabook_pro_keyboard.jpg", 0, 3, "UltraBook Pro 16 keyboard close-up"),
        (None, 3, "oxford_shirt_blue_front.jpg", 1, 1, "Blue Oxford Shirt front view"),
        (None, 3, "oxford_shirt_blue_back.jpg", 0, 2, "Blue Oxford Shirt back view"),
        (None, 3, "oxford_shirt_blue_detail.jpg", 0, 3, "Blue Oxford Shirt fabric detail"),
        (None, 4, "wool_cardigan_gray_front.jpg", 1, 1, "Gray Merino Wool Cardigan front view"),
        (None, 4, "wool_cardigan_gray_side.jpg", 0, 2, "Gray Merino Wool Cardigan side view"),
        (None, 4, "wool_cardigan_gray_detail.jpg", 0, 3, "Gray Merino Wool Cardigan knit detail"),
        (None, 5, "chef_knife_main.jpg", 1, 1, "Pro Chef Kitchen Knife full view"),
        (None, 5, "chef_knife_cutting.jpg", 0, 2, "Pro Chef Kitchen Knife in use"),
        (None, 5, "chef_knife_handle.jpg", 0, 3, "Pro Chef Kitchen Knife handle detail"),
        (None, 6, "strategic_thinking_cover.jpg", 1, 1, "The Art of Strategic Thinking book cover"),
        (None, 6, "strategic_thinking_back.jpg", 0, 2, "The Art of Strategic Thinking back cover"),
        (None, 6, "strategic_thinking_open.jpg", 0, 3, "The Art of Strategic Thinking open to table of contents"),
        (None, 7, "trail_shoes_pair.jpg", 1, 1, "Ultra Trail Running Shoes pair"),
        (None, 7, "trail_shoes_sole.jpg", 0, 2, "Ultra Trail Running Shoes sole detail"),
        (None, 7, "trail_shoes_side.jpg", 0, 3, "Ultra Trail Running Shoes side profile")
    ]
    
    cursor.executemany('''
    INSERT INTO product_images (
        id, product_id, image_url, is_primary, display_order, alt_text
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ''', product_images)
    
    # Insert product tags
    product_tags = [
        (1, 1),  # XPhone 15 Pro - Best Seller
        (1, 2),  # XPhone 15 Pro - New Arrival
        (1, 8),  # XPhone 15 Pro - Premium
        (2, 2),  # UltraBook Pro 16 - New Arrival
        (2, 8),  # UltraBook Pro 16 - Premium
        (3, 3),  # Oxford Shirt - Sale
        (3, 9),  # Oxford Shirt - Budget
        (4, 8),  # Wool Cardigan - Premium
        (4, 10), # Wool Cardigan - Gift Idea
        (5, 1),  # Chef Knife - Best Seller
        (5, 8),  # Chef Knife - Premium
        (5, 10), # Chef Knife - Gift Idea
        (6, 9),  # Strategy Book - Budget
        (6, 10), # Strategy Book - Gift Idea
        (7, 4),  # Trail Shoes - Limited Edition
        (7, 8)   # Trail Shoes - Premium
    ]
    
    cursor.executemany('''
    INSERT INTO product_tags (product_id, tag_id)
    VALUES (?, ?)
    ''', product_tags)
    
    # Insert product attributes
    product_attributes = [
        # XPhone attributes
        (None, 1, "Display", "6.7-inch Super Retina XDR", 1, 1, 1),
        (None, 1, "Processor", "A17 Pro chip", 2, 1, 1),
        (None, 1, "Storage", "128GB / 256GB / 512GB / 1TB", 3, 1, 1),
        (None, 1, "Camera", "48MP main, 12MP ultrawide, 12MP telephoto", 4, 1, 1),
        (None, 1, "Battery", "4400mAh", 5, 1, 1),
        (None, 1, "Water Resistance", "IP68", 6, 1, 1),
        (None, 1, "Operating System", "iOS 17", 7, 1, 1),
        
        # UltraBook attributes
        (None, 2, "Display", "16-inch Liquid Retina XDR", 1, 1, 1),
        (None, 2, "Processor", "M2 Pro (12-core CPU, 19-core GPU)", 2, 1, 1),
        (None, 2, "Memory", "32GB unified memory", 3, 1, 1),
        (None, 2, "Storage", "1TB SSD", 4, 1, 1),
        (None, 2, "Battery", "Up to 22 hours", 5, 1, 1),
        (None, 2, "Ports", "3x Thunderbolt 4, HDMI, SDXC, MagSafe 3", 6, 1, 1),
        (None, 2, "Operating System", "macOS", 7, 1, 1),
        
        # Oxford Shirt attributes
        (None, 3, "Material", "100% Cotton", 1, 1, 1),
        (None, 3, "Fit", "Classic Fit", 2, 1, 1),
        (None, 3, "Care", "Machine washable", 3, 0, 1),
        (None, 3, "Collar", "Button-down", 4, 1, 1),
        (None, 3, "Cuff", "Adjustable button cuff", 5, 0, 1),
        
        # Wool Cardigan attributes
        (None, 4, "Material", "100% Merino Wool", 1, 1, 1),
        (None, 4, "Fit", "Relaxed Fit", 2, 1, 1),
        (None, 4, "Care", "Hand wash cold", 3, 0, 1),
        (None, 4, "Closure", "5-button front", 4, 0, 1),
        (None, 4, "Features", "Ribbed cuffs and hem", 5, 0, 1),
        
        # Chef Knife attributes
        (None, 5, "Blade Material", "High-carbon German stainless steel", 1, 1, 1),
        (None, 5, "Blade Length", "8 inches", 2, 1, 1),
        (None, 5, "Handle Material", "G10 composite", 3, 1, 1),
        (None, 5, "Edge Angle", "15 degrees per side", 4, 0, 1),
        (None, 5, "Construction", "Full tang", 5, 1, 1),
        
        # Book attributes
        (None, 6, "Format", "Hardcover", 1, 1, 1),
        (None, 6, "Pages", "384", 2, 0, 1),
        (None, 6, "Publication Date", "2023-05-15", 3, 0, 1),
        (None, 6, "Language", "English", 4, 1, 1),
        (None, 6, "ISBN", "978-1234567890", 5, 0, 1),
        
        # Trail Shoes attributes
        (None, 7, "Upper", "Breathable mesh with TPU overlays", 1, 1, 1),
        (None, 7, "Outsole", "Vibram Megagrip", 2, 1, 1),
        (None, 7, "Drop", "5mm", 3, 1, 1),
        (None, 7, "Weight", "310g (US Men's 9)", 4, 1, 1),
        (None, 7, "Features", "Rock plate, quick-lace system", 5, 0, 1)
    ]
    
    cursor.executemany('''
    INSERT INTO product_attributes (
        id, product_id, attribute_name, attribute_value, display_order, is_filterable, is_visible
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', product_attributes)
    
    # Insert product variants for products that have them
    product_variants = [
        # XPhone variants (storage options)
        (None, 1, "XP15PRO-128", "XPhone 15 Pro 128GB", 0, 100, json.dumps({"storage": "128GB", "color": "Deep Blue"}), "xphone_15_pro_blue_128.jpg", 1),
        (None, 1, "XP15PRO-256", "XPhone 15 Pro 256GB", 100, 50, json.dumps({"storage": "256GB", "color": "Deep Blue"}), "xphone_15_pro_blue_256.jpg", 1),
        (None, 1, "XP15PRO-512", "XPhone 15 Pro 512GB", 200, 25, json.dumps({"storage": "512GB", "color": "Deep Blue"}), "xphone_15_pro_blue_512.jpg", 1),
        (None, 1, "XP15PRO-1TB", "XPhone 15 Pro 1TB", 300, 10, json.dumps({"storage": "1TB", "color": "Deep Blue"}), "xphone_15_pro_blue_1tb.jpg", 1),
        (None, 1, "XP15PRO-128-G", "XPhone 15 Pro 128GB", 0, 100, json.dumps({"storage": "128GB", "color": "Graphite"}), "xphone_15_pro_graphite_128.jpg", 1),
        (None, 1, "XP15PRO-256-G", "XPhone 15 Pro 256GB", 100, 50, json.dumps({"storage": "256GB", "color": "Graphite"}), "xphone_15_pro_graphite_256.jpg", 1),
        
        # Oxford Shirt variants (sizes and colors)
        (None, 3, "MOS-CF-BLUE-S", "Oxford Shirt Blue Small", 0, 30, json.dumps({"size": "S", "color": "Blue"}), "oxford_shirt_blue_s.jpg", 1),
        (None, 3, "MOS-CF-BLUE-M", "Oxford Shirt Blue Medium", 0, 50, json.dumps({"size": "M", "color": "Blue"}), "oxford_shirt_blue_m.jpg", 1),
        (None, 3, "MOS-CF-BLUE-L", "Oxford Shirt Blue Large", 0, 50, json.dumps({"size": "L", "color": "Blue"}), "oxford_shirt_blue_l.jpg", 1),
        (None, 3, "MOS-CF-BLUE-XL", "Oxford Shirt Blue XL", 0, 40, json.dumps({"size": "XL", "color": "Blue"}), "oxford_shirt_blue_xl.jpg", 1),
        (None, 3, "MOS-CF-WHITE-S", "Oxford Shirt White Small", 0, 30, json.dumps({"size": "S", "color": "White"}), "oxford_shirt_white_s.jpg", 1),
        (None, 3, "MOS-CF-WHITE-M", "Oxford Shirt White Medium", 0, 50, json.dumps({"size": "M", "color": "White"}), "oxford_shirt_white_m.jpg", 1),
        (None, 3, "MOS-CF-WHITE-L", "Oxford Shirt White Large", 0, 50, json.dumps({"size": "L", "color": "White"}), "oxford_shirt_white_l.jpg", 1),
        (None, 3, "MOS-CF-WHITE-XL", "Oxford Shirt White XL", 0, 40, json.dumps({"size": "XL", "color": "White"}), "oxford_shirt_white_xl.jpg", 1),
        
        # Wool Cardigan variants (sizes and colors)
        (None, 4, "WWC-MERINO-GRAY-S", "Wool Cardigan Gray Small", 0, 20, json.dumps({"size": "S", "color": "Gray"}), "wool_cardigan_gray_s.jpg", 1),
        (None, 4, "WWC-MERINO-GRAY-M", "Wool Cardigan Gray Medium", 0, 30, json.dumps({"size": "M", "color": "Gray"}), "wool_cardigan_gray_m.jpg", 1),
        (None, 4, "WWC-MERINO-GRAY-L", "Wool Cardigan Gray Large", 0, 30, json.dumps({"size": "L", "color": "Gray"}), "wool_cardigan_gray_l.jpg", 1),
        (None, 4, "WWC-MERINO-GRAY-XL", "Wool Cardigan Gray XL", 0, 20, json.dumps({"size": "XL", "color": "Gray"}), "wool_cardigan_gray_xl.jpg", 1),
        (None, 4, "WWC-MERINO-NAVY-S", "Wool Cardigan Navy Small", 0, 20, json.dumps({"size": "S", "color": "Navy"}), "wool_cardigan_navy_s.jpg", 1),
        (None, 4, "WWC-MERINO-NAVY-M", "Wool Cardigan Navy Medium", 0, 30, json.dumps({"size": "M", "color": "Navy"}), "wool_cardigan_navy_m.jpg", 1),
        (None, 4, "WWC-MERINO-NAVY-L", "Wool Cardigan Navy Large", 0, 30, json.dumps({"size": "L", "color": "Navy"}), "wool_cardigan_navy_l.jpg", 1),
        (None, 4, "WWC-MERINO-NAVY-XL", "Wool Cardigan Navy XL", 0, 20, json.dumps({"size": "XL", "color": "Navy"}), "wool_cardigan_navy_xl.jpg", 1),
        
        # Trail Shoes variants (sizes)
        (None, 7, "TRAIL-X5-8", "Trail Shoes Size 8", 0, 15, json.dumps({"size": "8", "color": "Gray/Blue"}), "trail_shoes_8.jpg", 1),
        (None, 7, "TRAIL-X5-9", "Trail Shoes Size 9", 0, 20, json.dumps({"size": "9", "color": "Gray/Blue"}), "trail_shoes_9.jpg", 1),
        (None, 7, "TRAIL-X5-10", "Trail Shoes Size 10", 0, 25, json.dumps({"size": "10", "color": "Gray/Blue"}), "trail_shoes_10.jpg", 1),
        (None, 7, "TRAIL-X5-11", "Trail Shoes Size 11", 0, 20, json.dumps({"size": "11", "color": "Gray/Blue"}), "trail_shoes_11.jpg", 1),
        (None, 7, "TRAIL-X5-12", "Trail Shoes Size 12", 0, 10, json.dumps({"size": "12", "color": "Gray/Blue"}), "trail_shoes_12.jpg", 1)
    ]
    
    cursor.executemany('''
    INSERT INTO product_variants (
        id, product_id, sku, variant_name, price_adjustment, stock_quantity, 
        attributes, image_url, is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', product_variants)
    
    # Insert users
    # Note: In a real application, passwords would be properly hashed
    users = [
        (None, "admin@example.com", "hashed_password_admin", "Admin", "User", "+1234567890", 1, 1, datetime.datetime.now(), None, None),
        (None, "john.doe@example.com", "hashed_password_john", "John", "Doe", "+1987654321", 0, 1, datetime.datetime.now(), None, None),
        (None, "jane.smith@example.com", "hashed_password_jane", "Jane", "Smith", "+1122334455", 0, 1, datetime.datetime.now(), None, None)
    ]
    
    cursor.executemany('''
    INSERT INTO users (
        id, email, password_hash, first_name, last_name, phone, 
        is_admin, is_active, last_login, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)
    
    # Insert addresses
    addresses = [
        (None, 2, "shipping", "123 Main St", "Apt 4B", "New York", "NY", "10001", "USA", 1, None, None),
        (None, 2, "billing", "123 Main St", "Apt 4B", "New York", "NY", "10001", "USA", 1, None, None),
        (None, 3, "shipping", "456 Oak Ave", None, "San Francisco", "CA", "94102", "USA", 1, None, None),
        (None, 3, "billing", "789 Pine St", "Suite 101", "San Francisco", "CA", "94103", "USA", 1, None, None)
    ]
    
    cursor.executemany('''
    INSERT INTO addresses (
        id, user_id, address_type, address_line1, address_line2, city,
        state, postal_code, country, is_default, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', addresses)
    
    # Insert orders
    orders = [
        (None, 2, "ORD-10001", "2023-04-15 10:30:00", "delivered", 1049.98, 1, 2, "Express", 15.00, 95.45, 0, "Credit Card", "paid", "Please leave at front door", None, None),
        (None, 3, "ORD-10002", "2023-05-20 14:45:00", "shipped", 169.98, 3, 4, "Standard", 9.99, 15.45, 0, "PayPal", "paid", None, None, None),
        (None, 2, "ORD-10003", "2023-05-22 09:15:00", "processing", 2499.99, 1, 2, "Express", 25.00, 227.27, 200.00, "Credit Card", "paid", None, None, None)
    ]
    
    cursor.executemany('''
    INSERT INTO orders (
        id, user_id, order_number, order_date, status, total_amount,
        shipping_address_id, billing_address_id, shipping_method, shipping_cost,
        tax_amount, discount_amount, payment_method, payment_status, notes,
        created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', orders)
    
    # Insert order items
    order_items = [
        (None, 1, 1, 1, 1, 999.99, 999.99, 0, None),
        (None, 1, 5, None, 1, 49.99, 49.99, 0, None),
        (None, 2, 6, None, 1, 19.99, 19.99, 0, None),
        (None, 2, 3, 7, 3, 49.99, 149.97, 0, None),
        (None, 3, 2, None, 1, 2499.99, 2499.99, 200.00, None)
    ]
    
    cursor.executemany('''
    INSERT INTO order_items (
        id, order_id, product_id, variant_id, quantity,
        unit_price, subtotal, discount_amount, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', order_items)
    
    # Insert reviews
    reviews = [
        (None, 1, 2, 5, "Excellent smartphone", "This is the best phone I've ever owned. The camera is amazing and the battery lasts all day.", 1, 1, None, None),
        (None, 2, 3, 4, "Great laptop", "Very powerful and the screen is beautiful. A bit expensive but worth it for the performance.", 1, 1, None, None),
        (None, 3, 2, 3, "Nice shirt", "Good quality material but runs a bit large. I should have ordered a size smaller.", 1, 1, None, None),
        (None, 5, 3, 5, "Perfect knife", "Excellent balance and stays sharp. Professional quality at a reasonable price.", 1, 1, None, None),
        (None, 6, 2, 4, "Good read", "Insightful content and well-organized chapters. I use the frameworks regularly at work now.", 1, 1, None, None)
    ]
    
    cursor.executemany('''
    INSERT INTO reviews (
        id, product_id, user_id, rating, title, comment,
        is_verified_purchase, is_approved, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', reviews)
    
    # Insert promotions
    promotions = [
        (None, "Summer Sale", "20% off on selected items", "percentage", 20.0, "SUMMER20", "2023-06-01 00:00:00", "2023-08-31 23:59:59", 50.00, 1000, 124, 1, None, None),
        (None, "New Customer", "Get $10 off your first purchase", "fixed_amount", 10.0, "WELCOME10", None, None, 30.00, 1, 0, 1, None, None),
        (None, "Flash Sale", "15% off all electronics", "percentage", 15.0, "FLASH15", "2023-05-25 00:00:00", "2023-05-26 23:59:59", 100.00, 500, 0, 1, None, None)
    ]
    
    cursor.executemany('''
    INSERT INTO promotions (
        id, name, description, discount_type, discount_value, code,
        starts_at, ends_at, min_purchase_amount, usage_limit, used_count, is_active,
        created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', promotions)
    
    # Insert promotion product relationships
    promotion_products = [
        (1, 3),  # Summer Sale - Oxford Shirt
        (1, 4),  # Summer Sale - Wool Cardigan
        (3, 1),  # Flash Sale - XPhone
        (3, 2)   # Flash Sale - UltraBook
    ]
    
    cursor.executemany('''
    INSERT INTO promotion_products (promotion_id, product_id)
    VALUES (?, ?)
    ''', promotion_products)
    
    # Insert promotion category relationships
    promotion_categories = [
        (1, 5),  # Summer Sale - Clothing
        (3, 1)   # Flash Sale - Electronics
    ]
    
    cursor.executemany('''
    INSERT INTO promotion_categories (promotion_id, category_id)
    VALUES (?, ?)
    ''', promotion_categories)
    
    # Insert sample search logs
    search_logs = [
        (None, 2, "session123", "smartphone", 3, "2023-05-01 10:15:00"),
        (None, 3, "session456", "merino wool", 1, "2023-05-02 14:30:00"),
        (None, None, "session789", "kitchen knife", 2, "2023-05-03 09:45:00"),
        (None, 2, "session123", "trail running shoes", 1, "2023-05-04 16:20:00"),
        (None, None, "session567", "laptop", 2, "2023-05-05 11:10:00")
    ]
    
    cursor.executemany('''
    INSERT INTO search_logs (
        id, user_id, session_id, search_query, results_count, search_date
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ''', search_logs)
    
    print("Sample data inserted successfully.")

if __name__ == "__main__":
    populate_database()