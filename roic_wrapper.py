#!/usr/bin/env python3
"""
ROIC + OpenBB Integration Wrapper
Use this to add ROIC data to your OpenBB session
"""

from openbb import obb
import sys
sys.path.insert(0, '/Users/sdg223157/OPBB')

from openbb_roic_provider import roic_provider

class ROICEnhancedOBB:
    """Enhanced OBB with ROIC methods"""
    
    def __init__(self):
        self.obb = obb
        self.roic = roic_provider
    
    def get_complete_metrics(self, symbol):
        """Get both OpenBB and ROIC metrics"""
        result = {
            'symbol': symbol,
            'openbb': {},
            'roic': {}
        }
        
        # Get OpenBB data
        try:
            metrics = self.obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
            if metrics.results:
                data = metrics.results[0]
                result['openbb'] = {
                    'pe_ratio': getattr(data, 'pe_ratio', None),
                    'market_cap': getattr(data, 'market_cap', None),
                    'revenue': getattr(data, 'revenue', None),
                }
        except:
            pass
        
        # Get ROIC data
        try:
            roic_data = self.roic.get_metrics(symbol)
            result['roic'] = roic_data
        except:
            pass
        
        return result
    
    def display_analysis(self, symbol):
        """Display comprehensive analysis"""
        data = self.get_complete_metrics(symbol)
        
        print(f"""
{'='*60}
COMPREHENSIVE ANALYSIS: {symbol}
{'='*60}

OpenBB Metrics:
  P/E Ratio:    {data['openbb'].get('pe_ratio', 'N/A')}
  Market Cap:   {data['openbb'].get('market_cap', 'N/A')}

ROIC Metrics:
  ROIC:         {data['roic'].get('roic', 'N/A')}%
  Quality:      {data['roic'].get('quality_score', 'N/A')}/100
  Moat:         {data['roic'].get('moat_rating', 'N/A')}
{'='*60}
""")

# Create global instance
enhanced = ROICEnhancedOBB()

# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        enhanced.display_analysis(sys.argv[1].upper())
    else:
        print("Usage: python roic_wrapper.py SYMBOL")
        print("Example: python roic_wrapper.py AAPL")
