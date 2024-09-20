import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import pandas as pd
from zlapi import ZaloAPI
import threading
import json
import time
import random


class ZaloLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zalo Check")
        self.root.geometry("500x500")
        self.root.configure(bg="#f4f4f4")

        self.saved_data = self.load_login_data()
        self.screen1()
        self.cache = {}

    def apply_styles(self):
        """Apply modern styles using ttk"""
        style = ttk.Style()
        # Set a modern theme (like 'clam')
        style.theme_use('clam')
        # Style for buttons
        style.configure('TButton', font=('Helvetica', 12), padding=10,
                        relief='flat', background='#4CAF50', foreground='white')
        style.map('TButton', background=[
                  ('active', '#388E3C')], foreground=[('pressed', 'white')])
        # Style for Entry widgets
        style.configure('TEntry', font=('Helvetica', 12), padding=5)
        # Style for Labels
        style.configure('TLabel', font=('Helvetica', 12),
                        padding=10, background='#f0f0f0')

    def load_login_data(self):
        """Load the saved IMEI and cookies from a file."""
        if os.path.exists('login_data.json'):
            with open('login_data.json', 'r') as f:
                return json.load(f)
        return {}

    def save_login_data(self, imei, cookies):
        """Save the IMEI and cookies to a file."""
        with open('login_data.json', 'w') as f:
            json.dump({'imei': imei, 'cookies': cookies}, f)

    def screen1(self):
        self.clear_screen()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(expand=True)
        ttk.Label(frame, text="Enter Cookies Session (JSON):").grid(
            row=0, column=0, sticky="w", pady=10)
        self.cookies_entry = ttk.Entry(frame, width=50)
        self.cookies_entry.grid(row=1, column=0, pady=10)
        # Auto-fill cookies if available
        if 'cookies' in self.saved_data:
            self.cookies_entry.insert(
                0, json.dumps(self.saved_data['cookies']))
        ttk.Label(frame, text="Enter IMEI:").grid(
            row=2, column=0, sticky="w", pady=10)
        self.imei_entry = ttk.Entry(frame, width=50)
        self.imei_entry.grid(row=3, column=0, pady=10)
        # Auto-fill IMEI if available
        if 'imei' in self.saved_data:
            self.imei_entry.insert(0, self.saved_data['imei'])
        # Modern buttons with ttk.Style
        ttk.Button(frame, text="Next", command=self.screen2).grid(
            row=4, column=0, pady=20)

    def screen2(self):
        try:
            self.cookies = json.loads(self.cookies_entry.get())
        except json.JSONDecodeError:
            messagebox.showerror(
                "Error", "Invalid Cookies! Please enter valid JSON.")
            return
        self.imei = self.imei_entry.get()
        if not self.cookies or not self.imei:
            messagebox.showerror("Error", "Cookies and IMEI cannot be empty!")
            return
        self.clear_screen()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(expand=True)
        ttk.Label(frame, text="Enter Phone Number:").grid(
            row=0, column=0, sticky="w", pady=10)
        self.phone_entry = ttk.Entry(frame, width=50)
        self.phone_entry.grid(row=1, column=0, pady=10)
        ttk.Label(frame, text="Enter Password:").grid(
            row=2, column=0, sticky="w", pady=10)
        self.password_entry = ttk.Entry(frame, width=50, show="*")
        self.password_entry.grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Next", command=self.start_login_thread).grid(
            row=4, column=0, pady=20)
        ttk.Button(frame, text="Back", command=self.screen1).grid(
            row=5, column=0, pady=10)

    def start_login_thread(self):
        self.progress = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="disabled")
        # Add informative status message
        self.status_label = ttk.Label(
            self.root, text="Logging in, please wait...", background="#f0f0f0")
        self.status_label.pack(pady=10)
        threading.Thread(target=self.validate_login).start()

    def validate_login(self):
        self.phone = self.phone_entry.get()
        self.password = self.password_entry.get()
        if not self.phone or not self.password:
            self.root.after(0, lambda: self.show_error(
                "Phone number and password cannot be empty!"))
            return
        try:
            self.bot = ZaloAPI(phone=self.phone, password=self.password,
                               imei=self.imei, session_cookies=self.cookies)
            self.root.after(0, self.show_success)
        except Exception as e:
            self.root.after(0, lambda: self.show_error(
                f"Login failed: {str(e)}"))

    def show_success(self):
        self.clear_progress()
        messagebox.showinfo("Success", "Login successful!")

        # Save the login detail
        self.save_login_data(self.imei, self.cookies)
        self.status_label.destroy()  # Remove status message
        self.screen3()

    def show_error(self, message):
        self.clear_progress()
        messagebox.showerror("Error", message)
        self.screen1()

    def screen3(self):
        self.clear_screen()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        frame.pack(expand=True)
        ttk.Label(frame, text="Select Data File:").grid(
            row=0, column=0, sticky="w", pady=10)
        ttk.Button(frame, text="Browse", command=self.browse_file).grid(
            row=1, column=0, pady=10)
        self.selected_file_label = ttk.Label(
            frame, text="", background="#f0f0f0")
        self.selected_file_label.grid(row=2, column=0, pady=10)
        ttk.Button(frame, text="Next", command=self.save_file).grid(
            row=3, column=0, pady=20)
        ttk.Button(frame, text="Back", command=self.screen2).grid(
            row=4, column=0, pady=10)
        # Add a Text widget for displaying progress
        self.progress_text = tk.Text(
            frame, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.progress_text.grid(row=5, column=0, pady=10)

    def browse_file(self):
        self.filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
        self.selected_file_label.config(text=os.path.basename(self.filepath))

    def save_file(self):
        if not self.filepath:
            messagebox.showerror("Error", "No file selected!")
            return
        self.output_path = filedialog.asksaveasfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if not self.output_path:
            messagebox.showerror("Error", "No destination selected!")
            return
        self.progress = ttk.Progressbar(self.root, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="disabled")
        threading.Thread(target=self.process_file).start()

    def remove_non_number(self, phone):
        number = ''.join(filter(str.isdigit, phone))
        if len(number) > 10:
            return number[len(number) - 9:]
        else:
            return number

    def check_zalo(self, phone):
        if phone in self.cache:
            return self.cache[phone]
        retries = 5
        for i in range(retries):
            try:
                if len(phone) > 10 or len(phone) < 9:
                    return 'Not a phone number'
                response = self.bot.fetchPhoneNumber(phone)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    time.sleep(retry_after)
                    return self.check_zalo(phone)
                data = response.toDict()
                if "zalo_name" in data.keys():
                    status = "data['zalo_name']"
                else:
                    if data['error_code'] == 216:
                        status = 'Unknown'
                    elif data['error_code'] == 219:
                        status = 'Not a phone number'
                    else:
                        status = 'Have Zalo'
                self.cache[phone] = status
                return status
            except Exception:
                if i < retries - 1:
                    delay = (2 ** i) + random.uniform(0, 1)
                    time.sleep(delay)
                else:
                    return 'Error'

    def process_file(self):
        try:
            if self.filepath.endswith('.csv'):
                df = pd.read_csv(self.filepath)
            else:
                df = pd.read_excel(self.filepath)
            if df.empty:
                raise ValueError("The file is empty!")
            if 'Phone' not in df.columns:
                raise ValueError("The file must contain a 'Phone' column!")
            df['Phone'] = df['Phone'].astype(str)
            df['Phone'] = df['Phone'].apply(self.remove_non_number)
            df['IsZalo'] = ""
            # Clear previous progress messages
            self.progress_text.config(state=tk.NORMAL)
            self.progress_text.delete(1.0, tk.END)
            self.progress_text.insert(tk.END, "Processing file...\n")
            for idx, phone in df['Phone'].items():
                status = self.check_zalo(phone)
                if status != 'Error':
                    df.at[idx, 'IsZalo'] = status
                    self.progress_text.insert(
                        tk.END, f"Checked {phone}: {status}\n")
                    self.progress_text.yview(tk.END)  # Auto-scroll to the end
                    self.root.update_idletasks()
                    time.sleep(1)  # Adjust delay based on API rate limits
            if self.output_path.endswith('.csv'):
                df.to_csv(self.output_path + '.csv', index=False)
            else:
                df.to_excel(self.output_path + '.xlsx', index=False)
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", "File processed and saved successfully!"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Processing failed: {e}"))
        finally:
            self.root.after(0, self.clear_progress)
            self.root.after(0, self.screen3)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_progress(self):
        if hasattr(self, 'progress') and self.progress:
            self.progress.stop()
            self.progress.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ZaloLoginApp(root)
    root.mainloop()
