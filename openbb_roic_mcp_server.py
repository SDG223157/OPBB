#!/usr/bin/env python3
"""
OpenBB ROIC MCP Server
Compatible with OpenBB Workspace Agent Chat Interface
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import uvicorn
import sys
import os

# Add ROIC provider to path
sys.path.insert(0, '/Users/sdg223157/OPBB')
from openbb_roic_provider import roic_provider
from openbb import obb

app = FastAPI(
    title="OpenBB ROIC MCP Server",
    description="MCP-compatible server for ROIC quality metrics in OpenBB Workspace",
    version="1.0.0"
)

# MCP Tool definitions
MCP_TOOLS = {
    "roic_quality": {
        "name": "roic_quality",
        "description": "Get ROIC quality metrics for a stock symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g., AAPL)"
                }
            },
            "required": ["symbol"]
        }
    },
    "roic_forecast": {
        "name": "roic_forecast",
        "description": "Get quality-based price forecast for a stock",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol"
                },
                "years": {
                    "type": "integer",
                    "description": "Forecast years (1-3)",
                    "default": 3
                }
            },
            "required": ["symbol"]
        }
    },
    "roic_compare": {
        "name": "roic_compare",
        "description": "Compare ROIC metrics for multiple stocks",
        "parameters": {
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of stock symbols to compare"
                }
            },
            "required": ["symbols"]
        }
    },
    "complete_analysis": {
        "name": "complete_analysis",
        "description": "Get combined OpenBB and ROIC analysis for a stock",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol"
                }
            },
            "required": ["symbol"]
        }
    }
}

class MCPRequest(BaseModel):
    """MCP protocol request"""
    method: str
    params: Optional[Dict[str, Any]] = {}

@app.get("/mcp/")
async def mcp_root():
    """MCP root endpoint with server information"""
    return {
        "name": "OpenBB ROIC MCP Server",
        "version": "1.0.0",
        "protocol_version": "0.1.0",
        "capabilities": {
            "tools": True,
            "resources": False,
            "prompts": False
        }
    }

@app.get("/mcp/tools/list")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": list(MCP_TOOLS.values())
    }

@app.post("/mcp/tools/call")
async def call_tool(request: MCPRequest):
    """Execute MCP tool call"""
    tool_name = request.params.get("name")
    tool_args = request.params.get("arguments", {})
    
    try:
        if tool_name == "roic_quality":
            symbol = tool_args.get("symbol", "").upper()
            metrics = roic_provider.get_metrics(symbol)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"ROIC Metrics for {symbol}:\n"
                                f"• ROIC: {metrics.get('roic', 'N/A')}%\n"
                                f"• Quality Score: {metrics.get('quality_score', 'N/A')}/100\n"
                                f"• Moat Rating: {metrics.get('moat_rating', 'N/A')}"
                    }
                ]
            }
            
        elif tool_name == "roic_forecast":
            symbol = tool_args.get("symbol", "").upper()
            years = tool_args.get("years", 3)
            forecast = roic_provider.get_forecast(symbol)
            
            text = f"Quality-Based Forecast for {symbol}:\n"
            if years >= 1 and forecast.get("1_year_target"):
                text += f"• 1 Year: ${forecast['1_year_target']:.2f}\n"
            if years >= 2 and forecast.get("2_year_target"):
                text += f"• 2 Year: ${forecast['2_year_target']:.2f}\n"
            if years >= 3 and forecast.get("3_year_target"):
                text += f"• 3 Year: ${forecast['3_year_target']:.2f}\n"
            
            return {
                "content": [{"type": "text", "text": text}]
            }
            
        elif tool_name == "roic_compare":
            symbols = tool_args.get("symbols", [])
            results = []
            
            for symbol in symbols[:5]:  # Limit to 5 symbols
                symbol = symbol.upper()
                metrics = roic_provider.get_metrics(symbol)
                results.append({
                    "symbol": symbol,
                    "roic": metrics.get("roic", 0),
                    "quality": metrics.get("quality_score", 0)
                })
            
            # Sort by quality score
            results.sort(key=lambda x: x["quality"], reverse=True)
            
            text = "ROIC Comparison:\n"
            for r in results:
                text += f"• {r['symbol']}: ROIC {r['roic']:.1f}%, Quality {r['quality']}/100\n"
            
            if results:
                text += f"\nBest Quality: {results[0]['symbol']}"
            
            return {
                "content": [{"type": "text", "text": text}]
            }
            
        elif tool_name == "complete_analysis":
            symbol = tool_args.get("symbol", "").upper()
            
            # Get OpenBB data
            openbb_text = f"OpenBB Analysis for {symbol}:\n"
            try:
                metrics = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
                if metrics.results:
                    data = metrics.results[0]
                    openbb_text += f"• P/E Ratio: {getattr(data, 'pe_ratio', 'N/A')}\n"
                    openbb_text += f"• Market Cap: ${getattr(data, 'market_cap', 0)/1e9:.1f}B\n"
            except:
                openbb_text += "• OpenBB data unavailable\n"
            
            # Get ROIC data
            roic_text = f"\nROIC Analysis:\n"
            try:
                roic_metrics = roic_provider.get_metrics(symbol)
                roic_forecast = roic_provider.get_forecast(symbol)
                roic_text += f"• ROIC: {roic_metrics.get('roic', 'N/A')}%\n"
                roic_text += f"• Quality: {roic_metrics.get('quality_score', 'N/A')}/100\n"
                roic_text += f"• 1Y Target: ${roic_forecast.get('1_year_target', 'N/A')}\n"
            except:
                roic_text += "• ROIC data unavailable\n"
            
            return {
                "content": [{"type": "text", "text": openbb_text + roic_text}]
            }
            
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
            
    except Exception as e:
        return {
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "type": "mcp"}

def main():
    """Launch MCP server"""
    port = int(os.getenv("MCP_PORT", "6950"))
    host = os.getenv("MCP_HOST", "127.0.0.1")
    
    print(f"""
╔════════════════════════════════════════════════════════╗
║          OpenBB ROIC MCP Server                        ║
╠════════════════════════════════════════════════════════╣
║  MCP URL: http://{host}:{port}/mcp/                   ║
║  Add this URL to OpenBB Workspace Agent Chat           ║
╚════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
