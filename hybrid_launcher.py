#!/usr/bin/env python3
"""
Hybrid OpenBB + ROIC Launcher
Provides ROIC data alongside OpenBB
"""

import sys
import os

# Add ROIC to path
sys.path.insert(0, '/Users/sdg223157/OPBB/openbb_roic_provider_package')
sys.path.insert(0, '/Users/sdg223157/OPBB')

def roic_command(symbol):
    """Get ROIC data for a symbol"""
    from openbb_roic_provider import roic_provider
    
    metrics = roic_provider.get_metrics(symbol)
    forecast = roic_provider.get_forecast(symbol)
    
    print(f"""
{'='*50}
ROIC Analysis for {symbol}
{'='*50}
ROIC:           {metrics.get('roic', 'N/A')}%
Quality Score:  {metrics.get('quality_score', 'N/A')}/100
Moat Rating:    {metrics.get('moat_rating', 'N/A')}

Price Targets:
1 Year:  ${forecast.get('1_year_target', 'N/A')}
2 Year:  ${forecast.get('2_year_target', 'N/A')}
3 Year:  ${forecast.get('3_year_target', 'N/A')}
{'='*50}
""")

# Check command line args
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'roic' and len(sys.argv) > 2:
        roic_command(sys.argv[2].upper())
    else:
        # Launch normal OpenBB
        os.system('source /Users/sdg223157/OPBB/openbb-env/bin/activate && openbb')
else:
    print("""
Hybrid OpenBB + ROIC Launcher
=============================
Usage:
  python hybrid_launcher.py         # Launch OpenBB CLI
  python hybrid_launcher.py roic AAPL  # Get ROIC data
""")
