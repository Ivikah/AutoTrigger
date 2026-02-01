# Auto-Trigger - Screen Color Detection & Automation Tool

> **A smart automation tool for gaming that detects screen color changes and triggers actions**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

Auto-Trigger is a Python-based automation tool designed for gaming scenarios where you need to respond to visual changes on screen. Originally created for Roblox zombie games, it monitors a specific screen area and automatically performs actions (clicking, reloading) when color changes are detected.

### ✨ Key Features

- 🎯 **Movable Detection Box** - Visual 20x20px box showing exactly where you're monitoring
- 🎨 **Flexible Color Detection** - Pick colors from screen or enter hex codes
- 🔒 **Lock & Save Positions** - Lock box in place and save positions for quick switching
- ⚡ **Adjustable Sensitivity** - Fine-tune tolerance for perfect detection
- 🖱️ **Customizable Click Speed** - Control how fast it clicks (10-1000ms delay)
- 🔄 **Auto Reload** - Automatically press R key at custom intervals
- ⌨️ **F6 Hotkey** - Quick enable/disable without switching windows
- 🌙 **Modern Dark UI** - Professional, easy-to-use interface

---

## 🎮 Use Cases

- **Zombie Games** - Auto-kill zombies as they spawn
- **Defense Games** - Auto-attack enemies at spawn points
- **Resource Farming** - Auto-collect when resources appear
- **Reaction-Based Games** - Instant response to visual cues
- **Any Color Change Detection** - Monitor specific screen areas

---

## 📋 Requirements

### Python Version
- Python 3.8 or higher

### Dependencies
```bash
pip install PySide6 keyboard mss pydirectinput
```

**Package Details:**
- `PySide6` - Qt-based GUI framework
- `keyboard` - Global hotkey support (requires admin rights)
- `mss` - Fast screen capture
- `pydirectinput` - Reliable mouse and keyboard control

---

## 🚀 Installation

### Quick Install

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd auto-trigger
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install PySide6 keyboard mss pydirectinput
   ```

3. **Run the script**
   ```bash
   python main.py
   ```

### ⚠️ Important: Administrator Rights

For the F6 hotkey to work, the script needs administrator privileges:

**Windows:**
- Right-click `main.py` → "Run as administrator"
- Or run command prompt as admin, then run the script

**Linux:**
```bash
sudo python3 main.py
```

**macOS:**
```bash
sudo python3 main.py
```

---

## 📚 Documentation

We provide multiple documentation levels for different user needs:

### For New Users
- **[QUICK_START.md](QUICK_START.md)** - Get up and running in 5 minutes
- Just want to start? This is for you!

### For All Users
- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete feature documentation
  - Detailed feature explanations
  - Step-by-step tutorials
  - Tips & tricks
  - Troubleshooting guide
  - Advanced configuration

### Quick Reference
See the Quick Reference Card in USER_GUIDE.md for hotkeys and common settings.

---

## 🎯 Quick Start

1. **Launch the script** (as administrator)
2. **Position the red box** where you want to detect changes
3. **Pick a base color** from the background
4. **Press F6** to enable detection
5. Done! Script will click when colors change

Need help? Check [QUICK_START.md](QUICK_START.md) for detailed instructions.

---

## 🖼️ Interface Overview

### Main Window
```
┌─────────────────────────────────────┐
│     Auto-Trigger Configuration     │
├─────────────────────────────────────┤
│ ☐ Enable Detection (F6)  [Delay:30]│
│ Tolerance: [=========>] 20          │
│                                     │
│ Detection Box:                      │
│ [Hide Box] [Lock Box]              │
│ [Reset Pos] [Save/Load]            │
│                                     │
│ Color Mode: [Pick from Screen ▼]   │
│ [Click to Pick Color from Screen]  │
│                                     │
│ Base Color: RGB(0, 0, 0)           │
│ [        █████████        ]        │
│                                     │
│ ☐ Auto Reload    [Delay: 1s]      │
│                                     │
│ Status: Ready                      │
└─────────────────────────────────────┘
```

### Detection Box
- **Red Box** = Unlocked, draggable
- **Yellow Box** = Locked, fixed in place
- 20x20 pixels outer, 16x16 inner detection area

---

## ⚙️ Configuration

### Basic Settings

| Setting | Description | Recommended Values |
|---------|-------------|-------------------|
| Tolerance | Detection sensitivity | 15-30 for most games |
| Click Delay | Milliseconds between clicks | 30-50ms standard |
| Auto Reload Delay | Seconds between R presses | 1-3s typical |

### Detection Box States

- **Visible + Unlocked (Red)** - Can be moved, detection active
- **Visible + Locked (Yellow)** - Cannot be moved, detection active
- **Hidden** - Invisible but still detecting

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| F6 doesn't work | Run as administrator |
| Not detecting changes | Lower tolerance slider |
| Too many false triggers | Raise tolerance slider |
| Box disappeared | Click "Reset Position" |
| Can't move box | Click "Unlock Box" |

See [USER_GUIDE.md](USER_GUIDE.md) for comprehensive troubleshooting.

---

## 🛡️ Safety & Disclaimers

### ⚠️ Important Warnings

1. **Game Terms of Service**: This tool automates gameplay. Many games prohibit automation and may ban accounts using such tools.

2. **Use at Your Own Risk**: The developers are not responsible for:
   - Game bans or account suspensions
   - Any consequences of using this tool
   - Lost progress or data

3. **Ethical Use**: This tool is provided for educational purposes. Please respect:
   - Game developers and their rules
   - Other players and fair gameplay
   - Your own gaming experience

4. **Privacy**: The script captures screen content. Do not run it on screens containing sensitive information.

### ✅ Best Practices

- Test in single-player or practice modes first
- Read your game's Terms of Service
- Don't use in competitive/ranked matches
- Take breaks - don't run 24/7
- Monitor your usage to avoid detection

---

## 🔄 Version History

### Version 1.0 (Current)
- ✨ Initial release
- 🎯 Movable detection box with lock feature
- 💾 Save/load position system
- 🔄 Auto-reload functionality
- 🎨 Dark theme UI
- ⌨️ F6 hotkey support
- 🖱️ Adjustable click delay
- 📊 Tolerance slider with visual feedback

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with details
2. **Suggest Features**: Describe your idea in an issue
3. **Submit Code**: Fork, make changes, submit PR
4. **Improve Docs**: Fix typos, add examples, clarify instructions

### Development Setup
```bash
git clone <repository-url>
cd auto-trigger
pip install -r requirements.txt
python main.py
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What This Means

✅ You can:
- Use commercially
- Modify the code
- Distribute
- Use privately

❌ You cannot:
- Hold the authors liable
- Use authors' names for endorsement

📋 You must:
- Include the license and copyright notice
- State changes made to the code

---

## 🙏 Acknowledgments

- **PySide6** - For the beautiful Qt framework
- **mss** - For blazing-fast screen capture
- **pydirectinput** - For reliable input control
- **Community** - For feedback and testing

---

## 📞 Support

### Getting Help

1. **Check Documentation**
   - [QUICK_START.md](QUICK_START.md) for quick answers
   - [USER_GUIDE.md](USER_GUIDE.md) for detailed help

2. **Common Issues**
   - See Troubleshooting section above
   - Check USER_GUIDE.md Troubleshooting chapter

3. **Still Stuck?**
   - Open an issue with:
     - Your Python version
     - Operating system
     - Error message
     - Steps to reproduce

### Feature Requests

Have an idea? Open an issue with:
- Clear description of the feature
- Why it would be useful
- How you envision it working

---

## 🌟 Star History

If you find this tool useful, please consider giving it a star! ⭐

---

## 📊 Project Status

- **Status**: Active Development
- **Stability**: Stable
- **Python Version**: 3.8+
- **Platform**: Windows, Linux, macOS
- **Last Updated**: February 2026

---

**Built with ❤️ for the gaming community**

**Happy Gaming! 🎮**
