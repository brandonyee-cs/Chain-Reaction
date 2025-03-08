import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional, Union

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))



from backend.models.rating_models import StockInvestmentModel

class PortfolioOptimizationModel:
    """
    A portfolio optimization model that evaluates stocks using the StockInvestmentModel
    and allocates investments optimally.
    """
    
    def __init__(self, 
                 investment_amount: float = 10000.0,
                 min_investment_score: float = 0.65,  # Minimum score to be considered (Buy)
                 risk_aversion: float = 2.0,
                 max_weight_per_stock: float = 0.3,
                 investment_model: Optional[StockInvestmentModel] = None):
        """
        Initialize the portfolio optimization model.
        
        Args:
            investment_amount: Total amount to invest
            min_investment_score: Minimum investment score to consider a stock (0-1)
            risk_aversion: Risk aversion parameter (higher = more risk-averse)
            max_weight_per_stock: Maximum percentage of portfolio to allocate to single stock
            investment_model: StockInvestmentModel instance (creates a default one if None)
        """
        self.investment_amount = investment_amount
        self.min_investment_score = min_investment_score
        self.risk_aversion = risk_aversion
        self.max_weight_per_stock = max_weight_per_stock
        
        # Initialize the investment model if not provided
        if investment_model is None:
            self.investment_model = StockInvestmentModel()
        else:
            self.investment_model = investment_model
    
    def fetch_stock_data(self, ticker: str, period: str = '2y') -> Dict:
        """
        Fetch stock data for a given ticker.
        
        Args:
            ticker: Stock ticker symbol
            period: Time period for historical data
            
        Returns:
            Dictionary with stock data
        """
        try:
            # Fetch data using yfinance
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data available for {ticker}")
            
            # Calculate returns
            returns = hist['Close'].pct_change().dropna()
            
            # Get financial data
            try:
                info = stock.info
                pe_ratio = info.get('trailingPE', 20.0)
                de_ratio = info.get('debtToEquity', 100.0) / 100.0  # Convert to decimal
                roe = info.get('returnOnEquity', 0.15)
                try:
                    fcf = info.get('freeCashflow', 1000000000)
                    market_cap = info.get('marketCap', 10000000000)
                    fcf_yield = fcf / market_cap
                except:
                    fcf_yield = 0.05
                profit_margin = info.get('profitMargin', 0.15)
                current_price = hist['Close'].iloc[-1]
            except:
                # Use mock data if real data not available
                pe_ratio = 20.0
                de_ratio = 1.0
                roe = 0.15
                fcf_yield = 0.05
                profit_margin = 0.15
                current_price = hist['Close'].iloc[-1]
            
            # Generate technical indicators
            close_prices = hist['Close']
            volume = hist['Volume']
            
            # Moving averages
            ma_50 = close_prices.rolling(window=50).mean().iloc[-1]
            ma_200 = close_prices.rolling(window=200).mean().iloc[-1]
            
            # RSI (simplified)
            delta = close_prices.diff()
            gain = delta.clip(lower=0).rolling(window=14).mean()
            loss = -delta.clip(upper=0).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            # MACD (simplified)
            ema_12 = close_prices.ewm(span=12, adjust=False).mean()
            ema_26 = close_prices.ewm(span=26, adjust=False).mean()
            macd = ema_12.iloc[-1] - ema_26.iloc[-1]
            macd_signal = close_prices.ewm(span=9, adjust=False).mean().iloc[-1]
            
            # Avg volume
            avg_volume = volume.rolling(window=20).mean().iloc[-1]
            
            technical_indicators = {
                'price': close_prices.iloc[-1],
                'ma_50': ma_50,
                'ma_200': ma_200,
                'rsi': rsi,
                'macd': macd,
                'macd_signal': macd_signal,
                'volume': volume.iloc[-1],
                'avg_volume': avg_volume
            }
            
            # Create stock data dictionary
            stock_data = {
                'ticker': ticker,
                'price_history': hist['Close'],
                'returns': returns,
                'pe_ratio': pe_ratio,
                'de_ratio': de_ratio,
                'roe': roe,
                'fcf_yield': fcf_yield,
                'profit_margin': profit_margin,
                'technical_indicators': technical_indicators,
                'current_price': current_price
            }
            
            return stock_data
        
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def fetch_market_data(self) -> Dict:
        """
        Fetch market data for analysis.
        
        Returns:
            Dictionary with market data
        """
        try:
            # Fetch S&P 500 data as market proxy
            market = yf.Ticker('^GSPC')
            hist = market.history(period='2y')
            
            # Calculate returns
            market_returns = hist['Close'].pct_change().dropna()
            
            # Current risk-free rate (10-year Treasury yield)
            try:
                treasury = yf.Ticker('^TNX')
                treasury_yield = treasury.history(period='1d')['Close'].iloc[-1] / 100
            except:
                treasury_yield = 0.04  # 4% as fallback
            
            # Sector average ratios
            sector_pe = 20.0
            sector_de = 1.2
            
            # Create market data dictionary
            market_data = {
                'market_returns': market_returns,
                'treasury_yield': treasury_yield,
                'sector_pe': sector_pe,
                'sector_de': sector_de
            }
            
            return market_data
        
        except Exception as e:
            print(f"Error fetching market data: {e}")
            # Fallback market data
            return {
                'market_returns': pd.Series(),
                'treasury_yield': 0.04,
                'sector_pe': 20.0,
                'sector_de': 1.2
            }
    
    def generate_projections(self, ticker: str) -> Dict:
        """
        Generate growth projections for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with growth projections
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            growth = info.get('earningsGrowth', 0.1)
        except:
            growth = 0.1  # 10% as fallback
        
        # Create projections dictionary
        projections = {
            'earnings_growth': growth
        }
        
        return projections
    
    def evaluate_tickers(self, tickers: List[str], prices: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """
        Evaluate a list of tickers using the StockInvestmentModel.
        
        Args:
            tickers: List of stock ticker symbols
            prices: Optional dictionary of ticker -> price (overrides fetched prices)
            
        Returns:
            DataFrame with evaluation results
        """
        # Fetch market data (same for all stocks)
        market_data = self.fetch_market_data()
        
        # Evaluate each stock
        results = []
        valid_tickers = []
        
        for ticker in tickers:
            # Generate stock data
            stock_data = self.fetch_stock_data(ticker)
            
            if stock_data is None:
                continue
                
            # Override price if provided
            if prices is not None and ticker in prices:
                stock_data['current_price'] = prices[ticker]
                stock_data['technical_indicators']['price'] = prices[ticker]
            
            # Generate growth projections
            projections = self.generate_projections(ticker)
            
            # Evaluate stock
            try:
                evaluation = self.investment_model.evaluate_stock(stock_data, market_data, projections)
                evaluation['ticker'] = ticker
                evaluation['current_price'] = stock_data['current_price']
                results.append(evaluation)
                valid_tickers.append(ticker)
            except Exception as e:
                print(f"Error evaluating {ticker}: {e}")
        
        # Convert to DataFrame
        if not results:
            return pd.DataFrame()
            
        df_results = pd.DataFrame(results)
        
        # Add components as columns
        for component, values in zip(df_results['components'], df_results.index):
            for key, value in component.items():
                df_results.loc[values, key] = value
        
        # Drop the components column
        df_results = df_results.drop('components', axis=1)
        
        return df_results
    
    def calculate_expected_returns(self, evaluation_results: pd.DataFrame) -> pd.Series:
        """
        Calculate expected returns based on evaluation results.
        
        Args:
            evaluation_results: DataFrame with evaluation results
            
        Returns:
            Series with expected returns for each ticker
        """
        # Use a combination of historical returns and growth projections
        expected_returns = (
            0.3 * evaluation_results['historical_returns'] + 
            0.7 * evaluation_results['growth_projections']
        )
        
        # Adjust based on investment score
        expected_returns = expected_returns * (0.5 + 0.5 * evaluation_results['investment_score'])
        
        return expected_returns
    
    def calculate_covariance_matrix(self, tickers: List[str], period: str = '2y') -> pd.DataFrame:
        """
        Calculate covariance matrix for a set of tickers.
        
        Args:
            tickers: List of stock ticker symbols
            period: Time period for historical data
            
        Returns:
            Covariance matrix
        """
        # Fetch historical data
        hist_data = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    hist_data[ticker] = hist['Close'].pct_change().dropna()
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
        
        # Create a DataFrame with returns
        if not hist_data:
            # Fallback: identity matrix with some correlation
            n = len(tickers)
            cov = np.eye(n) * 0.04  # 20% vol
            for i in range(n):
                for j in range(i+1, n):
                    cov[i, j] = cov[j, i] = 0.02  # 0.5 correlation
            return pd.DataFrame(cov, index=tickers, columns=tickers)
            
        returns_df = pd.DataFrame(hist_data)
        
        # If missing tickers, create identity matrix for them
        missing = [t for t in tickers if t not in returns_df.columns]
        if missing:
            for t in missing:
                returns_df[t] = 0.0
        
        # Calculate annualized covariance matrix (252 trading days)
        cov_matrix = returns_df.cov() * 252
        
        return cov_matrix
    
    def optimize_portfolio(self, tickers: List[str], prices: Optional[Dict[str, float]] = None) -> List[List]:
        """
        Optimize portfolio allocation for a list of tickers.
        
        Args:
            tickers: List of stock ticker symbols
            prices: Optional dictionary of ticker -> price (overrides fetched prices)
            
        Returns:
            List of lists with [Ticker, Price, Amount Invested]
        """
        # Evaluate tickers
        evaluation_results = self.evaluate_tickers(tickers, prices)
        
        if evaluation_results.empty:
            return []
        
        # Filter stocks based on investment score
        filtered_results = evaluation_results[
            evaluation_results['investment_score'] >= self.min_investment_score
        ]
        
        if filtered_results.empty:
            # If no stocks meet the minimum score, take the top 3
            filtered_results = evaluation_results.nlargest(
                min(3, len(evaluation_results)), 'investment_score'
            )
        
        filtered_tickers = filtered_results['ticker'].tolist()
        
        # Calculate expected returns
        expected_returns = self.calculate_expected_returns(filtered_results)
        
        # Calculate covariance matrix
        cov_matrix = self.calculate_covariance_matrix(filtered_tickers)
        
        # Ensure all tickers are in the covariance matrix
        for ticker in filtered_tickers:
            if ticker not in cov_matrix.index:
                # Add placeholder row/column
                cov_matrix[ticker] = 0.04  # Default volatility
                cov_matrix.loc[ticker] = 0.04
                cov_matrix.loc[ticker, ticker] = 0.04
        
        # Keep only the relevant tickers in the covariance matrix
        cov_matrix = cov_matrix.loc[filtered_tickers, filtered_tickers]
        
        # Define objective function (mean-variance utility)
        def objective(weights):
            portfolio_return = np.sum(expected_returns * weights)
            portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            utility = portfolio_return - 0.5 * self.risk_aversion * portfolio_vol**2
            return -utility  # Minimize negative utility
        
        # Define constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0}  # Sum of weights = 1
        ]
        
        # Define bounds
        bounds = [(0.0, self.max_weight_per_stock) for _ in range(len(filtered_tickers))]
        
        # Initial guess (equal weights)
        initial_weights = np.array([1.0 / len(filtered_tickers)] * len(filtered_tickers))
        
        # Optimize
        result = minimize(
            objective, 
            initial_weights, 
            method='SLSQP', 
            bounds=bounds, 
            constraints=constraints
        )
        
        # Extract optimal weights
        optimal_weights = result['x']
        
        # Calculate amount to invest in each stock
        investments = optimal_weights * self.investment_amount
        
        # Create output in the required format
        prices_dict = dict(zip(filtered_results['ticker'], filtered_results['current_price']))
        portfolio = []
        
        for ticker, weight, investment in zip(filtered_tickers, optimal_weights, investments):
            if investment > 0:
                portfolio.append([ticker, prices_dict[ticker], investment])
        
        # Sort by investment amount (descending)
        portfolio.sort(key=lambda x: x[2], reverse=True)
        
        return portfolio
    
    def optimize_with_given_prices(self, tickers_and_prices: Dict[str, float]) -> List[List]:
        """
        Optimize portfolio with provided tickers and prices.
        
        Args:
            tickers_and_prices: Dictionary mapping tickers to their current prices
            
        Returns:
            List of lists with [Ticker, Price, Amount Invested]
        """
        tickers = list(tickers_and_prices.keys())
        return self.optimize_portfolio(tickers, tickers_and_prices)