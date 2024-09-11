from pathlib import Path
import mimetypes
from sys import argv

# Dictionary to store the total size of each category
category_sizes = {
    'Text file': 0,
    'Image file': 0,
    'Audio file': 0,
    'Video file': 0,
    'Executable file': 0,
    'Archive file': 0,
    'Application file': 0,
    'Unknown file type': 0,
    # 'Directory': 0
}


def classify_file(file_path):
    """
    Classify a file based on its MIME type.

    Args:
        file_path (Path): The file to be classified.

    Returns:
        str: The category of the file (e.g., 'Text file', 'Image file', etc.).
    """
    # Get the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)

    # Determine the file category based on the MIME type
    if mime_type:
        if mime_type.startswith('text'):
            return 'Text file'
        elif mime_type.startswith('image'):
            return 'Image file'
        elif mime_type.startswith('audio'):
            return 'Audio file'
        elif mime_type.startswith('video'):
            return 'Video file'
        elif mime_type.startswith('application'):
            # Check for specific application types (executables, archives, etc.)
            if mime_type == 'application/x-executable' or mime_type == 'application/x-msdownload':
                return 'Executable file'
            elif mime_type == 'application/zip' or mime_type == 'application/x-tar':
                return 'Archive file'
            else:
                return 'Application file'
        else:
            return 'Unknown file type'
    else:
        # If the file type is not determined, return 'Unknown file type'
        return 'Unknown file type'


def is_world_writable(file_path):
    """
    Check if a file has world-writable permissions.

    Args:
        file_path (Path): The file to check.

    Returns:
        bool: True if the file is world-writable, False otherwise.
    """
    return file_path.stat().st_mode & 0o0222 != 0


def list_and_classify_items_in_directory(directory, size_threshold_mb):
    """
    List all items in a directory and classify files by type. 
    Additionally, check for large files and world-writable permissions.

    Args:
        directory (str): The path to the directory to be scanned.
        size_threshold_mb (float): The size threshold in MB for large files.
    """
    # Get the absolute path of the directory
    abs_directory = Path(directory).resolve()
    # Convert size threshold from MB to bytes
    size_threshold = size_threshold_mb * 1024 * 1024

    # Check if the directory exists
    if not abs_directory.exists():
        print(f"The directory '{abs_directory}' does not exist.")
        return

    print(f"Listing and classifying items in directory: {abs_directory}")

    # Recursively go through all files and directories
    for item in abs_directory.rglob('*'):
        if item.is_file():  # If it's a file, classify and check size
            category = classify_file(item)  # Classify the file by MIME type
            size = item.stat().st_size  # Get file size in bytes
            category_sizes[category] += size  # Add file size to the appropriate category
            size_mb = size / (1024 * 1024)  # Convert size to MB
            print(f"{item.name} - {category} - {size_mb:.2f} MB")

            # Check if the file has world-writable permissions
            if is_world_writable(item):
                print(f"{item.name} has world-writable permissions")

            # Check if the file exceeds the size threshold
            if size > size_threshold:
                print(f"Large File: {item.name} - {size_mb:.2f} MB")
        elif item.is_dir():  # If it's a directory, print its name
            print(f"{item.name} - Directory")
        print()


def print_total_sizes():
    """
    Print the total size for each file category in MB.
    """
    print("\nTotal sizes for each category:")
    for category, size in category_sizes.items():
        size_mb = size / (1024 * 1024)  # Convert bytes to MB
        print(f"{category}: {size_mb:.2f} MB")


if __name__ == "__main__":
    # Ensure the script is called with the correct arguments
    try:
        directory = argv[1]
        size_threshold_mb = 5 if len(argv) < 3 else float(argv[2])    

    except Exception as err:
        print(
            f'Error: {err}',
            "Invalid input!",
            "Usage: analize <directory-path> <threshold-mb>",
            sep='\n'
            )
    # List and classify items in the directory, and print total sizes
    list_and_classify_items_in_directory(directory, size_threshold_mb)
    print_total_sizes()
