import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import our models
from backend.models import RatingModel, RiskProfile
from backend.models import analyze_stock_with_risk_profiles, get_investment_recommendation

def test_risk_profiles():
    """Test the rating models with different risk profiles"""
    
    # Example data for testing
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
    
    # Test the models with different risk profiles
    results = analyze_stock_with_risk_profiles(
        ticker=example_data['ticker'],
        price_history=example_data['price_history'],
        market_history=example_data['market_history'],
        fundamentals=example_data['fundamentals'],
        growth_metrics=example_data['growth_metrics'],
        technical_indicators=example_data['technical_indicators']
    )
    
    # Print recommendations for each risk profile
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
    
    return results

def plot_risk_profile_comparison(results):
    """Visualize the differences between risk profiles"""
    
    profiles = list(results.keys())
    scores = [results[p]['investment_score']['investment_score'] for p in profiles]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(profiles, scores)
    
    # Color code the bars
    colors = ['green' if s >= 0.7 else 'yellow' if s >= 0.4 else 'red' for s in scores]
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.title('Investment Scores by Risk Profile')
    plt.ylabel('Investment Score')
    plt.ylim(0, 1)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    plt.show()

if __name__ == "__main__":
    # Run the tests
    results = test_risk_profiles()
    
    # Plot the comparison
    plot_risk_profile_comparison(results) 