import os
import shutil

# --- Path configuration ---

# 1. Source root directory (contains every dpX folder)
#    Note: use either a raw string (r"...") or double the back-slashes.
source_base_dir = r"C:\Users\A\Desktop\klw\simple\simple_files"

# 2. Destination root directory (created automatically if missing)
destination_base_dir = r"C:\Users\A\Desktop\klw\simple\simple_files_new"

# 3. File name to copy from every case
file_name = "FFF.1-91.cas.h5"


# --- Main routine ---

def organize_files():
    """Flatten a deeply-nested per-case directory tree into a cleaner layout."""
    print("Script starting...")
    print(f"Source root:      {source_base_dir}")
    print(f"Destination root: {destination_base_dir}")

    if not os.path.exists(source_base_dir):
        print(f"ERROR: source directory '{source_base_dir}' does not exist. "
              "Check the path.")
        return

    os.makedirs(destination_base_dir, exist_ok=True)
    print("Destination directory created or already exists.")

    copied_files_count = 0

    # Iterate dp0 .. dp499
    for i in range(500):
        dp_folder_name = f"dp{i}"

        # Full source path, e.g.
        # C:\Users\A\Desktop\klw\simple\simple_files\dp0\FFF\Fluent\FFF.1-85.cas.h5
        source_file_path = os.path.join(
            source_base_dir, dp_folder_name, "FFF", "Fluent", file_name
        )

        if os.path.exists(source_file_path):

            # Destination folder, e.g.
            # C:\Users\A\Desktop\klw\simple\simple_files_new\dp0
            destination_dp_folder = os.path.join(destination_base_dir, dp_folder_name)
            os.makedirs(destination_dp_folder, exist_ok=True)

            # Full destination path, e.g.
            # C:\Users\A\Desktop\klw\simple\simple_files_new\dp0\FFF.1-85.cas.h5
            destination_file_path = os.path.join(destination_dp_folder, file_name)

            try:
                print(f"Copying: {source_file_path} -> {destination_file_path}")
                # copy2 preserves metadata
                shutil.copy2(source_file_path, destination_file_path)
                copied_files_count += 1
            except Exception as e:
                print(f"Failed to copy {source_file_path}: {e}")

    print("\n--------------------")
    print("Script finished.")
    print(f"Successfully copied {copied_files_count} files.")
    print(f"All files saved under: {destination_base_dir}")
    print("--------------------")


# --- Entry point ---
if __name__ == "__main__":
    organize_files()
