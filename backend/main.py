import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.openapi.docs import get_swagger_ui_html

# Get the project root directory (one level up from the backend directory)
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import backend modules
try:
    from backend.gemini.gemini import Gemini
    from backend.models.optimizationmodels import PortfolioOptimizationModel
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.error(traceback.format_exc())
    raise

# Initialize FastAPI app
app = FastAPI(title="Supply Chain Investment API")

# Configure CORS - Allow ALL origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS for preflight requests
    allow_headers=["*"],  # Allow all headers
)

# Define request models
class SupplyChainRequest(BaseModel):
    business_id: str

class InvestmentRequest(BaseModel):
    supply_chain: str
    investment_amount: float = 10000.0
    min_investment_score: float = 0.60
    risk_aversion: float = 2.0
    max_weight_per_stock: float = 0.3

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Supply Chain Investment API is running"}

@app.post("/generate-supply-chain/")
def generate_supply_chain(request: SupplyChainRequest):
    """Generate a supply chain analysis for a specific business"""
    logger.info(f"Received request to generate supply chain for business ID: {request.business_id}")
    
    try:
        gemini = Gemini()
        logger.info(f"Initialized Gemini model")
        
        supply_chain_text = gemini.generate_supply_chain(request.business_id)
        logger.info(f"Generated supply chain text: {supply_chain_text}")
        
        supply_chain_list = gemini.get_supply_chain()
        logger.info(f"Parsed supply chain list: {supply_chain_list}")
        
        return {
            "supply_chain_text": supply_chain_text,
            "supply_chain_list": supply_chain_list
        }
    except Exception as e:
        logger.error(f"Error generating supply chain: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-investment/")
def generate_investment(request: InvestmentRequest):
    """Generate an optimized investment portfolio based on supply chain"""
    logger.info(f"Received request to generate investment with parameters: {request}")
    
    try:
        # Initialize Gemini to get tickers for the supply chain
        gemini = Gemini()
        logger.info(f"Initialized Gemini model")
        
        ticker_dict = gemini.get_ticker_list(request.supply_chain)
        logger.info(f"Generated ticker dictionary: {ticker_dict}")
        
        # Get all tickers from the ticker dictionary
        all_tickers = [ticker for sublist in ticker_dict.values() for ticker in sublist]
        logger.info(f"Extracted tickers: {all_tickers}")
        
        if not all_tickers:
            logger.warning("No tickers found for the supply chain industries")
            return {"portfolio": [], "total_investment": 0.0}
        
        # Initialize portfolio optimization model
        portfolio_model = PortfolioOptimizationModel(
            investment_amount=request.investment_amount,
            min_investment_score=request.min_investment_score,
            risk_aversion=request.risk_aversion,
            max_weight_per_stock=request.max_weight_per_stock
        )
        logger.info(f"Initialized portfolio optimization model")
        
        # Optimize portfolio
        portfolio = portfolio_model.optimize_portfolio(all_tickers)
        logger.info(f"Optimized portfolio: {portfolio}")
        
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
        
        result = {
            "portfolio": portfolio_stocks,
            "total_investment": total_investment
        }
        logger.info(f"Returning investment result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error generating investment: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Custom documentation endpoint that works regardless of CORS
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)