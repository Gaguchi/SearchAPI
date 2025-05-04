import sqlite3
import datetime
import json
import random

# Database file path
DB_FILE = 'ecommerce.db'

def add_more_products():
    """Add 200+ more products to the existing e-commerce database"""
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
    
    print(f"Successfully added 200+ more products to database '{DB_FILE}'.")

def insert_additional_products(conn, start_id):
    """Insert 200+ products and their related data into the database"""
    cursor = conn.cursor()
    
    # Get all existing categories
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    category_map = {id: name for id, name in categories}
    
    # Product data templates for generating realistic product data
    product_templates = {
        # Electronics
        1: { # Electronics category
            "brands": ["TechPro", "NextGen", "ElectroVision", "InnovateX", "FutureTech", "SmartLife", "TechWave", "DigiTrend", "ElectraPrime", "CyberTech"],
            "prefixes": ["Smart", "Ultra", "Pro", "Elite", "Premium", "Advanced", "Digital", "Wireless", "High-Performance", "Intelligent"],
            "products": ["Laptop", "Tablet", "Speaker System", "Smartwatch", "Wireless Earbuds", "Home Theater", "Gaming Console", "Smart TV", "Power Bank", "Bluetooth Headphones"],
            "price_range": (199, 2499),
            "features": [
                "Advanced AI integration for personalized user experience",
                "Military-grade security protocols for data protection",
                "Premium construction with aerospace-grade materials",
                "Industry-leading battery life with rapid charging technology",
                "Seamless ecosystem integration across multiple devices",
                "Voice control with multi-language support",
                "Adaptive learning algorithms that improve over time",
                "Customizable interface with limitless personalization options",
                "Cloud synchronization with automatic backup",
                "Revolutionary energy efficiency with eco-friendly design"
            ]
        },
        # Smartphones
        2: {
            "brands": ["XPhone", "GalaxyTech", "PixelPro", "MobiMax", "SmartFone", "CellEdge", "OneTouch", "MobileX", "PhonePro", "TechCell"],
            "prefixes": ["Ultra", "Pro", "Max", "Edge", "Nova", "Prime", "Elite", "Flex", "Power", "Premium"],
            "products": ["Smartphone", "Foldable Phone", "5G Phone", "Camera Phone", "Gaming Phone", "Rugged Phone", "Slim Phone", "Note Phone", "Mini Phone", "Plus Phone"],
            "price_range": (499, 1499),
            "features": [
                "Revolutionary camera system with computational photography",
                "All-day battery life with intelligent power management",
                "Cutting-edge display with HDR10+ certification",
                "Processor built on advanced nanometer architecture",
                "Biometric security with facial and fingerprint recognition",
                "Water and dust resistance for all-weather use",
                "Expansive storage options with cloud integration",
                "Immersive audio system with spatial sound",
                "Advanced connectivity with Wi-Fi 6E and 5G support",
                "Durable design with Corning Gorilla Glass protection"
            ]
        },
        # Laptops
        3: {
            "brands": ["UltraBook", "MacroTech", "CompuPro", "LaptopX", "TechBook", "PowerLap", "NotePro", "ComputeX", "BookTech", "LapElite"],
            "prefixes": ["Ultra", "Pro", "Elite", "Power", "Gaming", "Creative", "Business", "Ultimate", "Slim", "Premium"],
            "products": ["Laptop", "Notebook", "Ultrabook", "2-in-1 Convertible", "Gaming Laptop", "Workstation", "Chromebook", "Studio Laptop", "Thin & Light", "Professional Laptop"],
            "price_range": (699, 3499),
            "features": [
                "Desktop-class performance in a portable design",
                "Revolutionary cooling system for sustained performance",
                "Studio-quality microphone array for clear communication",
                "Color-calibrated display for professional content creation",
                "Military-grade durability testing for reliability",
                "Backlit keyboard with customizable RGB lighting",
                "Multi-touch gesture support with precision trackpad",
                "Expansive connectivity options with Thunderbolt ports",
                "Immersive audio with Dolby Atmos certification",
                "All-day battery life with rapid charging technology"
            ]
        },
        # Audio
        4: {
            "brands": ["AudioTech", "SoundWave", "BeatPro", "AudioPhile", "SonicLife", "ClearSound", "RhythmX", "MelodyTech", "SoundCore", "AcousticPro"],
            "prefixes": ["Premium", "Ultra", "Pro", "Elite", "Studio", "Dynamic", "Immersive", "Wireless", "Noise-Canceling", "High-Fidelity"],
            "products": ["Headphones", "Earbuds", "Wireless Earphones", "Home Speaker", "Soundbar", "Portable Speaker", "DJ Headphones", "Gaming Headset", "Studio Monitors", "Bluetooth Speaker"],
            "price_range": (99, 699),
            "features": [
                "Active noise cancellation with adaptive environmental sensing",
                "Studio-quality sound profile tuned by Grammy-winning producers",
                "Custom-engineered acoustic architecture for precise sound",
                "Spatial audio with dynamic head tracking",
                "Ultra-low latency for perfect audio-visual synchronization",
                "Sweat and water resistance for active lifestyles",
                "Advanced Bluetooth codecs for lossless wireless audio",
                "Intuitive touch controls with customizable functions",
                "Multi-device connectivity with seamless switching",
                "Voice assistant integration with wake word activation"
            ]
        },
        # Clothing
        5: {
            "brands": ["StyleLife", "FashionEdge", "UrbanChic", "TrendSetters", "ModernWear", "ElegantStyle", "FashionForward", "ClassicThreads", "StylishEssentials", "PremiumApparel"],
            "prefixes": ["Premium", "Luxury", "Modern", "Classic", "Designer", "Signature", "Essential", "Contemporary", "Seasonal", "Bespoke"],
            "products": ["Collection", "Ensemble", "Wardrobe", "Attire", "Outfit", "Fashion Line", "Apparel Set", "Clothing Range", "Style Series", "Garment Collection"],
            "price_range": (99, 499),
            "features": [
                "Ethically sourced materials from sustainable suppliers",
                "Advanced fabric technology for comfort and durability",
                "Versatile designs that transition from day to evening",
                "Tailored fit with flattering silhouettes for all body types",
                "Season-spanning styles for year-round wearability",
                "Wrinkle-resistant finish for easy care and maintenance",
                "Innovative moisture-wicking properties for all-day comfort",
                "Thoughtful details with premium hardware and finishes",
                "Exclusive patterns designed by renowned textile artists",
                "Limited edition releases with numbered authenticity"
            ]
        },
        # Men's
        6: {
            "brands": ["GentlemanCraft", "ModernMan", "MaleEssentials", "DapperStyle", "ManCraft", "UrbanGent", "ClassicMen", "MensFinest", "MaleElite", "GentCore"],
            "prefixes": ["Premium", "Classic", "Modern", "Executive", "Athletic", "Urban", "Outdoor", "Professional", "Signature", "Rugged"],
            "products": ["Dress Shirt", "Chinos", "Suit", "Jeans", "Polo Shirt", "Sweater", "Oxford Shirt", "Performance Tee", "Blazer", "Cargo Pants"],
            "price_range": (49, 399),
            "features": [
                "Tailored fit with strategic stretch for unrestricted movement",
                "Wrinkle-resistant fabric for all-day professional appearance",
                "Moisture-wicking technology for comfort in any environment",
                "Hidden security pockets for valuables while traveling",
                "Stain-resistant finish that maintains like-new appearance",
                "Convertible design features for versatile styling options",
                "Temperature-regulating material for year-round wear",
                "Reinforced stitching at high-stress points for durability",
                "Classic design elements with modern performance upgrades",
                "Eco-friendly construction from sustainable materials"
            ]
        },
        # Women's
        7: {
            "brands": ["FemmeChic", "EleganceEra", "ModernWoman", "GraceStyle", "ChicEssentials", "FeminineFlair", "WomanlyGrace", "LadyLuxe", "FemStyle", "WomanCraft"],
            "prefixes": ["Elegant", "Chic", "Modern", "Classic", "Feminine", "Designer", "Signature", "Luxe", "Essential", "Sophisticated"],
            "products": ["Blouse", "Dress", "Skirt", "Cardigan", "Jeans", "Jumpsuit", "Blazer", "Wrap Dress", "Knit Sweater", "Palazzo Pants"],
            "price_range": (59, 449),
            "features": [
                "Figure-flattering silhouette with thoughtful tailoring",
                "Versatile styling options for day-to-evening transitions",
                "Wrinkle-resistant fabric perfect for travel or busy days",
                "Premium stretch material that maintains shape over time",
                "Hidden support elements for confidence and comfort",
                "Adjustable features for customizable fit",
                "Strategic pocket placement for functionality without bulk",
                "Temperature-regulating fabric for year-round comfort",
                "Engineered with movement in mind for unrestricted activity",
                "Timeless design elements with contemporary details"
            ]
        },
        # Home & Kitchen
        8: {
            "brands": ["HomeComfort", "KitchenCraft", "DomesticBliss", "CulinaryEdge", "HomeEssentials", "GourmetPro", "DwellLuxe", "KitchenElite", "HomeSavvy", "CulinaryMaster"],
            "prefixes": ["Professional", "Gourmet", "Premium", "Artisanal", "Smart", "Modern", "Luxury", "Essential", "Innovative", "Signature"],
            "products": ["Coffee Maker", "Blender", "Food Processor", "Stand Mixer", "Toaster Oven", "Cookware Set", "Knife Set", "Air Fryer", "Pressure Cooker", "Bakeware Collection"],
            "price_range": (99, 799),
            "features": [
                "Professional-grade construction for home kitchens",
                "Innovative technology that simplifies complex techniques",
                "Time-saving features for busy households",
                "Precision engineering for consistent, restaurant-quality results",
                "Versatile functionality that replaces multiple appliances",
                "Thoughtful design for intuitive operation and cleaning",
                "Energy-efficient performance with eco-friendly materials",
                "Space-saving design with multi-functional capabilities",
                "Smart connectivity for recipes and remote operation",
                "Durable construction backed by comprehensive warranty"
            ]
        },
        # Books
        9: {
            "brands": ["MindScape", "LiteraryVision", "IntellectPress", "WisdomHouse", "ThoughtCraft", "KnowledgeRealm", "PageTurner", "MindfulReads", "BrilliantWords", "InsightPublishing"],
            "prefixes": ["Essential", "Complete", "Definitive", "Modern", "Comprehensive", "Ultimate", "Practical", "Advanced", "Beginner's", "Professional"],
            "products": ["Guide", "Handbook", "Encyclopedia", "Masterclass", "Compendium", "Collection", "Manual", "Sourcebook", "Reference", "Anthology"],
            "price_range": (19, 89),
            "features": [
                "Comprehensive coverage with clear, accessible language",
                "Expert insights from leading authorities in the field",
                "Practical examples and case studies for real-world application",
                "Step-by-step instructions with detailed illustrations",
                "Supplemental online resources and interactive content",
                "Thoughtfully organized for both reference and cover-to-cover reading",
                "Distillation of complex concepts into actionable knowledge",
                "Up-to-date research and cutting-edge developments",
                "Balanced perspective with diverse viewpoints",
                "Engaging narrative that makes complex topics fascinating"
            ]
        },
        # Sports & Outdoors
        10: {
            "brands": ["PeakPerformance", "OutdoorElite", "AthleticEdge", "WildernessGear", "SportsPro", "TrailMaster", "FitnessFrontier", "ActiveLife", "OutdoorExcellence", "SportsCraft"],
            "prefixes": ["Professional", "Ultimate", "Advanced", "Extreme", "Performance", "Endurance", "Tactical", "Pro-Grade", "Competition", "Expedition"],
            "products": ["Trail Running Shoes", "Mountain Bike", "Hiking Backpack", "Camping Tent", "Fitness Tracker", "Yoga Mat", "Golf Club Set", "Tennis Racket", "Ski Goggles", "Climbing Harness"],
            "price_range": (79, 1499),
            "features": [
                "Performance-engineered design tested by professional athletes",
                "Lightweight construction that doesn't compromise durability",
                "Weather-resistant materials for all-condition reliability",
                "Ergonomic design for comfort during extended use",
                "Advanced technology that enhances natural capabilities",
                "Versatile functionality for multiple activities and environments",
                "Strategic ventilation and temperature management",
                "Impact protection and safety features for peace of mind",
                "Quick-adjust components for personalized fit in seconds",
                "Reflective elements for visibility in low-light conditions"
            ]
        },
        # Beauty & Personal Care (newly added category)
        11: {
            "brands": ["PureLuxe", "GlowEssence", "BeautyScience", "RadiantSkin", "LuxeBeauty", "NaturalGlow", "EssentialBeauty", "PristineBeauty", "VitalRadiance", "PureFormula"],
            "prefixes": ["Advanced", "Premium", "Intensive", "Essential", "Professional", "Luxury", "Nourishing", "Revitalizing", "Rejuvenating", "Purifying"],
            "products": ["Skincare Set", "Anti-Aging Cream", "Hair Care System", "Facial Serum", "Makeup Collection", "Body Treatment", "Exfoliant Scrub", "Hydrating Mask", "Cleansing System", "Beauty Tools"],
            "price_range": (39, 299),
            "features": [
                "Dermatologist-developed formula for all skin types",
                "Clinically proven results backed by scientific research",
                "Clean ingredient list free from harmful additives",
                "Advanced delivery system for deep penetration",
                "Multi-functional benefits from a single product",
                "Time-release technology for sustained effectiveness",
                "Innovative applicators for precision and convenience",
                "Eco-conscious packaging from sustainable materials",
                "Synergistic formulations that enhance each component's benefits",
                "Professional-grade quality for at-home use"
            ]
        },
        # Furniture & Decor (newly added category)
        12: {
            "brands": ["ModernDwelling", "HomeHarmony", "LuxeHabitat", "ElegantSpace", "UrbanNest", "DwellCraft", "InteriorVision", "HabitatPro", "DwellLuxe", "SpaceStyle"],
            "prefixes": ["Modern", "Luxury", "Classic", "Contemporary", "Ergonomic", "Designer", "Premium", "Handcrafted", "Signature", "Executive"],
            "products": ["Sofa", "Dining Set", "Bedroom Collection", "Office Desk", "Lounge Chair", "Coffee Table", "Bookshelf", "Console Table", "Accent Cabinet", "Wall Art"],
            "price_range": (299, 2999),
            "features": [
                "Heirloom-quality construction using time-honored techniques",
                "Ergonomic design for comfort and proper body alignment",
                "Space-saving features perfect for urban living",
                "Modular components that adapt to changing needs",
                "Premium materials selected for beauty and durability",
                "Multifunctional design with hidden storage solutions",
                "Customizable elements for personalized aesthetic",
                "Sustainably sourced materials with eco-friendly finishes",
                "Precision-engineered mechanisms for smooth operation",
                "Timeless design that transcends trends"
            ]
        },
        # Toys & Games (newly added category)
        13: {
            "brands": ["ImaginePlay", "FunQuest", "PlayfulMinds", "WonderToys", "CreativeKids", "PlayGenius", "JoyfulPlay", "BrainChild", "FunWorks", "PlaySmart"],
            "prefixes": ["Educational", "Interactive", "Creative", "Advanced", "Classic", "Strategic", "Developmental", "Ultimate", "Smart", "Innovative"],
            "products": ["Building Set", "Board Game", "Science Kit", "Art Supplies", "Puzzle Collection", "Coding Toy", "Role Play Set", "Educational Game", "Strategy Game", "Outdoor Play Equipment"],
            "price_range": (29, 199),
            "features": [
                "Curriculum-aligned activities developed by education experts",
                "Open-ended play possibilities that grow with the child",
                "Screen-free entertainment that builds real-world skills",
                "Collaborative elements that strengthen social connections",
                "Strategic thinking challenges for cognitive development",
                "High-quality construction designed for years of use",
                "Thoughtfully designed to engage multiple learning styles",
                "Progressive difficulty levels for continuous challenge",
                "Cross-generational appeal for family bonding time",
                "Develops crucial STEM/STEAM skills through play"
            ]
        },
        # Pet Supplies (newly added category)
        14: {
            "brands": ["PetPerfect", "FurryFriend", "PawComfort", "PetElite", "CompanionCare", "PetPremium", "TailWaggers", "PetEssentials", "FurBabies", "PawVIP"],
            "prefixes": ["Premium", "Deluxe", "Orthopedic", "Interactive", "Advanced", "Therapeutic", "Comfort", "Eco-Friendly", "Professional", "Natural"],
            "products": ["Pet Bed", "Training System", "Grooming Kit", "Toy Collection", "Feeding Station", "Travel Carrier", "Health Supplement", "Exercise Equipment", "Harness", "Cleaning Solution"],
            "price_range": (39, 249),
            "features": [
                "Veterinarian-developed design with animal wellness focus",
                "Intuitive features that work with natural pet behaviors",
                "Premium materials selected for safety and durability",
                "Thoughtful ergonomics for pets with mobility challenges",
                "Multi-functional design that adapts to changing needs",
                "Easy-clean surfaces that resist bacteria and odors",
                "Calming elements to reduce anxiety and stress",
                "Interactive components that provide mental stimulation",
                "Sustainable materials with non-toxic finishes",
                "Space-efficient design that complements home décor"
            ]
        }
    }

    # Calculate how many products to create per category
    total_categories = len(product_templates)
    base_products_per_category = 200 // total_categories
    extra_products = 200 % total_categories
    
    # Distribute products across categories
    category_product_counts = {}
    for cat_id in product_templates.keys():
        if extra_products > 0:
            category_product_counts[cat_id] = base_products_per_category + 1
            extra_products -= 1
        else:
            category_product_counts[cat_id] = base_products_per_category
    
    # Product description templates
    description_templates = [
        "The {prefix} {product_name} sets a new standard in {category} with its {feature1}. Designed for {user_type}, it offers {feature2} and {feature3}. The innovative {highlight_feature} provides {benefit}, while the {secondary_feature} ensures {secondary_benefit}. Built with {material} and finished with {quality}, this {product_type} delivers {performance} whether you're {use_case1} or {use_case2}. With {warranty} and {support}, the {brand} {product_name} is the perfect choice for those who demand excellence.",
        
        "Introducing the {brand} {prefix} {product_name}, the ultimate solution for {user_type} looking for exceptional {category} performance. Featuring {feature1} and {feature2}, this {product_type} delivers {performance} in all conditions. The {highlight_feature} technology provides {benefit}, while {secondary_feature} ensures {secondary_benefit}. Crafted from {material} with meticulous attention to {quality}, it's designed to excel whether you're {use_case1} or {use_case2}. Backed by {warranty} and {support}, it represents the pinnacle of {brand}'s innovation.",
        
        "Experience unparalleled {category} excellence with the {brand} {prefix} {product_name}. Engineered specifically for {user_type}, it combines {feature1} with {feature2} for outstanding {performance}. The revolutionary {highlight_feature} delivers {benefit}, complemented by {secondary_feature} that provides {secondary_benefit}. Meticulously crafted using {material} and finished to {quality} standards, this {product_type} excels in {use_case1} and {use_case2} scenarios. With {warranty} and industry-leading {support}, it embodies {brand}'s commitment to innovation and quality.",
        
        "The {brand} {prefix} {product_name} redefines what's possible in {category} technology. Created for discerning {user_type}, it features {feature1} and {feature2} for exceptional {performance}. At its core, the {highlight_feature} provides {benefit}, enhanced by {secondary_feature} for {secondary_benefit}. Premium {material} construction with {quality} craftsmanship ensures reliability during {use_case1} and {use_case2}. Complete with {warranty} and {support}, this {product_type} represents {brand}'s unwavering dedication to excellence."
    ]
    
    # User types by category
    user_types = {
        # Electronics
        1: ["tech enthusiasts", "busy professionals", "creative professionals", "digital nomads", "smart home enthusiasts"],
        # Smartphones
        2: ["mobile photographers", "business professionals", "tech-savvy users", "content creators", "on-the-go professionals"],
        # Laptops
        3: ["power users", "creative professionals", "business executives", "students", "remote workers"],
        # Audio
        4: ["audiophiles", "music lovers", "podcast enthusiasts", "commuters", "fitness enthusiasts"],
        # Clothing
        5: ["fashion-forward individuals", "style enthusiasts", "conscious consumers", "trend-setters", "urban professionals"],
        # Men's
        6: ["modern gentlemen", "active professionals", "style-conscious men", "outdoor enthusiasts", "business professionals"],
        # Women's
        7: ["fashion-forward women", "busy professionals", "active lifestyles", "style-conscious individuals", "urban professionals"],
        # Home & Kitchen
        8: ["home chefs", "culinary enthusiasts", "busy families", "entertaining hosts", "gourmet cooks"],
        # Books
        9: ["lifelong learners", "professionals", "enthusiasts", "students", "knowledge seekers"],
        # Sports & Outdoors
        10: ["serious athletes", "outdoor enthusiasts", "fitness fanatics", "weekend warriors", "adventure seekers"],
        # Beauty & Personal Care
        11: ["beauty enthusiasts", "skincare aficionados", "self-care devotees", "wellness-focused individuals", "beauty professionals"],
        # Furniture & Decor
        12: ["home design enthusiasts", "urban dwellers", "professional decorators", "new homeowners", "comfort seekers"],
        # Toys & Games
        13: ["developing minds", "creative children", "family game nights", "educational play", "STEM learning"],
        # Pet Supplies
        14: ["devoted pet parents", "animal lovers", "multiple pet households", "active pet owners", "pet health advocates"]
    }
    
    # Materials by category
    materials = {
        1: ["premium components", "aerospace-grade materials", "advanced composites", "precision-engineered elements", "high-grade electronics"],
        2: ["premium-grade components", "aerospace alloys", "precision-engineered elements", "impact-resistant materials", "high-grade glass"],
        3: ["premium-grade aluminum", "carbon fiber components", "high-density polymers", "military-grade materials", "premium-engineered alloys"],
        4: ["custom-designed acoustic materials", "premium-grade components", "precision-engineered drivers", "advanced composites", "acoustically-optimized materials"],
        5: ["premium natural fibers", "sustainably-sourced fabrics", "performance-grade textiles", "eco-friendly materials", "high-tech performance fabrics"],
        6: ["premium cotton blends", "performance-grade fabrics", "sustainable textiles", "technical performance materials", "luxury natural fibers"],
        7: ["premium sustainable fabrics", "high-performance blends", "luxury natural fibers", "technical textiles", "eco-conscious materials"],
        8: ["premium-grade stainless steel", "commercial-grade components", "high-performance ceramics", "precision-engineered elements", "professional-grade materials"],
        9: ["sustainably-sourced paper", "premium binding materials", "archival-quality components", "high-definition printing", "eco-friendly production"],
        10: ["aerospace-grade aluminum", "performance composites", "technical performance fabrics", "high-density foams", "carbon fiber components"],
        11: ["pharmaceutical-grade ingredients", "botanical extracts", "clinical-strength actives", "dermatologist-formulated compounds", "natural botanical complexes"],
        12: ["sustainably-harvested hardwoods", "premium upholstery materials", "high-resilience foams", "aircraft-grade aluminum", "ethically-sourced natural materials"],
        13: ["non-toxic premium plastics", "sustainable wood", "high-quality paper stock", "child-safe materials", "durable composites"],
        14: ["pet-safe premium materials", "orthopedic-grade foams", "durable natural fibers", "veterinarian-approved compounds", "high-performance fabrics"]
    }
    
    # Quality descriptors
    qualities = ["exceptional precision", "uncompromising standards", "meticulous attention to detail", "rigorous quality control", "artisanal care", "exacting specifications", "stringent quality testing", "professional-grade standards", "flawless execution", "superior craftsmanship"]
    
    # Performance descriptors
    performances = ["unparalleled performance", "exceptional results", "outstanding efficiency", "superior functionality", "remarkable effectiveness", "industry-leading capabilities", "benchmark-setting performance", "best-in-class operation", "flawless execution", "transformative results"]
    
    # Use cases by category
    use_cases = {
        1: ["at home", "in the office", "while traveling", "during creative projects", "for entertainment", "managing your smart home", "working remotely", "gaming"],
        2: ["capturing life's moments", "staying connected", "managing your digital life", "creating content", "gaming on the go", "multitasking", "video conferencing", "social networking"],
        3: ["handling demanding workloads", "creating digital content", "managing business operations", "attending virtual meetings", "gaming", "streaming media", "analyzing complex data", "studying"],
        4: ["enjoying music", "during workouts", "commuting", "in noisy environments", "taking calls", "watching movies", "gaming", "recording content"],
        5: ["attending special occasions", "during daily activities", "at work", "while traveling", "during seasonal transitions", "for casual outings", "at formal events", "weekend getaways"],
        6: ["at the office", "during business meetings", "for casual weekends", "at special events", "while traveling", "during outdoor activities", "for evening occasions", "day-to-day wear"],
        7: ["at professional settings", "during social gatherings", "for casual outings", "at formal events", "while traveling", "during seasonal transitions", "for weekend activities", "day-to-night transitions"],
        8: ["preparing family meals", "entertaining guests", "creating gourmet dishes", "batch cooking", "preparing quick meals", "experimenting with new recipes", "baking", "meal prepping"],
        9: ["studying", "researching", "developing professional skills", "personal growth", "reference", "teaching", "learning new concepts", "staying current in your field"],
        10: ["training", "competing", "weekend adventures", "daily workouts", "outdoor expeditions", "improving techniques", "team activities", "personal challenges"],
        11: ["daily skincare routines", "special treatment sessions", "professional beauty services", "travel skincare", "addressing specific concerns", "maintaining healthy skin", "anti-aging regimens", "deep cleansing rituals"],
        12: ["everyday living", "entertaining guests", "working from home", "relaxing", "organizing your space", "small space living", "family gatherings", "creating functional spaces"],
        13: ["educational play", "family game nights", "independent exploration", "skill development", "creative expression", "collaborative play", "outdoor adventures", "indoor activities"],
        14: ["daily pet care", "traveling with pets", "training sessions", "addressing health needs", "playtime", "grooming routines", "comfort and rest", "special needs care"]
    }
    
    # Warranty and support options
    warranties = ["comprehensive warranty coverage", "extended service protection", "lifetime technical support", "satisfaction guarantee", "worry-free warranty", "no-questions-asked return policy", "long-term service commitment", "product protection plan"]
    
    supports = ["24/7 customer support", "dedicated service teams", "online knowledge base", "expert technical assistance", "personalized setup help", "video tutorials", "community forums", "priority customer care"]
    
    # Generate products for each category
    all_products = []
    
    for category_id, count in category_product_counts.items():
        category_name = category_map.get(category_id, "Unknown")
        template = product_templates.get(category_id, product_templates[1])  # Default to electronics if category not found
        
        for i in range(count):
            # Generate product details
            brand = random.choice(template["brands"])
            prefix = random.choice(template["prefixes"])
            product_type = random.choice(template["products"])
            product_name = f"{product_type}"
            
            # Generate price in the category's range
            base_price = random.uniform(template["price_range"][0], template["price_range"][1])
            price = round(base_price, 2)
            
            # Determine if on sale (30% chance)
            on_sale = random.random() < 0.3
            sale_price = round(price * 0.85, 2) if on_sale else None
            
            # Calculate cost (usually 40-60% of retail price)
            cost_percentage = random.uniform(0.4, 0.6)
            cost = round(price * cost_percentage, 2)
            
            # Generate stock quantity (more for lower-priced items)
            stock_quantity = random.randint(10, 200)
            if price > 500:
                stock_quantity = random.randint(5, 50)
            
            # Generate SKU
            sku = f"{brand[:3].upper()}-{product_type[:3].upper()}-{random.randint(100, 999)}"
            
            # Generate weight and dimensions appropriate for the product type
            if product_type in ["Laptop", "Computer", "Tablet"]:
                weight = round(random.uniform(0.8, 3.5), 2)
                dimensions = json.dumps({
                    "length": round(random.uniform(9, 15), 2),
                    "width": round(random.uniform(6, 12), 2),
                    "height": round(random.uniform(0.3, 1.2), 2)
                })
            elif product_type in ["Smartphone", "Earbuds", "Watch"]:
                weight = round(random.uniform(0.1, 0.5), 2)
                dimensions = json.dumps({
                    "length": round(random.uniform(2, 6), 2),
                    "width": round(random.uniform(1, 3), 2),
                    "height": round(random.uniform(0.2, 0.8), 2)
                })
            elif "Clothing" in category_name or "Men's" in category_name or "Women's" in category_name:
                weight = round(random.uniform(0.2, 1.0), 2)
                dimensions = json.dumps({
                    "length": round(random.uniform(10, 30), 2),
                    "width": round(random.uniform(8, 20), 2),
                    "height": round(random.uniform(0.5, 3), 2)
                })
            else:
                weight = round(random.uniform(0.5, 15.0), 2)
                dimensions = json.dumps({
                    "length": round(random.uniform(5, 24), 2),
                    "width": round(random.uniform(5, 18), 2),
                    "height": round(random.uniform(2, 12), 2)
                })
            
            # Determine if featured (10% chance)
            is_featured = 1 if random.random() < 0.1 else 0
            
            # Generate product description using templates
            # Select random features
            features = random.sample(template["features"], 4)
            feature1, feature2, feature3, feature4 = features
            
            highlight_feature = random.choice([
                "advanced technology", "proprietary system", "innovative design", 
                "next-generation architecture", "exclusive feature", "cutting-edge component",
                "revolutionary approach", "state-of-the-art mechanism", "patented solution"
            ])
            
            secondary_feature = random.choice([
                "intuitive interface", "smart connectivity", "premium construction", 
                "thoughtful design", "intelligent system", "adaptive algorithm",
                "precision engineering", "ergonomic layout", "responsive controls"
            ])
            
            benefit = random.choice([
                "exceptional performance", "unparalleled convenience", "remarkable efficiency", 
                "outstanding results", "superior reliability", "incredible versatility",
                "enhanced productivity", "ultimate comfort", "seamless operation"
            ])
            
            secondary_benefit = random.choice([
                "long-term durability", "intuitive operation", "effortless integration", 
                "consistent results", "simplified workflow", "reduced maintenance",
                "enhanced safety", "increased efficiency", "maximum flexibility"
            ])
            
            # Select description template and fill it out
            desc_template = random.choice(description_templates)
            user_type = random.choice(user_types.get(category_id, user_types[1]))
            material = random.choice(materials.get(category_id, materials[1]))
            quality = random.choice(qualities)
            performance = random.choice(performances)
            use_case_options = use_cases.get(category_id, use_cases[1])
            use_case1, use_case2 = random.sample(use_case_options, 2)
            warranty = random.choice(warranties)
            support = random.choice(supports)
            
            description = desc_template.format(
                prefix=prefix,
                product_name=product_name,
                category=category_name,
                feature1=feature1,
                feature2=feature2,
                feature3=feature3,
                user_type=user_type,
                highlight_feature=highlight_feature,
                benefit=benefit,
                secondary_feature=secondary_feature,
                secondary_benefit=secondary_benefit,
                material=material,
                quality=quality,
                product_type=product_type.lower(),
                performance=performance,
                use_case1=use_case1,
                use_case2=use_case2,
                warranty=warranty,
                support=support,
                brand=brand
            )
            
            # Generate short description
            short_description = f"{prefix} {product_type.lower()} with {feature1.lower()}."
            
            # Add to products list
            all_products.append((
                None, f"{prefix} {product_name}", sku, description, short_description,
                price, sale_price, cost, stock_quantity, category_id, brand, weight,
                dimensions, is_featured, 1  # is_active is always 1
            ))
    
    # Insert all generated products
    cursor.executemany('''
    INSERT INTO products (
        id, name, sku, description, short_description, price, sale_price, cost, 
        stock_quantity, category_id, brand, weight, dimensions, is_featured, is_active
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', all_products)
    
    # Fetch the newly inserted product IDs
    cursor.execute("SELECT id FROM products WHERE id >= ?", (start_id,))
    new_product_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"Successfully generated and inserted {len(new_product_ids)} new products")
    
    # Create product attributes based on categories
    attributes_to_insert = []
    
    # Define attribute templates by category
    attribute_templates = {
        # Electronics
        1: [
            ("Color", ["Black", "Silver", "White", "Space Gray", "Midnight Blue", "Rose Gold", "Graphite"], 1, 1, 1),
            ("Warranty", ["1 Year", "2 Years", "3 Years", "5 Years", "Limited Lifetime"], 2, 1, 1),
            ("Connectivity", ["Bluetooth 5.2", "Wi-Fi 6E", "USB-C", "Thunderbolt 4", "HDMI 2.1", "5G"], 3, 1, 1),
            ("Power", ["Battery Powered", "Rechargeable", "USB Powered", "AC Adapter", "Wireless Charging"], 4, 1, 1)
        ],
        # Smartphones
        2: [
            ("Color", ["Midnight Black", "Stellar Silver", "Arctic Blue", "Sunset Gold", "Cosmic Gray", "Pearl White"], 1, 1, 1),
            ("Storage", ["64GB", "128GB", "256GB", "512GB", "1TB"], 2, 1, 1),
            ("Display", ["AMOLED", "Super Retina XDR", "Dynamic AMOLED", "Liquid Retina", "ProMotion"], 3, 1, 1),
            ("Camera", ["12MP Wide", "48MP Quad", "108MP Ultra", "Triple Lens System", "Periscope Zoom"], 4, 1, 1)
        ],
        # Laptops
        3: [
            ("Processor", ["Intel Core i7", "AMD Ryzen 9", "Apple M2", "Intel Core i9", "AMD Ryzen 7"], 1, 1, 1),
            ("Memory", ["8GB", "16GB", "32GB", "64GB"], 2, 1, 1),
            ("Storage", ["512GB SSD", "1TB SSD", "2TB SSD", "4TB SSD", "512GB + 2TB HDD"], 3, 1, 1),
            ("Display", ["13.3-inch Retina", "15.6-inch 4K", "17-inch UHD", "14-inch QHD", "16-inch XDR"], 4, 1, 1)
        ],
        # Audio
        4: [
            ("Type", ["Over-ear", "In-ear", "On-ear", "True Wireless", "Bone Conduction", "Open-back"], 1, 1, 1),
            ("Noise Cancellation", ["Active Noise Cancelling", "Passive Isolation", "Transparency Mode", "Adaptive ANC", "None"], 2, 1, 1),
            ("Battery Life", ["Up to 8 hours", "Up to 20 hours", "Up to 30 hours", "Up to 40 hours", "Up to 60 hours"], 3, 1, 1),
            ("Water Resistance", ["IPX4", "IPX5", "IPX7", "IP68", "Not water resistant"], 4, 1, 1)
        ],
        # Clothing
        5: [
            ("Material", ["Cotton", "Polyester", "Wool", "Cashmere", "Silk", "Linen", "Nylon", "Blend"], 1, 1, 1),
            ("Fit", ["Regular", "Slim", "Relaxed", "Athletic", "Oversized", "Tailored"], 2, 1, 1),
            ("Season", ["All-season", "Summer", "Winter", "Spring/Fall", "Resort"], 3, 1, 1),
            ("Care", ["Machine Wash", "Hand Wash", "Dry Clean Only", "Spot Clean", "Machine Wash Cold"], 4, 0, 1)
        ],
        # Men's
        6: [
            ("Material", ["100% Cotton", "Cotton Blend", "Merino Wool", "Performance Polyester", "Linen Blend", "Technical Fabric"], 1, 1, 1),
            ("Fit", ["Classic", "Slim", "Modern", "Athletic", "Regular", "Tailored"], 2, 1, 1),
            ("Occasion", ["Casual", "Business", "Formal", "Athletic", "Outdoor", "Everyday"], 3, 1, 1),
            ("Care", ["Machine Wash", "Hand Wash", "Dry Clean Only", "Tumble Dry Low", "Air Dry"], 4, 0, 1)
        ],
        # Women's
        7: [
            ("Material", ["Premium Cotton", "Silk Blend", "Cashmere Blend", "Sustainable Viscose", "Organic Cotton", "Technical Fabric"], 1, 1, 1),
            ("Fit", ["Relaxed", "Slim", "Classic", "Boyfriend", "Fitted", "Oversized"], 2, 1, 1),
            ("Style", ["Contemporary", "Classic", "Bohemian", "Minimalist", "Elegant", "Casual"], 3, 1, 1),
            ("Care", ["Machine Wash Cold", "Hand Wash", "Dry Clean Only", "Gentle Cycle", "Lay Flat to Dry"], 4, 0, 1)
        ],
        # Home & Kitchen
        8: [
            ("Material", ["Stainless Steel", "Cast Iron", "Ceramic", "Glass", "BPA-free Plastic", "Tempered Glass", "Aluminum"], 1, 1, 1),
            ("Capacity", ["Small", "Medium", "Large", "Extra Large", "Family Size", "Compact"], 2, 1, 1),
            ("Features", ["Programmable", "Timer", "Digital Display", "Quick Heat", "Energy Efficient", "Smart Enabled"], 3, 1, 1),
            ("Care", ["Dishwasher Safe", "Hand Wash Only", "Wipe Clean", "Self-Cleaning", "Easy Clean"], 4, 0, 1)
        ],
        # Books
        9: [
            ("Format", ["Hardcover", "Paperback", "e-Book", "Audiobook", "Spiral-bound", "Box Set"], 1, 1, 1),
            ("Pages", ["Under 200", "200-400", "400-600", "600-800", "Over 800"], 2, 0, 1),
            ("Level", ["Beginner", "Intermediate", "Advanced", "Professional", "All Levels"], 3, 1, 1),
            ("Language", ["English", "Spanish", "French", "German", "Chinese", "Japanese"], 4, 1, 1)
        ],
        # Sports & Outdoors
        10: [
            ("Material", ["Aluminum", "Carbon Fiber", "High-impact Plastic", "Nylon", "Synthetic", "Waterproof Fabric"], 1, 1, 1),
            ("Size", ["Small", "Medium", "Large", "X-Large", "Adjustable", "One Size"], 2, 1, 1),
            ("Activity", ["Running", "Hiking", "Cycling", "Swimming", "Camping", "Fitness", "Team Sports"], 3, 1, 1),
            ("Weather Rating", ["All-Weather", "3-Season", "Water-Resistant", "Waterproof", "UV Protection"], 4, 1, 1)
        ],
        # Beauty & Personal Care
        11: [
            ("Skin Type", ["All Skin Types", "Sensitive", "Dry", "Oily", "Combination", "Mature"], 1, 1, 1),
            ("Concerns", ["Anti-Aging", "Brightening", "Hydration", "Acne", "Redness", "Texture"], 2, 1, 1),
            ("Formulation", ["Cream", "Serum", "Gel", "Oil", "Lotion", "Powder", "Mousse"], 3, 1, 1),
            ("Free From", ["Parabens", "Sulfates", "Silicones", "Fragrance", "Dyes", "Phthalates"], 4, 0, 1)
        ],
        # Furniture & Decor
        12: [
            ("Material", ["Solid Wood", "Engineered Wood", "Metal", "Glass", "Upholstered", "Leather", "Fabric"], 1, 1, 1),
            ("Style", ["Modern", "Traditional", "Contemporary", "Industrial", "Mid-Century", "Rustic"], 2, 1, 1),
            ("Assembly", ["Ready Assembled", "Partial Assembly", "Full Assembly Required", "No Assembly"], 3, 0, 1),
            ("Room", ["Living Room", "Bedroom", "Dining Room", "Home Office", "Kitchen", "Outdoor"], 4, 1, 1)
        ],
        # Toys & Games
        13: [
            ("Age Range", ["3-5 years", "6-8 years", "9-12 years", "13+ years", "Adult", "All Ages"], 1, 1, 1),
            ("Type", ["Educational", "Building", "Strategy", "Cooperative", "Creative", "Active Play"], 2, 1, 1),
            ("Players", ["1 player", "2 players", "2-4 players", "4-6 players", "6+ players", "Team play"], 3, 1, 1),
            ("Duration", ["Under 30 minutes", "30-60 minutes", "1-2 hours", "2+ hours", "Varies"], 4, 0, 1)
        ],
        # Pet Supplies
        14: [
            ("Pet Type", ["Dogs", "Cats", "Small Pets", "Birds", "Fish", "Reptiles", "All Pets"], 1, 1, 1),
            ("Size", ["X-Small", "Small", "Medium", "Large", "X-Large", "Adjustable"], 2, 1, 1),
            ("Life Stage", ["Puppy/Kitten", "Adult", "Senior", "All Ages"], 3, 1, 1),
            ("Features", ["Washable", "Waterproof", "Chew-Resistant", "Portable", "Interactive", "Adjustable"], 4, 1, 1)
        ]
    }
    
    # Create attributes for all products
    for product_id in new_product_ids:
        # Get the category for this product
        cursor.execute("SELECT category_id FROM products WHERE id = ?", (product_id,))
        category_id = cursor.fetchone()[0]
        
        # Select appropriate attributes based on category
        attribute_template = attribute_templates.get(category_id, attribute_templates[1])  # Default to electronics
        
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
    print(f"Created {len(attributes_to_insert)} product attributes")
    
    # Insert product images (at least one per product)
    product_images = []
    for product_id in new_product_ids:
        # Get product name for image alt text
        cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
        product_name = cursor.fetchone()[0]
        
        # Create primary image
        product_images.append((None, product_id, f"product_{product_id}_main.jpg", 1, 1, f"{product_name} main view"))
        
        # Add 2-4 additional images
        num_additional = random.randint(2, 4)
        angles = ["front", "side", "back", "detail", "lifestyle", "packaging", "action", "closeup", "top", "interior"]
        selected_angles = random.sample(angles, min(num_additional, len(angles)))
        
        for i, angle in enumerate(selected_angles):
            product_images.append(
                (None, product_id, f"product_{product_id}_{angle}.jpg", 0, i+2, f"{product_name} {angle} view")
            )
    
    cursor.executemany('''
    INSERT INTO product_images (
        id, product_id, image_url, is_primary, display_order, alt_text
    )
    VALUES (?, ?, ?, ?, ?, ?)
    ''', product_images)
    print(f"Created {len(product_images)} product images")
    
    # Add tags to products
    product_tags = []
    
    # Get all tag IDs
    cursor.execute("SELECT id FROM tags")
    all_tag_ids = [row[0] for row in cursor.fetchall()]
    
    # Assign 2-4 random tags to each product
    for product_id in new_product_ids:
        num_tags = random.randint(2, 4)
        selected_tags = random.sample(all_tag_ids, min(num_tags, len(all_tag_ids)))
        for tag_id in selected_tags:
            product_tags.append((product_id, tag_id))
    
    cursor.executemany('''
    INSERT INTO product_tags (product_id, tag_id)
    VALUES (?, ?)
    ''', product_tags)
    print(f"Created {len(product_tags)} product tag associations")
    
    # Create product variants for appropriate categories (primarily clothing, electronics)
    variants_to_insert = []
    
    # Categories that commonly have variants
    variant_categories = [1, 2, 3, 4, 6, 7]
    
    # Select products in variant-appropriate categories (about 40% of them)
    cursor.execute("""
        SELECT id, name, sku, category_id FROM products 
        WHERE id >= ? AND category_id IN (1, 2, 3, 4, 6, 7)
    """, (start_id,))
    variant_candidates = cursor.fetchall()
    variant_product_count = int(len(variant_candidates) * 0.4)
    variant_product_ids = random.sample([row[0] for row in variant_candidates], min(variant_product_count, len(variant_candidates)))
    
    for product_id in variant_product_ids:
        # Find the product info
        cursor.execute("SELECT sku, name, category_id FROM products WHERE id = ?", (product_id,))
        base_sku, product_name, category_id = cursor.fetchone()
        
        if category_id in [1, 2, 3, 4]:  # Electronics
            # Create storage or color variants
            variant_types = random.choice([
                ("Color", ["Black", "Silver", "White", "Blue", "Red", "Gold", "Green", "Purple"]),
                ("Storage", ["64GB", "128GB", "256GB", "512GB", "1TB", "2TB"]),
                ("Memory", ["4GB", "8GB", "16GB", "32GB", "64GB"])
            ])
            attr_name, attr_values = variant_types
            
            # Select a subset of values
            num_variants = random.randint(2, min(5, len(attr_values)))
            selected_values = random.sample(attr_values, num_variants)
            
            for value in selected_values:
                # Variants with higher storage/memory cost more
                price_adj = 0
                if attr_name == "Storage" and "GB" in value:
                    # Extract numeric value and calculate price increase
                    try:
                        gb_value = int(value.replace("GB", "").replace("TB", "000"))
                        price_adj = (gb_value // 64) * 50  # $50 more per 64GB
                    except:
                        price_adj = random.choice([0, 50, 100, 150])
                elif attr_name == "Memory" and "GB" in value:
                    try:
                        gb_value = int(value.replace("GB", ""))
                        price_adj = (gb_value // 4) * 75  # $75 more per 4GB of RAM
                    except:
                        price_adj = random.choice([0, 75, 150, 225])
                
                variant_sku = f"{base_sku}-{value.replace(' ', '').replace('GB', '').replace('TB', 'T')}"
                variant_name = f"{product_name} {value}"
                stock = random.randint(10, 50)
                attr_json = json.dumps({attr_name.lower(): value})
                image_url = f"product_{product_id}_{value.lower().replace(' ', '').replace('gb', '').replace('tb', 't')}.jpg"
                
                variants_to_insert.append(
                    (None, product_id, variant_sku, variant_name, price_adj, stock, attr_json, image_url, 1)
                )
                
        elif category_id in [5, 6, 7]:  # Clothing
            # Create size and color variants
            sizes = ["XS", "S", "M", "L", "XL", "XXL"]
            colors = ["Black", "Navy", "Gray", "White", "Burgundy", "Olive", "Blue", "Red", "Charcoal", "Brown", "Beige"]
            
            # Pick a subset of sizes and colors
            size_count = random.randint(4, min(len(sizes), 6))
            color_count = random.randint(3, min(len(colors), 6))
            
            selected_sizes = random.sample(sizes, size_count)
            selected_colors = random.sample(colors, color_count)
            
            for size in selected_sizes:
                for color in selected_colors:
                    variant_sku = f"{base_sku}-{color[:3].upper()}-{size}"
                    variant_name = f"{product_name} {color} {size}"
                    
                    # Larger sizes might cost slightly more
                    price_adj = 0
                    if size in ["XL", "XXL"]:
                        price_adj = random.choice([0, 5, 10])
                    
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
    
    print(f"Created {len(variants_to_insert)} product variants")
    print(f"Successfully inserted {len(new_product_ids)} new products with complete details")

if __name__ == "__main__":
    add_more_products()