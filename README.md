# Relabeler

Relabeler is a batch file renaming tool with an intuitive graphical user interface (GUI) built using Python's Tkinter and tkinterdnd2 libraries. It allows you to rename multiple files in bulk with customizable patterns, preview changes before renaming, undo operations, and more.

Features

Batch rename files in a folder.

Custom rename pattern (e.g., File_##).

Include file creation date and/or time in filenames.

Change file extensions during rename.

Preview of renamed files before execution.

Undo the last rename operation.

Drag-and-drop folder selection.

Logging of renamed and skipped files to timestamped log files.

Progress bar and status updates within the app window.

Custom application icon and branding.

Multi-platform compatibility (Windows, macOS, Linux).

How It Works

Step-by-Step Instructions for Beginners

Launch the ApplicationDouble-click the executable file (if available) or run the Python script using your terminal.

Select a Folder

Click the "Browse" button at the top-left of the window.

A folder selection dialog will open. Choose the folder that contains the files you want to rename.

Alternatively, you can drag and drop a folder directly into the "Select a folder" input box.

Enter a Rename Pattern

In the field labeled "Rename pattern (e.g., File_##):", type the naming convention you wish to apply to your files.

Use "##" as a placeholder for the numbering. For example:Document_## will rename your files to Document_00001, Document_00002, etc.

(Optional) Modify Additional Settings

Include Date: Check this box to append the file's creation date (YYYYMMDD format) to the new filename.

Include Time: Check this box to append the file's creation time (HHMMSS format) as well.

Change File Extension: Check this box and type a new extension (for example, .txt or .jpg). This will change all selected files to the new extension.

Preview the Changes

Click the "Preview" button to see how your files will be renamed before making any actual changes.

A list will appear showing each original filename and what it will be renamed to.

Rename Files

Once you're satisfied with the preview, click the "Rename Files" button to rename all the files in the selected folder based on your inputs.

Undo a Rename Operation

If you make a mistake or change your mind, click the "Undo" button to revert the last batch of renamed files to their original names.

Check the Status

The status bar at the bottom of the window will show the current progress and messages.

A progress bar helps you track renaming progress.

Logs

Every renaming operation (including skipped files and errors) is recorded in a log file located in the logs folder. Logs are timestamped for easy tracking.

Installation

Clone or download this repository to your local machine.

Install Python 3.9 or newer from https://www.python.org.

Install the required libraries by opening a terminal or command prompt and running:

pip install tkinterdnd2

Usage

Run the Python script directly:

python relabeler_v10.py

Packaging into an Executable (Optional)

If you want to create a standalone executable for Windows:

Install PyInstaller (if you don't already have it):

pip install pyinstaller

Create the executable:

pyinstaller --noconsole --onefile --icon=relabeler.ico relabeler_v10.py

Make sure your relabeler.ico file is in the same directory as your Python script before running the command.

Planned Features for Version 2.0

Cross-platform drag-and-drop enhancements.

File filtering and selection options.

Better error handling and notifications.

User settings and preferences.

Dark mode theme.

Multi-language support.

Requirements

Python 3.9+

tkinter (usually included with Python)

tkinterdnd2

License

This project is licensed under the MIT License.

Developed by [Your Name]

For feedback, questions, or suggestions, please contact [Your Email or GitHub link].
