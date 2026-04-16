SLOT_ORDER_DICT = {
    "midnight": 0, "early_morning": 1, "dawn": 2, "morning": 3, "late_morning": 4,
    "afternoon": 5, "late_afternoon": 6, "evening": 7, "night": 8
}

def clamp_value(v, lo, hi):
    return max(lo, min(hi, v))

def compute_ac_temperature(room_temp, outdoor_temp, occupancy, time_slot):
    is_hot = max(0.0, (room_temp - 24) / 6)
    is_hot = min(1.0, is_hot)
    is_comfy = 1.0 - is_hot
    
    out_hot_ac = 18 if outdoor_temp >= 30 else 20
    if occupancy >= 3:
        out_hot_ac -= 1
    
    out_comfy_ac = 24 if occupancy > 0 else 26

    total = is_hot + is_comfy
    if total == 0:
        return 24.0
        
    final_ac = (is_hot * out_hot_ac + is_comfy * out_comfy_ac) / total
    return clamp_value(round(final_ac, 1), 16, 30)

def compute_brightness(ambient_light, time_slot):
    is_dark = max(0.0, (50 - ambient_light) / 50)
    is_dark = min(1.0, is_dark)
    is_bright = 1.0 - is_dark
    
    out_dark_bri = 80
    out_bright_bri = 15
    
    slot_idx = SLOT_ORDER_DICT.get(time_slot, 4)
    if slot_idx <= 2:
        out_dark_bri = 20
        out_bright_bri = 10
    elif 3 <= slot_idx <= 6:
        out_dark_bri = 90
        out_bright_bri = max(out_bright_bri, 40)
        
    total = is_dark + is_bright
    if total == 0:
        return 50.0
        
    final_bri = (is_dark * out_dark_bri + is_bright * out_bright_bri) / total
    return clamp_value(round(final_bri, 1), 0, 100)

def compute_warmth(time_slot):
    slot_idx = SLOT_ORDER_DICT.get(time_slot, 4)
    
    if slot_idx <= 1:
        warm = 85
    elif slot_idx == 2:
        warm = 55
    elif 3 <= slot_idx <= 6:
        warm = 25
    else:
        warm = 80
        
    return clamp_value(round(warm, 1), 0, 100)

def run_inference(room_temp, outdoor_temp, ambient_light, occupancy, time_slot):
    ac   = compute_ac_temperature(room_temp, outdoor_temp, occupancy, time_slot)
    bri  = compute_brightness(ambient_light, time_slot)
    warm = compute_warmth(time_slot)

    return {
        "ac_temp":    ac,
        "brightness": bri,
        "warmth":     warm,
    }



    # for explanationm
# Inputs: room_temp = 27.5, outdoor_temp = 34, occupancy = 4
#
# Step 1: Fuzzification
#   is_hot  = (27.5 - 24) / 6 = 0.58  → 58% Hot
#   is_comfy = 1.0 - 0.58     = 0.42  → 42% Comfy
#
# Step 2: Rule Evaluation
#   outdoor_temp = 34 >= 30, so hot target = 18
#   occupancy = 4 >= 3, so hot target drops to 17
#   occupancy = 4 > 0, so comfy target = 24
#
# Step 3: Defuzzification (Weighted Average)
#   Final AC = (0.58 * 17 + 0.42 * 24) / (0.58 + 0.42)
#            = (9.86 + 10.08) / 1.0
#            = 19.9°C
# ── Light Brightness Example ──
# Inputs: ambient_light = 20, time_slot = "afternoon"
#
# Step 1: Fuzzification
#   is_dark   = (50 - 20) / 50 = 0.60  → 60% Dark
#   is_bright = 1.0 - 0.60     = 0.40  → 40% Bright
#
# Step 2: Rule Evaluation
#   time_slot = "afternoon" → slot_idx = 5 → work hours (3 to 6)
#   dark target bumped to 90
#   bright target bumped to 40
#
# Step 3: Defuzzification (Weighted Average)
#   Final Brightness = (0.60 * 90 + 0.40 * 40) / (0.60 + 0.40)
#                    = (54 + 16) / 1.0
#                    = 70.0%
