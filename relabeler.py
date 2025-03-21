import os
import datetime
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

# Global variables and settings
file_mappings = []  # Stores the mapping between old and new file names for undo functionality.

# Function definitions
def browse_folder():
    """
    Opens a folder selection dialog and inserts the selected path
    into the entry_folder_path entry field.
    """
    folder_path = filedialog.askdirectory()  # Open dialog to choose folder.
    entry_folder_path.delete(0, tkinter.END)  # Clear any existing text in the folder path entry.
    entry_folder_path.insert(0, folder_path)  # Insert the selected folder path.

def rename_files():
    """
    Renames all files in the selected folder according to the pattern and options
    provided by the user (e.g., adding date, time, and/or changing the extension).
    """
    skipped_files = []  # Stores files that couldn't be renamed (e.g., if filename already exists).

    folder_path = entry_folder_path.get()  # Get the selected folder path from entry.
    pattern = entry_pattern.get()  # Get the rename pattern from entry.

    # Check if the folder path and pattern are provided.
    if folder_path == "":
        messagebox.showerror("Error", "Please select a folder")
        return
    
    if pattern == "":
        messagebox.showerror("Error", "Please enter a rename pattern")
        return
    
    log_dir = "logs"  # Directory to store rename operation logs.
    os.makedirs(log_dir, exist_ok=True)  # Create logs directory if it doesn't exist.

    # Create a timestamped log file to store operation logs.
    log_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"log_file_{log_timestamp}.log")
    
    file_mappings.clear()  # Clear previous mappings to avoid conflicts.

    # Get and filter the files (exclude directories).
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

    # Sort files alphabetically in a case-insensitive manner.
    files.sort(key=lambda s: s.lower())

    # Configure progress bar.
    progress_bar['maximum'] = len(files)
    progress_bar['value'] = 0

    # Start renaming files one by one.
    for index, file_name in enumerate(files):
        number = str(index + 1).zfill(5)  # Create a padded 5-digit number for sequencing.
        new_name = pattern.replace('##', number)  # Replace placeholder with the generated number.
        base, ext = os.path.splitext(file_name)  # Split filename and extension.

        # If "Change Extension" is enabled, use the provided extension.
        if change_extension_var.get():
            new_ext = entry_extension.get().strip()
            if not new_ext.startswith("."):
                new_ext = "." + new_ext
            ext = new_ext

        new_name_with_ext = new_name + ext  # Combine new name with extension.

        # Add date/time to filename if selected by the user.
        if date_var.get():
            file_path = os.path.join(folder_path, file_name)
            stats = os.stat(file_path)
            created_time = datetime.datetime.fromtimestamp(stats.st_ctime)
            date_str = created_time.strftime("%Y%m%d")  # Format as YYYYMMDD
            time_str = created_time.strftime("%H%M%S")  # Format as HHMMSS

            # Append date and optionally time.
            if time_var.get():
                final_name = f"{new_name}_{date_str}_{time_str}{ext}"
            else:
                final_name = f"{new_name}_{date_str}{ext}"
        else:
            final_name = new_name_with_ext

        # Full paths for renaming.
        new_path = os.path.join(folder_path, final_name)
        old_path = os.path.join(folder_path, file_name)

        try:
            # Skip if file with the new name already exists.
            if os.path.exists(new_path):
                skipped_files.append(final_name)
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"[{current_time}] Skipped (already exists): {final_name}\n")
                continue

            # Rename file and save mapping for undo.
            os.rename(old_path, new_path)
            file_mappings.append((new_path, old_path))

            # Log the renaming action.
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file_path, "a") as log_file:
                log_file.write(f"[{current_time}] Renamed: {file_name} -> {final_name}\n")

        except Exception as e:
            messagebox.showerror("Error", f"Error renaming {file_name}: {e}")

        # Update progress bar and status label.
        progress_bar['value'] += 1
        mainwindow.update_idletasks()
        status_label.config(text=f"Renaming file {index + 1} of {len(files)}: {file_name}")

    # Notify user about skipped files, if any.
    if skipped_files:
        messagebox.showwarning(
            "Warning",
            "The following files were skipped because they already exist:\n\n" + "\n".join(skipped_files)
        )

    status_label.config(text="Renaming complete!")
    messagebox.showinfo("Success", "All files renamed successfully!")
    button_undo.config(state='normal')  # Enable undo button after renaming.

def preview_files():
    """
    Displays a preview of the renamed files in the listbox, based on the user-specified pattern.
    """
    folder_path = entry_folder_path.get()
    pattern = entry_pattern.get()
    preview_listbox.delete(0, tkinter.END)  # Clear previous preview entries.

    if folder_path == "":
        messagebox.showerror("Error", "Please select a folder")
        return
    
    if pattern == "":
        messagebox.showerror("Error", "Please enter a rename pattern")
        return
    
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    files.sort(key=lambda s: s.lower())

    for index, file_name in enumerate(files):
        number = str(index + 1).zfill(5)
        new_name = pattern.replace('##', number)
        base, ext = os.path.splitext(file_name)
        new_name_with_ext = new_name + ext

        if date_var.get():
            file_path = os.path.join(folder_path, file_name)
            stats = os.stat(file_path)
            created_time = datetime.datetime.fromtimestamp(stats.st_ctime)
            date_str = created_time.strftime("%Y%m%d")
            time_str = created_time.strftime("%H%M%S")

            if time_var.get():
                final_name = f"{new_name}_{date_str}_{time_str}{ext}"
            else:
                final_name = f"{new_name}_{date_str}{ext}"
        else:
            final_name = new_name_with_ext

        # Show old -> new mapping in the preview listbox.
        preview_listbox.insert(tkinter.END, f'{file_name} "->" {final_name}')

def undo_rename():
    """
    Reverts the last rename operation by renaming files back to their original names.
    """
    if file_mappings:
        for new_path, old_path in reversed(file_mappings):
            try:
                os.rename(new_path, old_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error undoing rename: {os.path.basename(new_path)}: {e}")

        messagebox.showinfo("Success", "Undo successful!")
        file_mappings.clear()  # Clear mappings after undo.
        button_undo.config(state='disabled')  # Disable undo button.

def handle_drag_and_drop(event):
    """
    Allows user to drag and drop a folder onto the entry to select it.
    """
    dropped_path = event.data.strip()

    # Handle paths with curly braces (common in some OS drag events).
    if dropped_path.startswith("{") and dropped_path.endswith("}"):
        dropped_path = dropped_path[1:-1]

    # If valid directory, insert it in the entry field.
    if os.path.isdir(dropped_path):
        entry_folder_path.delete(0, tkinter.END)
        entry_folder_path.insert(0, dropped_path)
    else:
        messagebox.showerror("Error", "Please drop a valid folder.")

def toggle_extension_entry():
    """
    Toggles the extension entry field based on the state of the checkbox.
    """
    if change_extension_var.get():
        entry_extension.config(state='normal')
    else:
        entry_extension.delete(0, tkinter.END)
        entry_extension.config(state='disabled')

def show_about():
    """
    Displays information about the Relabeler application.
    """
    messagebox.showinfo(
        "About Relabeler",
        "Relabeler Version 1.0\n\nDeveloped by Benoit Monette\n\nA batch file renaming tool with preview, undo, drag-and-drop, and more!"
    )
    
# Main window setup
mainwindow = TkinterDnD.Tk()  # Create main window with drag-and-drop support.
mainwindow.title("Relabeler Version 1.0")
mainwindow.resizable(True, True)
mainwindow.geometry("600x400")
mainwindow.minsize(780, 400)
mainwindow.maxsize(800, 600)

# Boolean variables tied to checkboxes.
date_var = tkinter.BooleanVar()  # Add date option.
time_var = tkinter.BooleanVar()  # Add time option.
change_extension_var = tkinter.BooleanVar()  # Change extension option.

# Folder selection widgets
label_select_folder = tkinter.Label(mainwindow, text="Select a folder:")
label_select_folder.grid(row=0, column=0, padx=5, pady=5, sticky='w')

entry_folder_path = tkinter.Entry(mainwindow)
entry_folder_path.grid(row=0, column=1, padx=5, pady=5)
entry_folder_path.drop_target_register(DND_FILES)
entry_folder_path.dnd_bind('<<Drop>>', handle_drag_and_drop)

button_browse = tkinter.Button(mainwindow, text="Browse", command=browse_folder)
button_browse.grid(row=0, column=2, padx=5, pady=5)

checkbox_extension = tkinter.Checkbutton(
    mainwindow,
    text="Change File Extension",
    variable=change_extension_var,
    command=toggle_extension_entry
)
checkbox_extension.grid(row=0, column=3, padx=5, pady=5)

entry_extension = tkinter.Entry(mainwindow, state='disabled')
entry_extension.grid(row=0, column=4, padx=5, pady=5)

# Rename pattern widgets
label_pattern = tkinter.Label(mainwindow, text="Rename pattern (e.g., File_##):")
label_pattern.grid(row=1, column=0, padx=5, pady=5, sticky='w')

entry_pattern = tkinter.Entry(mainwindow)
entry_pattern.grid(row=1, column=1, padx=5, pady=5)

checkbox_date = tkinter.Checkbutton(mainwindow, text="Include Date", variable=date_var)
checkbox_date.grid(row=1, column=2, padx=5, pady=5)

checkbox_time = tkinter.Checkbutton(mainwindow, text="Include Time", variable=time_var)
checkbox_time.grid(row=1, column=3, padx=5, pady=5)

# Preview listbox
label_preview = tkinter.Label(mainwindow, text="Preview of renamed files:")
label_preview.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='w')

preview_listbox = tkinter.Listbox(mainwindow, width=105, height=10)
preview_listbox.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

# Buttons frame
button_frame = tkinter.Frame(mainwindow)
button_frame.grid(row=3, column=4, padx=10, pady=5, sticky='n')

button_preview = tkinter.Button(button_frame, text="Preview", command=preview_files, width=15)
button_preview.pack(pady=5)

button_rename = tkinter.Button(button_frame, text="Rename Files", command=rename_files, width=15)
button_rename.pack(pady=5)

button_undo = tkinter.Button(button_frame, text="Undo", command=undo_rename, state='disabled', width=15)
button_undo.pack(pady=5)

button_about = tkinter.Button(button_frame, text="About", command=show_about, width=15)
button_about.pack(pady=5)

# Progress bar and status label
progress_bar = ttk.Progressbar(mainwindow, orient='horizontal', length=600, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='we')

status_label = tkinter.Label(mainwindow, text="")
status_label.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='w')

# Start the application loop
mainwindow.mainloop()
