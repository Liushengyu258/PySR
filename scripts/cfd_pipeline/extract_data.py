import os
from pathlib import Path
import pandas as pd

# Project root (scripts/cfd_pipeline/ -> PySR/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 1. Folder containing the Fluent output files (the r"..." prefix avoids escape issues)
folder_path = r"C:\Users\A\Desktop\klw\simple\data"

# 2. Column headers (derived from the report file structure)
columns = [
    "Time Step", "area", "flow-time"
]

data_list = []
index_labels = []

print("Processing files...")

# 3. Iterate dp0 .. dp499
for i in range(500):
    filename = f"dp{i}_area.out"
    file_full_path = os.path.join(folder_path, filename)

    # Row label: dp0, dp1, ...
    row_label = f"dp{i}"

    if os.path.exists(file_full_path):
        try:
            with open(file_full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # Grab the last non-empty line
                last_line = lines[-1].strip()

                # If the final line is blank, fall back to the previous one
                if not last_line and len(lines) > 1:
                    last_line = lines[-2].strip()

                if last_line:
                    values = last_line.split()

                    # Sanity check: column count should match the header
                    if len(values) != len(columns):
                        print(f"WARN: {filename} column count ({len(values)}) "
                              f"!= header count ({len(columns)}).")

                    data_list.append(values)
                    index_labels.append(row_label)
                else:
                    print(f"WARN: {filename} is empty.")
                    # Insert a blank row to preserve row ordering, or skip
                    data_list.append([None] * len(columns))
                    index_labels.append(row_label)

        except Exception as e:
            print(f"Error reading {filename}: {e}")
    else:
        print(f"File not found: {filename}")
        # Skip missing files (or uncomment below to keep the row index aligned)
        # data_list.append([None] * len(columns))
        # index_labels.append(row_label)

# 4. Build the DataFrame
df = pd.DataFrame(data_list, columns=columns, index=index_labels)

# 5. Export as CSV into the project root
output_file = str(PROJECT_ROOT / "summary_dp0_499.csv")
df.to_csv(output_file, encoding='utf-8-sig')

print(f"Done. Saved to: {output_file}")
