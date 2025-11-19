#!/usr/bin/env python3
"""
Get Chinese Stock Data - Example: Kweichow Moutai (600519.SS)
Shanghai Stock Exchange listing analysis
"""

from openbb import obb
import os
from datetime import datetime, timedelta

# Set API keys
os.environ['POLYGON_API_KEY'] = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
os.environ['FINVIZ_API_KEY'] = 'be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6'
os.environ['FRED_API_KEY'] = '7c26de454d31a77bfdf9aaa33f2f55a8'

obb.user.credentials.polygon_api_key = 'Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai'
obb.user.credentials.finviz_api_key = 'be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6'
obb.user.credentials.fred_api_key = '7c26de454d31a77bfdf9aaa33f2f55a8'

def get_chinese_stock_data(symbol):
    """
    Get data for Chinese stocks (Shanghai .SS or Shenzhen .SZ)
    """
    
    print(f"\n{'='*80}")
    print(f"  📊 CHINESE STOCK ANALYSIS: {symbol}")
    if symbol == "600519.SS":
        print("  贵州茅台 (Kweichow Moutai) - Premium Baijiu Producer")
    print('='*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*80)
    
    # Note: Chinese stocks may have limited data availability through some providers
    # YFinance typically has the best coverage for Asian markets
    
    # 1. Try to get current quote
    print("\n💹 CURRENT MARKET DATA")
    print("-"*60)
    
    current_price = None
    currency = "CNY"
    
    try:
        # YFinance is best for Chinese stocks
        quote = obb.equity.price.quote(symbol=symbol, provider='yfinance')
        if quote and quote.results:
            data = quote.results[0]
            current_price = data.last_price
            
            print(f"Symbol: {symbol}")
            print(f"Exchange: Shanghai Stock Exchange")
            print(f"Last Price: ¥{current_price:.2f} CNY")
            
            if hasattr(data, 'open') and data.open:
                print(f"Open: ¥{data.open:.2f}")
            if hasattr(data, 'high') and data.high:
                print(f"Day High: ¥{data.high:.2f}")
            if hasattr(data, 'low') and data.low:
                print(f"Day Low: ¥{data.low:.2f}")
            if hasattr(data, 'volume') and data.volume:
                print(f"Volume: {data.volume:,.0f}")
            if hasattr(data, 'previous_close') and data.previous_close:
                print(f"Previous Close: ¥{data.previous_close:.2f}")
                
                if current_price and data.previous_close:
                    change = current_price - data.previous_close
                    change_pct = (change / data.previous_close) * 100
                    print(f"Change: ¥{change:.2f} ({change_pct:+.2f}%)")
    
    except Exception as e:
        print(f"Note: Real-time quote not available - {str(e)[:100]}")
        print("\nTrying alternative data source...")
    
    # 2. Get historical data
    print("\n📈 HISTORICAL PRICE DATA (Last 30 Days)")
    print("-"*60)
    
    try:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        hist = obb.equity.price.historical(
            symbol=symbol,
            start_date=start_date,
            provider='yfinance'
        )
        
        if hist and hist.results:
            print(f"Successfully retrieved {len(hist.results)} days of data")
            
            # Show recent 5 days
            print("\nRecent 5 Trading Days:")
            for data in hist.results[-5:]:
                date = data.date.strftime('%Y-%m-%d') if hasattr(data.date, 'strftime') else str(data.date)[:10]
                print(f"{date}: Open ¥{data.open:.2f}, Close ¥{data.close:.2f}, "
                      f"High ¥{data.high:.2f}, Low ¥{data.low:.2f}")
            
            # Calculate performance metrics
            first_close = hist.results[0].close
            last_close = hist.results[-1].close
            period_return = ((last_close - first_close) / first_close) * 100
            
            print(f"\n30-Day Performance: {period_return:+.2f}%")
            print(f"Starting Price: ¥{first_close:.2f}")
            print(f"Ending Price: ¥{last_close:.2f}")
            
    except Exception as e:
        print(f"Historical data error: {str(e)[:100]}")
    
    # 3. Get company profile
    print("\n🏢 COMPANY PROFILE")
    print("-"*60)
    
    try:
        profile = obb.equity.profile(symbol=symbol, provider='yfinance')
        if profile and profile.results:
            info = profile.results[0]
            
            if hasattr(info, 'name'):
                print(f"Company: {info.name}")
            if hasattr(info, 'sector'):
                print(f"Sector: {info.sector}")
            if hasattr(info, 'industry'):
                print(f"Industry: {info.industry}")
            if hasattr(info, 'market_cap') and info.market_cap:
                # Convert to billions CNY
                market_cap_b = info.market_cap / 1e9
                print(f"Market Cap: ¥{market_cap_b:.1f}B CNY")
            if hasattr(info, 'employees') and info.employees:
                print(f"Employees: {info.employees:,}")
            
            # Additional info for Moutai
            if symbol == "600519.SS":
                print("\n📝 Company Notes:")
                print("• China's most valuable liquor company")
                print("• Premium baijiu (Chinese liquor) producer")
                print("• Known as 'liquid gold' in China")
                print("• Often called the 'Hermès of China'")
                
    except Exception as e:
        print(f"Profile data not available: {str(e)[:100]}")
    
    # 4. Get fundamental data
    print("\n💰 FUNDAMENTAL METRICS")
    print("-"*60)
    
    try:
        fundamentals = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
        if fundamentals and fundamentals.results:
            metrics = fundamentals.results[0]
            
            if hasattr(metrics, 'pe_ratio') and metrics.pe_ratio:
                print(f"P/E Ratio: {metrics.pe_ratio:.2f}")
            if hasattr(metrics, 'forward_pe') and metrics.forward_pe:
                print(f"Forward P/E: {metrics.forward_pe:.2f}")
            if hasattr(metrics, 'peg_ratio') and metrics.peg_ratio:
                print(f"PEG Ratio: {metrics.peg_ratio:.2f}")
            if hasattr(metrics, 'dividend_yield') and metrics.dividend_yield:
                print(f"Dividend Yield: {metrics.dividend_yield:.2%}")
            if hasattr(metrics, 'profit_margin') and metrics.profit_margin:
                print(f"Profit Margin: {metrics.profit_margin:.2%}")
            if hasattr(metrics, 'return_on_equity') and metrics.return_on_equity:
                print(f"ROE: {metrics.return_on_equity:.2%}")
                
    except Exception as e:
        print(f"Fundamental data not available: {str(e)[:100]}")
    
    # 5. Alternative data sources for Chinese stocks
    print("\n📊 ADDITIONAL DATA SOURCES")
    print("-"*60)
    print("""
For comprehensive Chinese stock data, consider:

1. **Yahoo Finance Web**:
   https://finance.yahoo.com/quote/600519.SS

2. **Investing.com**:
   https://www.investing.com/equities/kweichow-moutai-co-ltd

3. **TradingView**:
   https://www.tradingview.com/symbols/SSE-600519/

4. **Direct Chinese Sources**:
   • Sina Finance (新浪财经): http://finance.sina.com.cn/
   • East Money (东方财富): https://www.eastmoney.com/
   • Xueqiu (雪球): https://xueqiu.com/

Note: Some Chinese stocks may have limited data through Western APIs.
YFinance typically provides the most comprehensive coverage.
""")
    
    return current_price

def main():
    print("="*80)
    print(" "*20 + "CHINESE STOCK DATA TOOL")
    print("="*80)
    
    # Example: Kweichow Moutai
    moutai_symbol = "600519.SS"
    
    print(f"\n🥃 Analyzing Kweichow Moutai ({moutai_symbol})...")
    get_chinese_stock_data(moutai_symbol)
    
    # Show how to analyze other Chinese stocks
    print("\n" + "="*80)
    print("OTHER POPULAR CHINESE STOCKS")
    print("="*80)
    
    chinese_stocks = {
        "600519.SS": "Kweichow Moutai (贵州茅台) - Liquor",
        "000858.SZ": "Wuliangye (五粮液) - Liquor",
        "000002.SZ": "China Vanke (万科) - Real Estate",
        "600036.SS": "China Merchants Bank (招商银行)",
        "000001.SZ": "Ping An Bank (平安银行)",
        "002594.SZ": "BYD (比亚迪) - Electric Vehicles",
        "300750.SZ": "CATL (宁德时代) - EV Batteries",
        "600900.SS": "China Yangtze Power (长江电力)",
        "601318.SS": "Ping An Insurance (中国平安)",
        "000333.SZ": "Midea Group (美的集团) - Appliances"
    }
    
    print("\nPopular Chinese stocks you can analyze:")
    for symbol, name in chinese_stocks.items():
        exchange = "Shanghai" if symbol.endswith(".SS") else "Shenzhen"
        print(f"  {symbol}: {name} ({exchange})")
    
    print("\n" + "="*80)
    print("HOW TO USE IN OPENBB CLI")
    print("="*80)
    print("""
# Launch OpenBB with APIs
./launch-openbb-premium.sh

# Get Chinese stock data (YFinance works best)
/equity/price/quote --symbol 600519.SS --provider yfinance
/equity/price/historical --symbol 600519.SS --provider yfinance
/equity/fundamental/income --symbol 600519.SS --provider yfinance
/equity/profile --symbol 600519.SS --provider yfinance

# Export data
/equity/price/historical --symbol 600519.SS --provider yfinance --export csv

# For other Chinese stocks:
/equity/price/quote --symbol 000858.SZ --provider yfinance  # Wuliangye
/equity/price/quote --symbol 002594.SZ --provider yfinance  # BYD
/equity/price/quote --symbol 300750.SZ --provider yfinance  # CATL

Note: Use .SS for Shanghai, .SZ for Shenzhen exchange stocks
""")

if __name__ == "__main__":
    main()
