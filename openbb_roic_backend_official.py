#!/usr/bin/env python3
"""
OpenBB ROIC Backend - Official Pattern
Following the structure from https://github.com/OpenBB-finance/backends-for-openbb
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import json
import os
import sys

# Add ROIC provider to path
sys.path.insert(0, '/Users/sdg223157/OPBB')

# Import ROIC provider
try:
    from openbb_roic_provider import roic_provider
except:
    # Fallback if provider not available
    roic_provider = None

# Import OpenBB
try:
    from openbb import obb
except:
    obb = None

app = FastAPI(
    title="ROIC Backend for OpenBB",
    description="Quality metrics backend following OpenBB official patterns",
    version="1.0.0"
)

# CORS configuration - REQUIRED for OpenBB Workspace
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load widgets configuration
WIDGETS_FILE = os.path.join(os.path.dirname(__file__), "widgets.json")
APPS_FILE = os.path.join(os.path.dirname(__file__), "apps.json")

@app.get("/")
async def root():
    """Root endpoint - provides backend information"""
    return {
        "name": "ROIC Quality Metrics Backend",
        "description": "Professional ROIC analysis for OpenBB Workspace",
        "version": "1.0.0",
        "author": "OPBB",
        "endpoints": [
            "/widgets.json",
            "/roic/metrics?symbol=AAPL",
            "/roic/forecast?symbol=AAPL",
            "/analysis/complete?symbol=AAPL",
            "/health"
        ]
    }

@app.get("/widgets.json")
async def get_widgets():
    """Return widgets configuration - REQUIRED endpoint"""
    if os.path.exists(WIDGETS_FILE):
        return FileResponse(WIDGETS_FILE)
    else:
        return JSONResponse(content={
            "widgets": [],
            "error": "widgets.json not found"
        })

@app.get("/apps.json")
async def get_apps():
    """Return apps configuration - Optional but recommended"""
    if os.path.exists(APPS_FILE):
        return FileResponse(APPS_FILE)
    else:
        # Return minimal apps configuration
        return JSONResponse(content={
            "apps": [{
                "id": "roic",
                "name": "ROIC Quality Metrics",
                "description": "Quality-based investment analysis"
            }]
        })

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ROIC Backend"}

# ============= Data Endpoints =============

@app.get("/roic/metrics")
async def get_roic_metrics(symbol: str):
    """Get ROIC metrics - returns data in OpenBB format"""
    if not roic_provider:
        return {"error": "ROIC provider not available"}
    
    try:
        metrics = roic_provider.get_metrics(symbol.upper())
        
        # Format for OpenBB Workspace table widget
        return {
            "data": [{
                "Symbol": symbol.upper(),
                "ROIC %": metrics.get("roic", 0),
                "Quality Score": metrics.get("quality_score", 0),
                "Moat Rating": metrics.get("moat_rating", "N/A"),
                "Trend": "↑" if metrics.get("roic", 0) > 20 else "↓"
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/roic/forecast")
async def get_roic_forecast(symbol: str, years: int = 3):
    """Get forecast data - returns chart-ready format"""
    if not roic_provider:
        return {"error": "ROIC provider not available"}
    
    try:
        forecast = roic_provider.get_forecast(symbol.upper())
        
        # Format for OpenBB Workspace chart widget
        chart_data = []
        current_price = forecast.get("current_price", 100)
        
        # Add data points for chart
        chart_data.append({
            "year": "Current",
            "price_target": current_price,
            "quality_score": forecast.get("roic", 50)
        })
        
        if forecast.get("1_year_target"):
            chart_data.append({
                "year": "1 Year",
                "price_target": forecast["1_year_target"],
                "quality_score": forecast.get("roic", 50)
            })
        
        if forecast.get("2_year_target"):
            chart_data.append({
                "year": "2 Year",
                "price_target": forecast["2_year_target"],
                "quality_score": forecast.get("roic", 50)
            })
        
        if forecast.get("3_year_target"):
            chart_data.append({
                "year": "3 Year",
                "price_target": forecast["3_year_target"],
                "quality_score": forecast.get("roic", 50)
            })
        
        return {"data": chart_data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/complete")
async def get_complete_analysis(symbol: str):
    """Combined analysis - OpenBB + ROIC data"""
    symbol = symbol.upper()
    
    result = {
        "Symbol": symbol,
        "ROIC %": None,
        "Quality Score": None,
        "P/E Ratio": None,
        "Market Cap": None,
        "1Y Target": None
    }
    
    # Get ROIC data
    if roic_provider:
        try:
            metrics = roic_provider.get_metrics(symbol)
            forecast = roic_provider.get_forecast(symbol)
            
            result["ROIC %"] = metrics.get("roic")
            result["Quality Score"] = metrics.get("quality_score")
            result["1Y Target"] = forecast.get("1_year_target")
        except:
            pass
    
    # Get OpenBB data
    if obb:
        try:
            data = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
            if data.results:
                result["P/E Ratio"] = getattr(data.results[0], 'pe_ratio', None)
                result["Market Cap"] = getattr(data.results[0], 'market_cap', None)
        except:
            pass
    
    return result

@app.post("/analysis/compare")
async def compare_stocks(request: Dict[str, Any]):
    """Compare multiple stocks"""
    symbols = request.get("symbols", [])
    
    if not symbols:
        return {"comparison": [], "error": "No symbols provided"}
    
    comparison_data = []
    
    for symbol in symbols[:10]:  # Limit to 10 symbols
        symbol = symbol.upper()
        row = {
            "Symbol": symbol,
            "ROIC %": None,
            "Quality": None,
            "P/E": None
        }
        
        # Get ROIC data
        if roic_provider:
            try:
                metrics = roic_provider.get_metrics(symbol)
                row["ROIC %"] = round(metrics.get("roic", 0), 1)
                row["Quality"] = metrics.get("quality_score", 0)
            except:
                pass
        
        # Get P/E from OpenBB
        if obb:
            try:
                data = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
                if data.results:
                    row["P/E"] = getattr(data.results[0], 'pe_ratio', None)
            except:
                pass
        
        # Calculate combined score
        if row["ROIC %"] and row["P/E"]:
            quality = row.get("Quality", 50)
            pe_score = max(0, 100 - (row["P/E"] * 2)) if row["P/E"] else 50
            row["Score"] = round((quality * 0.6 + pe_score * 0.4), 1)
        
        comparison_data.append(row)
    
    # Sort by score
    comparison_data.sort(key=lambda x: x.get("Score", 0), reverse=True)
    
    return {"comparison": comparison_data}

@app.get("/market/movers")
async def get_market_movers():
    """Get top ROIC quality stocks"""
    # Example movers - in production would scan market
    movers = [
        {"Symbol": "AAPL", "ROIC %": 51.5, "Quality": 95, "Change": "+2.3%"},
        {"Symbol": "MSFT", "ROIC %": 20.2, "Quality": 85, "Change": "+1.8%"},
        {"Symbol": "GOOGL", "ROIC %": 18.7, "Quality": 82, "Change": "-0.5%"},
        {"Symbol": "NVDA", "ROIC %": 42.3, "Quality": 92, "Change": "+5.2%"},
    ]
    
    return {"movers": movers}

def main():
    """Launch the backend server"""
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    
    print(f"""
╔════════════════════════════════════════════════════════════╗
║   ROIC Backend for OpenBB Workspace                       ║
║   Following Official Pattern from:                        ║
║   https://github.com/OpenBB-finance/backends-for-openbb   ║
╠════════════════════════════════════════════════════════════╣
║   Server:   http://{host}:{port}                          ║
║   Widgets:  http://{host}:{port}/widgets.json             ║
║   Docs:     http://{host}:{port}/docs                     ║
╠════════════════════════════════════════════════════════════╣
║   To connect in OpenBB Workspace:                         ║
║   1. Add backend URL: http://{host}:{port}                ║
║   2. Widgets will auto-load from widgets.json             ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
