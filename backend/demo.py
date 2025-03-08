from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nessie.client import Client
from nessie.models.address import Address as NessieAddress
from typing import List, Optional
import json
import os
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set
import heapq

app = FastAPI()
client = Client()  # Uses API key from .env

# Models
class Address(BaseModel):
    street_number: str
    street_name: str
    city: str
    state: str
    zip: str

class Location(BaseModel):
    lat: float
    lng: float

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    address: Address

class AccountCreate(BaseModel):
    type: str
    nickname: str
    balance: float
    rewards: int = 0

class MerchantCreate(BaseModel):
    name: str
    category: str
    address: Address
    location: Location

class Purchase(BaseModel):
    merchant_id: str
    amount: float
    timestamp: datetime

class MerchantRelation(BaseModel):
    merchant_id: str
    connected_merchants: List[str]
    relationship_string: str

# Add this to the models section
class InvestmentCreate(BaseModel):
    investment_id: str
    amount: float
    type: str
    description: Optional[str]

# Database paths
DB_PATH = os.path.join(os.path.dirname(__file__), "datastore")
os.makedirs(DB_PATH, exist_ok=True)

CUSTOMERS_FILE = os.path.join(DB_PATH, "customers.json")
MERCHANTS_FILE = os.path.join(DB_PATH, "merchants.json")
ACCOUNTS_FILE = os.path.join(DB_PATH, "accounts.json")

# Helper functions
def load_db(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_db(file_path: str, data: dict):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def update_user_investments(user_id: str, investment_id: str) -> bool:
    """Add investment to user's portfolio"""
    users = load_db("users.json")
    if user_id not in users:
        return False
    
    # Initialize investments array if it doesn't exist
    if "investments" not in users[user_id]:
        users[user_id]["investments"] = []
    
    users[user_id]["investments"].append(investment_id)
    save_db("users.json", users)
    return True

# API Routes
@app.post("/customers/")
async def create_customer(customer: CustomerCreate):
    """Create a new customer in both Nessie and local storage"""
    try:
        # Create in Nessie
        nessie_address = NessieAddress(
            street_number=customer.address.street_number,
            street_name=customer.address.street_name,
            city=customer.address.city,
            state=customer.address.state,
            zip=customer.address.zip
        )
        
        nessie_customer = client.customer.create_customer(
            customer.first_name,
            customer.last_name,
            nessie_address
        )
        
        # Save to local storage
        customers = load_db(CUSTOMERS_FILE)
        customers[nessie_customer.customer_id] = {
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "address": customer.address.dict(),
            "accounts": []
        }
        save_db(CUSTOMERS_FILE, customers)
        
        return {"customer_id": nessie_customer.customer_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/customers/{customer_id}/accounts")
async def create_account(customer_id: str, account: AccountCreate):
    """Create a new account for a customer"""
    try:
        # Create in Nessie
        nessie_account = client.account.create_account(
            customer_id,
            {
                "type": account.type,
                "nickname": account.nickname,
                "rewards": account.rewards,
                "balance": account.balance
            }
        )
        
        # Save to local storage
        accounts = load_db(ACCOUNTS_FILE)
        accounts[nessie_account.account_id] = {
            "customer_id": customer_id,
            "type": account.type,
            "nickname": account.nickname,
            "balance": account.balance,
            "rewards": account.rewards,
            "transactions": []
        }
        save_db(ACCOUNTS_FILE, accounts)
        
        # Update customer's accounts list
        customers = load_db(CUSTOMERS_FILE)
        if customer_id in customers:
            customers[customer_id]["accounts"].append(nessie_account.account_id)
            save_db(CUSTOMERS_FILE, customers)
        
        return {"account_id": nessie_account.account_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/merchants/")
async def create_merchant(merchant: MerchantCreate):
    """Create a new merchant in local storage"""
    merchant_id = f"m_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    merchants = load_db(MERCHANTS_FILE)
    merchants[merchant_id] = merchant.dict()
    save_db(MERCHANTS_FILE, merchants)
    return {"merchant_id": merchant_id}

@app.get("/merchants/nearby/")
async def get_nearby_merchants(lat: float, lng: float, radius: float = 5.0):
    """Find merchants within specified radius (in km)"""
    merchants = load_db(MERCHANTS_FILE)
    nearby = []
    
    for id, merchant in merchants.items():
        dlat = merchant["location"]["lat"] - lat
        dlng = merchant["location"]["lng"] - lng
        if (dlat**2 + dlng**2)**0.5 <= radius:
            merchant["id"] = id
            nearby.append(merchant)
    
    return nearby

@app.get("/customers/{customer_id}/purchase-history")
async def get_purchase_history(customer_id: str):
    """Get customer's purchase history with merchant relationships"""
    try:
        users = load_db("users.json")
        merchants = load_db("merchants.json")
        
        if customer_id not in users:
            raise HTTPException(status_code=404, detail="Customer not found")
            
        # Build merchant spending map
        merchant_spending = defaultdict(float)
        user_purchases = users[customer_id]["account"].get("purchases", [])
        
        for purchase in user_purchases:
            merchant_id = purchase["merchant_id"]
            merchant_spending[merchant_id] += purchase["amount"]
        
        # Sort merchants by spending (descending)
        sorted_merchants = sorted(
            [(mid, amount) for mid, amount in merchant_spending.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Build merchant details with spending
        merchant_details = []
        for mid, amount in sorted_merchants:
            if mid in merchants:
                merchant_info = merchants[mid].copy()
                merchant_info["total_spent"] = amount
                merchant_info["merchant_id"] = mid
                merchant_details.append(merchant_info)
        
        return {
            "customer_id": customer_id,
            "total_merchants": len(merchant_details),
            "merchants": merchant_details
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_merchant_connections(connection_string: str) -> Dict[str, Set[str]]:
    """Parse merchant connection string (head connected connected)"""
    if not connection_string:
        return {}
        
    parts = connection_string.split(" ")
    connections = defaultdict(set)
    
    head = parts[0].strip()
    connected = [m.strip() for m in parts[1:]]
    
    # Build connection graph
    for i, merchant in enumerate(connected):
        if i == 0:
            connections[head].add(merchant)
        else:
            connections[connected[i-1]].add(merchant)
    
    return dict(connections)

@app.post("/merchants/connections")
async def create_merchant_connections(relation: MerchantRelation):
    """Create connections between merchants"""
    try:
        merchants = load_db(MERCHANTS_FILE)
        
        # Validate merchant exists
        if relation.merchant_id not in merchants:
            raise HTTPException(status_code=404, detail="Main merchant not found")
            
        # Parse connections
        connections = parse_merchant_connections(relation.relationship_string)
        
        # Update merchant with connections
        merchants[relation.merchant_id]["connected_merchants"] = list(
            connections.get(relation.merchant_id, [])
        )
        
        # Update connected merchants
        for merchant_id, connected_to in connections.items():
            if merchant_id in merchants:
                merchants[merchant_id]["connected_merchants"] = list(connected_to)
        
        save_db(MERCHANTS_FILE, merchants)
        return {"message": "Merchant connections updated"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/merchants/{merchant_id}/connected")
async def get_connected_merchants(merchant_id: str, depth: int = 1):
    """Get merchants connected to given merchant up to specified depth"""
    try:
        merchants = load_db(MERCHANTS_FILE)
        if merchant_id not in merchants:
            raise HTTPException(status_code=404, detail="Merchant not found")
            
        connected = set()
        to_visit = [(merchant_id, 0)]
        visited = set()
        
        while to_visit:
            current_id, current_depth = to_visit.pop(0)
            
            if current_id in visited or current_depth > depth:
                continue
                
            visited.add(current_id)
            if current_id != merchant_id:
                connected.add(current_id)
                
            if current_depth < depth:
                merchant = merchants.get(current_id, {})
                for connected_id in merchant.get("connected_merchants", []):
                    if connected_id not in visited:
                        to_visit.append((connected_id, current_depth + 1))
        
        connected_merchants = [
            {**merchants[mid], "merchant_id": mid}
            for mid in connected
            if mid in merchants
        ]
        
        return {
            "merchant_id": merchant_id,
            "depth": depth,
            "connected_count": len(connected_merchants),
            "connected_merchants": connected_merchants
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Add this new endpoint
@app.post("/customers/{customer_id}/investments")
async def add_investment(customer_id: str, investment: InvestmentCreate):
    """Add investment to customer's portfolio"""
    try:
        # Validate customer exists
        customers = load_db(CUSTOMERS_FILE)
        if customer_id not in customers:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Add investment to customer's portfolio
        success = update_user_investments(customer_id, investment.investment_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update investments")
        
        # Store investment details in accounts file
        accounts = load_db(ACCOUNTS_FILE)
        account_id = customers[customer_id]["accounts"][0]  # Assuming first account
        
        if "investments" not in accounts[account_id]:
            accounts[account_id]["investments"] = {}
        accounts[account_id]["investments"][investment.investment_id] = {
            "amount": investment.amount,
            "type": investment.type,
            "description": investment.description,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        save_db(ACCOUNTS_FILE, accounts)
        
        return {
            "message": "Investment added successfully",
            "investment_id": investment.investment_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Add this endpoint to get investments
@app.get("/customers/{customer_id}/investments")
async def get_investments(customer_id: str):
    """Get all investments for a customer"""
    try:
        customers = load_db(CUSTOMERS_FILE)
        accounts = load_db(ACCOUNTS_FILE)
        
        if customer_id not in customers:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        account_id = customers[customer_id]["accounts"][0]  # Assuming first account
        account = accounts.get(account_id, {})
        investments = account.get("investments", {})
        
        return {
            "customer_id": customer_id,
            "investment_count": len(investments),
            "investments": investments
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))