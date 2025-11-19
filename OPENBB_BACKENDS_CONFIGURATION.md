# 🚀 OpenBB Backends Configuration Guide

Complete guide for configuring ROIC backends in OpenBB Workspace's Backends screen.

## Overview

OpenBB Workspace provides a professional backend management system that perfectly supports our ROIC integration. This guide shows how to configure all our backends.

## 📋 Backend Configurations

### 1. ROIC Quality API Backend

**Purpose**: Main REST API for ROIC metrics

```yaml
Backend Name: ROIC Quality API
Environment: openbb
Executable: python openbb_roic_backend.py
Working Directory: /Users/sdg223157/OPBB
Environment Variables:
  OPENBB_API_HOST=127.0.0.1
  OPENBB_API_PORT=8000
  OPENBB_API_POLYGON_KEY=Po4bGB8fz_u3AA9TNkwt5CAeUnSLarai
  OPENBB_API_FINVIZ_KEY=be56a0a4-c7b3-4094-85b6-0ad5a3b49fc6
  OPENBB_API_FRED_KEY=7c26de454d31a77bfdf9aaa33f2f55a8
  OPENBB_API_ROIC_KEY=a365bff224a6419fac064dd52e1f80d9
Start Automatically: Yes (recommended)
```

**Access**: http://127.0.0.1:8000/docs

### 2. ROIC MCP Server

**Purpose**: MCP server for OpenBB Workspace Agent Chat

```yaml
Backend Name: ROIC MCP Server
Environment: openbb
Executable: python openbb_roic_mcp_server.py
Working Directory: /Users/sdg223157/OPBB
Environment Variables:
  MCP_HOST=127.0.0.1
  MCP_PORT=6950
Start Automatically: Yes
Start at Login: Optional
```

**Add to Workspace Chat**: http://127.0.0.1:6950/mcp/

### 3. OpenBB Platform API (Enhanced)

**Purpose**: Standard OpenBB API with ROIC available

```yaml
Backend Name: OpenBB Platform API
Environment: openbb
Executable: openbb-api --port 9000
Working Directory: /Users/sdg223157/OPBB
Environment File: /Users/sdg223157/OPBB/.env
Start Automatically: Yes
```

**Access**: http://127.0.0.1:9000/docs

### 4. Development Backend (Hot Reload)

**Purpose**: Development server with auto-reload

```yaml
Backend Name: ROIC Dev Server
Environment: openbb
Executable: uvicorn openbb_roic_backend:app --reload --port 8001
Working Directory: /Users/sdg223157/OPBB
Environment Variables:
  PYTHONPATH=/Users/sdg223157/OPBB
  DEBUG=True
```

### 5. Production Backend (HTTPS)

**Purpose**: Secure production server

#### Step 1: Generate Certificate
1. Click **Generate Certificate**
2. Enter:
   - Common Name: `127.0.0.1`
   - Organization: `ROIC Analytics`
   - Alternative Names: `localhost,0.0.0.0`
   - Output Directory: `/Users/sdg223157/OPBB/certs`
3. Check "Add to trust store"
4. Click Generate

#### Step 2: Configure Backend
```yaml
Backend Name: ROIC Secure API
Environment: openbb
Executable: uvicorn openbb_roic_backend:app --port 8443
Working Directory: /Users/sdg223157/OPBB
Environment Variables:
  UVICORN_SSL_CERTFILE=/Users/sdg223157/OPBB/certs/certificate.pem
  UVICORN_SSL_KEYFILE=/Users/sdg223157/OPBB/certs/private/private.key
  OPENBB_API_HOST=0.0.0.0
```

**Access**: https://127.0.0.1:8443/docs

## 🎯 Quick Setup Steps

### For Basic Users:

1. Open OpenBB Workspace
2. Go to Backends screen
3. Click "New Backend"
4. Copy configuration #1 (ROIC Quality API)
5. Click "Create"
6. Press "Start"
7. Open http://127.0.0.1:8000/docs

### For Agent Chat Users:

1. Configure backend #2 (MCP Server)
2. Start the backend
3. Open Workspace Chat
4. Add MCP server: http://127.0.0.1:6950/mcp/
5. Ask: "Get ROIC metrics for AAPL"

### For Developers:

1. Configure backend #4 (Dev Server)
2. Edit code in your IDE
3. Server auto-reloads on save
4. Test at http://127.0.0.1:8001/docs

## 📊 Backend Status Indicators

| Status | Meaning | Action |
|--------|---------|--------|
| 🟢 Running | Backend is active | Access the URL |
| 🟡 Starting | Backend is launching | Wait 5-10 seconds |
| 🔴 Stopped | Backend is not running | Click "Start" |
| ⚠️ Error | Backend failed to start | Check "Logs" |

## 🔧 Environment Variables

### Required API Keys
```bash
# Add to Environment Variables or .env file
OPENBB_API_POLYGON_KEY=your_polygon_key
OPENBB_API_FINVIZ_KEY=your_finviz_key  
OPENBB_API_FRED_KEY=your_fred_key
OPENBB_API_ROIC_KEY=your_roic_key
```

### Optional Configuration
```bash
# Server configuration
OPENBB_API_HOST=0.0.0.0  # Expose to LAN
OPENBB_API_PORT=8000      # Custom port

# HTTPS configuration
UVICORN_SSL_CERTFILE=/path/to/cert.pem
UVICORN_SSL_KEYFILE=/path/to/private.key

# Development
DEBUG=True
PYTHONPATH=/Users/sdg223157/OPBB
```

## 📝 Troubleshooting

### Port Already in Use
**Solution**: Edit backend, change port number
```yaml
Executable: python openbb_roic_backend.py --port 8002
```

### Backend Won't Start
**Solution**: Check logs
1. Click "Logs" button
2. Look for error messages
3. Common issues:
   - Missing dependencies: `pip install fastapi uvicorn`
   - Path issues: Check working directory
   - Python errors: Fix code syntax

### Can't Connect from Browser
**Solution**: Check firewall
```bash
# macOS
sudo pfctl -d  # Disable firewall temporarily

# Allow specific port
sudo pfctl -e
echo "pass in proto tcp from any to any port 8000" | sudo pfctl -f -
```

### MCP Server Not Working
**Solution**: Verify MCP URL
- Must include `/mcp/` at the end
- Example: `http://127.0.0.1:6950/mcp/`
- Not: `http://127.0.0.1:6950`

## 🚀 Advanced Features

### Multi-Environment Setup

Run different Python versions:
```yaml
# Python 3.11 backend
Environment: py311-openbb
Executable: python openbb_roic_backend.py

# Python 3.12 backend  
Environment: py312-openbb
Executable: python openbb_roic_backend.py
```

### Load Balancing

Run multiple instances:
```yaml
# Instance 1
Backend Name: ROIC API 1
Executable: python openbb_roic_backend.py --port 8001

# Instance 2
Backend Name: ROIC API 2
Executable: python openbb_roic_backend.py --port 8002

# Load balancer (nginx)
Backend Name: Load Balancer
Executable: nginx -c /path/to/nginx.conf
```

### Database Backend

Add database support:
```yaml
Backend Name: ROIC Database
Environment: openbb
Executable: python roic_db_server.py
Environment Variables:
  DATABASE_URL=postgresql://user:pass@localhost/roic
  REDIS_URL=redis://localhost:6379
```

## 📊 Monitoring

### View Logs
1. Click "Logs" button on any backend
2. Logs show last 10,000 lines
3. Color codes removed for clarity
4. Auto-scrolls to bottom

### Health Checks
```bash
# Check all backends
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:6950/health
curl http://127.0.0.1:9000/health
```

### Performance Monitoring
```yaml
Backend Name: ROIC Monitoring
Executable: python -m prometheus_client --port 9090
Environment Variables:
  METRICS_PORT=9090
```

## 🎉 Benefits of OpenBB Backends

1. **Centralized Management** - All servers in one place
2. **Auto-Start** - Services start with OpenBB
3. **Environment Isolation** - Each backend uses specific conda env
4. **Easy HTTPS** - Built-in certificate generation
5. **Integrated Logging** - View logs without terminal
6. **MCP Support** - Direct Agent Chat integration

## Summary

The OpenBB Backends system provides professional management for all our ROIC services:

- ✅ REST API Backend
- ✅ MCP Server for Chat
- ✅ Development Server
- ✅ Production HTTPS
- ✅ Monitoring & Logs

This integration makes ROIC a first-class citizen in the OpenBB ecosystem!
