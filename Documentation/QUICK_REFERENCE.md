# 🛡️ SafeBank AI - Quick Reference Card

## 🚀 Launch Commands

```bash
# Premium UI (Recommended)
run_premium_ui.bat

# Or manually
streamlit run app_premium.py

# Standard UI
streamlit run streamlit_app.py

# Custom port
streamlit run app_premium.py --server.port 8502
```

## 🌐 Access URLs

```
Local:   http://localhost:8501
Network: http://YOUR_IP:8501
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app_premium.py` | Premium UI main app |
| `streamlit_app.py` | Standard UI |
| `run_premium_ui.bat` | Windows launcher |
| `run_all.py` | Train all models |

## 🎯 Navigation

| Icon | Page | Purpose |
|------|------|---------|
| 🏠 | Single Transaction | Analyze one transaction |
| 📊 | Batch Processing | Process CSV files |
| 📈 | Analytics | View dashboard |
| 🔧 | System Info | Monitor system |

## 🔧 Common Tasks

### Train Models
```bash
python run_all.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Clear Cache
```
System Info → Clear Cache button
```

### Export Results
```
Batch Processing → Download button
```

## 📊 Risk Levels

| Level | Score | Color | Action |
|-------|-------|-------|--------|
| HIGH | ≥70% | 🔴 Red | BLOCK |
| MEDIUM | 40-69% | 🟡 Yellow | REVIEW |
| LOW | <40% | 🔵 Blue | MONITOR |
| SAFE | <30% | 🟢 Green | APPROVE |

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Models not loading | Run `python run_all.py` |
| Port in use | Use `--server.port 8502` |
| Import error | Run `pip install -r requirements.txt` |
| Slow performance | Clear cache in System Info |

## 📞 Documentation

| File | Content |
|------|---------|
| `LAUNCH_GUIDE.md` | Complete launch guide |
| `UI_GUIDE.md` | Detailed UI features |
| `PREMIUM_UI_README.md` | Premium UI overview |
| `UI_COMPARISON.md` | Standard vs Premium |

## 🎨 Color Codes

```
Primary:   #1e3a8a (Navy Blue)
Accent:    #fbbf24 (Gold)
Success:   #10b981 (Green)
Warning:   #f59e0b (Orange)
Danger:    #ef4444 (Red)
```

## ⌨️ Keyboard Shortcuts

```
Ctrl + R  →  Refresh page
Ctrl + C  →  Stop server
F5        →  Reload page
```

## 📈 Performance

```
Load Time:      2-3 seconds
Processing:     <100ms per transaction
Memory:         ~250-350 MB
Batch Speed:    50-100ms per transaction
```

## 🔐 Security

```
✅ Session-based isolation
✅ No persistent storage
✅ Local inference
✅ Input validation
✅ Secure model loading
```

## 📊 CSV Format

Required columns for batch processing:
```
Transaction_Amount
Transaction_Date
Transaction_Time
Transaction_Location
Card_Type
Transaction_Currency
Transaction_Status
Previous_Transaction_Count
Distance_Between_Transactions_km
Time_Since_Last_Transaction_min
Authentication_Method
Transaction_Velocity
Transaction_Category
```

## 🎯 Quick Test Cases

### Low Risk
```
Amount: ₹5,000
Time: 2:00 PM
Auth: PIN
Distance: 5 km
```

### High Risk
```
Amount: ₹95,00,000
Time: 2:30 AM
Auth: Failed
Distance: 800 km
```

## 📞 Quick Support

1. Check System Info page
2. Review error messages
3. Consult documentation
4. Clear cache and retry

## 🎉 Quick Start

```bash
# 1. Train models (if needed)
python run_all.py

# 2. Launch UI
run_premium_ui.bat

# 3. Open browser
http://localhost:8501

# 4. Start detecting fraud!
```

---

**🛡️ SafeBank AI v2.0.1**  
*Quick Reference for Fraud Detection*

**Need detailed help?** See `LAUNCH_GUIDE.md`
