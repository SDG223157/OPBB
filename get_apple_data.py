#!/usr/bin/env python3
"""Get Apple (AAPL) Stock Data"""

from openbb import obb
import pandas as pd
from datetime import datetime, timedelta

print('='*60)
print('APPLE (AAPL) STOCK DATA')
print('='*60)

# Get current quote
print('\n📊 CURRENT QUOTE:')
print('-'*40)
try:
    quote = obb.equity.price.quote(symbol='AAPL', provider='yfinance')
    if quote and quote.results:
        data = quote.results[0]
        print(f'Symbol: {data.symbol}')
        print(f'Company: Apple Inc.')
        print(f'Last Price: ${data.last_price:.2f}')
        if data.open:
            print(f'Open: ${data.open:.2f}')
        if data.high:
            print(f'Day High: ${data.high:.2f}')
        if data.low:
            print(f'Day Low: ${data.low:.2f}')
        if data.volume:
            print(f'Volume: {data.volume:,}')
        if data.previous_close:
            print(f'Previous Close: ${data.previous_close:.2f}')
        # Calculate change
        if data.previous_close and data.last_price:
            change = data.last_price - data.previous_close
            change_pct = (change / data.previous_close) * 100
            print(f'Change: ${change:.2f} ({change_pct:+.2f}%)')
except Exception as e:
    print(f'Error fetching quote: {e}')

# Get recent historical data
print('\n📈 RECENT PRICE HISTORY (Last 10 Trading Days):')
print('-'*40)
try:
    start_date = (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')
    hist = obb.equity.price.historical(
        symbol='AAPL',
        start_date=start_date,
        provider='yfinance'
    )
    if hist and hist.results:
        df = pd.DataFrame([d.model_dump() for d in hist.results[-10:]])
        # Format the dataframe for better display
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['change'] = df['close'] - df['open']
        df['change_pct'] = (df['change'] / df['open'] * 100)
        
        # Display table
        for _, row in df.iterrows():
            print(f"{row['date']}  "
                  f"Open: ${row['open']:.2f}  "
                  f"Close: ${row['close']:.2f}  "
                  f"High: ${row['high']:.2f}  "
                  f"Low: ${row['low']:.2f}  "
                  f"Vol: {row['volume']/1e6:.1f}M  "
                  f"Chg: {row['change_pct']:+.2f}%")
        
        # Calculate some statistics
        print('\n📊 STATISTICS (Last 10 Days):')
        print('-'*40)
        print(f'Average Close: ${df["close"].mean():.2f}')
        print(f'Highest Close: ${df["close"].max():.2f} on {df.loc[df["close"].idxmax(), "date"]}')
        print(f'Lowest Close: ${df["close"].min():.2f} on {df.loc[df["close"].idxmin(), "date"]}')
        print(f'Average Volume: {df["volume"].mean()/1e6:.1f}M shares')
        print(f'Total Volume: {df["volume"].sum()/1e6:.1f}M shares')
        
        # Calculate simple returns
        returns = df['close'].pct_change().dropna()
        if len(returns) > 0:
            print(f'Average Daily Return: {returns.mean()*100:.2f}%')
            print(f'Volatility (Std Dev): {returns.std()*100:.2f}%')
            
            # Trend analysis
            first_close = df.iloc[0]['close']
            last_close = df.iloc[-1]['close']
            period_return = ((last_close - first_close) / first_close) * 100
            print(f'10-Day Return: {period_return:+.2f}%')
            
            # Simple moving average
            if len(df) >= 5:
                df['SMA_5'] = df['close'].rolling(window=5).mean()
                current_sma = df['SMA_5'].iloc[-1]
                if pd.notna(current_sma):
                    print(f'5-Day Moving Average: ${current_sma:.2f}')
        
except Exception as e:
    print(f'Error fetching historical data: {e}')

# Get company fundamentals
print('\n💼 KEY FUNDAMENTALS:')
print('-'*40)
try:
    # Try to get additional company info
    profile = obb.equity.profile(symbol='AAPL', provider='yfinance')
    if profile and profile.results:
        info = profile.results[0]
        if hasattr(info, 'market_cap') and info.market_cap:
            print(f'Market Cap: ${info.market_cap/1e12:.2f}T')
        if hasattr(info, 'employees') and info.employees:
            print(f'Employees: {info.employees:,}')
        if hasattr(info, 'sector'):
            print(f'Sector: {info.sector}')
        if hasattr(info, 'industry'):
            print(f'Industry: {info.industry}')
except:
    pass

print('\n' + '='*60)
print('Data provided by Yahoo Finance via OpenBB')
print('='*60)
