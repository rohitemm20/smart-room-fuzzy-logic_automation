import csv
import os
from datetime import datetime
import fuzzy_logic as fl

FEEDBACK_FILE = "user_feedback.csv"

FIELDNAMES = [
    "timestamp", "row_id", "time_slot",
    "room_temp", "outdoor_temp", "ambient_light", "occupancy",
    "fuzzy_ac", "fuzzy_brightness", "fuzzy_warmth",
    "user_ac", "user_brightness", "user_warmth",
    "override_ac", "override_brightness", "override_warmth",
]

def ensure_feedback_file():
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def _prompt_override(label, current, lo, hi):
    print(f"  {label}: {current}  (range {lo}–{hi})")
    raw = input(f"    Override {label}? (press Enter to keep, or type new value): ").strip()
    if raw == "":
        return current, False
    try:
        val = float(raw)
        val = max(lo, min(hi, val))
        print(f"    ✓ {label} set to {val}")
        return round(val, 1), True
    except ValueError:
        print(f"    ✗ Invalid input. Keeping {current}.")
        return current, False

def collect_user_feedback(env_row, fuzzy_outputs):
    print("\n  ┌─ Fuzzy Outputs ─────────────────────────────┐")
    print(f"  │  AC Temp   : {fuzzy_outputs['ac_temp']} °C")
    print(f"  │  Brightness: {fuzzy_outputs['brightness']} %")
    print(f"  │  Warmth    : {fuzzy_outputs['warmth']} / 100")
    print("  └────────────────────────── (override below) ─┘")

    user_ac,  ov_ac  = _prompt_override("AC Temp (°C)",   fuzzy_outputs["ac_temp"],   16, 30)
    user_bri, ov_bri = _prompt_override("Brightness (%)", fuzzy_outputs["brightness"], 0, 100)
    user_wrm, ov_wrm = _prompt_override("Warmth (0–100)", fuzzy_outputs["warmth"],    0, 100)

    had_override = ov_ac or ov_bri or ov_wrm

    final_outputs = {
        "ac_temp":    user_ac,
        "brightness": user_bri,
        "warmth":     user_wrm,
    }

    return final_outputs, had_override

def generate_feedback_row(env_row, fuzzy_outputs, final_outputs):
    return {
        "timestamp":         datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "row_id":            env_row.get("row_id", ""),
        "time_slot":         env_row.get("time_slot", ""),
        "room_temp":         env_row.get("room_temp", ""),
        "outdoor_temp":      env_row.get("outdoor_temp", ""),
        "ambient_light":     env_row.get("ambient_light", ""),
        "occupancy":         env_row.get("occupancy", ""),
        "fuzzy_ac":          fuzzy_outputs["ac_temp"],
        "fuzzy_brightness":  fuzzy_outputs["brightness"],
        "fuzzy_warmth":      fuzzy_outputs["warmth"],
        "user_ac":           final_outputs["ac_temp"],
        "user_brightness":   final_outputs["brightness"],
        "user_warmth":       final_outputs["warmth"],
        "override_ac":       1 if fuzzy_outputs["ac_temp"]    != final_outputs["ac_temp"]    else 0,
        "override_brightness":1 if fuzzy_outputs["brightness"] != final_outputs["brightness"] else 0,
        "override_warmth":   1 if fuzzy_outputs["warmth"]     != final_outputs["warmth"]     else 0,
    }

def save_feedback_rows(rows_list):
    if not rows_list:
        return
    ensure_feedback_file()
    with open(FEEDBACK_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerows(rows_list)
