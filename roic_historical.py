#!/usr/bin/env python3
"""
ROIC Historical Analysis - 10-year quality metrics
Supports international stocks including Chinese (SSE/SZSE)
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Add virtual environment packages
sys.path.insert(0, '/Users/sdg223157/OPBB')

def calculate_historical_roic(symbol: str, years: int = 10) -> pd.DataFrame:
    """
    Calculate historical ROIC for the past N years
    """
    from openbb import obb
    
    print(f"\n{'='*80}")
    print(f"  📊 HISTORICAL ROIC ANALYSIS: {symbol}")
    if symbol == "600519.SS":
        print(f"  贵州茅台 (Kweichow Moutai)")
    print(f"  Period: {years} Years")
    print('='*80)
    
    results = []
    current_year = datetime.now().year
    
    # Get historical financial statements
    try:
        print(f"\n⏳ Fetching {years} years of financial data...")
        
        # Get income statements (Yahoo limits to 5 years)
        max_limit = min(years, 5)
        income = obb.equity.fundamental.income(
            symbol=symbol, 
            provider='yfinance',
            period='annual',
            limit=max_limit
        )
        
        # Get balance sheets (Yahoo limits to 5 years)
        balance = obb.equity.fundamental.balance(
            symbol=symbol,
            provider='yfinance', 
            period='annual',
            limit=max_limit
        )
        
        if income and income.results and balance and balance.results:
            print(f"✅ Retrieved {len(income.results)} years of income statements")
            print(f"✅ Retrieved {len(balance.results)} years of balance sheets")
            
            # Match income and balance sheet data by year
            for i in range(min(len(income.results), len(balance.results))):
                income_stmt = income.results[i]
                balance_stmt = balance.results[i]
                
                year_data = {
                    'year': None,
                    'revenue': None,
                    'operating_income': None,
                    'net_income': None,
                    'total_assets': None,
                    'current_liabilities': None,
                    'roic': None,
                    'profit_margin': None,
                    'asset_turnover': None
                }
                
                # Get year
                if hasattr(income_stmt, 'period_ending'):
                    year_data['year'] = income_stmt.period_ending.year
                elif hasattr(income_stmt, 'date'):
                    year_data['year'] = income_stmt.date.year
                else:
                    year_data['year'] = current_year - i
                
                # Get financial metrics
                if hasattr(income_stmt, 'total_revenue'):
                    year_data['revenue'] = income_stmt.total_revenue
                
                if hasattr(income_stmt, 'operating_income'):
                    year_data['operating_income'] = income_stmt.operating_income
                
                if hasattr(income_stmt, 'net_income'):
                    year_data['net_income'] = income_stmt.net_income
                
                if hasattr(balance_stmt, 'total_assets'):
                    year_data['total_assets'] = balance_stmt.total_assets
                
                if hasattr(balance_stmt, 'current_liabilities'):
                    year_data['current_liabilities'] = balance_stmt.current_liabilities
                
                # Calculate ROIC
                if year_data['operating_income'] and year_data['total_assets'] and year_data['current_liabilities']:
                    # NOPAT = Operating Income * (1 - Tax Rate)
                    # Estimate tax rate at 25% for Chinese companies
                    nopat = year_data['operating_income'] * 0.75
                    
                    # Invested Capital = Total Assets - Current Liabilities
                    invested_capital = year_data['total_assets'] - year_data['current_liabilities']
                    
                    if invested_capital > 0:
                        year_data['roic'] = (nopat / invested_capital) * 100
                
                # Calculate profit margin
                if year_data['net_income'] and year_data['revenue']:
                    year_data['profit_margin'] = (year_data['net_income'] / year_data['revenue']) * 100
                
                # Calculate asset turnover
                if year_data['revenue'] and year_data['total_assets']:
                    year_data['asset_turnover'] = year_data['revenue'] / year_data['total_assets']
                
                results.append(year_data)
        
        # Also get historical price data for context
        if len(results) > 0 and years > 5:
            print(f"\n📊 Note: Fundamental data limited to {len(results)} years")
            print("Fetching price history for context...")
            
            try:
                start_date = datetime.now() - timedelta(days=365 * years)
                hist = obb.equity.price.historical(
                    symbol=symbol,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    interval='1mo',
                    provider='yfinance'
                )
                
                if hist and hist.results:
                    # Get yearly price points
                    yearly_prices = {}
                    for price_data in hist.results:
                        year = price_data.date.year
                        if year not in yearly_prices:
                            yearly_prices[year] = {
                                'high': price_data.high,
                                'low': price_data.low,
                                'close': price_data.close
                            }
                    
                    print(f"✅ Retrieved {len(yearly_prices)} years of price data")
                    
                    # Add price data to results
                    for result in results:
                        year = result.get('year')
                        if year in yearly_prices:
                            result['stock_price'] = yearly_prices[year]['close']
            except:
                pass
                
    except Exception as e:
        print(f"Error fetching financial data: {str(e)[:200]}")
        
        # Try alternative calculation method
        print("\n📈 Attempting simplified calculation...")
        try:
            # Get key statistics
            stats = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
            if stats and stats.results:
                current_data = stats.results[0]
                
                # Add current year data
                year_data = {
                    'year': current_year,
                    'roic': None,
                    'profit_margin': None,
                    'return_on_equity': None
                }
                
                if hasattr(current_data, 'return_on_equity'):
                    year_data['return_on_equity'] = current_data.return_on_equity * 100
                
                if hasattr(current_data, 'profit_margin'):
                    year_data['profit_margin'] = current_data.profit_margin * 100
                
                # Estimate ROIC from ROE
                if year_data['return_on_equity']:
                    year_data['roic'] = year_data['return_on_equity'] * 0.8  # Conservative estimate
                
                results.append(year_data)
                
        except Exception as e2:
            print(f"Alternative method also failed: {str(e2)[:100]}")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Sort by year
    if not df.empty and 'year' in df.columns:
        df = df.sort_values('year')
    
    return df

def display_historical_roic(symbol: str, years: int = 10):
    """
    Display historical ROIC analysis with quality trends
    """
    df = calculate_historical_roic(symbol, years)
    
    if df.empty:
        print("\n❌ No historical data available")
        return df
    
    # Display results
    print("\n" + "="*80)
    print("📊 HISTORICAL ROIC ANALYSIS")
    print("="*80)
    
    for _, row in df.iterrows():
        year = row.get('year', 'N/A')
        roic = row.get('roic')
        profit_margin = row.get('profit_margin')
        
        print(f"\n📅 Year {year}:")
        print("-" * 40)
        
        if roic:
            print(f"ROIC: {roic:.2f}%", end="")
            
            # Quality assessment
            if roic > 30:
                print(" ⭐⭐⭐⭐⭐ Exceptional")
            elif roic > 20:
                print(" ⭐⭐⭐⭐⭐ Excellent")
            elif roic > 15:
                print(" ⭐⭐⭐⭐ Very Good")
            elif roic > 10:
                print(" ⭐⭐⭐ Good")
            else:
                print(" ⭐⭐ Fair")
        
        if profit_margin:
            print(f"Profit Margin: {profit_margin:.1f}%")
        
        if row.get('revenue'):
            revenue_b = row['revenue'] / 1e9
            print(f"Revenue: ¥{revenue_b:.1f}B CNY")
        
        if row.get('net_income'):
            income_b = row['net_income'] / 1e9
            print(f"Net Income: ¥{income_b:.1f}B CNY")
    
    # Calculate trends
    print("\n" + "="*80)
    print("📈 TREND ANALYSIS")
    print("="*80)
    
    if 'roic' in df.columns:
        roic_values = df['roic'].dropna()
        if len(roic_values) > 0:
            avg_roic = roic_values.mean()
            latest_roic = roic_values.iloc[-1] if len(roic_values) > 0 else None
            
            print(f"\nAverage ROIC ({len(roic_values)} years): {avg_roic:.2f}%")
            
            if latest_roic:
                print(f"Latest ROIC: {latest_roic:.2f}%")
                
                if len(roic_values) > 1:
                    first_roic = roic_values.iloc[0]
                    change = latest_roic - first_roic
                    
                    if change > 0:
                        print(f"Trend: ↗️ Improving (+{change:.1f}% over period)")
                    elif change < -5:
                        print(f"Trend: ↘️ Declining ({change:.1f}% over period)")
                    else:
                        print(f"Trend: → Stable (±{abs(change):.1f}% over period)")
            
            # Quality consistency
            high_quality_years = len(roic_values[roic_values > 20])
            consistency = (high_quality_years / len(roic_values)) * 100
            
            print(f"\nQuality Consistency:")
            print(f"Years with ROIC > 20%: {high_quality_years}/{len(roic_values)} ({consistency:.0f}%)")
            
            if consistency > 80:
                print("Assessment: ✅ Consistently High Quality Business")
            elif consistency > 50:
                print("Assessment: ⚠️ Generally Good Quality")
            else:
                print("Assessment: ❌ Quality Concerns")
    
    # Special notes for Chinese stocks
    if symbol.endswith('.SS') or symbol.endswith('.SZ'):
        print("\n" + "="*80)
        print("📝 NOTES FOR CHINESE STOCKS")
        print("="*80)
        print("""
• Data availability may be limited for older years
• Financial reporting standards differ from US GAAP
• Currency: Chinese Yuan (CNY/RMB)
• Tax rates typically 25% for mainland companies
• Consider state ownership and policy impacts
""")
        
        if symbol == "600519.SS":
            print("""
🥃 KWEICHOW MOUTAI SPECIFIC:
• Premium baijiu producer with pricing power
• High margins due to brand prestige
• Limited supply drives scarcity value
• Government relations important for business
• Compare with Wuliangye (000858.SZ) for context
""")
    
    return df

def export_historical_roic(symbol: str, years: int = 10, format: str = 'csv'):
    """
    Export historical ROIC data
    """
    df = calculate_historical_roic(symbol, years)
    
    if not df.empty:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_historical_roic_{years}y_{timestamp}.{format}"
        
        if format == 'csv':
            df.to_csv(filename, index=False)
        elif format == 'xlsx':
            df.to_excel(filename, index=False)
        elif format == 'json':
            df.to_json(filename, orient='records', indent=2)
        
        print(f"\n✅ Data exported to: {filename}")
        return filename
    
    return None

if __name__ == "__main__":
    # Test with Kweichow Moutai
    symbol = "600519.SS"
    
    print("="*80)
    print(" "*20 + "ROIC HISTORICAL ANALYSIS TOOL")
    print("="*80)
    
    # Run 10-year analysis
    display_historical_roic(symbol, years=10)
    
    # Export option
    print("\n" + "="*80)
    print("EXPORT OPTIONS")
    print("="*80)
    print("""
To export this data:
python roic_historical.py --export csv
python roic_historical.py --export xlsx
python roic_historical.py --export json
""")
    
    # Check for export flag
    if len(sys.argv) > 1 and '--export' in sys.argv:
        export_idx = sys.argv.index('--export')
        if export_idx + 1 < len(sys.argv):
            format = sys.argv[export_idx + 1]
            export_historical_roic(symbol, years=10, format=format)
