"""ROIC Provider for OpenBB Platform."""

from openbb_core.provider.abstract.provider import Provider

from openbb_roic.models.fundamental_metrics import ROICMetricsFetcher
from openbb_roic.models.quality_forecast import ROICForecastFetcher

roic_provider = Provider(
    name="roic",
    display_name="ROIC.ai",
    description="Quality investing metrics and ROIC analysis",
    website="https://roic.ai",
    credentials=["api_key"],
    fetcher_dict={
        "FundamentalMetrics": ROICMetricsFetcher,
        "PriceTarget": ROICForecastFetcher,
    },
)

__all__ = ["roic_provider"]
