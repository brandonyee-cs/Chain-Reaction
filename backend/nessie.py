import requests
import json
import os
import datetime

class NessieIntegration:
    def __init__(self, api_key=None):
        """Initialize the Nessie Integration with optional API key"""
        self.api_key = api_key or os.environ.get('NESSIE_API_KEY')
        self.base_url = "http://api.reimaginebanking.com"
        self.merchants_db_file = "merchants.json"
        self.user_purchases_file = "user_purchases.json"
        self.supply_chain_file = "supply_chain.json"
        
        # Initialize JSON databases if they don't exist
        self._initialize_db_files()
    
    def _initialize_db_files(self):
        """Initialize the JSON database files if they don't exist"""
        for file_path, default_content in [
            (self.merchants_db_file, {"merchants": []}),
            (self.user_purchases_file, {}),
            (self.supply_chain_file, {})
        ]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_content, f)
    
    def _load_json(self, file_path):
        """Load JSON data from a file"""
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    
    def _save_json(self, file_path, data):
        """Save JSON data to a file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_customer(self, first_name, last_name, street_number, street_name, city, state, zipcode):
        """Create a customer using the Nessie API endpoints directly"""
        url = f"{self.base_url}/customers?key={self.api_key}"
        
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "address": {
                "street_number": street_number,
                "street_name": street_name,
                "city": city,
                "state": state,
                "zip": zipcode
            }
        }
        
        response = requests.post(
            url, 
            data=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )
        
        if response.status_code == 201:
            customer_id = response.json()['objectCreated']['_id']
            print(f"Customer created with ID: {customer_id}")
            return customer_id
        else:
            print(f"Failed to create customer: {response.text}")
            return None
    
    def create_account(self, customer_id, account_type, nickname, balance):
        """Create an account for a customer using the Nessie API endpoints directly"""
        url = f"{self.base_url}/customers/{customer_id}/accounts?key={self.api_key}"
        
        payload = {
            "type": account_type,
            "nickname": nickname,
            "rewards": 0,
            "balance": balance
        }
        
        response = requests.post(
            url, 
            data=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )
        
        if response.status_code == 201:
            account_id = response.json()['objectCreated']['_id']
            print(f"Account created with ID: {account_id}")
            return account_id
        else:
            print(f"Failed to create account: {response.text}")
            return None
    
    def create_merchant(self, name, category, location=None):
        """Create a merchant and save to the merchant database"""
        merchants = self._load_json(self.merchants_db_file)
        
        merchant_id = f"m_{len(merchants['merchants']) + 1:03d}"
        
        merchant = {
            "merchant_id": merchant_id,
            "name": name,
            "category": category
        }
        
        if location:
            merchant["location"] = location
            
        merchants["merchants"].append(merchant)
        self._save_json(self.merchants_db_file, merchants)
        
        return merchant_id
    
    def get_merchant_by_id(self, merchant_id):
        """Get a merchant by ID"""
        merchants = self._load_json(self.merchants_db_file)
            
        for merchant in merchants["merchants"]:
            if merchant.get("merchant_id") == merchant_id:
                return merchant
                
        return None
    
    def make_purchase(self, customer_id, account_id, merchant_id, amount, description=None):
        """Record a purchase from a customer to a merchant using Nessie API"""
        url = f"{self.base_url}/accounts/{account_id}/purchases?key={self.api_key}"
        
        payload = {
            "merchant_id": merchant_id,
            "medium": "balance",
            "purchase_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "amount": amount,
            "status": "pending"
        }
        
        if description:
            payload["description"] = description
        
        response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )
        
        if response.status_code == 201:
            purchase_id = response.json()['objectCreated']['_id']
            print(f"Purchase created with ID: {purchase_id}")
            
            # Also record in our local database
            timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            purchase = {
                "purchase_id": purchase_id,
                "merchant_id": merchant_id,
                "amount": amount,
                "timestamp": timestamp
            }
            
            if description:
                purchase["description"] = description
            
            user_purchases = self._load_json(self.user_purchases_file)
            
            if customer_id not in user_purchases:
                user_purchases[customer_id] = {
                    "username": f"user_{customer_id[-5:]}",
                    "account": {
                        "id": account_id,
                        "balance": 0,
                        "purchases": []
                    }
                }
            
            user_purchases[customer_id]["account"]["purchases"].append(purchase)
            self._save_json(self.user_purchases_file, user_purchases)
            
            return purchase
        else:
            print(f"Failed to create purchase: {response.text}")
            return None
    
    def get_merchant_ids(self, user):
        """
        Return a hashmap which maps the user -> merchant ids with amounts spent.
        """
        user_purchases = self._load_json(self.user_purchases_file)
        
        if user not in user_purchases or "account" not in user_purchases[user]:
            return {}
        
        purchases = user_purchases[user]["account"]["purchases"]
        
        merchant_amounts = {}
        for purchase in purchases:
            merchant_id = purchase.get("merchant_id")
            amount = purchase.get("amount", 0)
            
            if merchant_id in merchant_amounts:
                merchant_amounts[merchant_id] += amount
            else:
                merchant_amounts[merchant_id] = amount
        
        return merchant_amounts
    
    def get_sorted_merchants_by_amount(self, user):
        """
        Sort user's merchants in descending order by amount spent.
        """
        merchant_amounts = self.get_merchant_ids(user)
        
        sorted_merchants = sorted(
            merchant_amounts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return sorted_merchants
    
    def add_supply_chain(self, business_id, supply_chain_components):
        """
        Add supply chain components for a business.
        mp[merchant.id] = [s1, s2, s3, ...]
        """
        supply_chains = self._load_json(self.supply_chain_file)
        supply_chains[business_id] = supply_chain_components
        self._save_json(self.supply_chain_file, supply_chains)
    
    def get_supply_chain(self, business_id):
        """Get supply chain components for a business"""
        supply_chains = self._load_json(self.supply_chain_file)
        return supply_chains.get(business_id, [])
    
    def get_investment_opportunities(self, user):
        """
        Generate investment opportunities based on user's purchase history.
        Returns business supply chains in order of priority based on spending.
        """
        sorted_merchants = self.get_sorted_merchants_by_amount(user)
        
        investment_opportunities = []
        
        for merchant_id, amount in sorted_merchants:
            merchant = self.get_merchant_by_id(merchant_id)
            supply_chain = self.get_supply_chain(merchant_id)
            
            if merchant and supply_chain:
                opportunity = {
                    "business": merchant["name"],
                    "merchant_id": merchant_id,
                    "amount_spent": amount,
                    "supply_chain": supply_chain
                }
                investment_opportunities.append(opportunity)
        
        return investment_opportunities
    
    def add_investment(self, user, investment_details):
        """
        Add an investment to the user's portfolio.
        """
        user_purchases = self._load_json(self.user_purchases_file)
        
        if user not in user_purchases:
            return False
        
        if "investments" not in user_purchases[user]:
            user_purchases[user]["investments"] = []
        
        investment_details["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        user_purchases[user]["investments"].append(investment_details)
        self._save_json(self.user_purchases_file, user_purchases)
        
        return True


# Example usage
def main():
    # Replace with your actual API key
    api_key = "your_api_key_here"
    integration = NessieIntegration(api_key)
    
    # Create a customer
    customer_id = integration.create_customer(
        "Jane", "Doe", "456", "Oak St", "Sometown", "CA", "54321"
    )
    
    if not customer_id:
        print("Failed to create customer. Exiting.")
        return
    
    # Create an account
    account_id = integration.create_account(
        customer_id, "Savings", "Main Account", 5000
    )
    
    if not account_id:
        print("Failed to create account. Exiting.")
        return
    
    # Create merchants
    restaurant = integration.create_merchant("Local Restaurant", "Food")
    bookstore = integration.create_merchant("Book Haven", "Retail")
    electronics = integration.create_merchant("Tech Galaxy", "Electronics")
    
    # Define supply chains
    integration.add_supply_chain(restaurant, [
        "local-farms",
        "food-distributors",
        "equipment-suppliers",
        "kitchen-tools-manufacturers"
    ])
    
    integration.add_supply_chain(bookstore, [
        "publishers",
        "paper-mills",
        "printing-services",
        "logistics-companies"
    ])
    
    integration.add_supply_chain(electronics, [
        "chip-manufacturers",
        "display-makers",
        "battery-suppliers",
        "assembly-plants"
    ])
    
    # Make purchases
    integration.make_purchase(customer_id, account_id, restaurant, 75, "Dinner")
    integration.make_purchase(customer_id, account_id, bookstore, 45, "Books")
    integration.make_purchase(customer_id, account_id, electronics, 650, "New Phone")
    integration.make_purchase(customer_id, account_id, restaurant, 85, "Family Dinner")
    integration.make_purchase(customer_id, account_id, electronics, 200, "Headphones")
    
    # Get merchant spending
    merchant_amounts = integration.get_merchant_ids(customer_id)
    print("\nMerchant spending:")
    for merchant_id, amount in merchant_amounts.items():
        merchant = integration.get_merchant_by_id(merchant_id)
        print(f"{merchant['name']}: ${amount}")
    
    # Get sorted merchants
    sorted_merchants = integration.get_sorted_merchants_by_amount(customer_id)
    print("\nMerchants sorted by spending:")
    for merchant_id, amount in sorted_merchants:
        merchant = integration.get_merchant_by_id(merchant_id)
        print(f"{merchant['name']}: ${amount}")
    
    # Get investment opportunities
    opportunities = integration.get_investment_opportunities(customer_id)
    print("\nInvestment opportunities:")
    for opportunity in opportunities:
        print(f"Business: {opportunity['business']}")
        print(f"Amount spent: ${opportunity['amount_spent']}")
        print(f"Supply chain components:")
        for component in opportunity['supply_chain']:
            print(f"  - {component}")
        print("-" * 40)
    
    # Make an investment
    if opportunities:
        top_opportunity = opportunities[0]
        investment = {
            "merchant_id": top_opportunity["merchant_id"],
            "supply_chain_component": top_opportunity["supply_chain"][0],
            "amount": 1000
        }
        
        integration.add_investment(customer_id, investment)
        print(f"\nInvested $1000 in {investment['supply_chain_component']} from {top_opportunity['business']}'s supply chain.")

if __name__ == "__main__":
    main()