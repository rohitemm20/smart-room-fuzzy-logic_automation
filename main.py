import os
import sys

from data_generator import generate_environment_data
from simulation     import run_simulation, load_environment_data
from utils          import print_welcome, print_separator

ENV_CSV      = "environment_data.csv"
FEEDBACK_CSV = "user_feedback.csv"

def main():
    print_welcome()

    if not os.path.exists(ENV_CSV):
        print("  [Setup] environment_data.csv not found. Generating now...\n")
        generate_environment_data(num_rows=250, output_path=ENV_CSV)
    else:
        print(f"  [Setup] Found {ENV_CSV}  ✓")

    print()
    print("  How many rows would you like to simulate?")
    print("  (Press Enter for ALL rows, or type a number e.g. 30)")
    raw_limit = input("  Rows to run: ").strip()

    try:
        row_limit = int(raw_limit)
    except ValueError:
        row_limit = None

    print()
    print("  Would you like to be prompted for manual overrides?")
    print("  (This lets you teach the system your preferences)")
    raw_interactive = input("  Interactive mode? (Y/n): ").strip().lower()
    interactive = raw_interactive != "n"

    rows = load_environment_data(ENV_CSV)
    if not rows:
        print("[ERROR] No environment data found. Exiting.")
        sys.exit(1)

    if row_limit and row_limit < len(rows):
        rows = rows[:row_limit]

    try:
        run_simulation(rows, interactive=interactive)
    except KeyboardInterrupt:
        print("\n\n  [Stopped] Simulation interrupted by user.")

    print("  Thank you for using the Smart Room System!")
    print(f"  Your feedback is saved in → {FEEDBACK_CSV}\n")


if __name__ == "__main__":
    main()
