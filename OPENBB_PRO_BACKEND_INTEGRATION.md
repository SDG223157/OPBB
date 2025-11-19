# 🚀 OpenBB Pro-Style Backend for ROIC Integration

## Overview

Inspired by [OpenBB Platform Pro Backend](https://github.com/OpenBB-finance/openbb-platform-pro-backend), this implementation creates a professional API backend that combines OpenBB Platform with ROIC quality metrics.

## 🏗️ Architecture Comparison

### OpenBB Platform Pro Backend
```
OpenBB Terminal Pro
        ↓
widgets.json (UI Configuration)
        ↓
OpenBB Platform Pro Backend
        ↓
OpenBB Platform API
```

### Our ROIC Backend
```
Client Applications / Terminal
        ↓
widgets.json (UI Configuration)
        ↓
OpenBB ROIC Backend (FastAPI)
        ↓
OpenBB Platform + ROIC Provider
```

## 📊 Features

### API Endpoints

| Endpoint | Description | Similar to Pro Backend |
|----------|-------------|------------------------|
| `/` | API information | ✅ Root endpoint |
| `/widgets.json` | Widget configuration | ✅ Terminal Pro widgets |
| `/api/v1/roic/metrics/{symbol}` | ROIC quality metrics | Custom endpoint |
| `/api/v1/roic/forecast/{symbol}` | Quality-based forecasts | Custom endpoint |
| `/api/v1/analysis/complete/{symbol}` | Combined OpenBB + ROIC | Enhanced analysis |
| `/api/v1/analysis/compare` | Multi-stock comparison | Professional feature |
| `/docs` | OpenAPI documentation | ✅ Swagger UI |
| `/health` | Health check | ✅ Service monitoring |

### Widget Configuration

Just like OpenBB Terminal Pro, our backend provides `widgets.json` for UI configuration:

```json
{
  "roic_metrics": {
    "title": "ROIC Quality Metrics",
    "type": "table",
    "endpoint": "/api/v1/roic/metrics",
    "refresh_rate": 300
  },
  "combined_analysis": {
    "title": "OpenBB + ROIC Analysis",
    "type": "mixed",
    "endpoint": "/api/v1/analysis/complete"
  }
}
```

## 🚀 Quick Start

### 1. Start the Backend Server

```bash
# Make script executable
chmod +x launch_roic_backend.sh

# Launch server
./launch_roic_backend.sh
```

The server will start at `http://127.0.0.1:8000`

### 2. Access the API

#### Via Browser
- API Docs: http://127.0.0.1:8000/docs
- Widgets: http://127.0.0.1:8000/widgets.json
- Root Info: http://127.0.0.1:8000/

#### Via Python Client

```python
# Use the provided client
python roic_backend_client.py
```

#### Via cURL

```bash
# Get ROIC metrics
curl http://127.0.0.1:8000/api/v1/roic/metrics/AAPL

# Get complete analysis
curl http://127.0.0.1:8000/api/v1/analysis/complete/MSFT

# Compare stocks
curl -X POST http://127.0.0.1:8000/api/v1/analysis/compare \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'
```

## 📈 Example Responses

### Complete Analysis Response
```json
{
  "symbol": "AAPL",
  "openbb": {
    "pe_ratio": 35.85,
    "market_cap": 3970000000000,
    "revenue": 385603000000,
    "profit_margin": 0.2531,
    "return_on_equity": 1.4725
  },
  "roic": {
    "roic": 51.54,
    "quality_score": 95,
    "moat_rating": "Wide",
    "1y_target": 315.58,
    "3y_target": 439.41
  },
  "combined_score": 75.3
}
```

### Comparison Response
```json
{
  "comparison": [
    {
      "symbol": "AAPL",
      "roic": 51.54,
      "quality_score": 95,
      "pe_ratio": 35.85,
      "combined_score": 75.3
    },
    {
      "symbol": "MSFT",
      "roic": 20.18,
      "quality_score": 85,
      "pe_ratio": 32.45,
      "combined_score": 71.2
    }
  ],
  "best_overall": "AAPL"
}
```

## 🔧 Configuration

### Environment Variables

```bash
# API Host and Port (same as OpenBB Pro Backend)
export OPENBB_API_HOST="0.0.0.0"  # Listen on all interfaces
export OPENBB_API_PORT="8000"     # Custom port

# API Keys (loaded automatically)
# Configured in ~/.openbb_platform/user_settings.json
```

## 🎯 Use Cases

### 1. Build a Trading Dashboard
Use the widgets.json to create a professional dashboard:
```javascript
fetch('http://localhost:8000/widgets.json')
  .then(res => res.json())
  .then(widgets => {
    // Render widgets in your UI
  });
```

### 2. Automated Analysis Pipeline
```python
client = ROICBackendClient()
symbols = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
comparison = client.compare_stocks(symbols)
best_stock = comparison["best_overall"]
```

### 3. Integration with Trading Systems
The API can be integrated with:
- Trading bots
- Portfolio management systems
- Research platforms
- Custom terminals

## 📊 Professional Features

### Combined Scoring Algorithm
The backend calculates a combined score using:
- **60%** ROIC Quality Score (fundamental strength)
- **40%** Valuation Score (based on P/E ratio)

This provides a balanced view of quality vs. value.

### Widget Types
- **Table**: Structured data display
- **Chart**: Time series visualization
- **Mixed**: Combined data types

### Refresh Rates
- Metrics: 5 minutes (300s)
- Forecasts: 10 minutes (600s)
- Configurable per widget

## 🔗 Comparison with OpenBB Terminal Pro

| Feature | OpenBB Pro Backend | Our ROIC Backend |
|---------|-------------------|------------------|
| FastAPI Server | ✅ | ✅ |
| widgets.json | ✅ | ✅ |
| OpenAPI Schema | ✅ | ✅ |
| Multiple Providers | ✅ | ✅ |
| Custom Endpoints | ❌ | ✅ ROIC Integration |
| Combined Analysis | ❌ | ✅ OpenBB + ROIC |
| Quality Metrics | ❌ | ✅ ROIC Scoring |

## 📚 Additional Resources

- [OpenBB Platform Pro Backend](https://github.com/OpenBB-finance/openbb-platform-pro-backend) - Original inspiration
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - API framework
- [OpenBB Platform Docs](https://docs.openbb.co/platform) - Core platform

## 🚀 Next Steps

1. **Deploy to Production**
   ```bash
   # Use production server
   pip install gunicorn
   gunicorn openbb_roic_backend:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Add Authentication**
   - JWT tokens
   - API key authentication
   - Rate limiting

3. **Enhance Widgets**
   - Real-time updates via WebSocket
   - More chart types
   - Custom indicators

4. **Scale the Backend**
   - Redis caching
   - Database integration
   - Load balancing

## Summary

This implementation demonstrates how to create a professional backend similar to OpenBB Terminal Pro, but enhanced with custom ROIC quality metrics. It provides:

- ✅ RESTful API with FastAPI
- ✅ Widget configuration for UI
- ✅ Combined analysis endpoints
- ✅ Professional documentation
- ✅ Client libraries
- ✅ Easy deployment

Perfect for building institutional-grade financial analysis tools!
