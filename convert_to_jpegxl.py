import os
import shutil
import subprocess
from multiprocessing import Pool, cpu_count
import hashlib
import csv


def hash_file_path(file_path: str) -> str:
    """Generate a hash for a file path to uniquely identify it in the log."""
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()


def get_file_size_in_mb(file_path: str) -> float:
    """Get the file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)


def run_task(task_func, tasks):
    """Run a task in parallel using multiprocessing."""
    log_data = []
    with Pool(cpu_count()) as pool:
        for source_file, target_file in pool.imap_unordered(task_func, tasks):
            if source_file and target_file:
                source_size = get_file_size_in_mb(source_file)
                target_size = get_file_size_in_mb(target_file)
                size_diff_percent = ((target_size - source_size) / source_size) * 100

                file_hash = hash_file_path(source_file)
                log_data.append([
                    file_hash,
                    source_file,
                    round(source_size, 2),
                    target_file,
                    round(target_size, 2),
                    round(size_diff_percent, 2)
                ])
                print(f"Processed: {source_file}")
    return log_data


def optimize_png_task(args):
    """Task to optimize a PNG file using optipng."""
    source_path, target_path = args
    try:
        shutil.copy2(source_path, target_path)  # Copy the file first
        subprocess.run(
            ["optipng", target_path, "-quiet"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return source_path, target_path
    except subprocess.CalledProcessError as e:
        print(f"Error optimizing PNG file {source_path}: {e.stderr.decode()}")
        return None, None


def convert_to_jpegxl_task(args):
    """Task to convert a JPEG file to JPEG XL format."""
    source_path, target_path = args
    try:
        subprocess.run(
            ["cjxl", source_path, target_path, "--quiet"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return source_path, target_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting {source_path} to JPEG XL: {e.stderr.decode()}")
        return None, None


def delete_empty_dirs(directory: str):
    """Recursively delete empty directories in the specified directory."""
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Check if directory is empty
                os.rmdir(dir_path)


def write_csv_log(file_path: str, log_data: list):
    """Write the processed file information to a CSV log file."""
    header = ["Hash", "Source Path", "Source Size (MB)", "Target Path", "Target Size (MB)", "Size Difference (%)"]
    write_header = not os.path.exists(file_path)  # Write header only if file doesn't exist

    with open(file_path, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        if write_header:
            writer.writerow(header)
        writer.writerows(log_data)


def copy_or_move(source: str, target: str, move: bool = False, resume: bool = False):
    """Recursively copy or move files from source to target. Convert JPEG files to JPEG XL and optimize PNG files."""
    if not os.path.exists(source):
        raise ValueError(f"Source folder does not exist: {source}")

    if os.path.exists(target):
        raise ValueError(f"Target folder already exists: {target}")

    # Create the target directory
    os.makedirs(target, exist_ok=True)

    csv_log_file = os.path.join(target, "processed_files.csv")
    processed_files = set()

    if resume and os.path.exists(csv_log_file):
        with open(csv_log_file, "r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip header
            processed_files = set(row[0] for row in reader)

    jpeg_tasks = []
    png_tasks = []
    log_data = []

    for root, _, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        target_dir = os.path.join(target, relative_path)

        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)

            file_hash = hash_file_path(source_file)
            if file_hash in processed_files:
                continue

            source_size = get_file_size_in_mb(source_file)

            if file.lower().endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
                target_file = os.path.splitext(target_file)[0] + '.jxl'
                jpeg_tasks.append((source_file, target_file))  # Add to JPEG conversion tasks
            elif file.lower().endswith(('.png', '.PNG')):
                png_tasks.append((source_file, target_file))  # Add to PNG optimization tasks
            else:
                # Copy or move non-JPEG/PNG files
                if move:
                    shutil.move(source_file, target_file)
                else:
                    shutil.copy2(source_file, target_file)

                target_size = get_file_size_in_mb(target_file)
                size_diff_percent = ((target_size - source_size) / source_size) * 100 if source_size > 0 else 0

                log_data.append([
                    file_hash,
                    source_file,
                    round(source_size, 2),
                    target_file,
                    round(target_size, 2),
                    round(size_diff_percent, 2)
                ])
                print(f"Processed: {source_file}")

    # Process JPEG and PNG tasks in parallel
    log_data += run_task(convert_to_jpegxl_task, jpeg_tasks)
    log_data += run_task(optimize_png_task, png_tasks)

    # Write CSV log
    if log_data:
        write_csv_log(csv_log_file, log_data)

    if move:
        delete_empty_dirs(source)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Copy or move files and convert JPEGs to JPEG XL or optimize PNGs.")
    parser.add_argument("source", type=str, help="Path to the source folder.")
    parser.add_argument("target", type=str, help="Path to the target folder.")
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying. Empty directories in the source will be deleted."
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume processing from where the script left off after an error."
    )

    args = parser.parse_args()

    try:
        copy_or_move(source=args.source, target=args.target, move=args.move, resume=args.resume)
        operation = "moved" if args.move else "copied"
        print(f"Files successfully {operation} from {args.source} to {args.target}")
    except Exception as e:
        print(f"Error: {e}")