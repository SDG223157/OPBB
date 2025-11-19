"""ROIC Quality Forecast Model."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.price_target import (
    PriceTargetData,
    PriceTargetQueryParams,
)
from pydantic import Field


class ROICForecastQueryParams(PriceTargetQueryParams):
    """ROIC Forecast Query Parameters."""
    
    forecast_period: Optional[int] = Field(
        default=3,
        description="Forecast period in years",
        ge=1,
        le=5
    )


class ROICForecastData(PriceTargetData):
    """ROIC Quality-Based Forecast Data Model."""
    
    roic: Optional[float] = Field(
        default=None,
        description="Current ROIC (%)"
    )
    quality_score: Optional[int] = Field(
        default=None,
        description="Quality score (0-100)"
    )
    implied_growth_rate: Optional[float] = Field(
        default=None,
        description="Quality-implied growth rate (%)"
    )
    target_1y: Optional[float] = Field(
        default=None,
        description="1-year price target based on quality"
    )
    target_2y: Optional[float] = Field(
        default=None,
        description="2-year price target based on quality"
    )
    target_3y: Optional[float] = Field(
        default=None,
        description="3-year price target based on quality"
    )
    confidence_level: Optional[str] = Field(
        default=None,
        description="Forecast confidence level (High/Medium/Low)"
    )


class ROICForecastFetcher(
    Fetcher[ROICForecastQueryParams, List[ROICForecastData]]
):
    """ROIC Quality Forecast Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> ROICForecastQueryParams:
        """Transform query parameters."""
        return ROICForecastQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: ROICForecastQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """Extract ROIC forecast data."""
        
        # Import the ROIC calculator
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        try:
            from openbb_roic_provider import roic_provider
            
            # Get forecast for the symbol
            symbol = query.symbol
            forecast = roic_provider.get_forecast(symbol)
            
            # Get current price for calculations
            current_price = forecast.get("current_price", 100)
            
            # Transform to OpenBB price target format
            data = {
                "symbol": symbol,
                "published_date": datetime.now(),
                "published_time": datetime.now().time(),
                "exchange": None,
                "company_name": symbol,
                "analyst_name": "ROIC Quality Model",
                "analyst_firm": "ROIC.ai",
                "currency": "USD",
                "price_target": forecast.get("1_year_target"),
                "adj_price_target": forecast.get("1_year_target"),
                "price_when_posted": current_price,
                "rating_current": "Quality-Based",
                "rating_previous": None,
                "action": None,
                
                # ROIC-specific fields
                "roic": forecast.get("roic"),
                "quality_score": forecast.get("quality_score"),
                "implied_growth_rate": forecast.get("implied_growth_rate"),
                "target_1y": forecast.get("1_year_target"),
                "target_2y": forecast.get("2_year_target"),
                "target_3y": forecast.get("3_year_target"),
            }
            
            # Determine confidence level based on ROIC
            if data["roic"]:
                if data["roic"] > 30:
                    data["confidence_level"] = "High"
                    data["rating_current"] = "Strong Buy"
                elif data["roic"] > 20:
                    data["confidence_level"] = "Medium-High"
                    data["rating_current"] = "Buy"
                elif data["roic"] > 15:
                    data["confidence_level"] = "Medium"
                    data["rating_current"] = "Hold"
                else:
                    data["confidence_level"] = "Low"
                    data["rating_current"] = "Neutral"
            
            return [data]
            
        except Exception as e:
            print(f"Error fetching ROIC forecast: {e}")
            # Return minimal data
            return [{
                "symbol": query.symbol,
                "published_date": datetime.now(),
                "price_target": None,
                "analyst_firm": "ROIC.ai",
                "rating_current": "N/A",
            }]

    @staticmethod
    def transform_data(
        query: ROICForecastQueryParams,
        data: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> List[ROICForecastData]:
        """Transform data to standard format."""
        return [ROICForecastData(**d) for d in data]
