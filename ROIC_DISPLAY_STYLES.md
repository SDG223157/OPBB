# 🎨 ROIC Display Styles - Why Different Layouts?

## Your Question: Why doesn't ROIC look like other APIs?

You noticed that ROIC output looks different from Yahoo Finance, Polygon, etc. in OpenBB. Here's why and how I've fixed it:

## 📊 The Difference Explained

### Other APIs (Yahoo Finance, Polygon, etc.)
- **Integrated into OpenBB core** as official providers
- **Standardized output** using OpenBB's display system
- **DataFrame/tabular format** by default
- **Consistent styling** across all providers

### ROIC Tool (Original)
- **Custom CLI tool** built outside OpenBB
- **Independent display** system
- **Text-based format** for clarity
- **Different styling** from OpenBB standards

## ✅ The Solution: Two Display Styles

I've now added **TWO display styles** you can switch between:

### 1️⃣ Custom Style (Original)
```
============================================================
  ROIC.AI QUALITY METRICS: AAPL
============================================================
Return on Invested Capital: 51.54%
Quality Rating: ⭐⭐⭐⭐⭐ Exceptional
Investment Grade: A+ (Premium business)
Quality Score: 95/100
Competitive Moat: Wide
```

**Pros:**
- Clean and simple
- Easy to read
- Focused on key metrics
- Mimics professional reports

### 2️⃣ OpenBB Style (New)
```
                    ROIC Quality Metrics - AAPL                     
╭────────────────────────────┬────────────┬────────────────────────╮
│ Metric                     │ Value      │ Assessment             │
├────────────────────────────┼────────────┼────────────────────────┤
│ Return on Invested Capital │ 51.54%     │ ⭐⭐⭐⭐⭐ Exceptional │
│ Quality Score              │ 95/100     │ A+                     │
│ Competitive Moat           │ Wide       │ 🏰                     │
│ Provider                   │ ROIC.ai    │ ✓                      │
│ Date                       │ 2025-11-19 │ Current                │
╰────────────────────────────┴────────────┴────────────────────────╯

────────────────────────────────────────────────────────────
symbol provider       date      roic  quality_score moat_rating
  AAPL     roic 2025-11-19 51.540468             95        Wide
────────────────────────────────────────────────────────────
```

**Pros:**
- Matches OpenBB's native style
- Professional table format
- DataFrame output for analysis
- Consistent with other providers

## 🔄 How to Switch Styles

### Check Current Style
```bash
./roic style
```

### Switch to OpenBB Style
```bash
./roic style openbb
./roic quality AAPL  # Now shows tables
```

### Switch to Custom Style
```bash
./roic style custom
./roic quality AAPL  # Shows original format
```

## 📊 Comparison with Other Providers

### Yahoo Finance in OpenBB
```
/equity/fundamental/metrics --symbol AAPL --provider yfinance

                     Fundamental Metrics                    
┏━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Symbol ┃ PE Ratio ┃ PEG Ratio┃ EPS      ┃ Revenue  ┃
┡━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ AAPL   │ 36.32    │ 3.51     │ 6.42     │ 385.6B   │
└────────┴──────────┴──────────┴──────────┴──────────┘
```

### ROIC with OpenBB Style
```
                    ROIC Quality Metrics - AAPL                     
╭────────────────────────────┬────────────┬────────────────────────╮
│ Metric                     │ Value      │ Assessment             │
├────────────────────────────┼────────────┼────────────────────────┤
│ Return on Invested Capital │ 51.54%     │ ⭐⭐⭐⭐⭐ Exceptional │
╰────────────────────────────┴────────────┴────────────────────────╯
```

Now they look similar! Both use tables and structured output.

## 🎯 Why Create a Custom Tool?

### OpenBB Providers
- Limited to what OpenBB officially supports
- Must follow OpenBB's provider interface
- Requires OpenBB Platform SDK integration
- Complex to add new providers

### Custom ROIC Tool
- **Flexible**: Can add any metrics we want
- **Independent**: Works alongside OpenBB
- **Specialized**: Focused on quality investing
- **Easy to extend**: Simple Python scripts

## 💡 Best of Both Worlds

You now have:

1. **Integration**: ROIC tool works alongside OpenBB
2. **Choice**: Two display styles to choose from
3. **Compatibility**: Export to CSV/JSON/Excel like OpenBB
4. **Flexibility**: Custom metrics not available elsewhere

## 🚀 Quick Examples

### OpenBB Style (Like Yahoo Finance)
```bash
./roic style openbb
./roic quality AAPL
./roic compare AAPL MSFT GOOGL
```

Shows professional tables with DataFrames, matching OpenBB's look.

### Custom Style (Original)
```bash
./roic style custom
./roic quality AAPL
./roic forecast AAPL
```

Shows clean, focused output optimized for readability.

## 📈 Advanced Integration Ideas

### Future Possibilities
1. **Full OpenBB Integration**: Register ROIC as official provider
2. **API Wrapper**: Make ROIC.ai API work in OpenBB directly
3. **Plugin System**: Create OpenBB extension package
4. **Terminal UI**: Build interactive dashboard

### Current Status
- ✅ Standalone CLI tool
- ✅ Two display styles
- ✅ Export capabilities
- ✅ Works alongside OpenBB

## 🎉 Summary

**Why Different?** ROIC is a custom tool, not an integrated OpenBB provider.

**Solution:** Added OpenBB-style display option to match native providers.

**Result:** You can now choose between:
- **Custom style**: Clean and simple
- **OpenBB style**: Professional tables

Both work great - it's just a matter of preference!

---
*Switch anytime with: `./roic style [openbb|custom]`*
