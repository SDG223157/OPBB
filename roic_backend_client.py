#!/usr/bin/env python3
"""
OpenBB ROIC Backend Client - Example usage
Shows how to interact with the ROIC Backend API
"""

import requests
import json
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

class ROICBackendClient:
    """Client for OpenBB ROIC Backend API"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
    
    def get_root_info(self) -> Dict[str, Any]:
        """Get API information"""
        response = self.session.get(f"{self.base_url}/")
        return response.json()
    
    def get_widgets(self) -> Dict[str, Any]:
        """Get widgets configuration"""
        response = self.session.get(f"{self.base_url}/widgets.json")
        return response.json()
    
    def get_roic_metrics(self, symbol: str) -> Dict[str, Any]:
        """Get ROIC quality metrics"""
        response = self.session.get(f"{self.base_url}/api/v1/roic/metrics/{symbol}")
        return response.json()
    
    def get_roic_forecast(self, symbol: str, years: int = 3) -> Dict[str, Any]:
        """Get quality-based forecast"""
        response = self.session.get(
            f"{self.base_url}/api/v1/roic/forecast/{symbol}",
            params={"years": years}
        )
        return response.json()
    
    def get_complete_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get combined OpenBB + ROIC analysis"""
        response = self.session.get(f"{self.base_url}/api/v1/analysis/complete/{symbol}")
        return response.json()
    
    def compare_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """Compare multiple stocks"""
        response = self.session.post(
            f"{self.base_url}/api/v1/analysis/compare",
            json={"symbols": symbols}
        )
        return response.json()
    
    def display_analysis(self, symbol: str):
        """Display formatted analysis for a symbol"""
        analysis = self.get_complete_analysis(symbol)
        
        # Create main panel
        console.print(Panel.fit(
            f"[bold cyan]Complete Analysis: {symbol}[/bold cyan]",
            box=box.DOUBLE
        ))
        
        # OpenBB Metrics Table
        openbb_table = Table(title="OpenBB Metrics", box=box.ROUNDED)
        openbb_table.add_column("Metric", style="cyan")
        openbb_table.add_column("Value", style="green")
        
        for key, value in analysis.get("openbb", {}).items():
            if value is not None:
                formatted_value = f"{value:,.2f}" if isinstance(value, (int, float)) else str(value)
                openbb_table.add_row(key.replace("_", " ").title(), formatted_value)
        
        console.print(openbb_table)
        
        # ROIC Metrics Table
        roic_table = Table(title="ROIC Quality Metrics", box=box.ROUNDED)
        roic_table.add_column("Metric", style="cyan")
        roic_table.add_column("Value", style="magenta")
        
        for key, value in analysis.get("roic", {}).items():
            if value is not None:
                if "target" in key:
                    formatted_value = f"${value:,.2f}"
                elif key == "roic":
                    formatted_value = f"{value:.2f}%"
                elif key == "quality_score":
                    formatted_value = f"{value}/100"
                else:
                    formatted_value = str(value)
                roic_table.add_row(key.replace("_", " ").title(), formatted_value)
        
        console.print(roic_table)
        
        # Combined Score
        if analysis.get("combined_score"):
            console.print(Panel(
                f"[bold yellow]Combined Score: {analysis['combined_score']:.1f}/100[/bold yellow]",
                box=box.DOUBLE
            ))
    
    def display_comparison(self, symbols: List[str]):
        """Display stock comparison"""
        comparison = self.compare_stocks(symbols)
        
        # Create comparison table
        table = Table(
            title=f"Stock Comparison: {', '.join(symbols)}",
            box=box.ROUNDED
        )
        
        table.add_column("Symbol", style="cyan", justify="center")
        table.add_column("ROIC %", style="green", justify="right")
        table.add_column("Quality", style="magenta", justify="center")
        table.add_column("P/E", style="yellow", justify="right")
        table.add_column("Score", style="bold white", justify="center")
        
        for stock in comparison.get("comparison", []):
            roic = f"{stock['roic']:.1f}%" if stock.get('roic') else "N/A"
            quality = f"{stock['quality_score']}/100" if stock.get('quality_score') else "N/A"
            pe = f"{stock['pe_ratio']:.1f}" if stock.get('pe_ratio') else "N/A"
            score = f"{stock['combined_score']:.1f}" if stock.get('combined_score') else "N/A"
            
            table.add_row(
                stock['symbol'],
                roic,
                quality,
                pe,
                score
            )
        
        console.print(table)
        
        if comparison.get("best_overall"):
            console.print(Panel(
                f"[bold green]Best Overall: {comparison['best_overall']}[/bold green]",
                box=box.DOUBLE
            ))

def main():
    """Example usage of the ROIC Backend Client"""
    
    # Initialize client
    client = ROICBackendClient()
    
    console.print("[bold cyan]OpenBB ROIC Backend Client[/bold cyan]\n")
    
    # Check if server is running
    try:
        info = client.get_root_info()
        console.print(f"✅ Connected to: {info['name']} v{info['version']}\n")
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Backend server not running![/red]")
        console.print("[yellow]Start it with: ./launch_roic_backend.sh[/yellow]")
        return
    
    # Example 1: Single stock analysis
    console.print("[bold]Example 1: Apple Analysis[/bold]")
    client.display_analysis("AAPL")
    
    # Example 2: Stock comparison
    console.print("\n[bold]Example 2: Tech Giants Comparison[/bold]")
    client.display_comparison(["AAPL", "MSFT", "GOOGL", "NVDA"])
    
    # Example 3: Get widgets configuration
    console.print("\n[bold]Example 3: Available Widgets[/bold]")
    widgets = client.get_widgets()
    for widget_id, config in widgets.items():
        console.print(f"  • {config['title']} ({config['type']})")
    
    console.print("\n[dim]API Docs available at: http://127.0.0.1:8000/docs[/dim]")

if __name__ == "__main__":
    main()
