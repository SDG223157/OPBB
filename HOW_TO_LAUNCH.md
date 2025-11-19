# 🚀 How to Launch OpenBB with Premium APIs

## ⚠️ Important: Exit OpenBB First!

If you see the butterfly prompt `(🦋) / $`, you're already inside OpenBB. You need to exit first:

```
/exit
```
or press `Ctrl+D`

## 📋 Correct Launch Process

### Step 1: Make sure you're in regular terminal (not in OpenBB)
Your prompt should look like:
```bash
username@machine ~ $ 
```
NOT like:
```
(🦋) / $
```

### Step 2: Navigate to the OPBB directory
```bash
cd /Users/sdg223157/OPBB
```

### Step 3: Launch with your premium APIs
```bash
./launch-openbb-premium.sh
```

## 🎯 Complete Example

```bash
# If you're in OpenBB, exit first
/exit

# Now in regular terminal, navigate to OPBB
cd /Users/sdg223157/OPBB

# Launch with all APIs
./launch-openbb-premium.sh

# You'll see:
==============================================
   OpenBB CLI - PREMIUM EDITION
   With Advanced Fundamental Analysis
==============================================
✅ ROIC.ai: Quality & ROIC Analysis
✅ Finviz Elite: Analyst Price Targets
✅ Polygon: Real-time Market Data
✅ FRED: Economic Indicators

# Then OpenBB will start with the (🦋) prompt
```

## 📊 Once Inside OpenBB

Now you can use premium commands:

```bash
# Get analyst price targets (Finviz)
/equity/estimates/price_target --symbol AAPL --provider finviz

# Get real-time quotes (Polygon)
/equity/price/quote --symbol AAPL --provider polygon

# Get economic data (FRED)
/economy/fred_series --symbol VIXCLS --provider fred

# Exit when done
/exit
```

## 🔄 Alternative: Run Python Scripts Directly

If you want forecast data without entering OpenBB CLI:

```bash
# Make sure you're in regular terminal (not OpenBB)
cd /Users/sdg223157/OPBB

# Activate Python environment
source openbb-env/bin/activate

# Run analysis scripts
python master_forecast.py      # Complete 3-year forecast
python roic_analysis.py        # Quality analysis
python get_complete_forecasts.py  # Analyst targets
```

## ❌ Common Mistakes

### Wrong: Trying to run shell commands inside OpenBB
```
(🦋) / $ ./launch-openbb-premium.sh  # ❌ Won't work
```

### Right: Run from regular terminal
```bash
$ ./launch-openbb-premium.sh  # ✅ Works
```

### Wrong: Forgetting to navigate to OPBB directory
```bash
$ ./launch-openbb-premium.sh  # ❌ File not found
```

### Right: Navigate first, then run
```bash
$ cd /Users/sdg223157/OPBB
$ ./launch-openbb-premium.sh  # ✅ Works
```

## 📝 Quick Reference

**Exit OpenBB**: `/exit` or `Ctrl+D`
**Launch with APIs**: `./launch-openbb-premium.sh`
**Python scripts**: `python master_forecast.py`

Remember: Shell scripts (`.sh` files) run in terminal, not inside OpenBB!
