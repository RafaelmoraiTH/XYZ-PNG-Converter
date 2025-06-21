import os
import sys
import time
import msvcrt
from tkinter import Tk, filedialog
from PIL import Image


def set_window_title(title):
    if os.name == "nt":
        os.system(f"title {title}")


def display_welcome():
    print(
        r"""
  ____  ____   __      ____      _
 |___ \| ___| / /_    / ___|___ | | ___  _ __ ___ 
   __) |___ \| '_ \  | |   / _ \| |/ _ \| '__/ __|
  / __/ ___) | (_) | | |__| (_) | | (_) | |  \__ \
 |_____|____/ \___/   \____\___/|_|\___/|_|  |___/

    PNG to 8-bit Color Converter
    """
    )
    print("Please select an option:")
    print("[1] Convert individual PNG file(s)")
    print("[2] Convert all PNG files in a folder (including subfolders)")
    print("[Q] Quit\n")


def get_user_choice():
    while True:
        choice = input("Your choice: ").strip().upper()
        if choice in ["1", "2", "Q"]:
            return choice
        print("Invalid choice. Please enter 1, 2, or Q.")


def convert_to_8bit(input_path, output_path):
    try:
        img = Image.open(input_path).convert("P", palette=Image.ADAPTIVE, colors=256)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        return True, None
    except Exception as e:
        return False, str(e)


def process_folder(folder_path, output_root, progress_callback=None):
    converted_files = []
    error_messages = []

    parent_folder_name = os.path.basename(os.path.normpath(folder_path))

    total_files = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                total_files += 1

    processed_files = 0
    start_time = time.time()

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".png"):
                full_path = os.path.join(root, file)

                relative_path = os.path.relpath(full_path, start=folder_path)
                relative_dir = os.path.dirname(relative_path)

                output_dir = os.path.join(output_root, parent_folder_name, relative_dir)
                output_filename = file
                output_path = os.path.join(output_dir, output_filename)

                success, message = convert_to_8bit(full_path, output_path)
                if success:
                    converted_files.append(output_path)
                else:
                    error_messages.append(f"Error in {relative_path}: {message}")

                processed_files += 1
                if progress_callback:
                    elapsed_time = time.time() - start_time
                    progress = processed_files / total_files
                    remaining_time = (
                        (elapsed_time / processed_files)
                        * (total_files - processed_files)
                        if processed_files > 0
                        else 0
                    )
                    progress_callback(
                        processed_files, total_files, progress, remaining_time
                    )

    return converted_files, error_messages


def display_progress(current, total, progress, remaining_time):
    bar_length = 40
    filled_length = int(bar_length * progress)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    mins, secs = divmod(int(remaining_time), 60)
    time_estimate = f"{mins:02d}:{secs:02d}" if remaining_time > 0 else "--:--"

    sys.stdout.write(f"\rConverting: [{bar}] {current}/{total} ({progress:.1%})")
    sys.stdout.write(f"\nETA: {time_estimate}\033")
    sys.stdout.flush()


def wait_for_key():
    print("\nPress any key to exit...")
    msvcrt.getch()


def main():
    set_window_title("256COLORS Converter - Made by Rafaelmorai")
    root = Tk()
    root.withdraw()

    output_root = os.path.join(os.path.expanduser("~"), "Downloads", "256COLORS_Output")

    display_welcome()
    choice = get_user_choice()

    if choice == "Q":
        print("\nGoodbye!")
        return

    total_converted = 0
    all_error_messages = []

    if choice == "1":
        initial_dir = os.getcwd()
        selected = filedialog.askopenfilenames(
            title="Select PNG file(s) to convert to 8-bit",
            initialdir=initial_dir,
            filetypes=[("PNG Files", "*.png"), ("All files", "*.*")],
        )

        if not selected:
            print("\nNo files selected. Exiting.")
            return

        total_files = len(selected)
        start_time = time.time()

        for i, path in enumerate(selected, 1):
            if path.lower().endswith(".png"):
                output_filename = os.path.basename(path)
                output_path = os.path.join(output_root, output_filename)
                success, message = convert_to_8bit(path, output_path)

                elapsed_time = time.time() - start_time
                progress = i / total_files
                remaining_time = (elapsed_time / i) * (total_files - i) if i > 0 else 0
                display_progress(i, total_files, progress, remaining_time)

                if success:
                    total_converted += 1
                else:
                    all_error_messages.append(
                        f"Error in {os.path.basename(path)}: {message}"
                    )

        print("\n")

    elif choice == "2":
        initial_dir = os.getcwd()
        current_folder = filedialog.askdirectory(
            title="Select folder containing PNG files", initialdir=initial_dir
        )

        if not current_folder:
            print("\nNo folder selected. Exiting.")
            return

        print(f"\nProcessing folder: {current_folder}")
        converted, errors = process_folder(
            current_folder, output_root, display_progress
        )
        total_converted += len(converted)
        all_error_messages.extend(errors)
        print("\n")

    summary = f"Conversion complete!\n\nTotal files converted: {total_converted}"

    if all_error_messages:
        summary += f"\n\nErrors encountered ({len(all_error_messages)}):\n" + "\n".join(
            all_error_messages[:5]
        )
        if len(all_error_messages) > 5:
            summary += f"\n\n... and {len(all_error_messages) - 5} more errors."

    summary += f"\n\nFiles saved to: {output_root}"
    print(summary)
    wait_for_key()


if __name__ == "__main__":
    try:
        from PIL import Image
    except ImportError:
        print("Error: PIL (Pillow) module not installed. Please install it with:")
        print("pip install pillow")
        wait_for_key()
        sys.exit(1)

    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
