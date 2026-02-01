# Quick Start Guide - Auto-Trigger

## 🚀 Get Started in 5 Minutes

### Installation
```bash
pip install PySide6 keyboard mss pydirectinput
python main.py
```

**Run as Administrator** for F6 hotkey to work!

---

## 📍 Basic Setup (4 Steps)

### Step 1: Position the Red Box
- Drag the red box to where zombies spawn
- Click "Lock Box" when positioned correctly

### Step 2: Set the Background Color
- Click "Pick from Screen" mode
- Click the button and click on the spawn background
- OR enter hex color if you know it

### Step 3: Test & Adjust
- Press **F6** to enable detection
- If it works: ✅ You're done!
- If not clicking: **Lower** tolerance slider
- If clicking randomly: **Raise** tolerance slider

### Step 4: Fine-Tune
- Adjust "Click Delay" for click speed (default 30ms is usually good)
- Enable "Auto Reload" if your game needs it
- Save your position using "Save/Load Position"

---

## 🎮 Usage

**Start Detection:** Press **F6**  
**Stop Detection:** Press **F6** again  

**Status meanings:**
- "Running" = Watching for zombies
- "SPAMMING" = Detected zombie, clicking!
- "Stopped" = Not active

---

## ⚡ Common Settings

| Game Type | Tolerance | Click Delay |
|-----------|-----------|-------------|
| Fast zombies | 15-20 | 20-30ms |
| Slow zombies | 25-35 | 30-50ms |
| Crowded spawns | 10-15 | 10-20ms |

---

## 🔧 Quick Fixes

**Not detecting?** → Lower tolerance to 10-15  
**False triggers?** → Raise tolerance to 30-40  
**F6 not working?** → Run as Administrator  
**Box stuck?** → Click "Unlock Box"  
**Lost the box?** → Click "Reset Position"  

---

## 📋 Feature Cheat Sheet

| Button | What It Does |
|--------|--------------|
| Hide Box | Makes box invisible (still works) |
| Lock Box | Prevents accidental movement (turns yellow) |
| Reset Position | Returns box to screen center |
| Save/Load Position | Save box locations for later |

**Tolerance Slider:** How sensitive detection is (lower = more sensitive)  
**Click Delay:** Milliseconds between clicks (lower = faster)  
**Auto Reload:** Automatically press R every X seconds  

---

## ⚠️ Important

1. **Game Bans:** Use at your own risk - some games ban automation
2. **Admin Rights:** Required for F6 hotkey
3. **Test First:** Try in safe areas before important gameplay

---

**Need more help?** Read the full USER_GUIDE.md

**Ready to go?** Press F6 and start hunting zombies! 🧟
