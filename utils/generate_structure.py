import os
import json

# Define the path to the comments file
COMMENTS_FILE = "comments.json"

# Define the output file
OUTPUT_FILE = os.path.join("docs", "folder_structure.txt")

def load_comments():
    """
    Load comments from the JSON file, or create an empty dictionary if the file doesn't exist.
    """
    if os.path.exists(COMMENTS_FILE):
        print(f"Loading existing comments from {COMMENTS_FILE}...")
        with open(COMMENTS_FILE, "r") as file:
            return json.load(file)
    else:
        print(f"{COMMENTS_FILE} not found, creating a new file...")
        with open(COMMENTS_FILE, "w") as file:
            json.dump({}, file, indent=4)
        return {}

def save_comments(comments):
    """
    Save comments back to the JSON file.
    """
    print(f"Saving comments to {COMMENTS_FILE}...")
    with open(COMMENTS_FILE, "w") as file:
        json.dump(comments, file, indent=4)

def get_current_files(base_dir="."):
    """
    Traverse the directory and collect the current file structure, excluding specified files and folders.
    """
    # Define exclusions
    EXCLUDED_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".git"}  # Add more folders to exclude
    EXCLUDED_FILES = {".DS_Store", "thumbs.db", ".gitignore"}  # Add specific files to exclude

    current_structure = {}
    for root, dirs, files in os.walk(base_dir):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        relative_path = os.path.relpath(root, base_dir)
        if relative_path == ".":
            relative_path = ""
        current_dict = current_structure
        if relative_path:
            for folder in relative_path.split(os.sep):
                current_dict = current_dict.setdefault(folder, {})
        for file in files:
            # Exclude specified files and .pyc files
            if file not in EXCLUDED_FILES and not file.endswith(".pyc"):
                current_dict[file] = None  # Placeholder for comments
    return current_structure

def write_structure_to_file(directory_structure, comments, file, indent=0):
    """
    Recursively write the directory structure and comments to the output file, placing files before subfolders.
    """
    # First, write all files at this level
    for name, value in directory_structure.items():
        if not isinstance(value, dict):
            comment = comments.get(name, "")
            file.write(f"{' ' * indent}|   {name}  # {comment}\n")

    # Then, recursively write all subdirectories and their contents
    for name, value in directory_structure.items():
        if isinstance(value, dict):
            file.write(" " * indent + f"+---{name}/\n")
            write_structure_to_file(value, comments.get(name, {}), file, indent + 4)

def check_missing_comments(directory_structure, comments, current_path=""):
    """
    Check for files or folders without comments in the JSON file.
    """
    missing = {}
    for name, value in directory_structure.items():
        path = os.path.join(current_path, name)
        if isinstance(value, dict):
            missing_sub = check_missing_comments(value, comments.get(name, {}), path)
            if missing_sub:
                missing[name] = missing_sub
        elif name not in comments:
            missing[name] = ""
    return missing

def merge_comments(existing_comments, new_comments):
    """
    Merge new comments into the existing ones without overwriting.
    """
    for key, value in new_comments.items():
        if isinstance(value, dict):
            existing_comments[key] = merge_comments(existing_comments.get(key, {}), value)
        else:
            if key not in existing_comments:
                existing_comments[key] = value
    return existing_comments

def generate_and_save_structure():
    """
    Generate folder structure and save the comments and structure to files.
    """
    # Create the docs folder if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Load comments from JSON (will create the file if it doesn't exist)
    comments = load_comments()

    # Get the current file structure
    current_structure = get_current_files()

    # Check for missing comments
    missing_comments = check_missing_comments(current_structure, comments)

    # Update the comments file with missing entries
    if missing_comments:
        print("The following files/folders are missing comments:")
        for name, _ in missing_comments.items():
            print(f" - {name}")
        comments = merge_comments(comments, missing_comments)
        save_comments(comments)
        print(f"Missing comments have been added to {COMMENTS_FILE}. Update them as needed.")

    # Write the folder structure to the output file
    with open(OUTPUT_FILE, "w") as f:
        write_structure_to_file(current_structure, comments, f)

    print(f"Folder structure has been written to '{OUTPUT_FILE}'.")
