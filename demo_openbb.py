#!/usr/bin/env python3
"""
OpenBB Python SDK Demo - Alternative way to use OpenBB
This shows how to use OpenBB programmatically instead of through the CLI
"""

from openbb import obb
import pandas as pd
from datetime import datetime, timedelta

def demo_equity_data():
    """Demonstrate fetching equity data"""
    print("\n" + "="*60)
    print("EQUITY DATA DEMO")
    print("="*60)
    
    # Get Apple stock quote
    print("\n1. Getting Apple (AAPL) stock quote...")
    try:
        quote = obb.equity.price.quote(symbol="AAPL", provider="yfinance")
        if quote and quote.results:
            data = quote.results[0]
            print(f"   Symbol: {data.symbol}")
            print(f"   Price: ${data.last_price:.2f}")
            print(f"   Change: ${data.change:.2f} ({data.change_percent:.2f}%)")
            print(f"   Volume: {data.volume:,}")
    except Exception as e:
        print(f"   Note: {e}")
    
    # Get historical data
    print("\n2. Getting Tesla (TSLA) historical data (last 5 days)...")
    try:
        start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        hist = obb.equity.price.historical(
            symbol="TSLA",
            start_date=start_date,
            provider="yfinance"
        )
        if hist and hist.results:
            df = pd.DataFrame([d.model_dump() for d in hist.results[-5:]])
            print(df[['date', 'open', 'high', 'low', 'close', 'volume']].to_string())
    except Exception as e:
        print(f"   Note: {e}")

def demo_crypto_data():
    """Demonstrate fetching crypto data"""
    print("\n" + "="*60)
    print("CRYPTOCURRENCY DATA DEMO")
    print("="*60)
    
    print("\n1. Getting Bitcoin (BTC-USD) price...")
    try:
        crypto = obb.crypto.price.quote(symbol="BTC-USD", provider="yfinance")
        if crypto and crypto.results:
            data = crypto.results[0]
            print(f"   Symbol: {data.symbol}")
            print(f"   Price: ${data.last_price:,.2f}")
            print(f"   24h Change: {data.change_percent:.2f}%")
    except Exception as e:
        print(f"   Note: {e}")

def demo_economic_data():
    """Demonstrate fetching economic data"""
    print("\n" + "="*60)
    print("ECONOMIC DATA DEMO")
    print("="*60)
    
    print("\n1. Getting US Treasury Rates...")
    try:
        rates = obb.fixedincome.treasury.rates(provider="federal_reserve")
        if rates and rates.results:
            data = rates.results[0]
            print(f"   Date: {data.date}")
            print(f"   3-Month: {data.month_3:.2f}%")
            print(f"   2-Year: {data.year_2:.2f}%")
            print(f"   10-Year: {data.year_10:.2f}%")
            print(f"   30-Year: {data.year_30:.2f}%")
    except Exception as e:
        print(f"   Note: {e}")

def demo_market_movers():
    """Demonstrate market discovery features"""
    print("\n" + "="*60)
    print("MARKET MOVERS DEMO")
    print("="*60)
    
    print("\n1. Top Gainers Today...")
    try:
        gainers = obb.equity.discovery.gainers(provider="yfinance")
        if gainers and gainers.results:
            print("   Top 5 Gainers:")
            for i, stock in enumerate(gainers.results[:5], 1):
                print(f"   {i}. {stock.symbol}: +{stock.change_percent:.2f}% (${stock.last_price:.2f})")
    except Exception as e:
        print(f"   Note: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("OpenBB Python SDK Demo")
    print("="*60)
    print("\nThis demonstrates using OpenBB programmatically.")
    print("Fetching live market data...\n")
    
    try:
        demo_equity_data()
        demo_crypto_data()
        demo_economic_data()
        demo_market_movers()
        
        print("\n" + "="*60)
        print("Demo Complete!")
        print("="*60)
        print("\nYou can use OpenBB in two ways:")
        print("1. CLI Mode: ./launch-openbb.sh (interactive terminal)")
        print("2. Python SDK: Import and use in Python scripts (as shown here)")
        print("\nFor CLI mode, see the tutorial in openbb-tutorial.md")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nNote: Some features may require API keys or market hours.")
        print(f"Error details: {e}")
