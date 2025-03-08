"""
Test script for stock analysis using different risk profiles.
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import our models
from backend.models import RatingModel, RiskProfile
from backend.models import analyze_stock_with_risk_profiles, get_investment_recommendation

def get_stock_data(ticker, period='2y'):
    """Get real stock data using yfinance"""
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        
        # Get market data (using S&P 500 as benchmark)
        market = yf.Ticker('^GSPC')
        market_hist = market.history(period=period)
        
        # Prepare fundamental metrics
        fundamentals = {
            'pe_ratio': info.get('forwardPE', 20),  # Forward P/E or default
            'de_ratio': info.get('debtToEquity', 1.0) / 100 if info.get('debtToEquity') else 1.0,
            'roe': info.get('returnOnEquity', 0.15) if info.get('returnOnEquity') else 0.15,
            'fcf_yield': info.get('freeCashflow', 0) / (info.get('marketCap', 1) or 1),
            'profit_margin': info.get('profitMargins', 0.1) if info.get('profitMargins') else 0.1,
            'sector_pe': 20.0,  # Default sector average
            'sector_de': 1.0    # Default sector average
        }
        
        # Prepare growth metrics
        growth_metrics = {
            'earnings_growth': info.get('earningsGrowth', 0.1) if info.get('earningsGrowth') else 0.1,
            'revenue_growth': info.get('revenueGrowth', 0.1) if info.get('revenueGrowth') else 0.1,
            'industry_growth': 0.1  # Default industry growth
        }
        
        # Calculate technical indicators
        price_data = hist['Close']
        current_price = price_data[-1]
        ma_50 = price_data.rolling(window=50).mean()[-1]
        ma_200 = price_data.rolling(window=200).mean()[-1]
        
        # Calculate RSI
        returns = price_data.pct_change()
        gains = returns[returns > 0].mean() if len(returns[returns > 0]) > 0 else 0
        losses = -returns[returns < 0].mean() if len(returns[returns < 0]) > 0 else 0
        rsi = 100 - (100 / (1 + gains/max(losses, 0.0001)))
        
        # Prepare technical indicators
        technical_indicators = {
            'price': current_price,
            'ma_50': ma_50,
            'ma_200': ma_200,
            'rsi': rsi,
            'macd': 0.0,  # Simplified
            'macd_signal': 0.0,
            'volume': hist['Volume'][-1],
            'avg_volume': hist['Volume'].mean()
        }
        
        return {
            'ticker': ticker,
            'price_history': hist['Close'],
            'market_history': market_hist['Close'],
            'fundamentals': fundamentals,
            'growth_metrics': growth_metrics,
            'technical_indicators': technical_indicators
        }
        
    except Exception as e:
        print(f"Error getting data for {ticker}: {str(e)}")
        return None

def analyze_stocks(tickers):
    """Analyze multiple stocks using all risk profiles"""
    results = {}
    
    for ticker in tickers:
        print(f"\nAnalyzing {ticker}...")
        
        # Get real stock data
        stock_data = get_stock_data(ticker)
        if stock_data is None:
            print(f"Skipping {ticker} due to data retrieval error")
            continue
        
        try:
            # Analyze with all risk profiles
            analysis = analyze_stock_with_risk_profiles(
                ticker=stock_data['ticker'],
                price_history=stock_data['price_history'],
                market_history=stock_data['market_history'],
                fundamentals=stock_data['fundamentals'],
                growth_metrics=stock_data['growth_metrics'],
                technical_indicators=stock_data['technical_indicators']
            )
            
            results[ticker] = analysis
            
            # Print summary for this stock
            print(f"\nResults for {ticker}:")
            for risk_profile in RiskProfile:
                recommendation = get_investment_recommendation(analysis, risk_profile)
                print(f"{risk_profile.value}: {recommendation['recommendation']} (Score: {recommendation['investment_score']:.2f})")
                if recommendation['risk_notes']:
                    print("Risk Notes:")
                    for note in recommendation['risk_notes']:
                        print(f"- {note}")
                
        except Exception as e:
            print(f"Error analyzing {ticker}: {str(e)}")
            continue
    
    return results

def plot_results_heatmap(results):
    """Plot a heatmap of investment scores across stocks and risk profiles"""
    
    # Extract scores for each stock and risk profile
    data = []
    for ticker in results:
        row = []
        for risk_profile in RiskProfile:
            score = results[ticker][risk_profile.value]['investment_score']['investment_score']
            row.append(score)
        data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(
        data,
        index=list(results.keys()),
        columns=[rp.value for rp in RiskProfile]
    )
    
    # Create heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        df,
        annot=True,
        fmt='.2f',
        cmap='RdYlGn',
        center=0.5,
        vmin=0,
        vmax=1
    )
    plt.title('Investment Scores by Stock and Risk Profile')
    plt.ylabel('Stock')
    plt.xlabel('Risk Profile')
    plt.tight_layout()
    plt.show()

def plot_risk_profile_distributions(results):
    """Plot the distribution of scores for each risk profile"""
    
    scores_by_profile = {rp.value: [] for rp in RiskProfile}
    
    # Collect scores for each risk profile
    for ticker in results:
        for risk_profile in RiskProfile:
            score = results[ticker][risk_profile.value]['investment_score']['investment_score']
            scores_by_profile[risk_profile.value].append(score)
    
    # Create violin plots
    plt.figure(figsize=(10, 6))
    data = [scores_by_profile[rp.value] for rp in RiskProfile]
    labels = [rp.value for rp in RiskProfile]
    
    parts = plt.violinplot(data, showmeans=True)
    
    # Customize plot
    plt.xticks(range(1, len(labels) + 1), labels)
    plt.title('Distribution of Investment Scores by Risk Profile')
    plt.ylabel('Investment Score')
    plt.ylim(0, 1)
    
    # Add mean values
    means = [np.mean(scores) for scores in data]
    for i, mean in enumerate(means, 1):
        plt.text(i, mean, f'μ={mean:.2f}', horizontalalignment='center', verticalalignment='bottom')
    
    plt.show()

def main():
    """Main function to run the analysis"""
    # Test with popular tech stocks
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA']
    
    print("Analyzing stocks with multiple risk profiles...")
    results = analyze_stocks(tickers)
    
    if results:
        print("\nPlotting results...")
        plot_results_heatmap(results)
        plot_risk_profile_distributions(results)
    else:
        print("No results to plot.")

if __name__ == "__main__":
    main() 