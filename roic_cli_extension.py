#!/usr/bin/env python3
"""
ROIC CLI Extension for OpenBB
Makes ROIC.ai data accessible through OpenBB-style commands
"""

import os
import sys
import json
from typing import Optional, List, Dict, Any
import pandas as pd
from datetime import datetime

# Add ROIC provider to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from openbb_roic_provider import roic_provider, roic_metrics, roic_forecast

class ROICExtension:
    """
    CLI extension that mimics OpenBB command structure
    """
    
    def __init__(self):
        self.provider = roic_provider
        
    def quality_metrics(self, symbol: str, export: Optional[str] = None) -> pd.DataFrame:
        """
        Get ROIC and quality metrics
        Usage: quality_metrics("AAPL")
        Mimics: /equity/fundamental/metrics --symbol AAPL --provider roic
        """
        data = roic_metrics(symbol)
        df = pd.DataFrame([data])
        
        # Display in CLI-friendly format
        print(f"\n{'='*60}")
        print(f"  ROIC.AI QUALITY METRICS: {symbol}")
        print('='*60)
        
        for col in df.columns:
            value = df[col].iloc[0]
            if value is not None:
                if col == 'roic':
                    print(f"Return on Invested Capital: {value:.2f}%")
                    self._print_quality_assessment(value)
                elif col == 'quality_score':
                    print(f"Quality Score: {value}/100")
                elif col == 'moat_rating':
                    print(f"Competitive Moat: {value}")
                elif col == 'fair_value' and isinstance(value, (int, float)):
                    print(f"Fair Value Estimate: ${value:.2f}")
                elif col == 'margin_of_safety' and isinstance(value, (int, float)):
                    print(f"Margin of Safety: {value:.1f}%")
        
        # Export if requested
        if export:
            self._export_data(df, symbol, "quality_metrics", export)
        
        return df
    
    def _print_quality_assessment(self, roic: float):
        """Print quality assessment based on ROIC"""
        if roic > 30:
            print(f"Quality Rating: ⭐⭐⭐⭐⭐ Exceptional")
            print("Investment Grade: A+ (Premium business)")
        elif roic > 20:
            print(f"Quality Rating: ⭐⭐⭐⭐⭐ Excellent")
            print("Investment Grade: A (High quality)")
        elif roic > 15:
            print(f"Quality Rating: ⭐⭐⭐⭐ Very Good")
            print("Investment Grade: B+ (Good quality)")
        elif roic > 10:
            print(f"Quality Rating: ⭐⭐⭐ Good")
            print("Investment Grade: B (Average quality)")
        elif roic > 5:
            print(f"Quality Rating: ⭐⭐ Fair")
            print("Investment Grade: C (Below average)")
        else:
            print(f"Quality Rating: ⭐ Poor")
            print("Investment Grade: D (Low quality)")
    
    def quality_forecast(self, symbol: str, export: Optional[str] = None) -> pd.DataFrame:
        """
        Get quality-based forecast
        Usage: quality_forecast("AAPL")
        Mimics: /equity/estimates/consensus --symbol AAPL --provider roic
        """
        data = roic_forecast(symbol)
        
        print(f"\n{'='*60}")
        print(f"  ROIC.AI QUALITY-BASED FORECAST: {symbol}")
        print('='*60)
        
        if data.get('current_price'):
            print(f"Current Price: ${data['current_price']:.2f}")
        
        if data.get('roic'):
            print(f"ROIC: {data['roic']:.2f}%")
        
        if data.get('quality_score'):
            print(f"Quality Score: {data['quality_score']}/100")
        
        if data.get('moat_rating'):
            print(f"Competitive Moat: {data['moat_rating']}")
        
        if data.get('implied_growth_rate'):
            print(f"\n📈 Implied Annual Growth: {data['implied_growth_rate']}%")
            
        print("\n💰 Quality-Based Price Targets:")
        if data.get('1_year_target'):
            print(f"  1 Year: ${data['1_year_target']:.2f}")
        if data.get('2_year_target'):
            print(f"  2 Years: ${data['2_year_target']:.2f}")
        if data.get('3_year_target'):
            print(f"  3 Years: ${data['3_year_target']:.2f}")
        
        df = pd.DataFrame([data])
        
        if export:
            self._export_data(df, symbol, "quality_forecast", export)
        
        return df
    
    def compare_quality(self, symbols: List[str], export: Optional[str] = None) -> pd.DataFrame:
        """
        Compare quality metrics across multiple symbols
        Usage: compare_quality(["AAPL", "MSFT", "GOOGL"])
        """
        results = []
        
        print(f"\n{'='*70}")
        print(f"  ROIC.AI QUALITY COMPARISON")
        print('='*70)
        
        for symbol in symbols:
            print(f"\nAnalyzing {symbol}...")
            data = roic_metrics(symbol)
            data['symbol'] = symbol
            results.append(data)
        
        df = pd.DataFrame(results)
        
        # Sort by ROIC
        if 'roic' in df.columns:
            df = df.sort_values('roic', ascending=False)
        
        # Display comparison table
        print("\n" + "="*70)
        print("QUALITY RANKINGS")
        print("="*70)
        
        for idx, row in df.iterrows():
            symbol = row['symbol']
            roic = row.get('roic', 0)
            quality = row.get('quality_score', 0)
            moat = row.get('moat_rating', 'Unknown')
            
            if roic:
                print(f"\n{symbol}:")
                print(f"  ROIC: {roic:.2f}%")
                print(f"  Quality Score: {quality}/100")
                print(f"  Moat: {moat}")
        
        if export:
            self._export_data(df, "comparison", "quality_comparison", export)
        
        return df
    
    def _export_data(self, df: pd.DataFrame, symbol: str, report_type: str, format: str):
        """Export data to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_{report_type}_{timestamp}"
        
        if format.lower() == 'csv':
            filepath = f"{filename}.csv"
            df.to_csv(filepath, index=False)
            print(f"\n✅ Data exported to: {filepath}")
        elif format.lower() == 'json':
            filepath = f"{filename}.json"
            df.to_json(filepath, orient='records', indent=2)
            print(f"\n✅ Data exported to: {filepath}")
        elif format.lower() == 'xlsx':
            filepath = f"{filename}.xlsx"
            df.to_excel(filepath, index=False)
            print(f"\n✅ Data exported to: {filepath}")


# Create global instance
roic_cli = ROICExtension()


# CLI-compatible functions
def cli_quality(symbol: str, export: Optional[str] = None):
    """CLI command: Get quality metrics"""
    return roic_cli.quality_metrics(symbol, export)


def cli_forecast(symbol: str, export: Optional[str] = None):
    """CLI command: Get quality-based forecast"""
    return roic_cli.quality_forecast(symbol, export)


def cli_compare(*symbols, export: Optional[str] = None):
    """CLI command: Compare quality across symbols"""
    return roic_cli.compare_quality(list(symbols), export)


if __name__ == "__main__":
    # Handle command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='ROIC.AI CLI Extension for OpenBB')
    parser.add_argument('command', choices=['quality', 'forecast', 'compare'],
                        help='Command to execute')
    parser.add_argument('symbols', nargs='+',
                        help='Stock symbol(s) to analyze')
    parser.add_argument('--export', choices=['csv', 'json', 'xlsx'],
                        help='Export format')
    
    args = parser.parse_args()
    
    if args.command == 'quality':
        cli_quality(args.symbols[0], args.export)
    elif args.command == 'forecast':
        cli_forecast(args.symbols[0], args.export)
    elif args.command == 'compare':
        cli_compare(*args.symbols, export=args.export)
