import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class SmallBusinessDataGenerator:
    """
    Generator for fake small business data in the 11367 zip code area (Flushing, NY)
    """
    
    def __init__(self):
        # Business types that exist in your DataLoader urls
        self.business_types = {
            'FWR': 'Flower Wall Rental',
            'GRAZE': 'Catering',
            'NAOMIS': 'Kosher Pizza',
            'BANDH': 'Plumbing and Heating',
            'AEROLA': 'Tattoo Shop',
            'ENOODLE': 'Noodle Restaurant',
            'BTFLI': 'Bathtub Refinishing',
            'MST': 'Taiwanese Restaurant',
            'ANDA': 'Cafe',
            'ARONS': 'Farms Market',
            'FARS': 'Appliance Repair',
            'OTNPP': 'Pizza Restaurant',
            'TSB': 'Sandwich Shop',
            'AS': 'Discount Store',
            'ZFSTG': 'Fusion Cuisine'
        }
        
        # Common NYC neighborhoods near 11367
        self.neighborhoods = [
            'Flushing', 'Kew Gardens Hills', 'Pomonok', 'Fresh Meadows', 
            'Jamaica Estates', 'Briarwood', 'Jamaica Hills'
        ]
        
        # Address format templates
        self.street_names = [
            'Main St', 'Kissena Blvd', 'Union St', 'Jewel Ave', 
            'Parsons Blvd', '150th St', 'Melbourne Ave', 'Horace Harding Expy'
        ]

        # Business name mapping
        self.business_names = {
            "FWR": "The Flower Wall Rental Co.",
            "GRAZE": "Graze & Gather Catering",
            "NAOMIS": "Naomi's Kosher Pizza",
            "BANDH": "B&H Plumbing and Heating",
            "AEROLA": "Areola Tattooing Studio",
            "ENOODLE": "East Noodle House",
            "BTFLI": "Bathtub Refinishing Long Island",
            "MST": "Main Street Taiwanese",
            "ANDA": "Anda Cafe Flushing",
            "ARONS": "Aron's Kisena Farms",
            "FARS": "Flushing Appliance Repair Specialists",
            "OTNPP": "Pizza Professor",
            "TSB": "The Sandwich Bar",
            "AS": "Amazing Savings",
            "ZFSTG": "Zen Fusion Cuisine To Go"
        }

        # Supplier name mapping
        self.supplier_names = {
            "Floral Supplier": ["Bloom Wholesale", "NYC Flower Market", "Garden State Flowers", "Eastern Floral Supply"],
            "Food Distributor": ["Sysco Metro NY", "US Foods NYC", "Restaurant Depot", "Gordon Food Service"],
            "Plumbing Supply": ["Ferguson", "F.W. Webb", "Blackman Plumbing", "Weinstein Supply"],
            "Ink Supplier": ["Eternal Ink", "Intenze Products", "Fusion Tattoo Ink", "Dynamic Color Co."],
            "Coating Supplier": ["Refinishing Solutions", "Bath Renew Supply", "Surface Specialists", "Porcelain Refinishers"],
            "Coffee Bean Supplier": ["Dallis Bros Coffee", "Cafe Grumpy Wholesale", "Porto Rico Importing", "Stumptown Coffee"],
            "Produce Farmer": ["Long Island Fresh", "Hudson Valley Harvest", "Queens County Farm", "NY Greenmarkets"],
            "Parts Distributor": ["Marcone Supply", "Reliable Parts", "Appliance Parts Depot", "1st Source Servall"],
            "Liquidation Wholesaler": ["Closeout Central", "Surplus Merchandise", "NYDiscount Wholesale", "Overstock Distributors"]
        }

        # Competitor name mapping by business type
        self.competitor_names = {
            "Flower Wall Rental": ["NYC Flower Walls", "Floral Backdrops NYC", "Manhattan Floral Events", "Brooklyn Bloom Walls"],
            "Kosher Pizza": ["Kosher Slice", "Jerusalem Pizza", "Queens Pizza House", "NY Style Kosher", "Main Street Pizza"],
            "Pizza Restaurant": ["Kosher Slice", "Jerusalem Pizza", "Queens Pizza House", "NY Style Kosher", "Main Street Pizza"],
            "Plumbing and Heating": ["Queens Plumbing Co.", "Five Boro Plumbing", "NY Plumbing & Heating", "AAA Plumbers"],
            "Tattoo Shop": ["Ink Masters NYC", "Queens Tattoo Studio", "Empire Ink", "New York Tattoo Collective"],
            "Noodle Restaurant": ["Noodle House", "Taiwan Cafe", "Eastern Fusion", "Golden Noodle", "Tasty Hand-Pulled Noodles"],
            "Taiwanese Restaurant": ["Noodle House", "Taiwan Cafe", "Eastern Fusion", "Golden Noodle", "Tasty Hand-Pulled Noodles"],
            "Fusion Cuisine": ["Noodle House", "Taiwan Cafe", "Eastern Fusion", "Golden Noodle", "Tasty Hand-Pulled Noodles"],
            "Bathtub Refinishing": ["NY Bath Renew", "Surface Solutions", "Queens Tub Refinishing", "Bathroom Makeover Pro"],
            "Cafe": ["Urban Coffee", "Main Street Cafe", "Brew & Bites", "Morning Roast", "Queens Cafe"],
            "Farms Market": ["Fresh Market", "Local Harvest", "Queens Farmers", "Organic Marketplace", "Fresh & Local"],
            "Appliance Repair": ["A1 Appliance Service", "Quick Fix Appliance", "NY Appliance Pros", "Same Day Repair"],
            "Sandwich Shop": ["Subway", "Queens Deli", "NY Sandwich Co.", "Fresh Subs", "Main Street Deli"],
            "Discount Store": ["Dollar Tree", "Family Dollar", "5 Below", "Amazing Buys", "Discount Paradise"],
            "Catering": ["Queens Catering", "NY Event Food", "Gourmet Gatherings", "Elegant Eats"]
        }
        
    def generate_business_data(self, business_id: str) -> Dict[str, Any]:
        """Generate comprehensive fake data for a single business"""
        business_type = self.business_types.get(business_id, "General Retail")
        
        # Basic information
        data = {
            "business_id": business_id,
            "name": self._generate_business_name(business_id, business_type),
            "business_type": business_type,
            "address": self._generate_address(),
            "zip_code": "11367",
            "neighborhood": random.choice(self.neighborhoods),
            "phone": f"(718) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "established": random.randint(1990, 2022),
            "employees": random.randint(2, 25),
            "sq_footage": random.randint(500, 5000),
            "annual_revenue": random.randint(80000, 1500000),
            "owner": self._generate_owner_name(),
        }
        
        # Additional data
        data["financials"] = self._generate_financials(data["annual_revenue"])
        data["inventory"] = self._generate_inventory(business_id, business_type)
        data["transactions"] = self._generate_transactions(business_id, data["annual_revenue"])
        data["hours"] = self._generate_hours(business_type)
        data["reputation"] = {
            "rating": round(random.uniform(3.5, 4.9), 1),
            "review_count": random.randint(10, 500),
            "yelp_url": f"https://yelp.com/biz/{business_id.lower()}-queens",
        }
        data["suppliers"] = self._generate_suppliers(business_type)
        data["competitors"] = self._generate_competitors(business_type)
        
        return data
    
    def _generate_business_name(self, business_id: str, business_type: str) -> str:
        """Generate a business name based on ID and type"""
        if business_id in self.business_names:
            return self.business_names[business_id]
        else:
            # Generic name generator
            adjectives = ["Royal", "Golden", "Premier", "Elite", "Family", "Signature"]
            nouns = ["Services", "Solutions", "Experts", "Specialists", "Group", "Enterprises"]
            return f"{random.choice(adjectives)} {business_type} {random.choice(nouns)}"
    
    def _generate_address(self) -> str:
        """Generate a random address in the 11367 area"""
        return f"{random.randint(40, 190)} {random.choice(self.street_names)}, Queens, NY"
    
    def _generate_owner_name(self) -> str:
        """Generate a random owner name"""
        first_names = [
            "Michael", "David", "Sarah", "Jennifer", "Daniel", "John", "Maria", 
            "Robert", "Linda", "Jessica", "Wei", "Li", "Ming", "Jun", "Ahmed",
            "Fatima", "Mohammad", "Ravi", "Priya", "Yusuf", "Rachel", "Rebecca"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Chen", "Wong", "Patel", "Khan", "Nguyen", "Kim",
            "Shah", "Lee", "Cohen", "Goldstein", "Rossi", "Russo", "Esposito"
        ]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_financials(self, annual_revenue: int) -> Dict[str, Any]:
        """Generate financial data based on annual revenue"""
        monthly_revenue = annual_revenue / 12
        
        # Seasonal variations - businesses tend to have higher revenue in certain months
        seasonal_factors = [0.85, 0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.0, 0.95, 1.1, 1.25]  # Dec higher for holidays
        
        # Generate monthly revenues with seasonal and random variations
        monthly_revenues = []
        for i in range(12):
            base = monthly_revenue * seasonal_factors[i]
            variation = random.uniform(0.9, 1.1)  # +/- 10% random variation
            monthly_revenues.append(round(base * variation))
        
        # Generate cost structure
        cost_of_goods_percent = random.uniform(0.35, 0.55)
        rent_percent = random.uniform(0.1, 0.2)
        labor_percent = random.uniform(0.15, 0.25)
        utilities_percent = random.uniform(0.03, 0.07)
        marketing_percent = random.uniform(0.02, 0.08)
        other_expenses_percent = random.uniform(0.05, 0.1)
        
        total_expenses_percent = (cost_of_goods_percent + rent_percent + labor_percent + 
                                 utilities_percent + marketing_percent + other_expenses_percent)
        
        # Ensure expenses don't exceed revenue by too much
        if total_expenses_percent > 0.95:
            scaling_factor = 0.9 / total_expenses_percent
            cost_of_goods_percent *= scaling_factor
            rent_percent *= scaling_factor
            labor_percent *= scaling_factor
            utilities_percent *= scaling_factor
            marketing_percent *= scaling_factor
            other_expenses_percent *= scaling_factor
        
        profit_margin = 1 - total_expenses_percent
        
        return {
            "monthly_revenue": monthly_revenues,
            "annual_revenue": annual_revenue,
            "cost_structure": {
                "cost_of_goods": round(cost_of_goods_percent * annual_revenue),
                "rent": round(rent_percent * annual_revenue),
                "labor": round(labor_percent * annual_revenue),
                "utilities": round(utilities_percent * annual_revenue),
                "marketing": round(marketing_percent * annual_revenue),
                "other_expenses": round(other_expenses_percent * annual_revenue)
            },
            "profit": round(profit_margin * annual_revenue),
            "profit_margin": round(profit_margin, 3)
        }
    
    def _generate_inventory(self, business_id: str, business_type: str) -> Dict[str, Any]:
        """Generate inventory data appropriate for the business type"""
        inventory_templates = {
            "Flower Wall Rental": {
                "total_items": random.randint(50, 200),
                "categories": ["Flower Walls", "Props", "Accessories", "Decor"],
                "average_item_cost": random.uniform(100, 500),
                "top_items": [
                    {"name": "Classic Rose Wall", "quantity": random.randint(5, 15), "cost": random.uniform(400, 800)},
                    {"name": "Peony Backdrop", "quantity": random.randint(3, 10), "cost": random.uniform(450, 900)},
                    {"name": "Wedding Arch", "quantity": random.randint(2, 8), "cost": random.uniform(350, 700)}
                ],
                "suppliers": ["Wholesale Florist", "Craft Supply Co.", "Import Decor LLC"]
            },
            "Kosher Pizza": {
                "total_items": random.randint(100, 300),
                "categories": ["Ingredients", "Beverages", "Packaging", "Cleaning Supplies"],
                "average_item_cost": random.uniform(10, 30),
                "top_items": [
                    {"name": "Flour (50lb bags)", "quantity": random.randint(15, 30), "cost": random.uniform(25, 35)},
                    {"name": "Mozzarella Cheese (5lb blocks)", "quantity": random.randint(20, 50), "cost": random.uniform(30, 45)},
                    {"name": "Tomato Sauce (1gal)", "quantity": random.randint(15, 40), "cost": random.uniform(15, 25)}
                ],
                "suppliers": ["Restaurant Depot", "Sysco", "US Foods", "Local Kosher Supplier"]
            },
            "Pizza Restaurant": {
                "total_items": random.randint(100, 300),
                "categories": ["Ingredients", "Beverages", "Packaging", "Cleaning Supplies"],
                "average_item_cost": random.uniform(10, 30),
                "top_items": [
                    {"name": "Flour (50lb bags)", "quantity": random.randint(15, 30), "cost": random.uniform(25, 35)},
                    {"name": "Mozzarella Cheese (5lb blocks)", "quantity": random.randint(20, 50), "cost": random.uniform(30, 45)},
                    {"name": "Tomato Sauce (1gal)", "quantity": random.randint(15, 40), "cost": random.uniform(15, 25)}
                ],
                "suppliers": ["Restaurant Depot", "Sysco", "US Foods"]
            },
            "Plumbing and Heating": {
                "total_items": random.randint(300, 800),
                "categories": ["Pipes", "Fixtures", "Tools", "Heating Equipment", "Parts"],
                "average_item_cost": random.uniform(50, 200),
                "top_items": [
                    {"name": "Copper Pipe (per foot)", "quantity": random.randint(200, 500), "cost": random.uniform(3, 8)},
                    {"name": "Water Heaters", "quantity": random.randint(3, 10), "cost": random.uniform(400, 900)},
                    {"name": "Toilet Repair Kits", "quantity": random.randint(20, 50), "cost": random.uniform(25, 60)}
                ],
                "suppliers": ["Ferguson", "Home Depot Pro", "Grainger", "F.W. Webb"]
            },
            "Tattoo Shop": {
                "total_items": random.randint(100, 400),
                "categories": ["Inks", "Needles", "Equipment", "Aftercare", "Disposables"],
                "average_item_cost": random.uniform(20, 100),
                "top_items": [
                    {"name": "Tattoo Ink Sets", "quantity": random.randint(5, 20), "cost": random.uniform(200, 500)},
                    {"name": "Tattoo Needles (box)", "quantity": random.randint(30, 100), "cost": random.uniform(15, 35)},
                    {"name": "Tattoo Machines", "quantity": random.randint(5, 15), "cost": random.uniform(300, 800)}
                ],
                "suppliers": ["Kingpin Tattoo Supply", "Worldwide Tattoo Supply", "Medical Supply Co."]
            },
            "Noodle Restaurant": {
                "total_items": random.randint(150, 400),
                "categories": ["Ingredients", "Beverages", "Kitchenware", "Packaging"],
                "average_item_cost": random.uniform(15, 40),
                "top_items": [
                    {"name": "Flour (50lb bags)", "quantity": random.randint(10, 30), "cost": random.uniform(25, 40)},
                    {"name": "Rice (50lb bags)", "quantity": random.randint(10, 30), "cost": random.uniform(30, 45)},
                    {"name": "Vegetables (weekly)", "quantity": random.randint(100, 300), "cost": random.uniform(300, 800)}
                ],
                "suppliers": ["Asian Food Distributor", "Restaurant Depot", "Local Farmers Market"]
            },
            "Taiwanese Restaurant": {
                "total_items": random.randint(150, 400),
                "categories": ["Ingredients", "Beverages", "Kitchenware", "Packaging"],
                "average_item_cost": random.uniform(15, 40),
                "top_items": [
                    {"name": "Rice (50lb bags)", "quantity": random.randint(10, 30), "cost": random.uniform(25, 40)},
                    {"name": "Tea Supplies", "quantity": random.randint(10, 30), "cost": random.uniform(30, 60)},
                    {"name": "Vegetables (weekly)", "quantity": random.randint(100, 300), "cost": random.uniform(300, 800)}
                ],
                "suppliers": ["Asian Food Distributor", "Specialty Tea Importer", "Local Farmers Market"]
            },
            "Fusion Cuisine": {
                "total_items": random.randint(150, 400),
                "categories": ["Ingredients", "Beverages", "Kitchenware", "Packaging"],
                "average_item_cost": random.uniform(15, 40),
                "top_items": [
                    {"name": "Specialty Spices", "quantity": random.randint(10, 30), "cost": random.uniform(50, 150)},
                    {"name": "Seafood (weekly)", "quantity": random.randint(10, 30), "cost": random.uniform(300, 700)},
                    {"name": "Vegetables (weekly)", "quantity": random.randint(100, 300), "cost": random.uniform(300, 800)}
                ],
                "suppliers": ["Global Food Importers", "Seafood Market", "Local Farmers Market"]
            },
            "Bathtub Refinishing": {
                "total_items": random.randint(50, 200),
                "categories": ["Coatings", "Primers", "Tools", "Safety Equipment"],
                "average_item_cost": random.uniform(50, 200),
                "top_items": [
                    {"name": "Refinishing Kits", "quantity": random.randint(5, 20), "cost": random.uniform(200, 400)},
                    {"name": "Epoxy Coating (gal)", "quantity": random.randint(10, 30), "cost": random.uniform(60, 120)},
                    {"name": "Respirators", "quantity": random.randint(3, 10), "cost": random.uniform(40, 100)}
                ],
                "suppliers": ["Refinishing Supply Co.", "Industrial Coatings Warehouse", "Safety Equipment Inc."]
            },
            "Cafe": {
                "total_items": random.randint(100, 300),
                "categories": ["Coffee Beans", "Teas", "Baked Goods", "Dairy", "Equipment"],
                "average_item_cost": random.uniform(10, 50),
                "top_items": [
                    {"name": "Coffee Beans (5lb bags)", "quantity": random.randint(10, 30), "cost": random.uniform(50, 90)},
                    {"name": "Milk (gal)", "quantity": random.randint(30, 80), "cost": random.uniform(3, 6)},
                    {"name": "Pastries (daily)", "quantity": random.randint(50, 150), "cost": random.uniform(100, 300)}
                ],
                "suppliers": ["Coffee Distributor", "Bakery Supplier", "Dairy Farm", "Wholesale Grocer"]
            },
            "Farms Market": {
                "total_items": random.randint(300, 1000),
                "categories": ["Produce", "Dairy", "Meat", "Bakery", "Specialty Items"],
                "average_item_cost": random.uniform(5, 30),
                "top_items": [
                    {"name": "Fresh Vegetables (weekly)", "quantity": random.randint(200, 500), "cost": random.uniform(1000, 3000)},
                    {"name": "Dairy Products (weekly)", "quantity": random.randint(100, 300), "cost": random.uniform(800, 2000)},
                    {"name": "Bread (daily)", "quantity": random.randint(50, 150), "cost": random.uniform(200, 500)}
                ],
                "suppliers": ["Local Farms", "Regional Distributors", "Specialty Food Importers"]
            },
            "Appliance Repair": {
                "total_items": random.randint(200, 600),
                "categories": ["Parts", "Tools", "Testing Equipment", "Cleaning Supplies"],
                "average_item_cost": random.uniform(30, 150),
                "top_items": [
                    {"name": "Refrigerator Parts", "quantity": random.randint(30, 100), "cost": random.uniform(500, 1500)},
                    {"name": "Washing Machine Parts", "quantity": random.randint(30, 100), "cost": random.uniform(400, 1200)},
                    {"name": "HVAC Components", "quantity": random.randint(20, 80), "cost": random.uniform(600, 1800)}
                ],
                "suppliers": ["Appliance Parts Warehouse", "Electronic Supply Co.", "HVAC Distributors"]
            },
            "Sandwich Shop": {
                "total_items": random.randint(100, 300),
                "categories": ["Bread", "Meats", "Cheeses", "Produce", "Condiments"],
                "average_item_cost": random.uniform(10, 40),
                "top_items": [
                    {"name": "Bread (daily)", "quantity": random.randint(50, 150), "cost": random.uniform(100, 300)},
                    {"name": "Deli Meats (weekly)", "quantity": random.randint(30, 80), "cost": random.uniform(300, 800)},
                    {"name": "Fresh Vegetables (weekly)", "quantity": random.randint(50, 150), "cost": random.uniform(150, 400)}
                ],
                "suppliers": ["Baker's Supply", "Meat Wholesaler", "Produce Distributor", "Restaurant Depot"]
            },
            "Discount Store": {
                "total_items": random.randint(1000, 5000),
                "categories": ["Household", "Clothing", "Toys", "Electronics", "Seasonal"],
                "average_item_cost": random.uniform(5, 25),
                "top_items": [
                    {"name": "Cleaning Supplies", "quantity": random.randint(200, 600), "cost": random.uniform(500, 1500)},
                    {"name": "Kitchen Items", "quantity": random.randint(150, 400), "cost": random.uniform(400, 1200)},
                    {"name": "Seasonal Decor", "quantity": random.randint(100, 300), "cost": random.uniform(300, 900)}
                ],
                "suppliers": ["Wholesale Liquidators", "Import Distributors", "Closeout Specialists"]
            },
            "Catering": {
                "total_items": random.randint(150, 400),
                "categories": ["Ingredients", "Cookware", "Serving Equipment", "Disposables"],
                "average_item_cost": random.uniform(20, 80),
                "top_items": [
                    {"name": "Catering Trays", "quantity": random.randint(30, 100), "cost": random.uniform(200, 600)},
                    {"name": "Chafing Dishes", "quantity": random.randint(10, 30), "cost": random.uniform(300, 800)},
                    {"name": "Food Containers", "quantity": random.randint(100, 300), "cost": random.uniform(150, 400)}
                ],
                "suppliers": ["Restaurant Supply Co.", "Food Service Distributor", "Party Supply Warehouse"]
            }
        }
        
        # Return inventory template for business type or generic inventory
        return inventory_templates.get(business_type, {
            "total_items": random.randint(100, 500),
            "categories": ["Category A", "Category B", "Category C", "Category D"],
            "average_item_cost": random.uniform(20, 100),
            "top_items": [
                {"name": "Item 1", "quantity": random.randint(10, 50), "cost": random.uniform(50, 200)},
                {"name": "Item 2", "quantity": random.randint(15, 40), "cost": random.uniform(40, 150)},
                {"name": "Item 3", "quantity": random.randint(5, 30), "cost": random.uniform(80, 250)}
            ],
            "suppliers": ["Supplier X", "Supplier Y", "Supplier Z"]
        })
    
    def _generate_transactions(self, business_id: str, annual_revenue: int) -> List[Dict[str, Any]]:
        """Generate a sample of recent transactions"""
        # Date range for transactions (last 30 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Calculate average transaction value based on business type
        business_type = self.business_types.get(business_id, "General Retail")
        avg_transaction = self._get_avg_transaction_value(business_type)
        
        # Estimate transactions per day
        avg_daily_revenue = annual_revenue / 365
        avg_daily_transactions = max(1, int(avg_daily_revenue / avg_transaction))
        
        # Payment methods with weighted probabilities
        payment_methods = ["Credit Card", "Cash", "Debit Card", "Mobile Payment", "Check"]
        payment_weights = [0.55, 0.2, 0.15, 0.08, 0.02]
        
        # Generate transactions
        transactions = []
        current_date = start_date
        
        while current_date <= end_date:
            is_weekend = current_date.weekday() >= 5
            daily_factor = self._get_daily_factor(business_type, is_weekend)
            daily_transactions = max(1, int(avg_daily_transactions * daily_factor * random.uniform(0.8, 1.2)))
            
            for _ in range(daily_transactions):
                transaction_value = avg_transaction * random.uniform(0.7, 1.3)
                
                transaction = {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "time": f"{random.randint(9, 19):02d}:{random.randint(0, 59):02d}",
                    "amount": round(transaction_value, 2),
                    "payment_method": random.choices(payment_methods, weights=payment_weights)[0],
                    "items": random.randint(1, 5),
                }
                transactions.append(transaction)
            
            current_date += timedelta(days=1)
        
        return transactions
    
    def _get_avg_transaction_value(self, business_type: str) -> float:
        """Get average transaction value based on business type"""
        if business_type in ["Flower Wall Rental"]:
            return random.uniform(200, 1000)
        elif business_type in ["Plumbing and Heating", "Bathtub Refinishing", "Appliance Repair"]:
            return random.uniform(150, 600)
        elif business_type in ["Tattoo Shop"]:
            return random.uniform(100, 400)
        elif business_type in ["Cafe", "Noodle Restaurant", "Taiwanese Restaurant", "Pizza Restaurant", "Sandwich Shop", "Fusion Cuisine"]:
            return random.uniform(15, 50)
        elif business_type in ["Farms Market", "Discount Store"]:
            return random.uniform(20, 80)
        else:
            return random.uniform(40, 150)
    
    def _get_daily_factor(self, business_type: str, is_weekend: bool) -> float:
        """Get daily business volume factor based on business type and day of week"""
        if business_type in ["Cafe", "Restaurant", "Farms Market", "Discount Store", 
                            "Noodle Restaurant", "Taiwanese Restaurant", "Pizza Restaurant", 
                            "Sandwich Shop", "Fusion Cuisine"]:
            # Retail and food businesses often busier on weekends
            return 1.4 if is_weekend else 0.9
        else:
            # Service businesses might be steadier
            return 1.1 if is_weekend else 0.95
    
    def _generate_hours(self, business_type: str) -> Dict[str, str]:
        """Generate business hours based on type"""
        # Define hour templates by business type
        hour_templates = {
            "Cafe": {
                "weekday_open": f"{random.choice([6, 7, 8])}:00 AM",
                "weekday_close": f"{random.choice([5, 6, 7])}:00 PM",
                "weekend_open": f"{random.choice([7, 8])}:00 AM",
                "weekend_close": f"{random.choice([4, 5, 6])}:00 PM",
                "sunday_closed": False
            },
            "Farms Market": {
                "weekday_open": f"{random.choice([6, 7, 8])}:00 AM",
                "weekday_close": f"{random.choice([5, 6, 7])}:00 PM",
                "weekend_open": f"{random.choice([7, 8])}:00 AM",
                "weekend_close": f"{random.choice([4, 5, 6])}:00 PM",
                "sunday_closed": False
            },
            "Noodle Restaurant": {
                "weekday_open": f"{random.choice([10, 11])}:00 AM",
                "weekday_close": f"{random.choice([9, 10])}:00 PM",
                "weekend_open": f"{random.choice([11, 12])}:00 AM",
                "weekend_close": f"{random.choice([10, 11])}:00 PM",
                "sunday_closed": False
            },
            "Taiwanese Restaurant": {
                "weekday_open": f"{random.choice([10, 11])}:00 AM",
                "weekday_close": f"{random.choice([9, 10])}:00 PM",
                "weekend_open": f"{random.choice([11, 12])}:00 AM",
                "weekend_close": f"{random.choice([10, 11])}:00 PM",
                "sunday_closed": False
            },
            "Pizza Restaurant": {
                "weekday_open": f"{random.choice([10, 11])}:00 AM",
                "weekday_close": f"{random.choice([9, 10])}:00 PM",
                "weekend_open": f"{random.choice([11, 12])}:00 AM",
                "weekend_close": f"{random.choice([10, 11])}:00 PM",
                "sunday_closed": False
            },
            "Sandwich Shop": {
                "weekday_open": f"{random.choice([10, 11])}:00 AM",
                "weekday_close": f"{random.choice([9, 10])}:00 PM",
                "weekend_open": f"{random.choice([11, 12])}:00 AM",
                "weekend_close": f"{random.choice([10, 11])}:00 PM",
                "sunday_closed": False
            },
            "Fusion Cuisine": {
                "weekday_open": f"{random.choice([10, 11])}:00 AM",
                "weekday_close": f"{random.choice([9, 10])}:00 PM",
                "weekend_open": f"{random.choice([11, 12])}:00 AM",
                "weekend_close": f"{random.choice([10, 11])}:00 PM",
                "sunday_closed": False
            },
            "Tattoo Shop": {
                "weekday_open": f"{random.choice([11, 12, 1])}:00 {random.choice(['AM', 'PM'])}", 
                "weekday_close": f"{random.choice([8, 9, 10])}:00 PM",
                "weekend_open": f"{random.choice([12, 1, 2])}:00 PM",
                "weekend_close": f"{random.choice([9, 10, 11])}:00 PM",
                "sunday_closed": random.random() < 0.5
            },
            "Plumbing and Heating": {
                "weekday_open": f"{random.choice([7, 8, 9])}:00 AM",
                "weekday_close": f"{random.choice([5, 6])}:00 PM",
                "weekend_open": f"{random.choice([8, 9])}:00 AM",
                "weekend_close": f"{random.choice([2, 3, 4])}:00 PM",
                "sunday_closed": random.random() < 0.5
            },
            "Bathtub Refinishing": {
                "weekday_open": f"{random.choice([7, 8, 9])}:00 AM",
                "weekday_close": f"{random.choice([5, 6])}:00 PM",
                "weekend_open": f"{random.choice([8, 9])}:00 AM",
                "weekend_close": f"{random.choice([2, 3, 4])}:00 PM",
                "sunday_closed": random.random() < 0.5
            },
            "Appliance Repair": {
                "weekday_open": f"{random.choice([7, 8, 9])}:00 AM",
                "weekday_close": f"{random.choice([5, 6])}:00 PM",
                "weekend_open": f"{random.choice([8, 9])}:00 AM",
                "weekend_close": f"{random.choice([2, 3, 4])}:00 PM",
                "sunday_closed": random.random() < 0.5
            }
        }
        
        # Get template or use default retail hours
        template = hour_templates.get(business_type, {
            "weekday_open": f"{random.choice([9, 10])}:00 AM",
            "weekday_close": f"{random.choice([6, 7, 8])}:00 PM",
            "weekend_open": f"{random.choice([10, 11])}:00 AM",
            "weekend_close": f"{random.choice([5, 6, 7])}:00 PM",
            "sunday_closed": False
        })
        
        # Generate hours dict from template
        hours = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            hours[day] = f"{template['weekday_open']} - {template['weekday_close']}"
        
        hours["Saturday"] = f"{template['weekend_open']} - {template['weekend_close']}"
        
        if template["sunday_closed"]:
            hours["Sunday"] = "Closed"
        else:
            hours["Sunday"] = f"{template['weekend_open']} - {template['weekend_close']}"
        
        return hours

    def _generate_suppliers(self, business_type: str) -> List[Dict[str, Any]]:
        """
        Generate a list of suppliers for a business type
        
        Args:
            business_type: Type of business
            
        Returns:
            List of supplier dictionaries
        """
        suppliers = []
        # Get relevant supplier types for this business
        if business_type in self.supplier_names:
            potential_suppliers = self.supplier_names[business_type]
            # Select 2-4 random suppliers
            num_suppliers = random.randint(2, 4)
            selected_suppliers = random.sample(potential_suppliers, min(num_suppliers, len(potential_suppliers)))
            
            for supplier_name in selected_suppliers:
                supplier = {
                    "name": supplier_name,
                    "type": business_type,
                    "reliability_score": round(random.uniform(0.7, 1.0), 2),
                    "years_partnership": random.randint(1, 10),
                    "payment_terms": random.choice(["Net 30", "Net 60", "COD", "Net 15"])
                }
                suppliers.append(supplier)
        
        return suppliers

    def _generate_competitors(self, business_type: str) -> List[Dict[str, Any]]:
        """
        Generate a list of competitors for a business type
        
        Args:
            business_type: Type of business
            
        Returns:
            List of competitor dictionaries
        """
        competitors = []
        # Get relevant competitors for this business type
        if business_type in self.competitor_names:
            potential_competitors = self.competitor_names[business_type]
            # Select 2-5 random competitors
            num_competitors = random.randint(2, 5)
            selected_competitors = random.sample(potential_competitors, min(num_competitors, len(potential_competitors)))
            
            for competitor_name in selected_competitors:
                competitor = {
                    "name": competitor_name,
                    "distance_miles": round(random.uniform(0.1, 5.0), 1),
                    "rating": round(random.uniform(3.0, 5.0), 1),
                    "price_level": random.choice(["$", "$$", "$$$"]),
                    "years_in_business": random.randint(1, 20)
                }
                competitors.append(competitor)
        
        return competitors