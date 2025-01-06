import os
import shutil
import subprocess
from multiprocessing import Pool, cpu_count
import csv


def get_file_size_in_mb(file_path: str) -> float:
    """Get the file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)


def log_entry(log_path, entry, is_csv=False):
    """Log an entry to a log file."""
    write_header = is_csv and not os.path.exists(log_path)
    mode = "a" if is_csv else "a"
    with open(log_path, mode, newline="" if is_csv else None) as log_file:
        if is_csv:
            writer = csv.writer(log_file)
            if write_header:
                writer.writerow(["Source Path", "Source Size (MB)", "Target Path", "Target Size (MB)", "Size Difference (%)"])
            writer.writerow(entry)
        else:
            log_file.write(f"{entry}\n")


def handle_failed_file(source_path, target_path, move):
    """Copy or move the file to the target location if processing fails."""
    if move:
        shutil.move(source_path, target_path)
    else:
        shutil.copy2(source_path, target_path)


def process_task(task_name, command, source_path, target_path, move, failed_log_path, csv_log_path):
    """Generalized function to process a task with a specific command."""
    try:
        shutil.copy2(source_path, target_path)  # Copy the file first
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        source_size = get_file_size_in_mb(source_path)
        target_size = get_file_size_in_mb(target_path)
        size_diff_percent = ((target_size - source_size) / source_size) * 100
        log_entry(csv_log_path, [source_path, round(source_size, 2), target_path, round(target_size, 2), round(size_diff_percent, 2)], is_csv=True)
        print(f"{task_name} completed: {source_path} -> {target_path}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode()
        print(f"Error during {task_name} for {source_path}: {error_message}")
        handle_failed_file(source_path, target_path, move)
        log_entry(failed_log_path, f"{target_path}: {error_message}")


def delete_empty_dirs(directory: str):
    """Recursively delete empty directories in the specified directory."""
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def copy_or_move(source: str, target: str, move: bool = False, max_workers: int = None):
    """Recursively copy or move files from source to target."""
    if not os.path.exists(source):
        raise ValueError(f"Source folder does not exist: {source}")

    if os.path.exists(target):
        raise ValueError(f"Target folder already exists: {target}")

    os.makedirs(target, exist_ok=True)

    failed_log_path = os.path.join(target, ".failed")
    csv_log_path = os.path.join(target, "processed_files.csv")

    max_workers = max_workers or max(1, cpu_count() // 2)  # Default: half of available cores

    tasks = []

    for root, _, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        target_dir = os.path.join(target, relative_path)

        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)

            if file.lower().endswith(('.jpg', '.jpeg')):
                target_file = os.path.splitext(target_file)[0] + '.jxl'
                tasks.append(("JPEG XL Conversion", ["cjxl", source_file, target_file, "--quiet", "--lossless_jpeg=1"], source_file, target_file))
            elif file.lower().endswith('.png'):
                tasks.append(("PNG Optimization", ["optipng", target_file, "-quiet"], source_file, target_file))
            else:
                if move:
                    shutil.move(source_file, target_file)
                else:
                    shutil.copy2(source_file, target_file)
                print(f"untouched: {source_file} -> {target_file}")

    # Process tasks in parallel
    with Pool(processes=max_workers) as pool:
        pool.starmap(process_task, [(task_name, command, source, target, move, failed_log_path, csv_log_path) for task_name, command, source, target in tasks])

    if move:
        delete_empty_dirs(source)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Move or copy files with processing.")
    parser.add_argument("source", type=str, help="Source directory.")
    parser.add_argument("target", type=str, help="Target directory.")
    parser.add_argument("--move", action="store_true", help="Move files instead of copying.")
    parser.add_argument("--max-workers", type=int, help="Limit the number of concurrent workers (default: half of CPU cores).")
    args = parser.parse_args()

    copy_or_move(source=args.source, target=args.target, move=args.move, max_workers=args.max_workers)