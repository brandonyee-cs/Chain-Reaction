import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Literal
import copy
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RiskProfile(Enum):
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"

class RatingModel:
    """
    An enhanced quantitative model for evaluating stock investment opportunities with risk profiles.
    
    This model incorporates both historical performance metrics and forward-looking
    projections to generate an investment score that can guide decision-making processes.
    It supports three risk profiles: low risk, medium risk, and high risk.
    
    Features:
    - Three predefined risk profiles with optimized parameter weightings
    - Detailed component-level analysis for each evaluation factor
    - Sensitivity analysis to identify key drivers of investment ratings
    - Detailed recommendations with confidence levels and risk notes
    - Performance monitoring and coefficient calibration functionality
    """
    """
    An enhanced quantitative model for evaluating stock investment opportunities with risk profiles.
    
    This model incorporates both historical performance metrics and forward-looking
    projections to generate an investment score that can guide decision-making processes.
    It supports three risk profiles: low risk, medium risk, and high risk.
    """
    
    # Risk profile model parameters
    RISK_PROFILES = {
        RiskProfile.LOW_RISK: {
            'alpha': 0.10,  # Lower weight on historical returns premium
            'beta': 0.10,   # Lower weight on growth projections
            'gamma': 0.40,  # Higher weight on fundamental metrics
            'delta': 0.20,  # Higher weight on historical volatility (more penalty)
            'epsilon': 0.15, # Higher weight on systematic risk (more penalty)
            'zeta': 0.05,   # Lower weight on market sentiment
            # Fundamental metric weights for low risk
            'w1': 0.25,     # Higher P/E weight (value focus)
            'w2': 0.30,     # Higher D/E weight (debt aversion)
            'w3': 0.15,     # Moderate ROE weight
            'w4': 0.20,     # Higher FCF weight (cash flow stability)
            'w5': 0.10,     # Lower profit margin weight
        },
        RiskProfile.MEDIUM_RISK: {
            'alpha': 0.20,  # Moderate weight on historical returns premium
            'beta': 0.20,   # Moderate weight on growth projections
            'gamma': 0.30,  # Moderate weight on fundamental metrics
            'delta': 0.10,  # Moderate weight on historical volatility
            'epsilon': 0.10, # Moderate weight on systematic risk
            'zeta': 0.10,   # Moderate weight on market sentiment 
            # Fundamental metric weights for medium risk
            'w1': 0.20,     # Moderate P/E weight
            'w2': 0.20,     # Moderate D/E weight
            'w3': 0.20,     # Moderate ROE weight
            'w4': 0.20,     # Moderate FCF weight
            'w5': 0.20,     # Moderate profit margin weight
        },
        RiskProfile.HIGH_RISK: {
            'alpha': 0.30,  # Higher weight on historical returns premium
            'beta': 0.30,   # Higher weight on growth projections
            'gamma': 0.20,  # Lower weight on fundamental metrics
            'delta': 0.05,  # Lower weight on historical volatility (less penalty)
            'epsilon': 0.05, # Lower weight on systematic risk (less penalty)
            'zeta': 0.10,   # Higher weight on market sentiment
            # Fundamental metric weights for high risk
            'w1': 0.10,     # Lower P/E weight (growth focus)
            'w2': 0.10,     # Lower D/E weight (more tolerance for debt)
            'w3': 0.30,     # Higher ROE weight (performance focus)
            'w4': 0.15,     # Lower FCF weight
            'w5': 0.35,     # Higher profit margin weight (profitability focus)
        }
    }
        
    @classmethod
    def get_model_for_risk_profile(cls, risk_profile: RiskProfile) -> 'RatingModel':
        """
        Factory method to create a RatingModel with the specified risk profile.
        
        Args:
            risk_profile: Low, medium, or high risk profile
            
        Returns:
            RatingModel configured for the specified risk profile
        """
        return cls(risk_profile=risk_profile)
    
    def switch_risk_profile(self, new_profile: RiskProfile) -> None:
        """
        Switch to a different risk profile while maintaining the same model instance.
        
        Args:
            new_profile: The new risk profile to use
        """
        profile_params = self.RISK_PROFILES[new_profile]
        self.risk_profile = new_profile
        
        # Update parameters from the new profile
        self.alpha = profile_params['alpha']
        self.beta = profile_params['beta']
        self.gamma = profile_params['gamma']
        self.delta = profile_params['delta']
        self.epsilon = profile_params['epsilon']
        self.zeta = profile_params['zeta']
        
        # Update fundamental metric weights
        self.w1 = profile_params['w1']
        self.w2 = profile_params['w2']
        self.w3 = profile_params['w3']
        self.w4 = profile_params['w4']
        self.w5 = profile_params['w5']
        
        logger.info(f"Successfully switched to {new_profile.value} risk profile")
    
    def __init__(self, 
                 risk_profile: RiskProfile = RiskProfile.MEDIUM_RISK,
                 alpha: Optional[float] = None, 
                 beta: Optional[float] = None, 
                 gamma: Optional[float] = None, 
                 delta: Optional[float] = None, 
                 epsilon: Optional[float] = None, 
                 zeta: Optional[float] = None,
                 w1: Optional[float] = None,
                 w2: Optional[float] = None,
                 w3: Optional[float] = None,
                 w4: Optional[float] = None,
                 w5: Optional[float] = None):
        """
        Initialize the model with a risk profile or custom weighting coefficients.
        
        Args:
            risk_profile: Low, medium, or high risk profile
            alpha: Weight for historical returns premium
            beta: Weight for growth projections
            gamma: Weight for fundamental metrics
            delta: Weight for historical volatility
            epsilon: Weight for systematic risk
            zeta: Weight for market sentiment
            w1-w5: Weights for fundamental metric components
        """
        # Apply risk profile parameters first
        profile_params = self.RISK_PROFILES[risk_profile]
        self.risk_profile = risk_profile
        
        # Set parameters from profile, but allow overrides with custom values
        self.alpha = alpha if alpha is not None else profile_params['alpha']
        self.beta = beta if beta is not None else profile_params['beta']
        self.gamma = gamma if gamma is not None else profile_params['gamma']
        self.delta = delta if delta is not None else profile_params['delta']
        self.epsilon = epsilon if epsilon is not None else profile_params['epsilon']
        self.zeta = zeta if zeta is not None else profile_params['zeta']
        
        # Weights for fundamental metrics
        self.w1 = w1 if w1 is not None else profile_params['w1']  # P/E weight
        self.w2 = w2 if w2 is not None else profile_params['w2']  # D/E weight
        self.w3 = w3 if w3 is not None else profile_params['w3']  # ROE weight
        self.w4 = w4 if w4 is not None else profile_params['w4']  # FCF weight
        self.w5 = w5 if w5 is not None else profile_params['w5']  # PM weight
        
        # Validate weights sum to 1 for model parameters
        total_model = self.alpha + self.beta + self.gamma + self.delta + self.epsilon + self.zeta
        if not np.isclose(total_model, 1.0):
            factor = 1.0 / total_model
            self.alpha *= factor
            self.beta *= factor
            self.gamma *= factor
            self.delta *= factor
            self.epsilon *= factor
            self.zeta *= factor
        
        # Validate weights sum to 1 for fundamental metrics
        total_fundamental = self.w1 + self.w2 + self.w3 + self.w4 + self.w5
        if not np.isclose(total_fundamental, 1.0):
            factor = 1.0 / total_fundamental
            self.w1 *= factor
            self.w2 *= factor
            self.w3 *= factor
            self.w4 *= factor
            self.w5 *= factor
    
    def calculate_historical_returns(self, price_history: pd.Series) -> Dict:
        """
        Calculate annualized returns based on historical price data.
        
        Args:
            price_history: Series of historical prices
            
        Returns:
            Dictionary with various return metrics
        """
        if len(price_history) < 2:
            return {
                'annualized_return': 0.0,
                '1y_return': 0.0,
                '3m_return': 0.0,
                '1m_return': 0.0,
                'total_return': 0.0
            }
            
        # Calculate period returns
        returns = price_history.pct_change().dropna()
        
        # Calculate total return
        total_return = (price_history.iloc[-1] / price_history.iloc[0]) - 1
        
        # Calculate years for annualization
        years = len(price_history) / 252  # Assuming 252 trading days per year
        
        # Calculate annualized return
        annualized_return = (1 + total_return) ** (1 / max(years, 1)) - 1
        
        # Calculate short-term returns if enough data
        one_month_return = 0.0
        three_month_return = 0.0
        one_year_return = 0.0
        
        if len(price_history) >= 21:  # ~1 month of trading days
            one_month_return = (price_history.iloc[-1] / price_history.iloc[-min(21, len(price_history))]) - 1
            
        if len(price_history) >= 63:  # ~3 months of trading days
            three_month_return = (price_history.iloc[-1] / price_history.iloc[-min(63, len(price_history))]) - 1
            
        if len(price_history) >= 252:  # ~1 year of trading days
            one_year_return = (price_history.iloc[-1] / price_history.iloc[-min(252, len(price_history))]) - 1
        
        return {
            'annualized_return': annualized_return,
            '1y_return': one_year_return,
            '3m_return': three_month_return,
            '1m_return': one_month_return,
            'total_return': total_return
        }
    
    def calculate_fundamental_score(self, 
                                   pe_ratio: float, 
                                   de_ratio: float, 
                                   roe: float, 
                                   fcf_yield: float, 
                                   profit_margin: float,
                                   sector_pe: float,
                                   sector_de: float) -> Dict:
        """
        Calculate the composite fundamental score with detailed components.
        
        Args:
            pe_ratio: Price-to-Earnings ratio
            de_ratio: Debt-to-Equity ratio
            roe: Return on Equity
            fcf_yield: Free Cash Flow yield
            profit_margin: Profit margin (trailing twelve months)
            sector_pe: Sector average PE ratio
            sector_de: Sector average DE ratio
            
        Returns:
            Dictionary with fundamental scores and normalized components
        """
        # Normalize P/E (lower is better, inverse relationship)
        if pe_ratio <= 0:  # Handle negative P/E
            normalized_pe = 0
            pe_assessment = "Negative (Poor)"
        elif pe_ratio < sector_pe * 0.7:
            normalized_pe = 1.0
            pe_assessment = "Significantly Below Sector Average (Excellent)"
        elif pe_ratio < sector_pe * 0.9:
            normalized_pe = 0.8
            pe_assessment = "Below Sector Average (Good)"
        elif pe_ratio < sector_pe * 1.1:
            normalized_pe = 0.6
            pe_assessment = "Near Sector Average (Average)"
        elif pe_ratio < sector_pe * 1.3:
            normalized_pe = 0.4
            pe_assessment = "Above Sector Average (Below Average)"
        elif pe_ratio < sector_pe * 1.5:
            normalized_pe = 0.2
            pe_assessment = "Significantly Above Sector Average (Poor)"
        else:
            normalized_pe = 0.0
            pe_assessment = "Extremely High (Very Poor)"
        
        # Normalize D/E (lower is better, inverse relationship)
        if de_ratio < 0:  # Handle negative D/E
            normalized_de = 0
            de_assessment = "Negative (Poor)"
        elif de_ratio < sector_de * 0.5:
            normalized_de = 1.0
            de_assessment = "Very Low Debt (Excellent)"
        elif de_ratio < sector_de * 0.8:
            normalized_de = 0.8
            de_assessment = "Below Sector Average (Good)"
        elif de_ratio < sector_de * 1.2:
            normalized_de = 0.6
            de_assessment = "Near Sector Average (Average)"
        elif de_ratio < sector_de * 1.5:
            normalized_de = 0.4
            de_assessment = "Above Sector Average (Below Average)"
        elif de_ratio < sector_de * 2.0:
            normalized_de = 0.2
            de_assessment = "High Debt (Poor)"
        else:
            normalized_de = 0.0
            de_assessment = "Very High Debt (Very Poor)"
        
        # Normalize ROE (higher is better)
        if roe < 0:
            normalized_roe = 0
            roe_assessment = "Negative (Poor)"
        elif roe < 0.05:
            normalized_roe = 0.2
            roe_assessment = "Low (Poor)"
        elif roe < 0.10:
            normalized_roe = 0.4
            roe_assessment = "Below Average (Below Average)"
        elif roe < 0.15:
            normalized_roe = 0.6
            roe_assessment = "Average (Average)"
        elif roe < 0.20:
            normalized_roe = 0.8
            roe_assessment = "Good (Good)"
        else:
            normalized_roe = 1.0
            roe_assessment = "Excellent (Excellent)"
        
        # Normalize FCF yield (higher is better)
        if fcf_yield < 0:
            normalized_fcf = 0
            fcf_assessment = "Negative (Poor)"
        elif fcf_yield < 0.02:
            normalized_fcf = 0.2
            fcf_assessment = "Low (Poor)"
        elif fcf_yield < 0.04:
            normalized_fcf = 0.4
            fcf_assessment = "Below Average (Below Average)"
        elif fcf_yield < 0.06:
            normalized_fcf = 0.6
            fcf_assessment = "Average (Average)"
        elif fcf_yield < 0.08:
            normalized_fcf = 0.8
            fcf_assessment = "Good (Good)"
        else:
            normalized_fcf = 1.0
            fcf_assessment = "Excellent (Excellent)"
        
        # Normalize profit margin (higher is better)
        if profit_margin < 0:
            normalized_pm = 0
            pm_assessment = "Negative (Poor)"
        elif profit_margin < 0.05:
            normalized_pm = 0.2
            pm_assessment = "Low (Poor)"
        elif profit_margin < 0.10:
            normalized_pm = 0.4
            pm_assessment = "Below Average (Below Average)"
        elif profit_margin < 0.15:
            normalized_pm = 0.6
            pm_assessment = "Average (Average)"
        elif profit_margin < 0.20:
            normalized_pm = 0.8
            pm_assessment = "Good (Good)"
        else:
            normalized_pm = 1.0
            pm_assessment = "Excellent (Excellent)"
        
        # Calculate composite fundamental score
        fundamental_score = (
            self.w1 * normalized_pe +
            self.w2 * normalized_de +
            self.w3 * normalized_roe +
            self.w4 * normalized_fcf +
            self.w5 * normalized_pm
        )
        
        # Return detailed scores
        return {
            'composite_score': fundamental_score,
            'components': {
                'pe_ratio': {
                    'value': pe_ratio,
                    'normalized_score': normalized_pe,
                    'weight': self.w1,
                    'assessment': pe_assessment,
                    'sector_average': sector_pe
                },
                'de_ratio': {
                    'value': de_ratio,
                    'normalized_score': normalized_de,
                    'weight': self.w2,
                    'assessment': de_assessment,
                    'sector_average': sector_de
                },
                'roe': {
                    'value': roe,
                    'normalized_score': normalized_roe,
                    'weight': self.w3,
                    'assessment': roe_assessment
                },
                'fcf_yield': {
                    'value': fcf_yield,
                    'normalized_score': normalized_fcf,
                    'weight': self.w4,
                    'assessment': fcf_assessment
                },
                'profit_margin': {
                    'value': profit_margin,
                    'normalized_score': normalized_pm,
                    'weight': self.w5,
                    'assessment': pm_assessment
                }
            }
        }
    
    def calculate_volatility(self, returns: pd.Series) -> Dict:
        """
        Calculate historical volatility and related risk metrics.
        
        Args:
            returns: Series of historical returns
            
        Returns:
            Dictionary with volatility metrics
        """
        if len(returns) < 2:
            return {
                'annualized_volatility': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'downside_deviation': 0.0,
                'volatility_assessment': "Insufficient Data"
            }
            
        # Annualize the standard deviation (assuming daily returns)
        daily_std = returns.std()
        annualized_volatility = daily_std * np.sqrt(252)
        
        # Calculate Sharpe ratio (assuming 0% risk-free rate for simplicity)
        mean_daily_return = returns.mean()
        sharpe_ratio = (mean_daily_return * 252) / annualized_volatility if annualized_volatility > 0 else 0
        
        # Calculate maximum drawdown
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns / running_max) - 1
        max_drawdown = drawdown.min()
        
        # Calculate downside deviation (returns below 0)
        negative_returns = returns[returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(252) if len(negative_returns) > 0 else 0
        
        # Assess volatility
        if annualized_volatility < 0.15:
            volatility_assessment = "Low Volatility"
        elif annualized_volatility < 0.25:
            volatility_assessment = "Moderate Volatility"
        elif annualized_volatility < 0.35:
            volatility_assessment = "High Volatility"
        else:
            volatility_assessment = "Very High Volatility"
        
        return {
            'annualized_volatility': annualized_volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'downside_deviation': downside_deviation,
            'volatility_assessment': volatility_assessment
        }
    
    def calculate_beta(self, stock_returns: pd.Series, market_returns: pd.Series) -> Dict:
        """
        Calculate beta (systematic risk) and related metrics.
        
        Args:
            stock_returns: Series of stock returns
            market_returns: Series of market returns
            
        Returns:
            Dictionary with beta and related metrics
        """
        if len(stock_returns) < 10 or len(market_returns) < 10:
            return {
                'beta': 1.0,
                'r_squared': 0.0,
                'alpha': 0.0,
                'tracking_error': 0.0,
                'beta_assessment': "Insufficient Data"
            }
            
        # Ensure the series are aligned
        aligned_data = pd.DataFrame({
            'stock': stock_returns,
            'market': market_returns
        }).dropna()
        
        if len(aligned_data) < 10:
            return {
                'beta': 1.0,
                'r_squared': 0.0,
                'alpha': 0.0,
                'tracking_error': 0.0,
                'beta_assessment': "Insufficient Data"
            }
        
        # Calculate beta using covariance and market variance
        covariance = aligned_data['stock'].cov(aligned_data['market'])
        market_variance = aligned_data['market'].var()
        
        if market_variance == 0:
            beta = 1.0  # Default to market beta
        else:
            beta = covariance / market_variance
        
        # Calculate R-squared (correlation coefficient squared)
        correlation = aligned_data['stock'].corr(aligned_data['market'])
        r_squared = correlation ** 2
        
        # Calculate alpha (Jensen's alpha, simplified)
        stock_mean = aligned_data['stock'].mean() * 252  # Annualized
        market_mean = aligned_data['market'].mean() * 252  # Annualized
        alpha = stock_mean - (beta * market_mean)
        
        # Calculate tracking error
        tracking_diff = aligned_data['stock'] - (beta * aligned_data['market'])
        tracking_error = tracking_diff.std() * np.sqrt(252)  # Annualized
        
        # Assess beta
        if beta < 0.5:
            beta_assessment = "Very Defensive"
        elif beta < 0.8:
            beta_assessment = "Defensive"
        elif beta < 1.2:
            beta_assessment = "Market-like"
        elif beta < 1.5:
            beta_assessment = "Aggressive"
        else:
            beta_assessment = "Very Aggressive"
        
        return {
            'beta': beta,
            'r_squared': r_squared,
            'alpha': alpha,
            'tracking_error': tracking_error,
            'beta_assessment': beta_assessment
        }
    
    def calculate_sentiment_score(self, technical_indicators: Dict) -> Dict:
        """
        Calculate market sentiment score with detailed breakdown.
        
        Args:
            technical_indicators: Dictionary of technical indicators
            
        Returns:
            Dictionary with sentiment score and component details
        """
        components = {}
        
        # Check if price is above moving averages
        if 'price' in technical_indicators and 'ma_50' in technical_indicators:
            price_vs_ma50 = technical_indicators['price'] > technical_indicators['ma_50']
            components['price_vs_ma50'] = {
                'value': 1.0 if price_vs_ma50 else 0.0,
                'description': "Price Above 50-day MA" if price_vs_ma50 else "Price Below 50-day MA"
            }
            
        if 'price' in technical_indicators and 'ma_200' in technical_indicators:
            price_vs_ma200 = technical_indicators['price'] > technical_indicators['ma_200']
            components['price_vs_ma200'] = {
                'value': 1.0 if price_vs_ma200 else 0.0,
                'description': "Price Above 200-day MA" if price_vs_ma200 else "Price Below 200-day MA"
            }
        
        # Check RSI
        if 'rsi' in technical_indicators:
            rsi = technical_indicators['rsi']
            rsi_score = 0.0
            rsi_description = ""
            
            if rsi > 70:
                rsi_score = 0.0
                rsi_description = "Overbought (RSI > 70)"
            elif rsi < 30:
                rsi_score = 0.5
                rsi_description = "Oversold (RSI < 30) - Potential Bounce"
            else:
                rsi_score = 1.0
                rsi_description = "Healthy RSI Range (30-70)"
                
            components['rsi'] = {
                'value': rsi_score,
                'raw_value': rsi,
                'description': rsi_description
            }
        
        # Check MACD
        if 'macd' in technical_indicators and 'macd_signal' in technical_indicators:
            macd_bullish = technical_indicators['macd'] > technical_indicators['macd_signal']
            components['macd'] = {
                'value': 1.0 if macd_bullish else 0.0,
                'raw_value': technical_indicators['macd'],
                'signal_line': technical_indicators['macd_signal'],
                'description': "MACD Above Signal Line" if macd_bullish else "MACD Below Signal Line"
            }
        
        # Volume trend
        if 'volume' in technical_indicators and 'avg_volume' in technical_indicators:
            volume_above_avg = technical_indicators['volume'] > technical_indicators['avg_volume']
            components['volume'] = {
                'value': 1.0 if volume_above_avg else 0.0,
                'raw_value': technical_indicators['volume'],
                'avg_volume': technical_indicators['avg_volume'],
                'ratio': technical_indicators['volume'] / technical_indicators['avg_volume'] if technical_indicators['avg_volume'] > 0 else 1.0,
                'description': "Volume Above Average" if volume_above_avg else "Volume Below Average"
            }
            
        # Calculate overall score
        total_score = sum(item['value'] for item in components.values())
        count = len(components)
        composite_score = total_score / max(1, count)
        
        # Determine sentiment assessment
        if composite_score >= 0.8:
            assessment = "Very Bullish"
        elif composite_score >= 0.6:
            assessment = "Bullish"
        elif composite_score >= 0.4:
            assessment = "Neutral"
        elif composite_score >= 0.2:
            assessment = "Bearish"
        else:
            assessment = "Very Bearish"
            
        return {
            'composite_score': composite_score,
            'assessment': assessment,
            'components': components
        }
    
    def calculate_growth_outlook(self, 
                                earnings_growth: float,
                                revenue_growth: float,
                                industry_growth: float,
                                analyst_recommendations: Optional[pd.DataFrame] = None) -> Dict:
        """
        Calculate comprehensive growth outlook score.
        
        Args:
            earnings_growth: Projected earnings growth rate
            revenue_growth: Projected revenue growth rate
            industry_growth: Average industry growth rate
            analyst_recommendations: DataFrame with analyst recommendations
            
        Returns:
            Dictionary with growth outlook assessment
        """
        # Normalize earnings growth relative to industry
        relative_earnings = earnings_growth / max(industry_growth, 0.01)
        
        # Assess earnings growth
        if earnings_growth < 0:
            earnings_assessment = "Negative Growth (Poor)"
            normalized_earnings = 0.0
        elif relative_earnings < 0.5:
            earnings_assessment = "Well Below Industry (Poor)"
            normalized_earnings = 0.2
        elif relative_earnings < 0.9:
            earnings_assessment = "Below Industry (Below Average)"
            normalized_earnings = 0.4
        elif relative_earnings < 1.1:
            earnings_assessment = "In-line with Industry (Average)"
            normalized_earnings = 0.6
        elif relative_earnings < 1.5:
            earnings_assessment = "Above Industry (Good)"
            normalized_earnings = 0.8
        else:
            earnings_assessment = "Well Above Industry (Excellent)"
            normalized_earnings = 1.0
            
        # Normalize revenue growth
        if revenue_growth < 0:
            revenue_assessment = "Negative Growth (Poor)"
            normalized_revenue = 0.0
        elif revenue_growth < industry_growth * 0.5:
            revenue_assessment = "Well Below Industry (Poor)"
            normalized_revenue = 0.2
        elif revenue_growth < industry_growth * 0.9:
            revenue_assessment = "Below Industry (Below Average)"
            normalized_revenue = 0.4
        elif revenue_growth < industry_growth * 1.1:
            revenue_assessment = "In-line with Industry (Average)"
            normalized_revenue = 0.6
        elif revenue_growth < industry_growth * 1.5:
            revenue_assessment = "Above Industry (Good)"
            normalized_revenue = 0.8
        else:
            revenue_assessment = "Well Above Industry (Excellent)"
            normalized_revenue = 1.0
            
        # Analyst sentiment if available
        analyst_score = 0.5  # Neutral default
        analyst_assessment = "No Data"
        
        if analyst_recommendations is not None and not analyst_recommendations.empty:
            # Example processing - would need to be adapted to actual data format
            buy_count = sum(1 for rec in analyst_recommendations if rec in ['Buy', 'Strong Buy'])
            sell_count = sum(1 for rec in analyst_recommendations if rec in ['Sell', 'Strong Sell'])
            hold_count = sum(1 for rec in analyst_recommendations if rec in ['Hold', 'Neutral'])
            
            total_count = buy_count + sell_count + hold_count
            
            if total_count > 0:
                buy_ratio = buy_count / total_count
                sell_ratio = sell_count / total_count
                
                # Score from 0 to 1 based on buy/sell ratio
                analyst_score = buy_ratio / (buy_ratio + sell_ratio) if (buy_ratio + sell_ratio) > 0 else 0.5
                
                if analyst_score > 0.8:
                    analyst_assessment = "Very Bullish"
                elif analyst_score > 0.6:
                    analyst_assessment = "Bullish"
                elif analyst_score > 0.4:
                    analyst_assessment = "Neutral"
                elif analyst_score > 0.2:
                    analyst_assessment = "Bearish"
                else:
                    analyst_assessment = "Very Bearish"
        
        # Calculate composite growth score - equal weight to earnings and revenue growth
        composite_score = (normalized_earnings + normalized_revenue) / 2
        
        # Overall growth assessment
        if composite_score > 0.8:
            growth_assessment = "Excellent Growth Outlook"
        elif composite_score > 0.6:
            growth_assessment = "Good Growth Outlook"
        elif composite_score > 0.4:
            growth_assessment = "Average Growth Outlook"
        elif composite_score > 0.2:
            growth_assessment = "Below Average Growth Outlook"
        else:
            growth_assessment = "Poor Growth Outlook"
            
        return {
            'composite_score': composite_score,
            'assessment': growth_assessment,
            'components': {
                'earnings_growth': {
                    'value': earnings_growth,
                    'industry_average': industry_growth,
                    'relative_to_industry': relative_earnings,
                    'normalized_score': normalized_earnings,
                    'assessment': earnings_assessment
                },
                'revenue_growth': {
                    'value': revenue_growth,
                    'industry_average': industry_growth,
                    'normalized_score': normalized_revenue,
                    'assessment': revenue_assessment
                },
                'analyst_sentiment': {
                    'score': analyst_score,
                    'assessment': analyst_assessment
                }
            }
        }
    
    def calculate_investment_score(self, 
                                  historical_returns: Dict,
                                  risk_free_rate: float,
                                  growth_outlook: Dict,
                                  fundamental_metrics: Dict,
                                  volatility_metrics: Dict,
                                  systematic_risk: Dict,
                                  market_sentiment: Dict) -> Dict:
        """
        Calculate the investment score with component breakdown.
        
        Args:
            historical_returns: Dictionary with return metrics
            risk_free_rate: Current risk-free rate (treasury yield)
            growth_outlook: Dictionary with growth metrics
            fundamental_metrics: Dictionary with fundamental metrics
            volatility_metrics: Dictionary with volatility metrics
            systematic_risk: Dictionary with risk metrics
            market_sentiment: Dictionary with sentiment metrics
            
        Returns:
            Dictionary with investment score and component details
        """
        # Extract the primary metrics from each component
        returns_premium = historical_returns['annualized_return'] - risk_free_rate
        growth_projection = growth_outlook['composite_score']
        fundamental_score = fundamental_metrics['composite_score']
        volatility = volatility_metrics['annualized_volatility']
        beta = systematic_risk['beta']
        sentiment = market_sentiment['composite_score']
        
        # Apply the model equation with component weights
        weighted_returns = self.alpha * returns_premium
        weighted_growth = self.beta * growth_projection
        weighted_fundamentals = self.gamma * fundamental_score
        weighted_volatility = -self.delta * volatility  # Negative impact
        weighted_beta = -self.epsilon * (beta - 1.0)  # Penalize deviation from market
        weighted_sentiment = self.zeta * sentiment
        
        # Calculate raw investment score
        raw_score = (
            weighted_returns +
            weighted_growth +
            weighted_fundamentals +
            weighted_volatility +
            weighted_beta +
            weighted_sentiment
        )
        
        # Normalize to 0-1 range - typical range for raw_score is -0.2 to 0.5
        normalized_score = min(1.0, max(0.0, (raw_score + 0.2) / 0.7))
        
        # Calculate each component's contribution to the final score
        total_positive = (
            max(0, weighted_returns) + 
            max(0, weighted_growth) + 
            max(0, weighted_fundamentals) + 
            max(0, weighted_volatility) + 
            max(0, weighted_beta) + 
            max(0, weighted_sentiment)
        )
        
        total_negative = (
            min(0, weighted_returns) + 
            min(0, weighted_growth) + 
            min(0, weighted_fundamentals) + 
            min(0, weighted_volatility) + 
            min(0, weighted_beta) + 
            min(0, weighted_sentiment)
        )
        
        # Handle division by zero
        if total_positive == 0 and total_negative == 0:
            contribution = {
                'returns_premium': 0,
                'growth_projection': 0,
                'fundamental_metrics': 0,
                'volatility': 0,
                'systematic_risk': 0,
                'market_sentiment': 0
            }
        else:
            # Calculate positive and negative contributions separately
            contribution = {
                'returns_premium': weighted_returns / (total_positive if weighted_returns > 0 else total_negative),
                'growth_projection': weighted_growth / (total_positive if weighted_growth > 0 else total_negative),
                'fundamental_metrics': weighted_fundamentals / (total_positive if weighted_fundamentals > 0 else total_negative),
                'volatility': weighted_volatility / (total_positive if weighted_volatility > 0 else total_negative),
                'systematic_risk': weighted_beta / (total_positive if weighted_beta > 0 else total_negative),
                'market_sentiment': weighted_sentiment / (total_positive if weighted_sentiment > 0 else total_negative)
            }
        
        return {
            'investment_score': normalized_score,
            'raw_score': raw_score,
            'risk_profile': self.risk_profile.value,
            'weighted_components': {
                'returns_premium': weighted_returns,
                'growth_projection': weighted_growth,
                'fundamental_metrics': weighted_fundamentals,
                'volatility': weighted_volatility,
                'systematic_risk': weighted_beta,
                'market_sentiment': weighted_sentiment
            },
            'component_contribution': contribution,
            'component_weights': {
                'alpha': self.alpha,
                'beta': self.beta,
                'gamma': self.gamma,
                'delta': self.delta,
                'epsilon': self.epsilon,
                'zeta': self.zeta
            }
        }
        """
        Calculate the investment score with component breakdown.
        
        Args:
            historical_returns: Dictionary with return metrics
            risk_free_rate: Current risk-free rate (treasury yield)
        """