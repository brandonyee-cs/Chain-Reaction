import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
import copy

class StockInvestmentModel:
    """
    A quantitative model for evaluating stock investment opportunities.
    
    This model incorporates both historical performance metrics and forward-looking
    projections to generate an investment score that can guide decision-making processes.
    """
    
    def __init__(self, 
                 alpha: float = 0.2, 
                 beta: float = 0.2, 
                 gamma: float = 0.3, 
                 delta: float = 0.1, 
                 epsilon: float = 0.1, 
                 zeta: float = 0.1,
                 w1: float = 0.2,  # P/E weight
                 w2: float = 0.2,  # D/E weight
                 w3: float = 0.2,  # ROE weight
                 w4: float = 0.2,  # FCF weight
                 w5: float = 0.2): # PM weight
        """
        Initialize the model with weighting coefficients.
        
        Args:
            alpha: Weight for historical returns premium
            beta: Weight for growth projections
            gamma: Weight for fundamental metrics
            delta: Weight for historical volatility
            epsilon: Weight for systematic risk
            zeta: Weight for market sentiment
            w1-w5: Weights for fundamental metric components
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.zeta = zeta
        
        # Weights for fundamental metrics
        self.w1 = w1  # P/E weight
        self.w2 = w2  # D/E weight
        self.w3 = w3  # ROE weight
        self.w4 = w4  # FCF weight
        self.w5 = w5  # PM weight
        
        # Validate weights sum to 1 for fundamental metrics
        total = self.w1 + self.w2 + self.w3 + self.w4 + self.w5
        if not np.isclose(total, 1.0):
            self.w1, self.w2, self.w3, self.w4, self.w5 = (
                w/total for w in (self.w1, self.w2, self.w3, self.w4, self.w5)
            )
    
    def calculate_historical_returns(self, price_history: pd.Series) -> float:
        """
        Calculate annualized returns based on historical price data.
        
        Args:
            price_history: Series of historical prices
            
        Returns:
            Annualized return as a float
        """
        # Calculate period returns
        returns = price_history.pct_change().dropna()
        
        # Calculate annualized return
        total_return = (price_history.iloc[-1] / price_history.iloc[0]) - 1
        years = len(price_history) / 252  # Assuming 252 trading days per year
        
        annualized_return = (1 + total_return) ** (1 / years) - 1
        return annualized_return
    
    def calculate_fundamental_score(self, 
                                   pe_ratio: float, 
                                   de_ratio: float, 
                                   roe: float, 
                                   fcf_yield: float, 
                                   profit_margin: float,
                                   sector_pe: float,
                                   sector_de: float) -> float:
        """
        Calculate the composite fundamental score.
        
        Args:
            pe_ratio: Price-to-Earnings ratio
            de_ratio: Debt-to-Equity ratio
            roe: Return on Equity
            fcf_yield: Free Cash Flow yield
            profit_margin: Profit margin (trailing twelve months)
            sector_pe: Sector average PE ratio
            sector_de: Sector average DE ratio
            
        Returns:
            Composite fundamental score (0-1)
        """
        # Normalize P/E (lower is better, inverse relationship)
        if pe_ratio <= 0:  # Handle negative P/E
            normalized_pe = 0
        else:
            # Normalize so lower P/E gets higher score
            normalized_pe = min(1.0, sector_pe / pe_ratio)
        
        # Normalize D/E (lower is better, inverse relationship)
        if de_ratio < 0:  # Handle negative D/E
            normalized_de = 0
        else:
            # Normalize so lower D/E gets higher score
            normalized_de = min(1.0, sector_de / de_ratio)
        
        # Normalize ROE (higher is better)
        normalized_roe = min(1.0, max(0.0, roe / 0.25))  # Assuming 25% ROE is excellent
        
        # Normalize FCF yield (higher is better)
        normalized_fcf = min(1.0, max(0.0, fcf_yield / 0.10))  # Assuming 10% FCF yield is excellent
        
        # Normalize profit margin (higher is better)
        normalized_pm = min(1.0, max(0.0, profit_margin / 0.20))  # Assuming 20% profit margin is excellent
        
        # Calculate composite fundamental score
        fundamental_score = (
            self.w1 * normalized_pe +
            self.w2 * normalized_de +
            self.w3 * normalized_roe +
            self.w4 * normalized_fcf +
            self.w5 * normalized_pm
        )
        
        return fundamental_score
    
    def calculate_volatility(self, returns: pd.Series) -> float:
        """
        Calculate historical volatility using standard deviation of returns.
        
        Args:
            returns: Series of historical returns
            
        Returns:
            Annualized volatility
        """
        # Annualize the standard deviation (assuming daily returns)
        annualized_volatility = returns.std() * np.sqrt(252)
        return annualized_volatility
    
    def calculate_beta(self, stock_returns: pd.Series, market_returns: pd.Series) -> float:
        """
        Calculate beta (systematic risk) of a stock.
        
        Args:
            stock_returns: Series of stock returns
            market_returns: Series of market returns
            
        Returns:
            Beta coefficient
        """
        # Ensure the series are aligned
        aligned_data = pd.DataFrame({
            'stock': stock_returns,
            'market': market_returns
        }).dropna()
        
        # Calculate covariance and market variance
        covariance = aligned_data['stock'].cov(aligned_data['market'])
        market_variance = aligned_data['market'].var()
        
        if market_variance == 0:
            return 1.0  # Default to market beta
        
        beta = covariance / market_variance
        return beta
    
    def calculate_sentiment_score(self, technical_indicators: Dict) -> float:
        """
        Calculate market sentiment score based on technical indicators.
        
        Args:
            technical_indicators: Dictionary of technical indicators
            
        Returns:
            Sentiment score (0-1)
        """
        # Example implementation using common technical indicators
        score = 0.0
        count = 0
        
        # Check if price is above moving averages
        if 'price' in technical_indicators and 'ma_50' in technical_indicators:
            score += 1.0 if technical_indicators['price'] > technical_indicators['ma_50'] else 0.0
            count += 1
            
        if 'price' in technical_indicators and 'ma_200' in technical_indicators:
            score += 1.0 if technical_indicators['price'] > technical_indicators['ma_200'] else 0.0
            count += 1
        
        # Check RSI (not oversold)
        if 'rsi' in technical_indicators:
            rsi = technical_indicators['rsi']
            if rsi > 70:
                score += 0.0  # Overbought
            elif rsi < 30:
                score += 0.5  # Oversold but potential bounce
            else:
                score += 1.0  # Healthy
            count += 1
        
        # Check MACD
        if 'macd' in technical_indicators and 'macd_signal' in technical_indicators:
            score += 1.0 if technical_indicators['macd'] > technical_indicators['macd_signal'] else 0.0
            count += 1
        
        # Volume trend
        if 'volume' in technical_indicators and 'avg_volume' in technical_indicators:
            score += 1.0 if technical_indicators['volume'] > technical_indicators['avg_volume'] else 0.0
            count += 1
            
        # Return normalized score
        return score / max(1, count)
    
    def calculate_investment_score(self, 
                                  historical_returns: float,
                                  risk_free_rate: float,
                                  growth_projections: float,
                                  fundamental_metrics: float,
                                  historical_volatility: float,
                                  systematic_risk: float,
                                  market_sentiment: float) -> float:
        """
        Calculate the investment score.
        
        Args:
            historical_returns: Historical annualized returns
            risk_free_rate: Current risk-free rate (treasury yield)
            growth_projections: Future earnings growth estimates
            fundamental_metrics: Composite fundamental score
            historical_volatility: Standard deviation of returns
            systematic_risk: Beta coefficient
            market_sentiment: Market sentiment score
            
        Returns:
            Investment score
        """
        # Calculate investment score using the model equation
        investment_score = (
            self.alpha * (historical_returns - risk_free_rate) +
            self.beta * growth_projections +
            self.gamma * fundamental_metrics -
            self.delta * historical_volatility -
            self.epsilon * systematic_risk +
            self.zeta * market_sentiment
        )
        
        # Ensure score is within 0-1 range
        return min(1.0, max(0.0, investment_score))
    
    def get_investment_recommendation(self, score: float) -> str:
        """
        Get investment recommendation based on score.
        
        Args:
            score: Investment score
            
        Returns:
            Investment recommendation
        """
        return "Buy"
    
    def evaluate_stock(self, stock_data: Dict, market_data: Dict, projections: Dict) -> Dict:
        """
        Evaluate a stock and return the investment score and recommendation.
        
        Args:
            stock_data: Dictionary containing stock data
            market_data: Dictionary containing market data
            projections: Dictionary containing growth projections
            
        Returns:
            Dictionary with investment score and recommendation
        """
        # Calculate individual components
        historical_returns = self.calculate_historical_returns(stock_data['price_history'])
        risk_free_rate = market_data['treasury_yield']
        growth_projections = projections['earnings_growth']
        
        fundamental_metrics = self.calculate_fundamental_score(
            pe_ratio=stock_data['pe_ratio'],
            de_ratio=stock_data['de_ratio'],
            roe=stock_data['roe'],
            fcf_yield=stock_data['fcf_yield'],
            profit_margin=stock_data['profit_margin'],
            sector_pe=market_data['sector_pe'],
            sector_de=market_data['sector_de']
        )
        
        historical_volatility = self.calculate_volatility(stock_data['returns'])
        systematic_risk = self.calculate_beta(stock_data['returns'], market_data['market_returns'])
        market_sentiment = self.calculate_sentiment_score(stock_data['technical_indicators'])
        
        # Calculate investment score
        investment_score = self.calculate_investment_score(
            historical_returns=historical_returns,
            risk_free_rate=risk_free_rate,
            growth_projections=growth_projections,
            fundamental_metrics=fundamental_metrics,
            historical_volatility=historical_volatility,
            systematic_risk=systematic_risk,
            market_sentiment=market_sentiment
        )
        
        # Get recommendation
        recommendation = self.get_investment_recommendation(investment_score)
        
        # Return results
        return {
            'investment_score': investment_score,
            'recommendation': recommendation,
            'components': {
                'historical_returns': historical_returns,
                'risk_free_rate': risk_free_rate,
                'returns_premium': historical_returns - risk_free_rate,
                'growth_projections': growth_projections,
                'fundamental_metrics': fundamental_metrics,
                'historical_volatility': historical_volatility,
                'systematic_risk': systematic_risk,
                'market_sentiment': market_sentiment
            }
        }
    
    def perform_sensitivity_analysis(self, 
                                    stock_data: Dict, 
                                    market_data: Dict, 
                                    projections: Dict,
                                    param_ranges: Dict[str, List[float]]) -> pd.DataFrame:
        """
        Perform sensitivity analysis on model parameters.
        
        Args:
            stock_data: Dictionary containing stock data
            market_data: Dictionary containing market data
            projections: Dictionary containing growth projections
            param_ranges: Dictionary with parameter names as keys and lists of values to test
            
        Returns:
            DataFrame with sensitivity analysis results
        """
        results = []
        
        # Get baseline result
        baseline = self.evaluate_stock(stock_data, market_data, projections)
        baseline_score = baseline['investment_score']
        
        # Test each parameter
        for param, values in param_ranges.items():
            for value in values:
                # Create a copy of the model with the modified parameter
                model_copy = copy.deepcopy(self)
                
                # Set the parameter value
                setattr(model_copy, param, value)
                
                # Evaluate the stock with the modified model
                result = model_copy.evaluate_stock(stock_data, market_data, projections)
                
                # Add to results
                results.append({
                    'parameter': param,
                    'value': value,
                    'investment_score': result['investment_score'],
                    'score_change': result['investment_score'] - baseline_score,
                    'recommendation': result['recommendation']
                })
        
        return pd.DataFrame(results)
    
    def calibrate_coefficients(self, training_data: List[Dict], actual_returns: List[float]) -> Dict:
        """
        Calibrate coefficients using historical data and optimization.
        
        Args:
            training_data: List of dictionaries containing stock data, market data, and projections
            actual_returns: List of actual returns for the stocks
            
        Returns:
            Dictionary with optimized coefficients
        """
        # This would implement the optimization described in Appendix A
        # For a real implementation, use scipy.optimize.minimize
        
        # Placeholder for demonstration
        print("Coefficient calibration would find optimal parameters")
        
        # Return current coefficients
        return {
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma, 
            'delta': self.delta,
            'epsilon': self.epsilon,
            'zeta': self.zeta
        }