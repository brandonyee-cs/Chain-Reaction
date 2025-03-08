import yfinance as yf
import pandas as pd
from typing import Dict, Optional

class DataLoader:
    def __init__(self) -> None:
        pass

    def get_raw_stock_data(self, ticker_symbol: str, period: str = "4y") -> Dict:
        """Get raw stock data directly from yfinance"""
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period)
            
            return {
                'info': ticker.info,
                'history': hist,  # Keep as DataFrame instead of converting to dict
                'recommendations': ticker.recommendations,
                'major_holders': ticker.major_holders,
                'institutional_holders': ticker.institutional_holders,
                'dividends': ticker.dividends,
                'splits': ticker.splits,
                'actions': ticker.actions
            }
        except Exception as e:
            return {'error': str(e), 'ticker': ticker_symbol}

    def get_rating_model_data(self, ticker_symbol: str, period: str = "4y") -> Dict:
        """Get processed data formatted for RatingModel"""
        try:
            raw_data = self.get_raw_stock_data(ticker_symbol, period)
            if 'error' in raw_data:
                raise ValueError(raw_data['error'])

            hist = raw_data['history']
            info = raw_data['info']
            
            # Calculate technical indicators
            technical_indicators = self._calculate_technical_indicators(hist)
            
            # Calculate returns
            returns = hist['Close'].pct_change().dropna()
            
            # Calculate FCF yield
            fcf_yield = self._calculate_fcf_yield(info)
            
            return {
                'ticker': ticker_symbol,
                'price_history': hist['Close'],
                'returns': returns,
                'pe_ratio': info.get('trailingPE', 20.0),
                'de_ratio': info.get('debtToEquity', 100.0) / 100.0,
                'roe': info.get('returnOnEquity', 0.15),
                'fcf_yield': fcf_yield,
                'profit_margin': info.get('profitMargin', 0.15),
                'technical_indicators': technical_indicators
            }
        except Exception as e:
            return self._get_default_data(ticker_symbol)

    def get_market_data(self, period: str = "5y") -> Dict:
        """Get market data formatted for RatingModel"""
        try:
            # Get S&P 500 data
            market = self.get_raw_stock_data('^GSPC', period)
            # Get treasury yield
            treasury = self.get_raw_stock_data('^TNX', '1d')
            
            market_hist = market['history']
            market_returns = market_hist['Close'].pct_change().dropna()
            treasury_yield = treasury['info'].get('regularMarketPrice', 400) / 100
            
            return {
                'market_returns': market_returns,
                'treasury_yield': treasury_yield,
                'sector_pe': 20.0,  # Default sector average
                'sector_de': 1.2    # Default sector average
            }
        except Exception as e:
            return self._get_default_market_data()

    def _calculate_technical_indicators(self, hist: pd.DataFrame) -> Dict:
        """Calculate technical indicators from historical data"""
        close = hist['Close']
        volume = hist['Volume']
        
        # Calculate RSI
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = -delta.clip(upper=0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # Calculate MACD
        ema_12 = close.ewm(span=12, adjust=False).mean()
        ema_26 = close.ewm(span=26, adjust=False).mean()
        
        return {
            'price': close.iloc[-1],
            'ma_50': close.rolling(window=50).mean().iloc[-1],
            'ma_200': close.rolling(window=200).mean().iloc[-1],
            'rsi': rsi,
            'macd': ema_12.iloc[-1] - ema_26.iloc[-1],
            'macd_signal': close.ewm(span=9, adjust=False).mean().iloc[-1],
            'volume': volume.iloc[-1],
            'avg_volume': volume.rolling(window=20).mean().iloc[-1]
        }

    def _calculate_fcf_yield(self, info: Dict) -> float:
        """Calculate free cash flow yield"""
        try:
            fcf = info.get('freeCashflow', 1000000000)
            market_cap = info.get('marketCap', 10000000000)
            return fcf / market_cap if market_cap else 0.05
        except (TypeError, ZeroDivisionError):
            return 0.05

    def _get_default_data(self, ticker_symbol: str) -> Dict:
        """Return default data structure for failed stock data fetch"""
        return {
            'ticker': ticker_symbol,
            'price_history': pd.Series(),
            'returns': pd.Series(),
            'pe_ratio': 20.0,
            'de_ratio': 1.0,
            'roe': 0.15,
            'fcf_yield': 0.05,
            'profit_margin': 0.15,
            'technical_indicators': {
                'price': 0, 'ma_50': 0, 'ma_200': 0,
                'rsi': 50, 'macd': 0, 'macd_signal': 0,
                'volume': 0, 'avg_volume': 0
            }
        }

    def _get_default_market_data(self) -> Dict:
        """Return default data structure for failed market data fetch"""
        return {
            'market_returns': pd.Series(),
            'treasury_yield': 0.04,
            'sector_pe': 20.0,
            'sector_de': 1.2
        }