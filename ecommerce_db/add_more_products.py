import sqlite3
import datetime
import json
import random

# Database file path
DB_FILE = 'ecommerce.db'

def add_more_products():
    """Add 25 more products to the existing e-commerce database"""
    # Connect to the existing database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get the current highest product ID to start our new products from
    cursor.execute("SELECT MAX(id) FROM products")
    max_product_id = cursor.fetchone()[0] or 0
    start_product_id = max_product_id + 1
    
    # Insert additional products and related data
    insert_additional_products(conn, start_product_id)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Successfully added 25 more products to database '{DB_FILE}'.")

def insert_additional_products(conn, start_id):
    """Insert 25 more products and their related data into the database"""
    cursor = conn.cursor()
    
    # Additional products to add
    products = [
        # Electronics - Smart Watches
        (None, "SmartWatch Ultra", "SW-ULTRA-V1", 
         "The SmartWatch Ultra features a stunning 2.0-inch AMOLED display with always-on capability and 1000 nits of brightness. Track your health with advanced sensors including ECG, blood oxygen, and continuous heart rate monitoring. With built-in GPS, 50m water resistance, and 7-day battery life, it's the perfect companion for fitness enthusiasts. The watch supports over 100 workout modes and automatically detects common exercises. Notifications, calls, and app alerts are seamlessly delivered to your wrist, while the voice assistant allows hands-free control. Crafted from premium materials including sapphire crystal and titanium, it offers both durability and style.",
         "Premium smartwatch with health tracking and 7-day battery life.", 
         349.99, 299.99, 150.00, 100, 1, "TechWear", 0.18, 
         json.dumps({"length": 1.77, "width": 1.49, "height": 0.42}), 1, 1),
        
        # Electronics - Wireless Earbuds
        (None, "SoundPods Pro", "SP-PRO-V2", 
         "SoundPods Pro wireless earbuds deliver an immersive audio experience with custom-designed dynamic drivers and active noise cancellation that adapts to your environment. The transparency mode lets you hear your surroundings when needed, while the spatial audio feature creates a three-dimensional listening experience. With 8 hours of listening time per charge and an additional 24 hours from the charging case, you won't have to worry about battery life. The earbuds are sweat and water-resistant, making them perfect for workouts. Voice calls are crystal clear thanks to beamforming microphones that focus on your voice and block out background noise.",
         "Premium wireless earbuds with adaptive noise cancellation and spatial audio.", 
         199.99, 179.99, 80.00, 150, 4, "AudioTech", 0.12, 
         json.dumps({"length": 2.1, "width": 1.8, "height": 0.9}), 0, 1),
        
        # Electronics - Tablet
        (None, "ProTab 12", "PT12-2023", 
         "The ProTab 12 features a stunning 12.9-inch Liquid Retina XDR display with mini-LED technology, delivering an exceptional visual experience for both creative work and entertainment. Powered by the M2 chip, it offers desktop-class performance in a thin and light design. The tablet supports the latest ProStylus with magnetic attachment and wireless charging, making digital art and note-taking feel natural and responsive. With up to 10 hours of battery life, a versatile USB-C port, and support for the latest ProKeyboard attachment, it can easily replace a laptop for many workflows. The advanced camera system includes a 12MP ultra-wide front camera with Center Stage for video calls, and a professional-grade rear camera system for document scanning and photography.",
         "Professional-grade tablet with desktop-class performance and stunning XDR display.", 
         999.99, 949.99, 600.00, 85, 1, "TabTech", 1.5, 
         json.dumps({"length": 11.04, "width": 8.46, "height": 0.25}), 1, 1),
        
        # Home & Kitchen - Coffee Maker
        (None, "Barista Pro Coffee System", "BPCS-X1", 
         "The Barista Pro Coffee System brings cafe-quality coffee to your home with its professional 15-bar pressure pump and precise temperature control system. The integrated conical burr grinder with 30 settings ensures the perfect grind for any coffee variety, while the digital display makes it easy to adjust brewing parameters. A powerful steam wand allows for cafe-quality microfoam for latte art. The system heats up in just 3 seconds and can brew a shot of espresso in under 30 seconds. With programmable shot volumes, automatic cleaning cycles, and a generous 2-liter water tank, this machine offers both convenience and exceptional coffee quality. The sleek stainless steel construction provides durability and complements any kitchen decor.",
         "Professional-grade espresso machine with integrated grinder and rapid heating system.", 
         799.99, 749.99, 400.00, 40, 8, "BrewMaster", 9.5, 
         json.dumps({"length": 13.5, "width": 12.5, "height": 16}), 0, 1),
        
        # Home & Kitchen - Air Purifier
        (None, "CleanAir Pro", "CAP-H13", 
         "The CleanAir Pro air purifier features a true HEPA H13 filter that captures 99.97% of particles as small as 0.3 microns, including dust, pollen, pet dander, and smoke. The activated carbon filter eliminates odors, VOCs, and harmful gases, while the UV-C light neutralizes airborne bacteria and viruses. Designed for spaces up to 800 square feet, it can completely filter the air 5 times per hour. The smart air quality sensor continuously monitors your environment and automatically adjusts the fan speed. With whisper-quiet operation at just 24dB on sleep mode, it won't disturb you while sleeping or working. Control settings via the touch display or connect to your smart home system through WiFi for voice control and scheduling.",
         "Advanced air purifier with true HEPA H13 filter and smart air quality monitoring.", 
         299.99, 279.99, 120.00, 60, 8, "PureHome", 7.2, 
         json.dumps({"length": 14.5, "width": 8.8, "height": 25}), 0, 1),
        
        # Home & Kitchen - Blender
        (None, "UltraBlend Professional", "UB-PRO-2000", 
         "The UltraBlend Professional sets the standard for high-performance blending with its 2000-watt motor and hardened stainless steel blades. The variable speed control and pulse feature give you precise control for any recipe, from silky smoothies to hot soups. The 64-ounce BPA-free jar is designed to create a powerful vortex that pulls ingredients down for consistent blending, while the tamper helps process thick mixtures. The blender features 6 pre-programmed settings for one-touch convenience, and the digital timer helps achieve precise blend times. The self-cleaning program makes cleanup effortless - just add water and dish soap, and run the cleaning cycle. Built with commercial-grade construction for durability, this blender is backed by a 7-year warranty.",
         "Professional-grade 2000-watt blender with variable speed control and preset programs.", 
         349.99, 329.99, 150.00, 55, 8, "KitchenElite", 5.8, 
         json.dumps({"length": 8.5, "width": 7.8, "height": 17.25}), 0, 1),
        
        # Clothing - Men's
        (None, "Performance Stretch Chinos", "MSC-KHAKI", 
         "These modern chinos combine style and performance with their innovative stretch fabric that offers exceptional comfort and mobility. The moisture-wicking material keeps you cool and dry throughout the day, while the wrinkle-resistant finish ensures you look polished with minimal maintenance. The hidden security pocket provides a safe place for small valuables. With a tailored fit that's not too slim and not too relaxed, these versatile pants transition seamlessly from office to casual settings. The reinforced stitching and quality construction ensure long-lasting wear, while the pre-washed fabric gives a soft, broken-in feel from the first wear. Available in multiple colors, these will quickly become a staple in your wardrobe.",
         "Performance chinos with moisture-wicking stretch fabric and tailored fit.", 
         79.99, 69.99, 30.00, 120, 6, "Modern Menswear", 0.6, 
         json.dumps({"length": 40, "width": 12, "height": 1}), 0, 1),
        
        # Clothing - Men's
        (None, "Waterproof Hiking Jacket", "MHJ-GORETEX", 
         "This premium hiking jacket offers reliable protection against the elements with its 3-layer Gore-Tex construction, providing waterproof, windproof, yet breathable performance. The adjustable storm hood, water-resistant zippers, and taped seams ensure you stay dry in heavy rain, while pit zips allow for ventilation during intense activity. Multiple pockets, including chest pockets accessible while wearing a backpack, offer convenient storage for essentials. The jacket features articulated sleeves for freedom of movement and adjustable cuffs and hem to seal out the elements. Compatible with the brand's inner layers for a versatile layering system, this jacket is perfect for year-round adventures. The durable water repellent finish is PFC-free, reflecting our commitment to environmental responsibility.",
         "Premium 3-layer Gore-Tex hiking jacket with waterproof breathable protection.", 
         299.99, 279.99, 120.00, 80, 6, "Alpine Gear", 0.85, 
         json.dumps({"length": 29, "width": 22, "height": 3}), 0, 1),
        
        # Clothing - Women's
        (None, "Yoga Flow Leggings", "WYL-HIGHRISE", 
         "These premium yoga leggings combine performance and comfort with their buttery-soft, four-way stretch fabric that moves with your body through any pose. The high-rise, wide waistband provides gentle compression and support without digging in, while the seamless construction eliminates chafing during dynamic movements. The moisture-wicking, quick-dry material keeps you comfortable throughout your practice, and the opacity testing ensures they remain non-see-through even in deep stretches. A hidden inner pocket at the waistband holds small essentials like keys or cards. Designed with flattering seam placement and available in a range of colors, these leggings transition easily from yoga studio to casual wear. The fabric is treated with an anti-bacterial finish to prevent odors, even after multiple wears.",
         "Premium high-rise yoga leggings with four-way stretch and hidden pocket.", 
         89.99, 79.99, 35.00, 150, 7, "Flow Athletics", 0.3, 
         json.dumps({"length": 36, "width": 12, "height": 0.5}), 0, 1),
        
        # Clothing - Women's
        (None, "Cashmere Blend Oversized Sweater", "WCS-OVERSIZE", 
         "This luxurious oversized sweater blends premium cashmere with responsibly sourced wool for exceptional softness and warmth without weight. The relaxed silhouette with dropped shoulders creates an effortlessly stylish look that pairs perfectly with slim pants or leggings. Ribbed cuffs and hem add structure to the relaxed fit, while the slight boat neck frames the collarbone beautifully. The versatile design works equally well for casual weekend wear or dressed up for evenings out. With careful construction techniques to prevent pilling, this sweater is designed to become even softer with wear while maintaining its shape. Available in a curated selection of timeless colors, this piece will become a cherished staple in your wardrobe for years to come.",
         "Luxurious oversized sweater with premium cashmere blend and relaxed silhouette.", 
         149.99, 139.99, 60.00, 85, 7, "Luxe Essentials", 0.5, 
         json.dumps({"length": 28, "width": 24, "height": 1}), 0, 1),
        
        # Books
        (None, "The Quantum Paradox", "BOOK-QP-HC", 
         "In this groundbreaking exploration of quantum physics and its philosophical implications, renowned physicist Dr. Maya Blackwell bridges the gap between cutting-edge science and profound questions about reality, consciousness, and the universe. Through accessible explanations and thought experiments, readers with little scientific background can grasp the strange and counter-intuitive nature of quantum mechanics. The book examines how quantum discoveries challenge our basic assumptions about causality, determinism, and the nature of existence itself. Blackwell weaves together theoretical physics, experimental breakthroughs, and philosophical inquiry to demonstrate how quantum science is forcing us to reconsider fundamental questions about the cosmos and our place within it. Complete with illustrations and diagrams to clarify complex concepts, this book invites readers on an intellectual journey that will forever change how they understand reality.",
         "Accessible exploration of quantum physics and its profound philosophical implications.", 
         28.99, 24.99, 10.00, 200, 9, "Horizon Press", 0.95, 
         json.dumps({"length": 9.3, "width": 6.2, "height": 1.3}), 0, 1),
        
        # Books
        (None, "Culinary Journeys: Flavors of the Silk Road", "BOOK-CJSR-HC", 
         "This stunning cookbook and cultural exploration traces the ancient Silk Road through its diverse cuisines, spanning from the Mediterranean to China. Award-winning chef and food historian Sophia Lin combines authentic recipes with rich storytelling, historical context, and gorgeous photography. Each chapter focuses on a different region along the historic trading route, exploring how spices, ingredients, and techniques moved between cultures and evolved over centuries. The 85+ recipes range from Levantine mezze and Turkish manti to Uzbek plov and Chinese Muslim lamb dishes, all adapted for modern home kitchens without sacrificing authenticity. Lin's thoughtful essays examine how food serves as a living cultural heritage and connects us across time and geography. This book is both a practical cooking resource and an invitation to understand diverse cultures through their culinary traditions.",
         "Beautiful cookbook exploring the cuisines and cultures along the ancient Silk Road.", 
         39.99, 34.99, 15.00, 150, 9, "Culinary Library", 1.6, 
         json.dumps({"length": 10.5, "width": 8.5, "height": 1.2}), 0, 1),
        
        # Home & Kitchen - Smart Home
        (None, "SmartHome Hub Controller", "SHH-PRO", 
         "This advanced smart home hub serves as the central command center for your connected home, seamlessly integrating devices across different brands and communication protocols. Supporting Wi-Fi, Bluetooth, Zigbee, Z-Wave, and Thread, it eliminates the need for multiple brand-specific hubs. The intuitive touchscreen interface allows direct control, while the powerful app enables automation routines based on time, presence, or triggers from connected devices. Compatible with over 10,000 smart products including lights, thermostats, locks, cameras, and entertainment systems, it allows you to expand your smart home over time. Voice control works with all major assistants, and bank-level encryption protects your privacy and security. The local processing option reduces cloud dependence for faster response and continued function during internet outages.",
         "Comprehensive smart home hub supporting multiple protocols with intuitive control interface.", 
         249.99, 229.99, 100.00, 75, 8, "SmartLife", 0.8, 
         json.dumps({"length": 5.8, "width": 5.8, "height": 1.2}), 0, 1),
        
        # Electronics - Camera
        (None, "ProCapture Mirrorless Camera", "PC-M50", 
         "The ProCapture M50 mirrorless camera combines professional-grade features with intuitive operation in a compact body. The 32MP full-frame sensor delivers exceptional image quality with 15 stops of dynamic range, while the advanced image processor enables continuous shooting at 20fps with autofocus tracking. The 5-axis in-body stabilization provides up to 8 stops of compensation, allowing handheld shooting in challenging conditions. For video creators, the camera offers 4K 60fps 10-bit recording with professional color profiles. The hybrid autofocus system with 759 phase-detection points ensures subjects stay sharp, even during fast action. The weather-sealed magnesium alloy body protects against dust and moisture, while dual card slots provide backup security. With Wi-Fi and Bluetooth connectivity, images can be transferred wirelessly to your devices for immediate sharing.",
         "Professional mirrorless camera with 32MP full-frame sensor and advanced video capabilities.", 
         1999.99, 1899.99, 1100.00, 40, 1, "ProCapture", 1.4, 
         json.dumps({"length": 5.3, "width": 3.8, "height": 3.2}), 1, 1),
        
        # Sports & Outdoors
        (None, "Carbon Fiber Mountain Bike", "MTB-CARBON-PRO", 
         "This high-performance mountain bike features a lightweight carbon fiber frame that offers the perfect balance of stiffness for power transfer and compliance for trail comfort. The cutting-edge suspension system provides 140mm of travel with adjustable compression and rebound to handle everything from technical climbs to aggressive descents. The 12-speed electronic shifting system delivers precise gear changes even under load, while the hydraulic disc brakes offer powerful stopping control in all conditions. Tubeless-ready carbon wheels reduce rotating weight for improved acceleration and responsiveness. The dropper seatpost allows for quick position changes to tackle varying terrain. Every component has been selected for the optimal blend of performance, durability, and weight savings, resulting in a versatile trail bike that excels in all mountain conditions.",
         "Professional-grade carbon fiber mountain bike with electronic shifting and premium suspension.", 
         3499.99, 3299.99, 2000.00, 15, 10, "AlpineTrail", 11.3, 
         json.dumps({"length": 69, "width": 24, "height": 43}), 0, 1),
        
        # Sports & Outdoors
        (None, "Ultralight Backpacking Tent", "UBT-2P", 
         "This ultralight backpacking tent represents the perfect balance between weight, durability, and livability for serious backcountry adventures. Weighing just 2 pounds 8 ounces, it's easy to carry on long treks, while the advanced DAC Featherlite aluminum poles and ripstop nylon construction ensure reliability in challenging conditions. The freestanding design features two doors and vestibules for convenient access and gear storage. The strategic mesh panels provide excellent ventilation while keeping insects out, and the silicone-treated rainfly delivers exceptional waterproofing with a 3000mm rating. The tent can be set up in under 3 minutes with the color-coded system, even in low light. Interior pockets and gear lofts keep essentials organized, while reflective guylines prevent nighttime tripping. Designed to comfortably fit two people with a floor space optimized for standard sleeping pads.",
         "Ultralight 2-person backpacking tent weighing just 2.5 pounds with exceptional weather protection.", 
         349.99, 299.99, 150.00, 35, 10, "TrailLite", 2.5, 
         json.dumps({"length": 18, "width": 6, "height": 6}), 0, 1),
        
        # Home & Kitchen - Cookware
        (None, "Professional Enameled Cast Iron Dutch Oven", "ECIDO-5QT", 
         "This premium 5-quart dutch oven combines the superior heat retention and distribution of cast iron with a porcelain enamel coating that eliminates the need for seasoning and allows for cooking acidic foods. The tight-fitting lid locks in moisture for perfect braises and stews, while the wide loop handles provide a secure grip even with oven mitts. The light-colored interior enamel makes it easy to monitor cooking progress and prevent burning. Suitable for all cooktops including induction, this versatile pot transitions seamlessly from stovetop to oven (safe up to 500°F). The chip-resistant enamel exterior comes in a range of rich colors and requires no special maintenance. From slow-cooking stews to baking artisan bread, this heirloom-quality piece delivers exceptional results and will become the centerpiece of your kitchen for generations.",
         "Premium 5-quart enameled cast iron dutch oven with superior heat retention and distribution.", 
         279.99, 249.99, 100.00, 60, 8, "Heritage Cookware", 12.5, 
         json.dumps({"length": 11.8, "width": 9.8, "height": 6.2}), 0, 1),
        
        # Electronics - Computer Accessories
        (None, "Ergonomic Mechanical Keyboard", "EMK-TKL", 
         "This premium mechanical keyboard combines exceptional typing experience with ergonomic design for comfort during extended use. The tenkeyless layout saves desk space while retaining function and arrow keys for productivity. Premium mechanical switches (available in tactile, linear, or clicky) offer precise actuation and are rated for 80 million keystrokes. The split ergonomic design and included magnetic wrist rest reduce strain on wrists and shoulders during long typing sessions. PBT double-shot keycaps resist shine and feature dye-sublimated legends that never fade. Customizable RGB backlighting with per-key control allows for personalized illumination, while programmable macros and key remapping support efficient workflows. Connect via USB-C or Bluetooth to up to 3 devices with easy switching. The aircraft-grade aluminum frame ensures durability while maintaining a refined aesthetic.",
         "Premium ergonomic mechanical keyboard with customizable switches and split design.", 
         149.99, 139.99, 70.00, 90, 1, "ErgoTech", 0.9, 
         json.dumps({"length": 14.5, "width": 6.2, "height": 1.5}), 0, 1),
        
        # Beauty & Personal Care
        (None, "Advanced Skincare Collection", "ASC-ESSENTIAL", 
         "This comprehensive skincare system delivers professional-grade results through a synergistic four-step routine backed by dermatological research. The gentle enzyme cleanser removes impurities without disrupting the skin barrier, while the vitamin C serum contains a stable 15% L-ascorbic acid formula to brighten and protect against environmental damage. The peptide moisturizer combines three advanced peptide complexes with hyaluronic acid to boost collagen production and deeply hydrate, and the broad-spectrum mineral sunscreen offers SPF 40 protection without leaving a white cast. All formulations are free from parabens, sulfates, phthalates, and artificial fragrances, making them suitable for sensitive skin. The airless pump packaging preserves ingredient efficacy and ensures hygienic application. This science-backed system addresses multiple skin concerns including fine lines, uneven texture, dullness, and environmental protection.",
         "Dermatologist-developed skincare system with four essential products for transformative results.", 
         189.99, 169.99, 75.00, 100, 11, "DermaScience", 1.2, 
         json.dumps({"length": 8, "width": 6, "height": 6}), 0, 1),
        
        # Beauty & Personal Care
        (None, "Professional Hair Styling Tool", "PHST-MULTI", 
         "This innovative 5-in-1 styling tool revolutionizes hair styling with interchangeable attachments that create everything from sleek straight styles to bouncy curls and defined waves. The digital temperature control ranges from 280°F to 450°F for all hair types, while the advanced ceramic tourmaline barrel ensures even heat distribution and reduces frizz by emitting negative ions. The cool-touch barrel tips and heat-resistant glove provide safe handling during styling. Auto shut-off after 60 minutes provides peace of mind, and worldwide voltage compatibility makes it perfect for travel. The tool heats up in just 30 seconds, and the 9-foot swivel cord allows for easy movement during styling. Included attachments feature a 1-inch curling barrel, flat iron plates, a volumizing root lifter, and two different-sized wave plates, making this the only styling tool you'll need.",
         "Versatile 5-in-1 hair styling tool with interchangeable attachments for multiple styling options.", 
         129.99, 119.99, 55.00, 70, 11, "StylePro", 1.3, 
         json.dumps({"length": 14, "width": 4, "height": 4}), 0, 1),
        
        # Furniture & Decor
        (None, "Modular Sofa System", "MSS-SECTIONAL", 
         "This innovative modular sofa system adapts to your needs with repositionable sections that can be arranged into countless configurations. The solid hardwood frame and sinuous spring suspension system ensure durability and comfort for years to come. Premium high-resilience foam cushions wrapped in down-alternative fiber maintain their shape while providing plush comfort. The performance fabric resists stains, fading, and wear while remaining soft and inviting. Each module connects securely with hidden fasteners, allowing you to easily transform your sofa from a standard configuration to a sectional, chaise arrangement, or even a guest bed. The removable and washable covers simplify maintenance, while the timeless design complements any interior style. Available in multiple fabric options and colors, this versatile system grows and changes with your lifestyle, making it the last sofa you'll need to buy.",
         "Versatile modular sofa system with repositionable sections and premium construction.", 
         1999.99, 1899.99, 900.00, 20, 12, "FlexLiving", 120.0, 
         json.dumps({"length": 100, "width": 37, "height": 33}), 0, 1),
        
        # Furniture & Decor
        (None, "Adjustable Standing Desk", "ASD-PRO", 
         "This premium standing desk transforms any workspace with its smooth, whisper-quiet dual-motor height adjustment system that transitions between sitting and standing positions at 1.5 inches per second. The anti-collision technology prevents damage if the desk meets an obstacle during height changes. The spacious desktop is crafted from sustainable bamboo with a water-resistant finish, supported by a steel frame that eliminates wobbling even at maximum height. The advanced control panel stores four height presets and includes a USB charging port for devices. Cable management solutions keep your workspace tidy, while the integrated power management system protects your electronics. The desk supports up to 350 pounds, accommodating multiple monitors and equipment. Assembly takes less than 30 minutes with the included tools and clear instructions, and the desk is backed by a 10-year warranty.",
         "Premium electric standing desk with dual motors, bamboo surface, and programmable height presets.", 
         599.99, 549.99, 250.00, 30, 12, "ErgoSpace", 85.0, 
         json.dumps({"length": 60, "width": 30, "height": 50}), 0, 1),
        
        # Toys & Games
        (None, "Educational Robotics Kit", "ERK-STEM", 
         "This comprehensive robotics kit introduces children ages 8-14 to coding, engineering, and problem-solving through engaging hands-on projects. The core controller features a programmable microprocessor compatible with block-based and text-based coding languages, allowing skills to grow as children advance. With over 850 components including structural parts, sensors, motors, and LED lights, kids can build 17 pre-designed robots or create unlimited custom designs. The detailed guidebook explains fundamental STEM concepts while the companion app provides interactive tutorials, coding challenges, and a community to share creations. All electronic components are housed in durable, child-safe casings with secure battery compartments. The kit aligns with educational standards and develops critical 21st-century skills including computational thinking, creativity, and digital literacy. Parents appreciate that the engaging projects limit screen time while teaching valuable tech skills.",
         "Comprehensive STEM robotics kit with 850+ components for building programmable robots.", 
         199.99, 179.99, 80.00, 50, 13, "STEM Explorers", 4.2, 
         json.dumps({"length": 18, "width": 14, "height": 6}), 0, 1),
        
        # Toys & Games
        (None, "Strategic Board Game Collection", "SBGC-DELUXE", 
         "This premium board game collection brings together five award-winning strategy games in one elegant wooden case. Each game has been carefully selected to offer unique gameplay mechanics that challenge different strategic thinking skills - from resource management and area control to diplomatic negotiation and long-term planning. The set includes the base games plus select expansions, accommodating 2-6 players with gameplay ranging from 45-120 minutes per game. All components are crafted from high-quality materials including wooden pieces, thick cardboard tiles, and premium cards with linen finish. The handsome storage case features felt-lined compartments that perfectly organize all components for easy setup and storage. Comprehensive rulebooks and strategy guides are included, along with exclusive variant rules not available in the standard editions. Perfect for game nights, this collection offers hundreds of hours of engaging gameplay for both new and experienced strategy gamers.",
         "Premium collection of five award-winning strategy board games in an elegant wooden case.", 
         149.99, 129.99, 60.00, 40, 13, "Strategic Minds", 9.5, 
         json.dumps({"length": 16, "width": 12, "height": 8}), 0, 1),
        
        # Pet Supplies
        (None, "Interactive Pet Feeder", "IPF-SMART", 
         "This innovative smart pet feeder combines precision feeding with interactive features to support your pet's health and mental stimulation. The programmable system dispenses customized portions on schedule, with up to 6 meals per day in portions from 1/8 cup to 4 cups. The slow-feed option prevents gulping and bloating by dispensing larger meals over 15 minutes. Built-in food-recognition sensors prevent jamming and alert you when food levels are low, while the sealed container keeps food fresh and secure from clever pets. The HD camera with night vision and two-way audio lets you check on and talk to your pet remotely. The puzzle feeder mode dispenses small treats as your pet solves simple puzzles, providing mental stimulation. The system works during power and WiFi outages thanks to battery backup and local scheduling backup. The app allows you to monitor feeding patterns and adjust portions based on your pet's activity level, which is tracked through an optional attachment.",
         "Smart pet feeding system with scheduled dispensing, camera monitoring, and interactive features.", 
         179.99, 159.99, 70.00, 60, 14, "PetTech", 7.8, 
         json.dumps({"length": 14, "width": 9, "height": 15}), 0, 1),
        
        # Pet Supplies
        (None, "Orthopedic Pet Bed", "OPB-MEMORY", 
         "This premium orthopedic pet bed provides therapeutic support for pets of all ages, particularly benefiting those with arthritis, hip dysplasia, or joint issues. The 4-inch memory foam base maintains 90% of its shape and support for 10+ years, contouring to your pet's body to relieve pressure on joints while the bolstered sides offer security and head support. The waterproof inner liner protects the foam from accidents, while the machine-washable microfiber cover resists fur, dirt, and odors. The non-slip bottom keeps the bed in place even on hard floors, and the low entry point allows easy access for senior or mobility-impaired pets. Available in multiple sizes to accommodate pets from 10 to 100+ pounds, this bed combines functional support with a design that complements home décor. Each bed undergoes compression testing to ensure long-term support and comes with a 10-year warranty against flattening.",
         "Premium orthopedic pet bed with 4-inch memory foam and bolstered sides for joint support.", 
         129.99, 109.99, 50.00, 75, 14, "ComfortPets", 8.5, 
         json.dumps({"length": 36, "width": 28, "height": 9}), 0, 1)
    ]
    
    cursor.executemany('''
    INSERT INTO products (
        id, name, sku, description, short_description, price, sale_price, cost, 
        stock_quantity, category_id, brand, weight, dimensions, is_featured, is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Fetch the newly inserted product IDs
    cursor.execute("SELECT id FROM products WHERE id >= ?", (start_id,))
    new_product_ids = [row[0] for row in cursor.fetchall()]
    
    # Create product attributes based on categories
    attributes_to_insert = []
    
    # Define attribute templates by category
    electronics_attributes = [
        ("Color", ["Black", "Silver", "White", "Blue", "Gold"], 1, 1, 1),
        ("Warranty", ["1 Year", "2 Years", "3 Years"], 2, 1, 1),
        ("Connectivity", ["Bluetooth 5.0", "Wi-Fi 6", "USB-C", "USB-A", "HDMI"], 3, 1, 1)
    ]
    
    clothing_attributes = [
        ("Material", ["Cotton", "Polyester", "Wool", "Nylon", "Cashmere Blend", "Gore-Tex"], 1, 1, 1),
        ("Care", ["Machine Wash", "Hand Wash", "Dry Clean Only"], 2, 0, 1),
        ("Fit", ["Regular", "Slim", "Relaxed", "Athletic", "Oversized"], 3, 1, 1)
    ]
    
    home_kitchen_attributes = [
        ("Material", ["Stainless Steel", "Glass", "Ceramic", "Plastic", "Wood", "Cast Iron"], 1, 1, 1),
        ("Dimensions", ["Small", "Medium", "Large", "Extra Large"], 2, 1, 1),
        ("Care", ["Dishwasher Safe", "Hand Wash Only", "Wipe Clean"], 3, 0, 1)
    ]
    
    # Create product attributes based on product category
    for product_id in new_product_ids:
        # Get the category for this product
        cursor.execute("SELECT category_id FROM products WHERE id = ?", (product_id,))
        category_id = cursor.fetchone()[0]
        
        # Select appropriate attributes based on category
        if category_id in [1, 2, 3, 4]:  # Electronics categories
            attribute_template = electronics_attributes
        elif category_id in [5, 6, 7]:  # Clothing categories
            attribute_template = clothing_attributes
        elif category_id in [8]:  # Home & Kitchen
            attribute_template = home_kitchen_attributes
        else:
            # For other categories, use generic attributes
            continue
        
        # Create attributes for this product
        for attr_name, attr_values, display_order, is_filterable, is_visible in attribute_template:
            # Pick a random value from the options
            attr_value = random.choice(attr_values)
            attributes_to_insert.append(
                (None, product_id, attr_name, attr_value, display_order, is_filterable, is_visible)
            )
    
    # Insert attributes
    cursor.executemany('''
    INSERT INTO product_attributes (
        id, product_id, attribute_name, attribute_value, display_order, is_filterable, is_visible
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', attributes_to_insert)
    
    # Insert product images (at least one per product)
    product_images = []
    for product_id in new_product_ids:
        # Get product name for image alt text
        cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
        product_name = cursor.fetchone()[0]
        
        # Create primary image
        product_images.append((None, product_id, f"product_{product_id}_main.jpg", 1, 1, f"{product_name} main view"))
        
        # Add 1-3 additional images randomly
        num_additional = random.randint(1, 3)
        for i in range(num_additional):
            angle = random.choice(["front", "side", "back", "detail", "lifestyle", "packaging"])
            product_images.append(
                (None, product_id, f"product_{product_id}_{angle}.jpg", 0, i+2, f"{product_name} {angle} view")
            )
    
    cursor.executemany('''
    INSERT INTO product_images (
        id, product_id, image_url, is_primary, display_order, alt_text
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ''', product_images)
    
    # Add tags to products
    product_tags = []
    
    # Get all tag IDs
    cursor.execute("SELECT id FROM tags")
    all_tag_ids = [row[0] for row in cursor.fetchall()]
    
    # Assign 2-4 random tags to each product
    for product_id in new_product_ids:
        num_tags = random.randint(2, 4)
        selected_tags = random.sample(all_tag_ids, num_tags)
        for tag_id in selected_tags:
            product_tags.append((product_id, tag_id))
    
    cursor.executemany('''
    INSERT INTO product_tags (product_id, tag_id)
    VALUES (?, ?)
    ''', product_tags)
    
    # Add variants for a subset of products
    variants_to_insert = []
    
    # Select 10 random products to create variants for
    variant_product_ids = random.sample(new_product_ids, 10)
    
    for product_id in variant_product_ids:
        # Get product SKU as base
        cursor.execute("SELECT sku, name, category_id FROM products WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        base_sku, product_name, category_id = result
        
        # Different variant types based on category
        if category_id in [1, 2, 3, 4]:  # Electronics
            # Create storage or color variants
            variant_types = random.choice([
                ("Color", ["Black", "Silver", "White", "Blue", "Red"]),
                ("Storage", ["64GB", "128GB", "256GB", "512GB", "1TB"])
            ])
            attr_name, attr_values = variant_types
            
            for value in attr_values[:3]:  # Limit to 3 variants per product
                variant_sku = f"{base_sku}-{value.replace(' ', '')}"
                variant_name = f"{product_name} {value}"
                price_adj = random.choice([0, 50, 100, 150]) if attr_name == "Storage" else 0
                stock = random.randint(10, 50)
                attr_json = json.dumps({attr_name.lower(): value})
                image_url = f"product_{product_id}_{value.lower().replace(' ', '')}.jpg"
                
                variants_to_insert.append(
                    (None, product_id, variant_sku, variant_name, price_adj, stock, attr_json, image_url, 1)
                )
                
        elif category_id in [5, 6, 7]:  # Clothing
            # Create size and color variants
            sizes = ["S", "M", "L", "XL"]
            colors = ["Black", "Navy", "Gray", "White", "Burgundy"]
            
            # Pick 2-3 colors
            selected_colors = random.sample(colors, random.randint(2, 3))
            
            for size in sizes:
                for color in selected_colors:
                    variant_sku = f"{base_sku}-{color[:3].upper()}-{size}"
                    variant_name = f"{product_name} {color} {size}"
                    price_adj = 0  # Same price for all sizes/colors
                    stock = random.randint(5, 30)
                    attr_json = json.dumps({"size": size, "color": color})
                    image_url = f"product_{product_id}_{color.lower()}_{size.lower()}.jpg"
                    
                    variants_to_insert.append(
                        (None, product_id, variant_sku, variant_name, price_adj, stock, attr_json, image_url, 1)
                    )
    
    cursor.executemany('''
    INSERT INTO product_variants (
        id, product_id, sku, variant_name, price_adjustment, stock_quantity, 
        attributes, image_url, is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', variants_to_insert)
    
    print(f"Successfully inserted 25 new products with attributes, images, tags, and variants.")

if __name__ == "__main__":
    add_more_products()