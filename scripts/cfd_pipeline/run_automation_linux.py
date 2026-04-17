import os
import csv
import math
from pathlib import Path

# Project root (scripts/cfd_pipeline/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Script directory (used to locate the fluent_template.jou sitting next to this file)
SCRIPT_DIR = Path(__file__).resolve().parent

# ==============================================================================
# --- User configuration ---
# ==============================================================================

# --- Windows-side configuration ---
CASES_ROOT_DIR_WINDOWS = r"C:\Users\A\Desktop\klw\simple\simple_files_new"
CSV_FILENAME = str(PROJECT_ROOT / "case.csv")
JOU_TEMPLATE_FILENAME = str(SCRIPT_DIR / "fluent_template.jou")

# --- Linux-side configuration ---
LINUX_FLUENT_EXEC_COMMAND = (
    "/public3/home/sc71124/software-sc71124/install231/install231/"
    "ansys_inc/v231/fluent/bin/fluent"
)
LINUX_CASES_ROOT_DIR = "/public3/home/sc71124/klw/simple_files_new"
NUM_CORES = 12
CASE_FILENAME = "FFF.1-91.cas.h5"

# --- Output configuration ---
# With 500 cases, splitting into a handful of shell scripts keeps each run tractable.
# Change this to 3 (or any other value) as needed.
NUM_SCRIPTS_TO_GENERATE = 5
OUTPUT_SCRIPT_PREFIX = "run_fluent_part"

# Total case count (dp0 .. dp499)
TOTAL_CASE_COUNT = 500


# ==============================================================================
# --- Main routine ---
# ==============================================================================

def main():
    print(f"Generating automation scripts (target: {TOTAL_CASE_COUNT} cases, "
          "custom report filenames)...")

    # --- 1. Read the CSV ---
    try:
        with open(CSV_FILENAME, 'r') as f:
            time_steps_list = [row[0].strip() for row in csv.reader(f) if row]
        print(f"Loaded {len(time_steps_list)} time-step entries.")
    except FileNotFoundError:
        print(f"[ERROR] CSV file '{CSV_FILENAME}' not found.")
        return

    # --- 2. Read the Journal template ---
    try:
        with open(JOU_TEMPLATE_FILENAME, 'r') as f:
            jou_template_content = f.read()
    except FileNotFoundError:
        print(f"[ERROR] JOU template '{JOU_TEMPLATE_FILENAME}' not found.")
        return

    # --- 3. Build commands ---
    all_commands = []
    num_cases_found = 0

    for i in range(TOTAL_CASE_COUNT):
        case_name = f"dp{i}"
        win_case_dir = os.path.join(CASES_ROOT_DIR_WINDOWS, case_name)
        win_cas_path = os.path.join(win_case_dir, CASE_FILENAME)

        linux_case_dir = f"{LINUX_CASES_ROOT_DIR}/{case_name}"
        linux_cas_path = f"{linux_case_dir}/{CASE_FILENAME}"
        linux_dat_path = linux_cas_path.replace(".cas.h5", ".dat.h5")

        if os.path.exists(win_cas_path):
            num_cases_found += 1

            # Guard against a CSV shorter than the case list
            if i < len(time_steps_list):
                time_steps = time_steps_list[i]
            else:
                print(f"[WARN] {case_name} has no time-step entry (CSV too short); "
                      "skipping.")
                continue

            # --- Per-case report filenames ---
            # Yields e.g. dp0_area.out and dp0_report.out on Linux
            report_file_area = f"{case_name}_area.out"
            report_file_report = f"{case_name}_report.out"

            # Fill the template
            jou_content = jou_template_content.format(
                case_path=linux_cas_path,
                time_steps=time_steps,
                dat_path=linux_dat_path,
                report_file_area=report_file_area,
                report_file_report=report_file_report,
            )

            # Write the per-case .jou file
            os.makedirs(win_case_dir, exist_ok=True)
            generated_jou_filename = f"run_{case_name}.jou"
            with open(os.path.join(win_case_dir, generated_jou_filename), 'w') as f:
                f.write(jou_content)

            # Build the Linux shell command (no outer double quotes)
            linux_jou_path = f"{linux_case_dir}/{generated_jou_filename}"
            command = (f'{LINUX_FLUENT_EXEC_COMMAND} 3ddp -g -t{NUM_CORES} '
                       f'-i {linux_jou_path}')
            all_commands.append((case_name, command))
        else:
            # Print only a few misses to avoid spamming the console
            if i < 5:
                print(f"[INFO] Not found: {win_cas_path} (ignore if partial).")

    print(f"\nProcessed {num_cases_found} valid cases.")

    if not all_commands:
        print("[ERROR] No commands generated.")
        return

    # --- 4. Emit .sh scripts ---
    total_cases = len(all_commands)
    cases_per_script = math.ceil(total_cases / NUM_SCRIPTS_TO_GENERATE)

    for i in range(NUM_SCRIPTS_TO_GENERATE):
        start_index = i * cases_per_script
        end_index = start_index + cases_per_script
        script_chunk = all_commands[start_index:end_index]

        if not script_chunk:
            continue

        script_filename = f"{OUTPUT_SCRIPT_PREFIX}_{i + 1}.sh"
        with open(script_filename, 'w', newline='\n') as f:
            f.write("#!/bin/bash\n")
            f.write(f'echo "Starting Part {i + 1}..."\n\n')
            for case_name, cmd in script_chunk:
                f.write(f'echo "[{case_name}] running..."\n')
                f.write(f'{cmd}\n')
                f.write(f'echo "[{case_name}] done."\n\n')

        print(f"Written: {script_filename} ({len(script_chunk)} cases)")

    print("\n--- Finished ---")
    print("Upload the new .sh files to the Linux box and run 'dos2unix *.sh' first.")


if __name__ == '__main__':
    main()
