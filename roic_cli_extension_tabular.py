#!/usr/bin/env python3
"""
ROIC CLI Extension - Tabular Output Version
Displays data in OpenBB-style tables like other APIs
"""

import sys
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import json

# Import the original ROIC provider
from openbb_roic_provider import roic_provider, roic_metrics, roic_forecast

console = Console()

class ROICTabularExtension:
    """
    CLI extension with OpenBB-style tabular output
    """
    
    def __init__(self):
        self.provider = roic_provider
        
    def quality_metrics_table(self, symbol: str, export: Optional[str] = None) -> pd.DataFrame:
        """
        Get ROIC metrics in OpenBB-style table format
        """
        data = roic_metrics(symbol)
        
        # Create Rich table like OpenBB
        table = Table(
            title=f"[bold cyan]ROIC Quality Metrics - {symbol}[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        # Add columns
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_column("Assessment", style="yellow")
        
        # Add rows
        if data.get('roic'):
            roic_val = data['roic']
            quality = self._get_quality_assessment(roic_val)
            table.add_row("Return on Invested Capital", f"{roic_val:.2f}%", quality)
        
        if data.get('quality_score'):
            table.add_row("Quality Score", f"{data['quality_score']}/100", self._get_score_rating(data['quality_score']))
        
        if data.get('moat_rating'):
            moat_emoji = "🏰" if data['moat_rating'] == "Wide" else "🛡️" if data['moat_rating'] == "Narrow" else "❌"
            table.add_row("Competitive Moat", data['moat_rating'], moat_emoji)
        
        table.add_row("Provider", "ROIC.ai", "✓")
        table.add_row("Date", datetime.now().strftime("%Y-%m-%d"), "Current")
        
        # Display table
        console.print(table)
        
        # Also create DataFrame for export
        df = pd.DataFrame([data])
        
        # Display as OpenBB-style DataFrame
        if not df.empty:
            print("\n" + "─" * 60)
            print(df.to_string(index=False))
            print("─" * 60)
        
        if export:
            self._export_data(df, symbol, "quality_metrics", export)
        
        return df
    
    def _get_quality_assessment(self, roic: float) -> str:
        """Get quality assessment with stars"""
        if roic > 30:
            return "⭐⭐⭐⭐⭐ Exceptional"
        elif roic > 20:
            return "⭐⭐⭐⭐⭐ Excellent"
        elif roic > 15:
            return "⭐⭐⭐⭐ Very Good"
        elif roic > 10:
            return "⭐⭐⭐ Good"
        elif roic > 5:
            return "⭐⭐ Fair"
        else:
            return "⭐ Poor"
    
    def _get_score_rating(self, score: int) -> str:
        """Get rating based on quality score"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        else:
            return "D"
    
    def forecast_table(self, symbol: str, export: Optional[str] = None) -> pd.DataFrame:
        """
        Display forecast in OpenBB-style table
        """
        data = roic_forecast(symbol)
        
        # Create forecast table
        table = Table(
            title=f"[bold cyan]ROIC Quality-Based Forecast - {symbol}[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")
        table.add_column("Change %", style="yellow", justify="right")
        
        current_price = data.get('current_price', 0)
        
        # Add current metrics
        if current_price:
            table.add_row("Current Price", f"${current_price:.2f}", "")
        
        if data.get('roic'):
            table.add_row("ROIC", f"{data['roic']:.2f}%", "")
        
        if data.get('implied_growth_rate'):
            table.add_row("Implied Growth Rate", f"{data['implied_growth_rate']}%", "Annual")
        
        # Add forecasts
        if data.get('1_year_target'):
            change_1y = ((data['1_year_target'] - current_price) / current_price * 100) if current_price else 0
            table.add_row("1 Year Target", f"${data['1_year_target']:.2f}", f"+{change_1y:.1f}%")
        
        if data.get('2_year_target'):
            change_2y = ((data['2_year_target'] - current_price) / current_price * 100) if current_price else 0
            table.add_row("2 Year Target", f"${data['2_year_target']:.2f}", f"+{change_2y:.1f}%")
        
        if data.get('3_year_target'):
            change_3y = ((data['3_year_target'] - current_price) / current_price * 100) if current_price else 0
            table.add_row("3 Year Target", f"${data['3_year_target']:.2f}", f"+{change_3y:.1f}%")
        
        console.print(table)
        
        # Create DataFrame
        forecast_df = pd.DataFrame({
            'Period': ['Current', '1 Year', '2 Years', '3 Years'],
            'Price': [
                current_price,
                data.get('1_year_target', 0),
                data.get('2_year_target', 0),
                data.get('3_year_target', 0)
            ],
            'ROIC': [data.get('roic', 0)] * 4,
            'Growth_Rate': [data.get('implied_growth_rate', 0)] * 4
        })
        
        print("\n" + "─" * 60)
        print(forecast_df.to_string(index=False))
        print("─" * 60)
        
        if export:
            self._export_data(forecast_df, symbol, "forecast", export)
        
        return forecast_df
    
    def compare_table(self, symbols: List[str], export: Optional[str] = None) -> pd.DataFrame:
        """
        Compare stocks in OpenBB-style table
        """
        results = []
        
        for symbol in symbols:
            data = roic_metrics(symbol)
            data['Symbol'] = symbol
            results.append(data)
        
        df = pd.DataFrame(results)
        
        # Reorder columns
        col_order = ['Symbol', 'roic', 'quality_score', 'moat_rating']
        available_cols = [col for col in col_order if col in df.columns]
        df = df[available_cols + [col for col in df.columns if col not in available_cols]]
        
        # Sort by ROIC
        if 'roic' in df.columns:
            df = df.sort_values('roic', ascending=False)
        
        # Create comparison table
        table = Table(
            title="[bold cyan]ROIC Quality Comparison[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Symbol", style="cyan")
        table.add_column("ROIC %", style="green", justify="right")
        table.add_column("Quality Score", style="yellow", justify="center")
        table.add_column("Moat", style="magenta")
        table.add_column("Grade", style="white")
        
        for _, row in df.iterrows():
            symbol = row.get('Symbol', '')
            roic = row.get('roic', 0)
            quality = row.get('quality_score', 0)
            moat = row.get('moat_rating', 'Unknown')
            
            grade = self._get_score_rating(quality) if quality else "N/A"
            
            table.add_row(
                symbol,
                f"{roic:.2f}" if roic else "N/A",
                f"{quality}/100" if quality else "N/A",
                moat,
                grade
            )
        
        console.print(table)
        
        # Also display as DataFrame
        print("\n" + "─" * 80)
        print("DataFrame Output (OpenBB Style):")
        print("─" * 80)
        display_df = df[['Symbol', 'roic', 'quality_score', 'moat_rating']].copy()
        display_df.columns = ['Symbol', 'ROIC_%', 'Quality_Score', 'Moat']
        print(display_df.to_string(index=False))
        print("─" * 80)
        
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
            console.print(f"\n[green]✅ Data exported to: {filepath}[/green]")
        elif format.lower() == 'json':
            filepath = f"{filename}.json"
            df.to_json(filepath, orient='records', indent=2)
            console.print(f"\n[green]✅ Data exported to: {filepath}[/green]")
        elif format.lower() == 'xlsx':
            filepath = f"{filename}.xlsx"
            df.to_excel(filepath, index=False)
            console.print(f"\n[green]✅ Data exported to: {filepath}[/green]")

# Create instance
roic_tabular = ROICTabularExtension()

# CLI functions
def cli_quality_table(symbol: str, export: Optional[str] = None):
    """Get quality metrics in table format"""
    return roic_tabular.quality_metrics_table(symbol, export)

def cli_forecast_table(symbol: str, export: Optional[str] = None):
    """Get forecast in table format"""
    return roic_tabular.forecast_table(symbol, export)

def cli_compare_table(*symbols, export: Optional[str] = None):
    """Compare stocks in table format"""
    return roic_tabular.compare_table(list(symbols), export)

if __name__ == "__main__":
    # Test the tabular display
    print("\n" + "="*80)
    print("ROIC TABULAR DISPLAY TEST")
    print("="*80)
    
    # Test quality metrics
    print("\n1. Quality Metrics (OpenBB Style):")
    cli_quality_table("AAPL")
    
    # Test forecast
    print("\n2. Forecast Table:")
    cli_forecast_table("AAPL")
    
    # Test comparison
    print("\n3. Comparison Table:")
    cli_compare_table("AAPL", "MSFT", "GOOGL")
