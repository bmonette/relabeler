import os
import datetime
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES

file_mappings = [] # List to store file mappings for undo feature.

def browse_folder():
    """This function is called when the user clicks the Browse button. It opens a dialob box
    to select a folder and inserts the folder path into the entry_folder_path Entry."""
    folder_path = filedialog.askdirectory() # Open a dialog box to select a folder.
    entry_folder_path.delete(0, tkinter.END) # Clear the entry_folder_path Entry.
    entry_folder_path.insert(0, folder_path) # Insert the selected folder path into the entry.

def rename_files():
    """This function is called when the user clicks the Rename Files button. It renames the files
    in the selected folder based on the rename pattern."""
    skipped_files = [] # List to store skipped files.

    folder_path = entry_folder_path.get() # Get the folder path from the entry_folder_path Entry.
    pattern = entry_pattern.get() # Get the rename pattern from the entry_pattern Entry.

    # Make sure the folder path is not empty
    if folder_path == "":
        messagebox.showerror("Error", "Please select a folder") # Show an error message if the folder path is empty.
        return
    
    # Make sure the pattern is not empty
    if pattern == "":
        messagebox.showerror("Error", "Please enter a rename pattern") # Show an error message if the pattern is empty.
        return
    
    log_dir = "logs" # Create a directory for log files.
    os.makedirs(log_dir, exist_ok=True) # Create the directory if it doesn't exist.

    log_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # Get the current timestamp.
    log_file_path = os.path.join(log_dir, f"log_file_{log_timestamp}.log") # Create the log file path.
    
    file_mappings.clear() # Clear the file mappings list to avoid conflicts.

    files = os.listdir(folder_path) # Get the list of files in the folder.
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))] # Make sure we only get files, not directories.

    files.sort(key=lambda s: s.lower()) # Sort the files in case-insensitive order.

    progress_bar['maximum'] = len(files) # Set the maximum value of the progress bar to the number of files.
    progress_bar['value'] = 0 # Reset the progress bar value to 0.

    for index, file_name in enumerate(files): # Loop through the files and generate the new names.
        number = str(index + 1).zfill(5) # Generate a five digits number for the file name.
        new_name = pattern.replace('##', number) # Replace the ## in the pattern with the number.
        base, ext = os.path.splitext(file_name) # Split the file name into base name and extension.

        if change_extension_var.get(): # Check if the change extension checkbox is checked.
            new_ext = entry_extension.get().strip() # Get the new extension from the entry_extension Entry

            if not new_ext.startswith("."): # Check if the new extension starts with a dot.
                new_ext = "." + new_ext # Add a dot to the beginning of the extension.

            ext = new_ext # Replace the extension with the user-provided extension.

        new_name_with_ext = new_name + ext # Add the original extension to the new name.

        if date_var.get(): # Check if the date checkbox is checked.
            file_path = os.path.join(folder_path, file_name) # Get the full path and name of the file.
            stats = os.stat(file_path) # Get the files stats.
            created_time = datetime.datetime.fromtimestamp(stats.st_ctime) # Get the created time of the file.
            date_str = created_time.strftime("%Y%m%d") # Format the date as YYYYMMDD.
            time_str = created_time.strftime("%H%M%S") # Format the time as HHMMSS.

            if time_var.get(): # Check if the time checkbox is checked.
                final_name = f"{new_name}_{date_str}_{time_str}{ext}" # Add the date and time to the new name.
            else:
                final_name = f"{new_name}_{date_str}{ext}" # Add the date to the new name.

        else:
            final_name = new_name_with_ext

        new_path = os.path.join(folder_path, final_name) # New path and file name.
        old_path = os.path.join(folder_path, file_name) # Original path and file name.

        try:
            if os.path.exists(new_path): # Check if the new name already exists.
                skipped_files.append(final_name) # Add the file to the skipped files list.

                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get the current time.

                with open(log_file_path, "a") as log_file: # Open the Log file in append mode.
                    log_file.write(f"[{current_time}] Skipped (already exists): {final_name}\n") # Log the skipped file.
                continue # Skip the file if it already exists.

            os.rename(old_path, new_path) # Rename the file.
            file_mappings.append((new_path, old_path)) # Save the file mapping for undo feature.

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get the current time.

            with open(log_file_path, "a") as log_file: # Open the Log file in append mode.
                log_file.write(f"[{current_time}] Renamed: {file_name} -> {final_name}\n") # Log the renamed file.

        except Exception as e:
            messagebox.showerror("Error", f"Error renaming {file_name}: {e}") # Show an error message if renaming fails.

        progress_bar['value'] += 1 # Increment the progress bar value.
        mainwindow.update_idletasks() # Update the main window.
        status_label.config(text=f"Renaming file {index + 1} of {len(files)}: {file_name}")

    if skipped_files: # Check if there are skipped files.
        messagebox.showwarning( # Show a warning message with the skipped files.
            "Warning",
            "The following files were skipped because they already exist:\n\n" + "\n".join(skipped_files)
        )

    status_label.config(text="Renaming complete!") # Update the status label.
    messagebox.showinfo("Success", "All files renamed successfully!") # Show a success message.
    button_undo.config(state='normal') # Enable the Undo button.

def preview_files():
    """This function is called when the user clicks the Preview button. It shows a preview of
    the changes before renaming the files."""
    folder_path = entry_folder_path.get() # Get the folder path from the entry_folder_path Entry.
    pattern = entry_pattern.get() # Get the rename pattern from the entry_pattern Entry.
    preview_listbox.delete(0, tkinter.END) # Clear the preview_listbox Listbox.

    # Make sure the folder path is not empty
    if folder_path == "":
        messagebox.showerror("Error", "Please select a folder") # Show an error message if the folder path is empty.
        return
    
    # Make sure the pattern is not empty
    if pattern == "":
        messagebox.showerror("Error", "Please enter a rename pattern") # Show an error message if the pattern is empty.
        return
    
    files = os.listdir(folder_path) # Get the list of files in the folder.
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))] # Make sure we only get files, not directories.
    files.sort(key=lambda s: s.lower()) # Sort the files in case-insensitive order.

    for index, file_name in enumerate(files): # Loop through the files and generate the new names.
        number = str(index + 1).zfill(5) # Generate a five digits number for the file name.
        new_name = pattern.replace('##', number) # Replace the ## in the pattern with the number.
        base, ext = os.path.splitext(file_name) # Split the file name into base name and extension.
        new_name_with_ext = new_name + ext # Add the original extension to the new name.

        if date_var.get(): # Check if the date checkbox is checked.
            file_path = os.path.join(folder_path, file_name) # Get the full path and name of the file.
            stats = os.stat(file_path) # Get the fils stats.
            created_time = datetime.datetime.fromtimestamp(stats.st_ctime) # Get the created time of the file.
            date_str = created_time.strftime("%Y%m%d") # Format the date as YYYYMMDD.
            time_str = created_time.strftime("%H%M%S") # Format the time as HHMMSS.

            if time_var.get(): # Check if the time checkbox is checked.
                final_name = f"{new_name}_{date_str}_{time_str}{ext}" # Add the date and time to the new name.
            else:
                final_name = f"{new_name}_{date_str}{ext}" # Add the date to the new name.

        else:
            final_name = new_name_with_ext

        preview_listbox.insert(tkinter.END, f'{file_name} "->" {final_name}') # Add the preview to the listbox.

def undo_rename():
    """This function is called when the user clicks the Undo button. It undoes the renaming of the files."""

    if file_mappings:
        for new_path, old_path in reversed(file_mappings):
            try:
                os.rename(new_path, old_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error undoing rename: {os.path.basename(new_path)}: {e}")

        messagebox.showinfo("Success", "Undo successful!")
        file_mappings.clear()
        button_undo.config(state='disabled')

def handle_drag_and_drop(event):
    """This function is called when files are dragged and dropped into the entry_folder_path Entry.
    It updates the entry with the dropped folder path."""

    dropped_path = event.data.strip() # Get the dropped path.

    if dropped_path.startswith("{") and dropped_path.endswith("}"): # Check if the path is enclosed in curly braces.
        dropped_path = dropped_path[1:-1] # Remove the curly braces.

    if os.path.isdir(dropped_path): # Check if the dropped path is a directory.
        entry_folder_path.delete(0, tkinter.END) # Clear the entry_folder_path Entry.
        entry_folder_path.insert(0, dropped_path) # Insert the dropped path into the entry.

    else:
        messagebox.showerror("Error", "Please drop a valid folder.") # Show an error message if the path is not a directory.

def toggle_extension_entry():
    """Enable or disable the extension entry field based on the checkbox state."""

    if change_extension_var.get(): # Check if the change extension checkbox is checked.
        entry_extension.config(state='normal') # Enable the extension entry.
    else:
        entry_extension.delete(0, tkinter.END) # Clear the extension entry.
        entry_extension.config(state='disabled') # Disable the extension entry.

def show_about():
    messagebox.showinfo("About Relabeler", "Relabeler Version 1.0\n\nDeveloped by Benoit Monette\n\nA batch file renaming tool with preview, undo, drag-and-drop, and more!")

# Create the main window.
mainwindow = TkinterDnD.Tk()
mainwindow.title("Relabeler Version 1.0")
mainwindow.resizable(True, True)
mainwindow.geometry("600x400")
mainwindow.minsize(780, 400)
mainwindow.maxsize(800, 600)

date_var = tkinter.BooleanVar() # Create a BooleanVar for the date checkbox.
time_var = tkinter.BooleanVar() # Create a BooleanVar for the time checkbox.
change_extension_var = tkinter.BooleanVar() # Create a BooleanVar for the change extension checkbox

label_select_folder = tkinter.Label(mainwindow, text="Select a folder:") # Create a Label to select a folder.
label_select_folder.grid(row=0, column=0, padx=5, pady=5, sticky='w') # Place the label in the main window.

entry_folder_path = tkinter.Entry(mainwindow) # Create an Entry to show the folder path).
entry_folder_path.grid(row=0, column=1, padx=5, pady=5) # Place the entry in the main window.
entry_folder_path.drop_target_register(DND_FILES) # Register the entry as a drop target.
entry_folder_path.dnd_bind('<<Drop>>', handle_drag_and_drop) # Bind the drop event to the handle_drag_and_drop function.

button_browse = tkinter.Button(mainwindow, text="Browse", command=browse_folder) # Create a button to browse the folder.
button_browse.grid(row=0, column=2, padx=5, pady=5) # Place the button in the main window.

checkbox_extension = tkinter.Checkbutton(mainwindow,
                                         text="Change File Extension", # Create a checkbox to change the file extension.
                                         variable=change_extension_var,
                                         command=toggle_extension_entry
                                         ) 
checkbox_extension.grid(row=0, column=3, padx=5, pady=5) # Place the checkbox in the main window.

entry_extension = tkinter.Entry(mainwindow, state='disabled') # Create an Entry for the new extension.
entry_extension.grid(row=0, column=4, padx=5, pady=5) # Place the entry in the main window.

label_pattern = tkinter.Label(mainwindow, text="Rename pattern (e.g., File_##):") # Create a label for the rename pattern.
label_pattern.grid(row=1, column=0, padx=5, pady=5, sticky='w') # Place the label in the main window.

entry_pattern = tkinter.Entry(mainwindow) # Create an Entry for the rename pattern.
entry_pattern.grid(row=1, column=1, padx=5, pady=5) # Place the pattern entry in the main widow.

checkbox_date = tkinter.Checkbutton(mainwindow, text="Include Date", variable=date_var) # Create a checkbox to include the date in file name.
checkbox_date.grid(row=1, column=2, padx=5, pady=5) # Place the checkbox in the main window.

checkbox_time = tkinter.Checkbutton(mainwindow, text="Include Time", variable=time_var) # Create a checkbox to include the date in file name.
checkbox_time.grid(row=1, column=3, padx=5, pady=5) # Place the checkbox in the main window.

label_preview = tkinter.Label(mainwindow, text="Preview of renamed files:") # Create a label for the preview.
label_preview.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky='w') # Place the label in the main window.

preview_listbox = tkinter.Listbox(mainwindow, width=105, height=10) # Create a Listbox to show the preview.
preview_listbox.grid(row=3, column=0, columnspan=4, padx=5, pady=5) # Place the listbox in the main window.

button_frame = tkinter.Frame(mainwindow) # Create a frame for the buttons.
button_frame.grid(row=3, column=4, padx=10, pady=5, sticky='n') # Place the frame in the main window.

button_preview = tkinter.Button(button_frame, text="Preview", command=preview_files, width=15) # Create a button to preview the changes.
button_preview.pack(pady=5) # Place the button in the frame.

button_rename = tkinter.Button(button_frame, text="Rename Files", command=rename_files, width=15) # Create a button to rename the files.
button_rename.pack(pady=5) # Place the button in the frame.

button_undo = tkinter.Button(button_frame, text="Undo", command=undo_rename, state='disabled', width=15) # Create a button to undo the renaming.
button_undo.pack(pady=5) # Place the button in the frame.

button_about = tkinter.Button(button_frame, text="About", command=show_about, width=15) # Create a button to show the about dialog.
button_about.pack(pady=5) # Place the button in the frame.

progress_bar = ttk.Progressbar(mainwindow, orient='horizontal', length=600, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky='we')

status_label = tkinter.Label(mainwindow, text="")  # Status label starts empty.
status_label.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='w') # Place the status label in the main window.

mainwindow.mainloop()
