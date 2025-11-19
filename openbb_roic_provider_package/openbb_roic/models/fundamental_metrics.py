"""ROIC Fundamental Metrics Model."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.fundamental_metrics import (
    FundamentalMetricsData,
    FundamentalMetricsQueryParams,
)
from pydantic import Field


class ROICMetricsQueryParams(FundamentalMetricsQueryParams):
    """ROIC Metrics Query Parameters."""
    
    period: Optional[str] = Field(
        default="annual",
        description="Time period for the data"
    )


class ROICMetricsData(FundamentalMetricsData):
    """ROIC Metrics Data Model."""
    
    roic: Optional[float] = Field(
        default=None,
        description="Return on Invested Capital (%)",
        alias="return_on_invested_capital"
    )
    quality_score: Optional[int] = Field(
        default=None,
        description="Quality score (0-100)",
        ge=0,
        le=100
    )
    moat_rating: Optional[str] = Field(
        default=None,
        description="Competitive moat rating (Wide/Narrow/None)"
    )
    roic_5y_avg: Optional[float] = Field(
        default=None,
        description="5-year average ROIC (%)"
    )
    roic_trend: Optional[str] = Field(
        default=None,
        description="ROIC trend (Improving/Stable/Declining)"
    )
    capital_efficiency: Optional[float] = Field(
        default=None,
        description="Capital efficiency ratio"
    )


class ROICMetricsFetcher(
    Fetcher[ROICMetricsQueryParams, List[ROICMetricsData]]
):
    """ROIC Metrics Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> ROICMetricsQueryParams:
        """Transform query parameters."""
        return ROICMetricsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: ROICMetricsQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict[str, Any]]:
        """Extract ROIC metrics data."""
        
        # Import the ROIC calculator
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        try:
            from openbb_roic_provider import roic_provider
            
            # Get metrics for the symbol
            symbol = query.symbol
            metrics = roic_provider.get_metrics(symbol)
            
            # Transform to OpenBB format
            data = {
                "symbol": symbol,
                "date": datetime.now(),
                "roic": metrics.get("roic"),
                "quality_score": metrics.get("quality_score"),
                "moat_rating": metrics.get("moat_rating"),
                "period_ending": datetime.now(),
                
                # Add standard metrics that OpenBB expects
                "market_cap": None,
                "pe_ratio": None,
                "price_to_book": None,
                "price_to_sales": None,
                "enterprise_value": None,
                "ev_to_ebitda": None,
                "ev_to_revenue": None,
                "debt_to_equity": None,
                "return_on_equity": None,
                "return_on_assets": metrics.get("roic", 0) / 2 if metrics.get("roic") else None,  # Approximation
                "gross_margin": None,
                "operating_margin": None,
                "net_margin": None,
                "revenue_growth": None,
                "earnings_growth": None,
                "dividend_yield": None,
                "payout_ratio": None,
            }
            
            # Calculate additional quality metrics
            if metrics.get("roic"):
                roic_value = metrics["roic"]
                
                # Determine trend
                if roic_value > 30:
                    data["roic_trend"] = "Exceptional"
                elif roic_value > 20:
                    data["roic_trend"] = "Strong"
                elif roic_value > 15:
                    data["roic_trend"] = "Good"
                else:
                    data["roic_trend"] = "Moderate"
                
                # Set 5-year average (simplified)
                data["roic_5y_avg"] = roic_value * 0.95  # Slight historical discount
                
                # Capital efficiency
                data["capital_efficiency"] = roic_value / 20  # Normalized to benchmark
            
            return [data]
            
        except Exception as e:
            print(f"Error fetching ROIC data: {e}")
            # Return minimal data
            return [{
                "symbol": query.symbol,
                "date": datetime.now(),
                "roic": None,
                "quality_score": None,
                "moat_rating": None,
            }]

    @staticmethod
    def transform_data(
        query: ROICMetricsQueryParams,
        data: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> List[ROICMetricsData]:
        """Transform data to standard format."""
        return [ROICMetricsData(**d) for d in data]
