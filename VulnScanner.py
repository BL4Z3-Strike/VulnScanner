import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import requests
from urllib.parse import urljoin
import re

# Common paths to check for vulnerabilities
COMMON_PATHS = [
    'admin/', 'login/', 'dashboard/', 'config.php', 'wp-admin/', 'test/', 'cgi-bin/', 'phpmyadmin/'
]

def is_valid_url(url):
    pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return pattern.match(url) is not None

# Function to check for vulnerabilities on the target URL
def scan_vulnerabilities(target_url, output_widget, progress_var):
    try:
        open_paths = []
        total_paths = len(COMMON_PATHS)

        for index, path in enumerate(COMMON_PATHS):
            url = urljoin(target_url, path)
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    open_paths.append((url, response.status_code))
            except requests.RequestException:
                pass
            
            # Update progress bar
            progress_var.set((index + 1) / total_paths * 100)
            root.update_idletasks()

        # Clear previous results
        output_widget.delete(1.0, tk.END)

        # Display results
        if open_paths:
            output_widget.insert(tk.END, "Potential vulnerabilities found:\n")
            for url, status in open_paths:
                output_widget.insert(tk.END, f"Potential issue found at: {url} (Status Code: {status})\n")
        else:
            output_widget.insert(tk.END, "No vulnerabilities found.\n")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to scan vulnerabilities: {e}")

def start_scan():
    target_url = url_entry.get()
    if not target_url:
        messagebox.showwarning("Input Required", "Please enter a target URL.")
        return
    if not is_valid_url(target_url):
        messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
        return
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url
    progress_var.set(0)  # Reset progress bar
    scan_vulnerabilities(target_url, result_output, progress_var)

def clear_results():
    result_output.delete(1.0, tk.END)
    progress_var.set(0)

def show_help():
    messagebox.showinfo("Help", "Enter the target URL and click 'Start Scan' to check for potential vulnerabilities. The results will be displayed in the text area.")

# Initialize Tkinter GUI
def create_gui():
    global url_entry, result_output, progress_var, root

    root = tk.Tk()
    root.title("Vulnerability Scanner")

    # Create and place widgets
    tk.Label(root, text="Target URL:").grid(row=0, column=0, padx=10, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(root, text="Start Scan", command=start_scan).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(root, text="Clear Results", command=clear_results).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Help", command=show_help).grid(row=1, column=2, padx=10, pady=10)

    result_output = scrolledtext.ScrolledText(root, height=20, width=80)
    result_output.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate", variable=progress_var)
    progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
