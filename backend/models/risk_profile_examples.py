import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from .rating_models import RatingModel, RiskProfile

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_stock_with_risk_profiles(
    ticker: str,
    price_history: pd.Series,
    market_history: pd.Series,
    fundamentals: Dict,
    growth_metrics: Dict,
    technical_indicators: Dict
) -> Dict[str, Dict]:
    """
    Analyze a stock using all three risk profiles and compare the results.
    
    Args:
        ticker: Stock ticker symbol
        price_history: Historical price data
        market_history: Market index historical data
        fundamentals: Dictionary containing fundamental metrics
        growth_metrics: Dictionary containing growth projections
        technical_indicators: Dictionary containing technical analysis indicators
    
    Returns:
        Dictionary containing analysis results for each risk profile
    """
    results = {}
    risk_free_rate = 0.04  # Example: 4% treasury yield
    
    # Analyze with each risk profile
    for risk_profile in RiskProfile:
        try:
            # Create model with specific risk profile
            model = RatingModel.get_model_for_risk_profile(risk_profile)
            
            # Calculate historical returns
            returns = model.calculate_historical_returns(price_history)
            
            # Calculate fundamental metrics
            fundamental_score = model.calculate_fundamental_score(
                pe_ratio=fundamentals['pe_ratio'],
                de_ratio=fundamentals['de_ratio'],
                roe=fundamentals['roe'],
                fcf_yield=fundamentals['fcf_yield'],
                profit_margin=fundamentals['profit_margin'],
                sector_pe=fundamentals['sector_pe'],
                sector_de=fundamentals['sector_de']
            )
            
            # Calculate risk metrics
            returns_series = price_history.pct_change().dropna()
            volatility = model.calculate_volatility(returns_series)
            beta = model.calculate_beta(returns_series, market_history.pct_change().dropna())
            
            # Calculate growth outlook
            growth_outlook = model.calculate_growth_outlook(
                earnings_growth=growth_metrics['earnings_growth'],
                revenue_growth=growth_metrics['revenue_growth'],
                industry_growth=growth_metrics['industry_growth'],
                analyst_recommendations=growth_metrics.get('analyst_recommendations')
            )
            
            # Calculate market sentiment
            sentiment = model.calculate_sentiment_score(technical_indicators)
            
            # Calculate final investment score
            investment_score = model.calculate_investment_score(
                historical_returns=returns,
                risk_free_rate=risk_free_rate,
                growth_outlook=growth_outlook,
                fundamental_metrics=fundamental_score,
                volatility_metrics=volatility,
                systematic_risk=beta,
                market_sentiment=sentiment
            )
            
            # Store results for this risk profile
            results[risk_profile.value] = {
                'investment_score': investment_score,
                'fundamental_score': fundamental_score,
                'volatility_metrics': volatility,
                'beta_metrics': beta,
                'growth_outlook': growth_outlook,
                'sentiment': sentiment,
                'model_weights': {
                    'alpha': model.alpha,
                    'beta': model.beta,
                    'gamma': model.gamma,
                    'delta': model.delta,
                    'epsilon': model.epsilon,
                    'zeta': model.zeta
                }
            }
            
            logger.info(f"Completed analysis for {ticker} with {risk_profile.value} risk profile")
            
        except Exception as e:
            logger.error(f"Error analyzing {ticker} with {risk_profile.value} risk profile: {str(e)}")
            results[risk_profile.value] = {'error': str(e)}
    
    return results

def get_investment_recommendation(analysis_results: Dict[str, Dict], investor_profile: RiskProfile) -> Dict:
    """
    Generate investment recommendations based on the analysis results and investor's risk profile.
    
    Args:
        analysis_results: Results from analyze_stock_with_risk_profiles
        investor_profile: Investor's risk profile preference
        
    Returns:
        Dictionary containing investment recommendations
    """
    try:
        # Get the analysis matching the investor's risk profile
        profile_analysis = analysis_results[investor_profile.value]
        investment_score = profile_analysis['investment_score']
        
        # Define score thresholds based on risk profile
        thresholds = {
            RiskProfile.LOW_RISK: {
                'strong_buy': 0.8,
                'buy': 0.7,
                'hold': 0.5,
                'sell': 0.3
            },
            RiskProfile.MEDIUM_RISK: {
                'strong_buy': 0.75,
                'buy': 0.6,
                'hold': 0.4,
                'sell': 0.25
            },
            RiskProfile.HIGH_RISK: {
                'strong_buy': 0.7,
                'buy': 0.5,
                'hold': 0.3,
                'sell': 0.2
            }
        }
        
        profile_thresholds = thresholds[investor_profile]
        score = investment_score['investment_score']
        
        # Determine recommendation
        if score >= profile_thresholds['strong_buy']:
            recommendation = "Strong Buy"
            confidence = "High"
            action = "Consider significant position within risk limits"
        elif score >= profile_thresholds['buy']:
            recommendation = "Buy"
            confidence = "Moderate to High"
            action = "Consider standard position size"
        elif score >= profile_thresholds['hold']:
            recommendation = "Hold"
            confidence = "Moderate"
            action = "Maintain current position or watch list"
        elif score >= profile_thresholds['sell']:
            recommendation = "Reduce"
            confidence = "Moderate to High"
            action = "Consider reducing position"
        else:
            recommendation = "Sell"
            confidence = "High"
            action = "Consider exiting position"
            
        # Generate risk notes
        risk_notes = []
        
        # Check volatility
        volatility = profile_analysis['volatility_metrics']
        if volatility['annualized_volatility'] > 0.25:  # 25% annualized volatility
            risk_notes.append("High price volatility detected")
            
        # Check beta
        beta = profile_analysis['beta_metrics']
        if beta['beta'] > 1.5:
            risk_notes.append("High market sensitivity (beta)")
            
        # Check fundamental metrics
        fundamentals = profile_analysis['fundamental_score']
        if fundamentals['components']['de_ratio']['normalized_score'] < 0.3:
            risk_notes.append("High debt levels relative to sector")
            
        # Check growth metrics
        growth = profile_analysis['growth_outlook']
        if growth['composite_score'] < 0.3:
            risk_notes.append("Weak growth outlook")
            
        return {
            'recommendation': recommendation,
            'confidence_level': confidence,
            'suggested_action': action,
            'investment_score': score,
            'risk_notes': risk_notes,
            'risk_profile_used': investor_profile.value,
            'analysis_summary': {
                'fundamental_score': fundamentals['composite_score'],
                'growth_score': growth['composite_score'],
                'volatility_assessment': volatility['volatility_assessment'],
                'beta': beta['beta'],
                'beta_assessment': beta['beta_assessment']
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        return {'error': str(e)}

def main():
    """
    Example usage of the risk profile models
    """
    # Example data (in practice, this would come from your data sources)
    example_data = {
        'ticker': 'AAPL',
        'price_history': pd.Series([150, 155, 153, 158, 160, 165]),
        'market_history': pd.Series([4500, 4550, 4525, 4575, 4600, 4650]),
        'fundamentals': {
            'pe_ratio': 25.5,
            'de_ratio': 1.2,
            'roe': 0.35,
            'fcf_yield': 0.05,
            'profit_margin': 0.25,
            'sector_pe': 22.0,
            'sector_de': 1.0
        },
        'growth_metrics': {
            'earnings_growth': 0.15,
            'revenue_growth': 0.12,
            'industry_growth': 0.10
        },
        'technical_indicators': {
            'price': 165,
            'ma_50': 155,
            'ma_200': 150,
            'rsi': 65,
            'macd': 2.5,
            'macd_signal': 2.0,
            'volume': 1000000,
            'avg_volume': 900000
        }
    }
    
    try:
        # Analyze stock with all risk profiles
        results = analyze_stock_with_risk_profiles(
            ticker=example_data['ticker'],
            price_history=example_data['price_history'],
            market_history=example_data['market_history'],
            fundamentals=example_data['fundamentals'],
            growth_metrics=example_data['growth_metrics'],
            technical_indicators=example_data['technical_indicators']
        )
        
        # Generate recommendations for each investor profile
        print("\nInvestment Recommendations by Risk Profile:")
        for risk_profile in RiskProfile:
            recommendation = get_investment_recommendation(results, risk_profile)
            print(f"\n{risk_profile.value.upper()} RISK PROFILE:")
            print(f"Recommendation: {recommendation['recommendation']}")
            print(f"Confidence Level: {recommendation['confidence_level']}")
            print(f"Suggested Action: {recommendation['suggested_action']}")
            print(f"Investment Score: {recommendation['investment_score']:.2f}")
            if recommendation['risk_notes']:
                print("Risk Notes:")
                for note in recommendation['risk_notes']:
                    print(f"- {note}")
                    
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 