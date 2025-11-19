#!/usr/bin/env python3
"""
OpenBB ROIC Backend - Professional API wrapper
Similar to OpenBB Platform Pro Backend but for ROIC integration

Inspired by: https://github.com/OpenBB-finance/openbb-platform-pro-backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uvicorn
import json
import os
import sys

# Add ROIC provider to path
sys.path.insert(0, '/Users/sdg223157/OPBB')
sys.path.insert(0, '/Users/sdg223157/OPBB/openbb_roic_provider_package')

from openbb import obb
from openbb_roic_provider import roic_provider

app = FastAPI(
    title="OpenBB ROIC Backend",
    description="Professional backend for ROIC quality metrics integrated with OpenBB Platform",
    version="1.0.0"
)

# Add CORS middleware to allow OpenBB frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    """Request model for analysis endpoints"""
    symbol: str
    provider: Optional[str] = "roic"
    include_openbb: Optional[bool] = True

class ComparisonRequest(BaseModel):
    """Request model for comparison endpoints"""
    symbols: List[str]
    metrics: Optional[List[str]] = ["roic", "quality_score", "pe_ratio"]

# Widget configuration for Terminal Pro style interface
WIDGETS_CONFIG = {
    "roic_metrics": {
        "title": "ROIC Quality Metrics",
        "type": "table",
        "endpoint": "/api/v1/roic/metrics",
        "refresh_rate": 300,
        "columns": ["symbol", "roic", "quality_score", "moat_rating"]
    },
    "roic_forecast": {
        "title": "Quality-Based Forecast",
        "type": "chart",
        "endpoint": "/api/v1/roic/forecast",
        "refresh_rate": 600,
        "chart_type": "line"
    },
    "combined_analysis": {
        "title": "OpenBB + ROIC Analysis",
        "type": "mixed",
        "endpoint": "/api/v1/analysis/complete",
        "refresh_rate": 300
    }
}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "OpenBB ROIC Backend",
        "version": "1.0.0",
        "description": "Professional ROIC integration for OpenBB Platform",
        "endpoints": {
            "widgets": "/widgets.json",
            "roic_metrics": "/api/v1/roic/metrics/{symbol}",
            "roic_forecast": "/api/v1/roic/forecast/{symbol}",
            "complete_analysis": "/api/v1/analysis/complete/{symbol}",
            "compare": "/api/v1/analysis/compare",
            "openapi": "/docs"
        },
        "powered_by": {
            "openbb": "OpenBB Platform",
            "roic": "ROIC.ai methodology"
        }
    }

@app.get("/widgets.json")
async def get_widgets():
    """Return widgets configuration for Terminal Pro style interface"""
    return JSONResponse(content=WIDGETS_CONFIG)

@app.get("/apps.json")
async def get_apps():
    """Return apps configuration for OpenBB integration"""
    import json
    import os
    
    apps_file = os.path.join(os.path.dirname(__file__), "apps.json")
    if os.path.exists(apps_file):
        with open(apps_file, 'r') as f:
            return JSONResponse(content=json.load(f))
    else:
        return JSONResponse(content={
            "apps": [{
                "id": "roic-metrics",
                "name": "ROIC Quality Metrics",
                "widgets": list(WIDGETS_CONFIG.keys())
            }]
        })

@app.get("/api/v1/roic/metrics/{symbol}")
async def get_roic_metrics(symbol: str):
    """Get ROIC quality metrics for a symbol"""
    try:
        metrics = roic_provider.get_metrics(symbol.upper())
        return {
            "symbol": symbol.upper(),
            "data": metrics,
            "provider": "roic"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/roic/forecast/{symbol}")
async def get_roic_forecast(symbol: str, years: int = 3):
    """Get quality-based forecast for a symbol"""
    try:
        forecast = roic_provider.get_forecast(symbol.upper())
        return {
            "symbol": symbol.upper(),
            "years": years,
            "data": forecast,
            "provider": "roic"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analysis/complete/{symbol}")
async def get_complete_analysis(symbol: str):
    """Get combined OpenBB + ROIC analysis"""
    try:
        result = {
            "symbol": symbol.upper(),
            "openbb": {},
            "roic": {},
            "combined_score": None
        }
        
        # Get OpenBB data
        try:
            metrics = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
            if metrics.results:
                data = metrics.results[0]
                result["openbb"] = {
                    "pe_ratio": getattr(data, 'pe_ratio', None),
                    "market_cap": getattr(data, 'market_cap', None),
                    "revenue": getattr(data, 'revenue', None),
                    "profit_margin": getattr(data, 'profit_margin', None),
                    "return_on_equity": getattr(data, 'return_on_equity', None)
                }
        except:
            pass
        
        # Get ROIC data
        try:
            roic_metrics = roic_provider.get_metrics(symbol.upper())
            roic_forecast = roic_provider.get_forecast(symbol.upper())
            
            result["roic"] = {
                "roic": roic_metrics.get("roic"),
                "quality_score": roic_metrics.get("quality_score"),
                "moat_rating": roic_metrics.get("moat_rating"),
                "1y_target": roic_forecast.get("1_year_target"),
                "3y_target": roic_forecast.get("3_year_target")
            }
            
            # Calculate combined score
            if result["roic"]["quality_score"] and result["openbb"].get("pe_ratio"):
                # Simple combined scoring: Quality vs Valuation
                quality = result["roic"]["quality_score"]
                pe = result["openbb"]["pe_ratio"]
                
                # Normalize P/E (lower is better, cap at 50)
                pe_score = max(0, 100 - (pe * 2)) if pe and pe > 0 else 50
                
                # Combined score weighted 60% quality, 40% valuation
                result["combined_score"] = (quality * 0.6 + pe_score * 0.4)
        except:
            pass
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analysis/compare")
async def compare_stocks(request: ComparisonRequest):
    """Compare multiple stocks across OpenBB and ROIC metrics"""
    try:
        results = []
        
        for symbol in request.symbols[:10]:  # Limit to 10 symbols
            analysis = await get_complete_analysis(symbol)
            
            comparison_data = {
                "symbol": symbol.upper(),
                "roic": analysis["roic"].get("roic"),
                "quality_score": analysis["roic"].get("quality_score"),
                "pe_ratio": analysis["openbb"].get("pe_ratio"),
                "market_cap": analysis["openbb"].get("market_cap"),
                "combined_score": analysis.get("combined_score")
            }
            
            results.append(comparison_data)
        
        # Sort by combined score
        results.sort(key=lambda x: x.get("combined_score") or 0, reverse=True)
        
        return {
            "comparison": results,
            "best_overall": results[0]["symbol"] if results else None,
            "metrics_used": request.metrics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/providers")
async def get_providers():
    """List available data providers"""
    return {
        "openbb_providers": ["yfinance", "polygon", "fred", "finviz"],
        "custom_providers": ["roic"],
        "integrated": True
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "OpenBB ROIC Backend"}

def main():
    """Launch the backend server"""
    host = os.getenv("OPENBB_API_HOST", "127.0.0.1")
    port = int(os.getenv("OPENBB_API_PORT", "8000"))
    
    print(f"""
╔════════════════════════════════════════════════════════╗
║          OpenBB ROIC Backend - Professional API        ║
╠════════════════════════════════════════════════════════╣
║  Inspired by OpenBB Platform Pro Backend               ║
║  https://github.com/OpenBB-finance/openbb-platform-pro ║
╠════════════════════════════════════════════════════════╣
║  API Docs:    http://{host}:{port}/docs           ║
║  Widgets:     http://{host}:{port}/widgets.json   ║
║  Health:      http://{host}:{port}/health         ║
╚════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
