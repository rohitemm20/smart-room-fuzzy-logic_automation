import csv
import random
import math
import os

OUTPUT_FILE = "environment_data.csv"

TIME_SLOTS = [
    "midnight",
    "early_morning",
    "dawn",
    "morning",
    "late_morning",
    "afternoon",
    "late_afternoon",
    "evening",
    "night",
]

def noisy(value, spread=1.5):
    return round(value + random.uniform(-spread, spread), 1)

def clamp(value, low, high):
    return max(low, min(high, value))

SLOT_PROFILES = {
    "midnight":       (22.0, 20.0,  0,  1),
    "early_morning":  (21.5, 19.0,  0,  0),
    "dawn":           (22.0, 21.0, 15,  1),
    "morning":        (24.0, 26.0, 55,  4),
    "late_morning":   (26.0, 30.0, 80,  5),
    "afternoon":      (28.5, 35.0, 95,  4),
    "late_afternoon": (27.0, 32.0, 70,  3),
    "evening":        (25.0, 27.0, 20,  5),
    "night":          (23.0, 22.0,  5,  3),
}

def generate_row(row_id, time_slot):
    base_room, base_out, base_light, occ_max = SLOT_PROFILES[time_slot]

    room_temp   = clamp(noisy(base_room, 1.5), 18.0, 35.0)
    outdoor_temp= clamp(noisy(base_out,  2.0), 15.0, 40.0)
    ambient     = clamp(int(noisy(base_light, 5)), 0, 100)
    occupancy   = random.randint(0, occ_max)

    return {
        "row_id":       row_id,
        "time_slot":    time_slot,
        "room_temp":    room_temp,
        "outdoor_temp": outdoor_temp,
        "ambient_light":ambient,
        "occupancy":    occupancy,
    }

def generate_environment_data(num_rows=250, output_path=OUTPUT_FILE):
    fieldnames = ["row_id", "time_slot", "room_temp", "outdoor_temp",
                  "ambient_light", "occupancy"]

    rows = []
    for i in range(num_rows):
        slot = TIME_SLOTS[i % len(TIME_SLOTS)]
        rows.append(generate_row(i + 1, slot))

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[DataGen] Generated {num_rows} rows → {output_path}")
    return output_path

if __name__ == "__main__":
    generate_environment_data()
