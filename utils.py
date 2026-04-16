def print_separator(char="-", width=55):
    print("  " + char * width)

def warmth_label(warmth_value):
    if warmth_value <= 30:
        return "Cool White "
    elif warmth_value <= 60:
        return "Neutral "
    else:
        return "Warm White "

def brightness_bar(brightness, width=20):
    filled = int((brightness / 100) * width)
    bar    = "█" * filled + "░" * (width - filled)
    return f"[{bar}]  {brightness:.0f}%"

def display_environment(row):
    print(f"    Room Temp     : {row['room_temp']} °C")
    print(f"    Outdoor Temp  : {row['outdoor_temp']} °C")
    print(f"    Ambient Light : {row['ambient_light']} / 100")
    print(f"    Occupancy     : {row['occupancy']} person(s)")

def display_outputs(outputs):
    bri_bar  = brightness_bar(outputs["brightness"])
    wth_lbl  = warmth_label(outputs["warmth"])

    print()
    print("  ┌─ System Outputs ────────────────────────────────┐")
    print(f" │   AC Temp      : {outputs['ac_temp']} °C")
    print(f" │  Brightness   : {bri_bar}")
    print(f" │  Warmth       : {outputs['warmth']} → {wth_lbl}")
    print("  └─────────────────────────────────────────────────┘")
    print()

def print_welcome():
    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║     Smart Room System                            ║")
    print("  ║                                                  ║")        
    print("  ╚══════════════════════════════════════════════════╝")
    print()
    print("  Controls: AC Temperature | Light Brightness | Warmth")
    print("  Engine  : Fuzzy Logic")
    print()
