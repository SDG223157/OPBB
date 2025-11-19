# ROIC Integration - Quick Test Guide

## 🎯 Testing in Different Environments

### 1. Regular Terminal Tests (bash/zsh)
```bash
# Navigate to project
cd /Users/sdg223157/OPBB-1

# Test ROIC CLI
./roic quality AAPL
./roic forecast MSFT  
./roic compare AAPL GOOGL

# Test wrapper (needs OpenBB env)
source /Users/sdg223157/OPBB/openbb-env/bin/activate
python3 roic_wrapper.py AAPL

# Run comprehensive tests
python3 test_roic_simple.py
```

### 2. OpenBB CLI Tests
```bash
# First launch OpenBB
./launch-openbb-premium.sh

# Inside OpenBB (you'll see 🦋 prompt):
/equity/fundamental/metrics --symbol AAPL --provider roic
/equity/fundamental/metrics --symbol AAPL --provider yfinance
/equity/estimates/consensus --symbol MSFT --provider roic

# Exit OpenBB
exit
```

### 3. Combined Workflow Example
```bash
# Step 1: Quick ROIC check in terminal
./roic quality AAPL

# Step 2: Get combined data
source /Users/sdg223157/OPBB/openbb-env/bin/activate
python3 roic_wrapper.py AAPL

# Step 3: Deep dive in OpenBB
./launch-openbb-premium.sh
# (Inside OpenBB):
/equity/fundamental/income --symbol AAPL --provider polygon
/equity/fundamental/metrics --symbol AAPL --provider roic
exit
```

## ❌ Common Mistakes to Avoid

| ❌ Wrong | ✅ Correct | Why |
|---------|----------|-----|
| Running `./roic` in OpenBB | Run `./roic` in bash/terminal | OpenBB doesn't understand shell commands |
| Using `python` command | Use `python3` command | macOS requires python3 |
| No environment activated for wrapper | `source .../openbb-env/bin/activate` first | Wrapper needs OpenBB modules |

## 🔍 How to Check Your Environment

```bash
# In terminal, check if you're in bash:
echo $SHELL  # Should show /bin/zsh or /bin/bash

# Check if OpenBB env is active:
which python3  # Should show openbb-env path if active

# Check if in OpenBB CLI:
# Look for 🦋 emoji in prompt
```

## 📊 Expected Results

### ROIC CLI Output:
```
ROIC Quality Metrics - AAPL
┌────────────────────┬──────┬──────────────┐
│ Return on Capital  │ 51%  │ Exceptional  │
│ Quality Score     │ 95   │ A+           │
│ Moat             │ Wide │ 🏰           │
└────────────────────┴──────┴──────────────┘
```

### OpenBB with ROIC Provider:
```
/equity/fundamental/metrics --symbol AAPL --provider roic
                           
    symbol  roic  quality_score  moat_rating
    AAPL   51.54         95        Wide
```

## 🎉 Success Indicators

✅ ROIC CLI returns quality scores
✅ Wrapper shows both OpenBB and ROIC data
✅ OpenBB recognizes `--provider roic` option
✅ All tests pass in `test_roic_simple.py`
