import os
import sys
from pathlib import Path

# Get the project root directory (one level up from the backend directory)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import backend modules
from backend.gemini.gemini import Gemini
from backend.models.optimizationmodels import PortfolioOptimizationModel
from backend.nessie import NessieIntegration

# Initialize FastAPI app
app = FastAPI(title="Supply Chain Investment API")

# Initialize Nessie Integration
nessie = NessieIntegration()

@app.post("/generate-supply-chain/")
def generate_supply_chain(business_id: str):
    """Generate a supply chain analysis for a specific business"""
    try:
        gemini = Gemini()
        supply_chain_text = gemini.generate_supply_chain(business_id)
        supply_chain_list = gemini.get_supply_chain()
        
        return {
            "supply_chain_text": supply_chain_text,
            "supply_chain_list": supply_chain_list
        }
    except Exception as e:
        logger.error(f"Error generating supply chain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-investment/")
def generate_investment(
    supply_chain: str,
    investment_amount: float = 10000.0,
    min_investment_score: float = 0.60,
    risk_aversion: float = 2.0,
    max_weight_per_stock: float = 0.3
):
    """Generate an optimized investment portfolio based on supply chain"""
    try:
        # Initialize Gemini to get tickers for the supply chain
        gemini = Gemini()
        ticker_dict = gemini.get_ticker_list(supply_chain)
        
        # Get all tickers from the ticker dictionary
        all_tickers = [ticker for sublist in ticker_dict.values() for ticker in sublist]
        
        if not all_tickers:
            logger.warning("No tickers found for the supply chain industries")
            return {"portfolio": [], "total_investment": 0.0}
        
        # Initialize portfolio optimization model
        portfolio_model = PortfolioOptimizationModel(
            investment_amount=investment_amount,
            min_investment_score=min_investment_score,
            risk_aversion=risk_aversion,
            max_weight_per_stock=max_weight_per_stock
        )
        
        # Optimize portfolio
        portfolio = portfolio_model.optimize_portfolio(all_tickers)
        
        # Transform portfolio data
        portfolio_stocks = []
        total_investment = 0.0
        
        for ticker, price, investment in portfolio:
            portfolio_stocks.append({
                "ticker": ticker,
                "price": price,
                "investment": investment
            })
            total_investment += investment
        
        return {
            "portfolio": portfolio_stocks,
            "total_investment": total_investment
        }
    except Exception as e:
        logger.error(f"Error generating investment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Nessie Integration Endpoints

@app.post("/customer/create")
def create_customer(
    first_name: str,
    last_name: str,
    street_number: str,
    street_name: str,
    city: str,
    state: str,
    zipcode: str
):
    """Create a customer"""
    try:
        customer_id = nessie.create_customer(
            first_name, last_name, street_number, street_name, city, state, zipcode
        )
        return {"customer_id": customer_id}
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/account/create")
def create_account(
    customer_id: str,
    account_type: str,
    nickname: str,
    balance: float
):
    """Create an account for a customer"""
    try:
        account_id = nessie.create_account(customer_id, account_type, nickname, balance)
        return {"account_id": account_id}
    except Exception as e:
        logger.error(f"Error creating account: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/merchant/create")
def create_merchant(
    name: str,
    category: str,
    location: Optional[Dict] = None
):
    """Create a merchant"""
    try:
        merchant_id = nessie.create_merchant(name, category, location)
        return {"merchant_id": merchant_id}
    except Exception as e:
        logger.error(f"Error creating merchant: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/merchant/{merchant_id}")
def get_merchant(merchant_id: str):
    """Get a merchant by ID"""
    try:
        merchant = nessie.get_merchant_by_id(merchant_id)
        if merchant:
            return merchant
        else:
            raise HTTPException(status_code=404, detail="Merchant not found")
    except Exception as e:
        logger.error(f"Error getting merchant: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/purchase/create")
def make_purchase(
    customer_id: str,
    account_id: str,
    merchant_id: str,
    amount: float,
    description: Optional[str] = None
):
    """Record a purchase"""
    try:
        purchase = nessie.make_purchase(customer_id, account_id, merchant_id, amount, description)
        return purchase
    except Exception as e:
        logger.error(f"Error making purchase: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/merchants/{user}")
def get_merchant_ids(user: str):
    """Get merchant IDs with amounts spent by a user"""
    try:
        merchant_amounts = nessie.get_merchant_ids(user)
        return merchant_amounts
    except Exception as e:
        logger.error(f"Error getting merchant IDs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/merchants/sorted/{user}")
def get_sorted_merchants(user: str):
    """Get merchants sorted by amount spent by a user"""
    try:
        sorted_merchants = nessie.get_sorted_merchants_by_amount(user)
        return {merchant_id: amount for merchant_id, amount in sorted_merchants}
    except Exception as e:
        logger.error(f"Error getting sorted merchants: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/supply-chain/add")
def add_supply_chain(
    business_id: str,
    supply_chain_components: List[str]
):
    """Add supply chain components for a business"""
    try:
        nessie.add_supply_chain(business_id, supply_chain_components)
        return {"status": "success", "business_id": business_id}
    except Exception as e:
        logger.error(f"Error adding supply chain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supply-chain/{business_id}")
def get_supply_chain_by_id(business_id: str):
    """Get supply chain components for a business"""
    try:
        supply_chain = nessie.get_supply_chain(business_id)
        return {"business_id": business_id, "supply_chain": supply_chain}
    except Exception as e:
        logger.error(f"Error getting supply chain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/investment/opportunities/{user}")
def get_investment_opportunities(user: str):
    """Get investment opportunities based on user's purchase history"""
    try:
        opportunities = nessie.get_investment_opportunities(user)
        return {"opportunities": opportunities}
    except Exception as e:
        logger.error(f"Error getting investment opportunities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/investment/add")
def add_investment(
    user: str,
    merchant_id: str,
    supply_chain_component: str,
    amount: float,
    additional_details: Optional[Dict] = None
):
    """Add an investment to the user's portfolio"""
    try:
        investment_details = {
            "merchant_id": merchant_id,
            "supply_chain_component": supply_chain_component,
            "amount": amount
        }
        
        if additional_details:
            investment_details.update(additional_details)
        
        success = nessie.add_investment(user, investment_details)
        
        if success:
            return {"status": "success", "user": user, "investment": investment_details}
        else:
            raise HTTPException(status_code=404, detail=f"User {user} not found")
    except Exception as e:
        logger.error(f"Error adding investment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)