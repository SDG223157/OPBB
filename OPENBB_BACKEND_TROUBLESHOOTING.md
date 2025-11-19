# 🔧 OpenBB Backend Connection Troubleshooting

## Quick Fix for Your Current Issue

### ❌ The Problems You're Seeing:

1. **Error 500** - Server not reachable
2. **Missing apps.json** - Now fixed! ✅
3. **Wrong URL** - Using 0.0.0.0 instead of 127.0.0.1

### ✅ Solution Steps:

## Step 1: Start the Backend Server

```bash
# Open a new terminal
cd /Users/sdg223157/OPBB

# Make the script executable
chmod +x start_roic_backend_for_openbb.sh

# Start the server
./start_roic_backend_for_openbb.sh
```

**Keep this terminal open!** The server must be running.

## Step 2: Fix the URL in OpenBB

In the OpenBB "Add apps" dialog:

1. **Name**: `ROIC Quality Metrics API`
2. **Endpoint URL**: `http://127.0.0.1:8000` (NOT 0.0.0.0!)
3. **Validate widgets**: Set to `No` (initially)

## Step 3: Test the Connection

Before clicking "Test" in OpenBB, verify the server is working:

```bash
# In another terminal, test the endpoints:
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/apps.json
curl http://127.0.0.1:8000/widgets.json
```

You should see JSON responses.

## Step 4: Add to OpenBB

1. Click **"Test"** - Should show success
2. Click **"Add"** to add the backend

## 📋 Complete Configuration Checklist

| Step | Action | Status |
|------|--------|---------|
| 1 | Backend server running | Check terminal |
| 2 | Using correct URL (127.0.0.1:8000) | ✅ |
| 3 | apps.json file exists | ✅ Created |
| 4 | CORS enabled in backend | ✅ Added |
| 5 | Server responds to /health | Test with curl |

## 🚀 Alternative: Use OpenBB Backends Screen

Instead of adding manually, configure in OpenBB's **Backends** screen:

```yaml
Backend Name: ROIC API
Environment: openbb
Executable: python openbb_roic_backend.py
Working Directory: /Users/sdg223157/OPBB
Start Automatically: Yes
```

Then the backend will:
- Start automatically
- Show URL when ready
- Be available for app connection

## 🔍 Common Issues and Fixes

### Issue: "Server error occurred" (500)

**Causes:**
- Server not running
- Wrong URL (0.0.0.0 vs 127.0.0.1)
- Port blocked

**Fix:**
```bash
# Check if server is running
lsof -i :8000

# If nothing shows, start server:
./start_roic_backend_for_openbb.sh
```

### Issue: "Missing apps.json file"

**Fix:** Already created! The file now exists at `/Users/sdg223157/OPBB/apps.json`

### Issue: Connection refused

**Fix:**
```bash
# Check firewall
sudo pfctl -sr | grep 8000

# Allow port 8000
sudo pfctl -d  # Disable firewall temporarily
```

### Issue: CORS error in browser console

**Fix:** Already added CORS middleware to backend! ✅

## 📊 Test URLs

Once the server is running, test these:

| Endpoint | URL | Expected |
|----------|-----|----------|
| Root | http://127.0.0.1:8000/ | API info |
| Apps | http://127.0.0.1:8000/apps.json | Apps config |
| Widgets | http://127.0.0.1:8000/widgets.json | Widget list |
| Docs | http://127.0.0.1:8000/docs | Swagger UI |
| Health | http://127.0.0.1:8000/health | {"status": "healthy"} |

## 🎯 Quick Test Command

Run this to test everything at once:

```bash
# Test all endpoints
for endpoint in "" "apps.json" "widgets.json" "health"; do
  echo "Testing /$endpoint:"
  curl -s http://127.0.0.1:8000/$endpoint | head -n 2
  echo ""
done
```

## ✨ Working Configuration

When everything is working, you'll see:

1. ✅ Server running in terminal
2. ✅ "Test" button shows success in OpenBB
3. ✅ Apps appear in OpenBB interface
4. ✅ Widgets load without errors

## 📝 Final Notes

- **Always use 127.0.0.1** for localhost connections (not 0.0.0.0)
- **Keep server terminal open** while using the backend
- **Check logs** if you see errors: Look at the terminal where server is running
- **Restart server** if needed: Ctrl+C then run start script again

## Need More Help?

1. Check server logs in the terminal
2. Verify all files exist: `ls -la /Users/sdg223157/OPBB/*.json`
3. Test with curl before adding to OpenBB
4. Use OpenBB Backends screen for automatic management
