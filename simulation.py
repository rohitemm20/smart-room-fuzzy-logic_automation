import csv
import os
import time

import fuzzy_logic as fl
import feedback as fb
from utils import print_separator, display_environment, display_outputs, warmth_label

ENV_FILE    = "environment_data.csv"
ROW_DELAY   = 0.8
PROMPT_FREQ = 3

def load_environment_data(filepath=ENV_FILE):
    if not os.path.exists(filepath):
        print(f"[ERROR] {filepath} not found. Run data_generator.py first.")
        return []

    rows = []
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "row_id":       int(row["row_id"]),
                "time_slot":    row["time_slot"],
                "room_temp":    float(row["room_temp"]),
                "outdoor_temp": float(row["outdoor_temp"]),
                "ambient_light":int(row["ambient_light"]),
                "occupancy":    int(row["occupancy"]),
            })
    return rows

def run_simulation(rows, interactive=True):
    fb.ensure_feedback_file()

    print_separator("=")
    print("    Smart Room Fuzzy Control — Simulation Starting")
    print_separator("=")
    print(f"  Loaded {len(rows)} environment readings.")
    print("  Press Ctrl+C at any time to stop.\n")
    time.sleep(1)

    total_overrides = 0
    feedback_buffer = []

    for idx, row in enumerate(rows):
        print_separator("-")
        print(f"  Row {row['row_id']} / {len(rows)}  |  Time slot: {row['time_slot'].upper()}")
        print_separator("-")

        display_environment(row)

        fuzzy_out = fl.run_inference(
            room_temp     = row["room_temp"],
            outdoor_temp  = row["outdoor_temp"],
            ambient_light = row["ambient_light"],
            occupancy     = row["occupancy"],
            time_slot     = row["time_slot"],
        )

        if interactive and (idx % PROMPT_FREQ == 0):
            ask = input("\n  Do you want to review/override outputs? (y/N): ").strip().lower()
            if ask == "y":
                final_out, had_override = fb.collect_user_feedback(row, fuzzy_out)
                if had_override:
                    total_overrides += 1
            else:
                final_out = fuzzy_out
                display_outputs(final_out)
        else:
            final_out = fuzzy_out
            display_outputs(final_out)

        feedback_buffer.append(fb.generate_feedback_row(row, fuzzy_out, final_out))

        if interactive:
            time.sleep(ROW_DELAY)

    print_separator("=")
    fb.save_feedback_rows(feedback_buffer)
    print(f"  Simulation complete. Total user overrides: {total_overrides}")
    print(f"  Feedback saved to → user_feedback.csv")
    print_separator("=")
