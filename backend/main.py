import os
import sys
from pathlib import Path

# Get the project root directory (one level up from the backend directory)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import backend modules
from backend.gemini.gemini import Gemini
from backend.models.optimizationmodels import PortfolioOptimizationModel

# Initialize FastAPI app
app = FastAPI(title="Supply Chain Investment API")

# ------ Pydantic Models ------

class BusinessRequest(BaseModel):
    business_id: str

class SupplyChainResponse(BaseModel):
    supply_chain_text: str
    supply_chain_list: List[str]

class InvestmentRequest(BaseModel):
    supply_chain: str
    investment_amount: float = 10000.0
    min_investment_score: float = 0.60
    risk_aversion: float = 2.0
    max_weight_per_stock: float = 0.3

class InvestmentStock(BaseModel):
    ticker: str
    price: float
    investment: float

class InvestmentResponse(BaseModel):
    portfolio: List[InvestmentStock]
    total_investment: float

# ------ API Endpoints ------

@app.post("/generate-supply-chain/", response_model=SupplyChainResponse)
def generate_supply_chain(request: BusinessRequest):
    """Generate a supply chain analysis for a specific business"""
    try:
        gemini = Gemini()
        supply_chain_text = gemini.generate_supply_chain(request.business_id)
        supply_chain_list = gemini.get_supply_chain()
        
        return SupplyChainResponse(
            supply_chain_text=supply_chain_text,
            supply_chain_list=supply_chain_list
        )
    except Exception as e:
        logger.error(f"Error generating supply chain: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-investment/", response_model=InvestmentResponse)
def generate_investment(request: InvestmentRequest):
    """Generate an optimized investment portfolio based on supply chain"""
    try:
        # Initialize Gemini to get tickers for the supply chain
        gemini = Gemini()
        ticker_dict = gemini.get_ticker_list(request.supply_chain)
        
        # Get all tickers from the ticker dictionary
        all_tickers = [ticker for sublist in ticker_dict.values() for ticker in sublist]
        
        if not all_tickers:
            logger.warning("No tickers found for the supply chain industries")
            return InvestmentResponse(portfolio=[], total_investment=0.0)
        
        # Initialize portfolio optimization model
        portfolio_model = PortfolioOptimizationModel(
            investment_amount=request.investment_amount,
            min_investment_score=request.min_investment_score,
            risk_aversion=request.risk_aversion,
            max_weight_per_stock=request.max_weight_per_stock
        )
        
        # Optimize portfolio
        portfolio = portfolio_model.optimize_portfolio(all_tickers)
        
        # Transform portfolio data
        portfolio_stocks = []
        total_investment = 0.0
        
        for ticker, price, investment in portfolio:
            portfolio_stocks.append(
                InvestmentStock(
                    ticker=ticker,
                    price=price,
                    investment=investment
                )
            )
            total_investment += investment
        
        return InvestmentResponse(
            portfolio=portfolio_stocks,
            total_investment=total_investment
        )
    except Exception as e:
        logger.error(f"Error generating investment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)