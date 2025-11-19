#!/usr/bin/env python3
"""
ROIC CLI Wrapper - Runs with proper environment
"""

import sys
import os
from roic_cli_extension import cli_quality, cli_forecast, cli_compare
from roic_historical import display_historical_roic, export_historical_roic

# Check display style preference
try:
    from roic_style_config import get_display_style
    style = get_display_style()
    
    if style == "openbb":
        # Use OpenBB-style tabular display
        from roic_cli_extension_tabular import cli_quality_table, cli_forecast_table, cli_compare_table
        USE_TABULAR = True
    else:
        USE_TABULAR = False
except:
    USE_TABULAR = False

def main():
    if len(sys.argv) < 3:
        print("""
ROIC.AI Command Line Tool
========================

Usage:
  ./roic quality SYMBOL [--export FORMAT]    Get quality metrics
  ./roic forecast SYMBOL [--export FORMAT]   Get quality-based forecast
  ./roic compare SYM1 SYM2 ... [--export FORMAT]  Compare multiple stocks
  ./roic historical SYMBOL [--years N] [--export FORMAT]  Get historical ROIC
  ./roic style [openbb|custom]  Switch display style

Examples:
  ./roic quality AAPL
  ./roic forecast MSFT --export csv
  ./roic compare AAPL MSFT GOOGL NVDA
  ./roic historical 600519.SS --years 10
  ./roic style openbb  # Switch to OpenBB-style tables

Export formats: csv, json, xlsx
""")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Check for export flag
    export = None
    if '--export' in sys.argv:
        export_idx = sys.argv.index('--export')
        if export_idx + 1 < len(sys.argv):
            export = sys.argv[export_idx + 1]
            # Remove export args from list
            del sys.argv[export_idx:export_idx + 2]
    
    if command == 'quality':
        if len(sys.argv) >= 3:
            symbol = sys.argv[2].upper()
            if USE_TABULAR:
                cli_quality_table(symbol, export)
            else:
                cli_quality(symbol, export)
    
    elif command == 'forecast':
        if len(sys.argv) >= 3:
            symbol = sys.argv[2].upper()
            if USE_TABULAR:
                cli_forecast_table(symbol, export)
            else:
                cli_forecast(symbol, export)
    
    elif command == 'compare':
        if len(sys.argv) >= 3:
            symbols = [s.upper() for s in sys.argv[2:]]
            if USE_TABULAR:
                cli_compare_table(*symbols, export=export)
            else:
                cli_compare(*symbols, export=export)
    
    elif command == 'style':
        # Switch display style
        if len(sys.argv) >= 3:
            new_style = sys.argv[2].lower()
            if new_style in ['openbb', 'custom']:
                from roic_style_config import set_display_style
                set_display_style(new_style)
                print(f"\nRestart the roic command to see the new style.")
            else:
                print("Usage: ./roic style [openbb|custom]")
        else:
            from roic_style_config import get_display_style
            current = get_display_style()
            print(f"\nCurrent style: {current}")
            print("Change with: ./roic style openbb  or  ./roic style custom")
    
    elif command == 'historical':
        if len(sys.argv) >= 3:
            symbol = sys.argv[2].upper()
            
            # Check for years parameter
            years = 10  # Default to 10 years
            if '--years' in sys.argv:
                years_idx = sys.argv.index('--years')
                if years_idx + 1 < len(sys.argv):
                    try:
                        years = int(sys.argv[years_idx + 1])
                    except ValueError:
                        years = 10
            
            # Display historical ROIC
            df = display_historical_roic(symbol, years)
            
            # Export if requested
            if export and not df.empty:
                export_historical_roic(symbol, years, format=export)
    
    else:
        print(f"Unknown command: {command}")
        print("Use: quality, forecast, compare, historical, or style")

if __name__ == "__main__":
    main()
