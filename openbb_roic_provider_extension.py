#!/usr/bin/env python3
"""
OpenBB ROIC Provider Extension
Full integration as an OpenBB provider like Yahoo Finance and FRED
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field
import warnings

# OpenBB imports
try:
    from openbb_core.provider.abstract.fetcher import Fetcher
    from openbb_core.provider.abstract.provider import Provider
    from openbb_core.provider.abstract.query_params import QueryParams
    from openbb_core.provider.abstract.data import Data
    from openbb_core.app.model.obbject import OBBject
except ImportError:
    warnings.warn("OpenBB Core modules not found. Installing mock interfaces.")
    # Mock classes for development
    class QueryParams(BaseModel):
        pass
    class Data(BaseModel):
        pass
    class Fetcher:
        pass
    class Provider:
        pass

# ROIC Data Models (following OpenBB pattern)
class ROICMetricsQueryParams(QueryParams):
    """Query parameters for ROIC metrics."""
    symbol: str = Field(description="Symbol to get data for")
    period: Optional[str] = Field(default="latest", description="Time period")

class ROICMetricsData(Data):
    """ROIC metrics data model - matches OpenBB's data structure."""
    symbol: str = Field(description="Stock symbol")
    date: datetime = Field(description="Date of the data")
    roic: Optional[float] = Field(description="Return on Invested Capital (%)")
    quality_score: Optional[int] = Field(description="Quality score (0-100)")
    moat_rating: Optional[str] = Field(description="Competitive moat rating")
    profit_margin: Optional[float] = Field(description="Profit margin (%)")
    asset_turnover: Optional[float] = Field(description="Asset turnover ratio")
    financial_leverage: Optional[float] = Field(description="Financial leverage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "date": "2024-01-01",
                "roic": 51.54,
                "quality_score": 95,
                "moat_rating": "Wide",
                "profit_margin": 25.0,
                "asset_turnover": 1.2,
                "financial_leverage": 5.5
            }
        }

class ROICForecastData(Data):
    """ROIC forecast data model."""
    symbol: str = Field(description="Stock symbol")
    current_price: Optional[float] = Field(description="Current stock price")
    roic: Optional[float] = Field(description="Current ROIC")
    implied_growth_rate: Optional[float] = Field(description="Implied growth rate (%)")
    target_1y: Optional[float] = Field(description="1-year price target")
    target_2y: Optional[float] = Field(description="2-year price target")
    target_3y: Optional[float] = Field(description="3-year price target")
    upside_1y: Optional[float] = Field(description="1-year upside (%)")
    upside_3y: Optional[float] = Field(description="3-year upside (%)")

# ROIC Fetcher (following OpenBB pattern)
class ROICMetricsFetcher(Fetcher[ROICMetricsQueryParams, ROICMetricsData]):
    """Fetcher for ROIC metrics."""
    
    @staticmethod
    def transform_query(params: Dict[str, Any]) -> ROICMetricsQueryParams:
        """Transform query parameters."""
        return ROICMetricsQueryParams(**params)
    
    @staticmethod
    def extract_data(
        query: ROICMetricsQueryParams,
        credentials: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Extract data from ROIC source."""
        # Import our existing ROIC calculator
        from openbb_roic_provider import roic_provider
        
        # Get ROIC data
        data = roic_provider.get_metrics(query.symbol)
        
        # Add required fields
        data['symbol'] = query.symbol
        data['date'] = datetime.now()
        
        return data
    
    @staticmethod
    def transform_data(
        data: Dict[str, Any],
        query: ROICMetricsQueryParams
    ) -> ROICMetricsData:
        """Transform data to standard format."""
        return ROICMetricsData(**data)

class ROICForecastFetcher(Fetcher[ROICMetricsQueryParams, ROICForecastData]):
    """Fetcher for ROIC forecasts."""
    
    @staticmethod
    def transform_query(params: Dict[str, Any]) -> ROICMetricsQueryParams:
        """Transform query parameters."""
        return ROICMetricsQueryParams(**params)
    
    @staticmethod
    def extract_data(
        query: ROICMetricsQueryParams,
        credentials: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Extract forecast data."""
        from openbb_roic_provider import roic_provider
        
        # Get forecast
        data = roic_provider.get_forecast(query.symbol)
        
        # Transform to match schema
        transformed = {
            'symbol': query.symbol,
            'current_price': data.get('current_price'),
            'roic': data.get('roic'),
            'implied_growth_rate': data.get('implied_growth_rate'),
            'target_1y': data.get('1_year_target'),
            'target_2y': data.get('2_year_target'),
            'target_3y': data.get('3_year_target'),
        }
        
        # Calculate upside
        if transformed['current_price'] and transformed['target_1y']:
            transformed['upside_1y'] = ((transformed['target_1y'] - transformed['current_price']) 
                                        / transformed['current_price'] * 100)
        if transformed['current_price'] and transformed['target_3y']:
            transformed['upside_3y'] = ((transformed['target_3y'] - transformed['current_price']) 
                                        / transformed['current_price'] * 100)
        
        return transformed
    
    @staticmethod
    def transform_data(
        data: Dict[str, Any],
        query: ROICMetricsQueryParams
    ) -> ROICForecastData:
        """Transform data to standard format."""
        return ROICForecastData(**data)

# ROIC Provider Class (main integration point)
class ROICProvider(Provider):
    """ROIC.ai provider for OpenBB Platform."""
    
    name = "roic"
    display_name = "ROIC.ai"
    description = "Quality investing metrics and ROIC analysis"
    credentials = ["roic_api_key"]
    website = "https://roic.ai"
    
    # Map OpenBB endpoints to ROIC fetchers
    fetcher_dict = {
        "EquityFundamentalMetrics": ROICMetricsFetcher,
        "EquityEstimatesConsensus": ROICForecastFetcher,
    }

# Registration function for OpenBB
def register_roic_provider():
    """Register ROIC as an OpenBB provider."""
    try:
        from openbb import obb
        from openbb_core.app.provider_interface import ProviderInterface
        
        # Register the provider
        interface = ProviderInterface()
        interface.register_provider(ROICProvider)
        
        print("✅ ROIC provider registered successfully!")
        print("\nYou can now use:")
        print("  /equity/fundamental/metrics --symbol AAPL --provider roic")
        print("  /equity/estimates/consensus --symbol AAPL --provider roic")
        
        return True
        
    except ImportError:
        print("⚠️  OpenBB Core modules not available for full integration")
        print("    The provider code is ready but requires OpenBB Platform SDK")
        return False

# OpenBB-compatible functions that can be called directly
def equity_fundamental_metrics(symbol: str, provider: str = "roic") -> OBBject:
    """
    Get fundamental metrics with ROIC
    Compatible with: /equity/fundamental/metrics --symbol AAPL --provider roic
    """
    fetcher = ROICMetricsFetcher()
    params = {"symbol": symbol}
    query = fetcher.transform_query(params)
    data = fetcher.extract_data(query)
    result = fetcher.transform_data(data, query)
    
    # Convert to OBBject-like response
    return {
        "results": [result.dict()],
        "provider": "roic",
        "symbol": symbol,
        "date": datetime.now().isoformat()
    }

def equity_estimates_consensus(symbol: str, provider: str = "roic") -> OBBject:
    """
    Get consensus estimates with ROIC-based forecasts
    Compatible with: /equity/estimates/consensus --symbol AAPL --provider roic
    """
    fetcher = ROICForecastFetcher()
    params = {"symbol": symbol}
    query = fetcher.transform_query(params)
    data = fetcher.extract_data(query)
    result = fetcher.transform_data(data, query)
    
    return {
        "results": [result.dict()],
        "provider": "roic",
        "symbol": symbol,
        "date": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("="*80)
    print(" "*20 + "ROIC PROVIDER FOR OPENBB")
    print("="*80)
    
    # Try to register
    success = register_roic_provider()
    
    if not success:
        print("\n📝 Testing standalone functions...")
        
        # Test metrics
        print("\n1. Fundamental Metrics (ROIC):")
        metrics = equity_fundamental_metrics("AAPL")
        print(f"   Results: {metrics['results'][0]}")
        
        # Test forecast
        print("\n2. Consensus Estimates (ROIC):")
        forecast = equity_estimates_consensus("AAPL")
        print(f"   Results: {forecast['results'][0]}")
    
    print("\n" + "="*80)
    print("INTEGRATION STATUS")
    print("="*80)
    print("""
    ✅ Provider code ready
    ✅ Data models defined
    ✅ Fetchers implemented
    ⏳ Awaiting OpenBB Platform SDK for full integration
    
    Once integrated, ROIC will work exactly like Yahoo and FRED:
    - /equity/fundamental/metrics --provider roic
    - /equity/estimates/consensus --provider roic
    - Shows in OpenBB's native display
    - Available in provider dropdown
    """)
