"""
This script converts all Markdown files (.md) in a directory and its subdirectories to .docx files.
It can also optionally upload the converted files to a cloud storage provider using rclone.

It uses a two-step conversion process:
1. Markdown to Rich Text Format (.rtf)
2. Rich Text Format to .docx

Usage:
python convert.py [directory] [rclone_destination]

- [directory]: The directory to search for .md files. Defaults to the current directory.
- [rclone_destination]: Optional. The rclone remote and path (e.g., 'gdrive:MyFolder').
                       If provided, .docx files will be moved to this destination.
"""

import os
import subprocess
import sys

def convert_and_upload(directory, rclone_dest=None):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                rtf_path = os.path.join(root, os.path.splitext(file)[0] + ".rtf")
                docx_path = os.path.join(root, os.path.splitext(file)[0] + ".docx")

                print(f"Converting {md_path} to .rtf...")
                try:
                    subprocess.run(["pandoc", "-s", md_path, "-t", "rtf", "-o", rtf_path], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"  Error converting {md_path} to .rtf: {e.stderr}")
                    continue
                except FileNotFoundError:
                    print("  Error: pandoc command not found. Please make sure pandoc is installed and in your PATH.")
                    return

                print(f"Converting {rtf_path} to .docx...")
                try:
                    subprocess.run(["pandoc", rtf_path, "-o", docx_path], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"  Error converting {rtf_path} to .docx: {e.stderr}")
                    os.remove(rtf_path) # Clean up even if docx conversion fails
                    continue
                except FileNotFoundError:
                    print("  Error: pandoc command not found. Please make sure pandoc is installed and in your PATH.")
                    return

                # Clean up the intermediate .rtf file
                os.remove(rtf_path)
                print(f"  Successfully converted {md_path} to {docx_path}")

                if rclone_dest:
                    print(f"  Moving {docx_path} to {rclone_dest}...")
                    try:
                        # Use rclone move to transfer the file and remove the local copy
                        subprocess.run(["rclone", "move", docx_path, rclone_dest], check=True, capture_output=True, text=True)
                        print(f"  Successfully moved {docx_path} to {rclone_dest}")
                    except subprocess.CalledProcessError as e:
                        print(f"  Error moving file with rclone: {e.stderr}")
                        print(f"  The converted file is still available at {docx_path}")
                    except FileNotFoundError:
                        print("  Error: rclone command not found. Please make sure rclone is installed and in your PATH.")
                        return


if __name__ == "__main__":
    target_directory = "."
    rclone_destination = None

    if len(sys.argv) > 1:
        # Check if the first argument is a directory
        if os.path.isdir(sys.argv[1]):
            target_directory = sys.argv[1]
            if len(sys.argv) > 2:
                rclone_destination = sys.argv[2]
        # Check if the first argument is an rclone path
        elif ":" in sys.argv[1]:
             rclone_destination = sys.argv[1]
        else:
            print(f"Error: Directory not found at '{sys.argv[1]}'")
            sys.exit(1)

    if len(sys.argv) > 2 and not rclone_destination:
        rclone_destination = sys.argv[2]


    print(f"Starting conversion in directory: '{os.path.abspath(target_directory)}'")
    if rclone_destination:
        print(f"Uploading results to: {rclone_destination}")

    convert_and_upload(target_directory, rclone_destination)