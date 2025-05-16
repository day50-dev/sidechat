#!/usr/bin/python3 
import argparse
import re
import sys
import os

def split_on_regex(regex, base_path):
    """
    Splits the input from stdin based on the provided regex and writes each match
    to a separate file in the specified base path.

    Args:
        regex: The PCRE regex to use for splitting.
        base_path: The base path where the split files will be created.

    Returns:
        A list of file paths that were created.
    """

    file_paths = []
    counter = 0
    input_data = sys.stdin.read()

    matches = re.findall(regex, input_data, re.DOTALL)

    for match in matches:
        file_path = os.path.join(base_path, f"out.{counter}")  #Construct file path
        try :
            with open(file_path, "w") as outfile:
                outfile.write(match)  # Use match, not the entire input
            file_paths.append(file_path)
        except OSError as e:
            print(f"Error creating or writing to file {file_path}: {e}", file=sys.stderr)
            return []  # Handle error gracefully, return empty list

        counter += 1

    return file_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Splits input from stdin based on a regex and writes each match to a file."
    )
    parser.add_argument(
        "-r", "--regex", required=True, help="The PCRE regex to use for splitting."
    )
    parser.add_argument(
        "-b", "--base_path", required=True, help="The base path where the split files will be created."
    )

    args = parser.parse_args()

    # Create the base path if it doesn't exist.  Important for proper functioning
    if not os.path.exists(args.base_path):
        try:
            os.makedirs(args.base_path)
        except OSError as e:
            print(f"Error creating base path {args.base_path}: {e}", file=sys.stderr)
            sys.exit(1)

    file_paths = split_on_regex(args.regex, args.base_path)

    for path in file_paths:
        print(path)
