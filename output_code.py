import os


def print_file_contents(directory_path):
    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        # Exclude '__pycache__' directories from the traversal
        dirs[:] = [d for d in dirs if d != '__pycache__']

        for file in files:
            file_path = os.path.join(root, file)

            # Print the relative file path from the root directory
            relative_path = os.path.relpath(file_path, directory_path)
            print(f"{relative_path}")

            # Open the file and print its content
            try:
                with open(file_path, 'r', encoding='utf-8') as file_content:
                    print(file_content.read())
            except UnicodeDecodeError:
                print("[Unable to decode file content]")

            # Print separator
            print("\n-----------------------\n")


if __name__ == "__main__":
    # Input directory path
    directory_path = input("Enter the directory path: ")

    # Call the function to print files and contents
    print_file_contents(directory_path)
