# 🚀 Quick Start Guide

## Installation (One-Time Setup)

```bash
# 1. Navigate to project folder
cd "c:\Users\Kothi Srinish Reddy\OneDrive\Desktop\sravya pinni"

# 2. Install dependencies
python -m pip install -r requirements.txt
```

## Running the Application

```bash
# Simply run:
streamlit run app.py

# The app will open at http://localhost:8501
```

## First Steps

### Step 1: Upload an Image
- Click "📤 Upload Image" in Live Detection page
- Select a JPG, JPEG, or PNG file from your gallery exhibit

### Step 2: Adjust Sensitivity (Optional)
- Use the slider to set detection sensitivity
- Default value (0.7) works well for most cases
- Higher = more sensitive to small defects

### Step 3: Analyze
- Click "🔍 Analyze Image" button
- Wait for the analysis to complete

### Step 4: Review Results
- **Results Tab**: See defect table and metrics
- **Processed Image Tab**: View annotated image
- **Statistics Tab**: Check detailed analytics

## Navigation

| Page | Purpose |
|------|---------|
| 🔍 Live Detection | Upload and analyze exhibit images |
| 📊 Detection History | View past analyses and trends |
| ⚠️ Alert Dashboard | Monitor critical issues |
| ⚙️ System Settings | Configure and manage system |

## Quick Tips

✅ **Better Detection**: Use clear, well-lit images
✅ **Avoid False Positives**: Lower sensitivity for smooth surfaces
✅ **Track Trends**: Use history to monitor exhibit condition
✅ **Regular Checks**: Schedule periodic analyses

## Troubleshooting

### App Won't Start
```bash
# Check Python is installed
python --version

# Verify pip installation
python -m pip --version

# Reinstall dependencies
python -m pip install --upgrade -r requirements.txt
```

### Image Upload Not Working
- Ensure image is JPG, JPEG, or PNG format
- Check file size is under 200MB
- Try refreshing the browser (Ctrl+R)

### Slow Analysis
- Use smaller image resolution
- Lower the sensitivity value
- Close other applications

## File Structure

```
sravya pinni/
├── app.py                 # Main application
├── detector.py            # Detection module
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
├── assets/               # Images/assets folder
├── images/               # Output images folder
├── reports/              # Reports folder
└── history.csv           # Session history log
```

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for dependencies
- **Browser**: Chrome, Edge, Firefox, or Safari
- **Internet**: Not required (offline capable)

## Keyboard Shortcuts

- **Ctrl+R**: Refresh the app
- **Ctrl+Shift+R**: Hard refresh
- **F12**: Open browser dev tools

## Getting Help

1. **In-App Help**: Click the "?" icon on any setting
2. **System Info**: Check ⚙️ Settings → System Information
3. **Documentation**: Read the full README.md file

## Common Workflows

### Daily Inspection
1. Go to Live Detection
2. Upload photo of exhibit
3. Click Analyze
4. Check Results tab for issues
5. Document in history

### Trend Analysis
1. Go to Detection History
2. Review Average Accuracy
3. Check Total Defects Found
4. Monitor patterns over time

### Alert Management
1. Go to Alert Dashboard
2. Check Active Alerts count
3. Review Critical Issues
4. Monitor Success Rate

## Best Practices

✓ Save important analyses
✓ Regular monitoring schedule
✓ Document environmental conditions
✓ Keep detection sensitivity consistent
✓ Use high-quality images

## Advanced Configuration

### Adjust Detection Sensitivity
- **Settings → Detection Configuration**
- Minimum Defect Area: 50-500 pixels
- Confidence Threshold: 50-99%

### Customize Display
- **Settings → Display Preferences**
- Toggle bounding boxes
- Show/hide confidence scores

## Support

For issues:
1. Check Settings → System Information
2. Verify Python 3.8+ installed
3. Reinstall requirements
4. Check browser console (F12) for errors

---

**Ready to analyze your exhibits?** 🎨

Just run `streamlit run app.py` and get started!
