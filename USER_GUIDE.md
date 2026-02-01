# Auto-Trigger User Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Feature Guide](#feature-guide)
- [Step-by-Step Usage](#step-by-step-usage)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Auto-Trigger** is a color-detection automation tool designed for gaming (specifically Roblox zombie games). The script monitors a specific area of your screen and automatically clicks when it detects a color change, helping you auto-kill zombies as they spawn.

### Key Capabilities:
- ✅ Detects color changes in a customizable screen area
- ✅ Automatically clicks when changes are detected
- ✅ Movable, lockable detection box
- ✅ Save/load detection box positions
- ✅ Auto-reload functionality
- ✅ Adjustable sensitivity and click speed
- ✅ Dark theme UI

---

## Requirements

Before running the script, ensure you have these Python packages installed:

```bash
pip install PySide6 keyboard mss pydirectinput
```

**Required Packages:**
- `PySide6` - User interface
- `keyboard` - Hotkey functionality
- `mss` - Screen capture
- `pydirectinput` - Mouse/keyboard control

**Important:** The script may require **administrator privileges** for the F6 hotkey to work properly.

---

## Getting Started

### First Launch

1. **Run the script:**
   ```bash
   python main.py
   ```

2. **You'll see two windows:**
   - Main control panel (dark theme UI)
   - Red detection box (20x20 pixels) in the center of your screen

3. **The detection box:**
   - Red border = unlocked and ready to move
   - Yellow border = locked in place
   - Inner 16x16 area = actual detection zone

---

## Feature Guide

### 🎯 Detection Box

**What it does:** Visual indicator showing where the script is monitoring for color changes.

**Controls:**

#### Hide/Show Box
- **Purpose:** Toggles the visibility of the detection box
- **Usage:** Click to hide the red box from view (useful when it's in your way)
- **Note:** Detection still works when hidden

#### Lock/Unlock Box
- **Purpose:** Prevents accidental movement of the detection box
- **Usage:** Click to toggle between locked (yellow) and unlocked (red)
- **When Locked:** Box turns yellow and cannot be dragged
- **When Unlocked:** Box is red and can be moved by clicking anywhere inside it

#### Reset Position
- **Purpose:** Returns the detection box to the center of your screen
- **Usage:** Click to instantly center the box

#### Save/Load Position
- **Purpose:** Save and load detection box positions for different spawn points
- **Usage:** 
  1. Position the box where you want
  2. Click "Save/Load Position"
  3. Click "Save Current" and enter a name (e.g., "Left Spawn")
  4. Later, click "Load Selected" to return to that exact position
- **Features:**
  - Save multiple positions with custom names
  - Double-click a saved position to load it instantly
  - Delete custom positions (default positions are protected)

---

### 🎨 Color Detection Settings

#### Base Color

**What it is:** The "default" color the script expects to see in the detection area.

**How to set it:**

**Method 1: Enter Hex Value**
1. Select "Enter Hex Value" from the Color Mode dropdown
2. Type the hex color code (e.g., `#FF0000` for red)
3. Color updates automatically

**Method 2: Pick from Screen**
1. Select "Pick from Screen" from the Color Mode dropdown
2. Click "Click to Pick Color from Screen"
3. Your cursor becomes a crosshair
4. Click anywhere on your screen to sample that color
5. Press ESC to cancel

**The colored bar:** Shows your selected base color for visual confirmation

---

#### Tolerance Slider

**What it does:** Controls how different a color must be from the base color to trigger detection.

**Range:** 1-100
- **Lower values (1-20):** Very sensitive, detects small color changes
- **Medium values (20-50):** Balanced sensitivity
- **Higher values (50-100):** Less sensitive, only detects major color changes

**How to adjust:**
1. Start with the default value (20)
2. If it's triggering too often: increase tolerance
3. If it's not triggering when it should: decrease tolerance

**The number:** Shows the current tolerance value in real-time

---

### ⚡ Enable Detection (F6)

**Main toggle:** Starts and stops the detection system.

**How to use:**
- **Click the checkbox** OR **Press F6** on your keyboard to toggle
- ✅ Checked = Detection active, script is monitoring and will spam clicks
- ☐ Unchecked = Detection disabled, script is idle

**Status indicators:**
- "Status: Ready" - Script configured, waiting to start
- "Status: Running" - Actively monitoring for color changes
- "Status: SPAMMING" - Color change detected, clicking rapidly
- "Status: Stopped" - Detection disabled

**Note:** When detection is active, most settings are locked to prevent interference.

---

### 🖱️ Click Delay

**What it does:** Controls how fast the script clicks when a color change is detected.

**Range:** 10-1000 milliseconds
- **10ms:** Extremely fast clicking (~100 clicks/second)
- **30ms (default):** Fast clicking (~33 clicks/second)
- **100ms:** Moderate clicking (~10 clicks/second)
- **1000ms:** Slow clicking (1 click/second)

**When to adjust:**
- Game has click rate limits → Increase delay
- Need faster reaction → Decrease delay
- Getting kicked for "spam" → Increase delay

---

### 🔄 Auto Reload

**What it does:** Automatically presses the 'R' key at regular intervals.

**Use case:** Many games require periodic reloading of weapons.

**Controls:**

#### Auto Reload Checkbox
- ☐ Unchecked = Auto reload disabled
- ✅ Checked = Auto reload active, pressing 'R' automatically

#### Delay (seconds)
**Range:** 1-60 seconds
- **1s (default):** Presses 'R' every second
- **5s:** Presses 'R' every 5 seconds
- **10s:** Presses 'R' every 10 seconds

**Note:** Auto reload works independently of color detection - you can use it alone or together with the detection system.

---

## Step-by-Step Usage

### Basic Setup (For Zombie Auto-Kill)

**Step 1: Position the Detection Box**
1. Launch the script
2. Go to your zombie game
3. Find where zombies spawn
4. Drag the red detection box to that spawn point
5. Click "Lock Box" to prevent accidental movement

**Step 2: Set the Base Color**
1. Option A: Pick the color of the spawn area background
   - Select "Pick from Screen"
   - Click "Click to Pick Color from Screen"
   - Click on the spawn area background
   
2. Option B: Enter the hex code if you know it
   - Select "Enter Hex Value"
   - Type the hex code

**Step 3: Adjust Tolerance**
1. Start with default (20)
2. Enable detection (F6) to test
3. If it clicks when zombies appear: ✅ Perfect!
4. If it doesn't click: Lower tolerance (try 10-15)
5. If it clicks randomly: Raise tolerance (try 30-40)

**Step 4: Set Click Speed**
1. Adjust "Click Delay" based on game
2. For most games, 30-50ms works well
3. Test and adjust as needed

**Step 5: Enable Auto Reload (Optional)**
1. Check "Auto Reload"
2. Set delay based on your weapon's reload time
3. Common values: 1-3 seconds

**Step 6: Activate**
1. Press F6 or check "Enable Detection"
2. Watch the status: "Running" → "SPAMMING" when zombies appear
3. Press F6 again to stop

---

### Saving Positions for Multiple Spawn Points

If zombies spawn from multiple locations:

1. **Position 1:**
   - Move box to first spawn point
   - Click "Save/Load Position"
   - Click "Save Current"
   - Name it "Left Spawn"

2. **Position 2:**
   - Move box to second spawn point
   - Click "Save/Load Position"
   - Click "Save Current"
   - Name it "Right Spawn"

3. **Switch between positions:**
   - Click "Save/Load Position"
   - Double-click "Left Spawn" or "Right Spawn" to switch instantly

---

## Tips & Tricks

### 🎯 Optimal Detection Box Placement
- Place the box where zombies' bodies first appear
- Avoid placing it where environmental objects might pass
- The smaller the movement area, the more reliable the detection

### 🎨 Choosing Base Colors
- Pick a color that contrasts strongly with zombie colors
- Avoid dynamic areas (shadows, moving objects)
- Test by enabling detection and watching for false triggers

### ⚙️ Performance Optimization
- Close unnecessary background programs
- If the script is slow, increase click delay slightly
- Lower tolerance values require more processing

### 🔒 Prevent Accidental Changes
- Always lock the box once positioned correctly
- Save important positions so you can restore them easily
- Disable detection (F6) before adjusting settings

### 🎮 Game-Specific Tips
- **High zombie spawn rate:** Lower click delay (10-20ms)
- **Slow zombie spawn rate:** Higher tolerance (30-40)
- **Multiple spawn points:** Save positions for quick switching
- **Fast-moving zombies:** Place box closer to spawn point

---

## Troubleshooting

### ❌ Script Won't Start
**Problem:** Error messages when launching
**Solution:**
- Ensure all required packages are installed: `pip install PySide6 keyboard mss pydirectinput`
- Try running as administrator

---

### ❌ F6 Hotkey Doesn't Work
**Problem:** Pressing F6 does nothing
**Solution:**
- Run the script as administrator (right-click → Run as administrator)
- Check if another program is using F6
- Look at the status label - if it says "Hotkey failed to register", restart as admin

---

### ❌ Detection Box Not Visible
**Problem:** Can't see the red box
**Solution:**
- Click "Show Box" button
- It might be off-screen - click "Reset Position"
- Check if it's behind your game window

---

### ❌ Not Detecting Color Changes
**Problem:** Zombies appear but script doesn't click
**Solutions:**
1. **Lower the tolerance** (try values below 20)
2. **Verify base color** - re-pick the background color
3. **Check box position** - ensure it's on the spawn point
4. **Test with extreme tolerance** - set to 1 and see if it detects anything

---

### ❌ False Triggers / Random Clicking
**Problem:** Script clicks when nothing is there
**Solutions:**
1. **Raise the tolerance** (try 30-50)
2. **Reposition the box** - avoid dynamic areas
3. **Re-pick base color** - might have drifted
4. **Lock the box** - ensure it's not moving

---

### ❌ Box Can't Be Moved
**Problem:** Clicking and dragging doesn't move the box
**Solution:**
- Check if it's locked (yellow = locked, red = unlocked)
- Click "Unlock Box" button
- If still stuck, click "Reset Position"

---

### ❌ Clicking Too Slow/Fast
**Problem:** Not clicking at the right speed
**Solution:**
- Adjust "Click Delay (ms)"
- Lower = faster clicks
- Higher = slower clicks
- Try 30ms as a starting point

---

### ❌ Getting Kicked from Game
**Problem:** Game detects you as "spamming" or "botting"
**Solutions:**
1. **Increase click delay** to 100-200ms
2. **Use auto reload less frequently**
3. **Don't run 24/7** - take breaks
4. Some games have anti-cheat - use at your own risk

---

### ❌ Position Manager Not Saving
**Problem:** Saved positions disappear
**Solution:**
- Positions only persist during the current session
- For permanent positions, add them to DEFAULT_POSITIONS in the code (see below)

---

## Advanced: Adding Permanent Default Positions

For script distributors who want to pre-configure positions:

1. Open `main.py` in a text editor
2. Find the `PositionManagerDialog` class (around line 104)
3. Locate the `DEFAULT_POSITIONS` dictionary:

```python
DEFAULT_POSITIONS = {
    # Example: "Name": QPoint(x, y),
}
```

4. Add your positions:

```python
DEFAULT_POSITIONS = {
    "Left Spawn": QPoint(500, 400),
    "Right Spawn": QPoint(1200, 400),
    "Center": QPoint(960, 540),
}
```

5. Save and restart the script
6. These positions will appear for all users and cannot be deleted

**Finding coordinates:**
- Position the box where you want
- The position is shown in the Save/Load dialog
- Format: `Name (x, y)` → use those x, y values

---

## ⚠️ Important Warnings

1. **Use Responsibly:** This script automates gameplay. Some games may consider this cheating.
2. **Risk of Bans:** Use at your own risk. We are not responsible for any game bans.
3. **Administrator Rights:** Required for full functionality (F6 hotkey).
4. **Screen Capture:** The script captures your screen. Don't run on sensitive screens.
5. **Resource Usage:** Continuous screen monitoring uses CPU. Close other programs if needed.

---

## 📝 Quick Reference Card

| Feature | Shortcut | Purpose |
|---------|----------|---------|
| Enable/Disable | **F6** | Start/stop detection |
| Detection Box | Click & Drag | Move to spawn point |
| Lock Box | Button | Prevent movement |
| Pick Color | Button | Sample screen color |
| Tolerance | Slider (1-100) | Adjust sensitivity |
| Click Delay | Input (10-1000ms) | Control click speed |
| Auto Reload | Checkbox | Auto-press R key |
| Save Position | Dialog | Save box location |

---

## 🎓 Learning Path

**Beginner:**
1. Learn to position and lock the box
2. Pick a base color using screen picker
3. Enable detection and test
4. Adjust tolerance until it works

**Intermediate:**
5. Save multiple positions
6. Fine-tune click delay
7. Enable auto reload

**Advanced:**
8. Add permanent default positions in code
9. Optimize for specific games
10. Create custom configurations for different scenarios

---

## 💡 Final Tips

- **Start Simple:** Begin with just basic detection before adding auto-reload
- **Test in Safe Areas:** Practice positioning in low-risk game areas first
- **Save Good Configs:** When you find settings that work, save the position!
- **Monitor Status:** Always watch the status label to know what the script is doing
- **Stay Legal:** Check your game's Terms of Service regarding automation tools

---

**Script Version:** 1.0  
**Last Updated:** February 2026  
**Created for:** Roblox Zombie Games  

For questions, issues, or feature requests, refer to the project repository or contact the developer.

**Happy Gaming! 🎮**
