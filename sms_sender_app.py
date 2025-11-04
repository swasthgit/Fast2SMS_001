"""
Fast2SMS Desktop Application
M-SWASTH Team
Version 2.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path
import threading

# ==================== TEMPLATES ====================
TEMPLATES = {
    173865: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "Dear {#var#} customer {#var#}, you are covered with policy {#var#}, https://c0i.in/MSWAST/{#var#}. Find your nearest clinic https://mswast-map.glitch.me/map2.html  -MSWASTH -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    173903: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "प्रिय {#var#} ग्राहक {#var#}, आप {#var#} बीमा के अंतर्गत आते हैं, https://c0i.in/MSWAST/{#var#}. अधिक जानकारी के लिए कृपया {#var#} पर कॉल करें -MSWASTH",
        "dlt_id": 1107172768969047732
    },
    173904: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "ಆತ್ಮೀಯ {#var#} ಗ್ರಾಹಕ {#var#}, ನೀವು {#var#} ವಿಮೆಯಡಿ ಒಳಗಾಗಿದ್ದೀರಿ, https://c0i.in/MSWAST/{#var#}. ಯಾವುದೇ ವಿವರಗಳಿಗಾಗಿ ದಯವಿಟ್ಟು {#var#} ಗೆ ಕರೆ ಮಾಡಿ -MSWASTH -MSWASTH",
        "dlt_id": 1107172768964776740
    },
    174779: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "அன்புள்ள {#var#} வாடிக்கையாளர்களே {#var#}, உங்கள் {#var#} கொள்கையின் கீழ் பாதுகாக்கப்படுகிறீர்கள், https://c0i.in/MSWAST/{#var#}. பற்றிய விவரங்களுக்கு {#var#} ஜ அழைக்கவும் -MSWASTH",
        "dlt_id": 1107172768960388249
    },
    174780: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "প্রিয় {#var#} গ্রাহক {#var#}, আপনি  {#var#} স্কিমের অধীনে আবৃত, https://c0i.in/MSWAST/{#var#}. যেকোন বিবরণের জন্য অনুগ্রহ করে কল করুন {#var#} -MSWASTH",
        "dlt_id": 1107172768955025536
    },
    174781: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "പ്രിയപ്പെട്ട {#var#} ഉപഭോക്താവേ {#var#}, നിങ്ങൾ {#var#} പോളിസിയിൽ ഉൾപ്പെട്ടിരിക്കുന്നു, https://c0i.in/MSWAST/{#var#}. ഏതെങ്കിലും വിശദാംശങ്ങൾക്ക് ദയവായി വിളിക്കുക {#var#} -MSWASTH",
        "dlt_id": 1107172768941070312
    },
    175561: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "ప్రియమైన {#var#} కస్టమర్ {#var#}, మీరు {#var#} పాలసీ కింద కవరై ఉన్నారు, https://c0i.in/MSWAST/{#var#} సందర్శించండి లేదా {#var#} కి కాల్ చేయండి -MSWASTH",
        "dlt_id": 1107173165717883763
    },
    175562: {
        "sender": "MSWAST",
        "vars": 6,
        "text": "प्रिय {#var#} ग्राहक {#var#}, तुम्ही {#var#} विमा अंतर्गत आहात, https://c0i.in/MSWAST/{#var#}. कोणत्याही तपशिलांसाठी कृपया {#var#} वर कॉल करा -MSWASTH",
        "dlt_id": 1107173165711431532
    },
    181629: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "Dear {#var#} customer {#var#}, you are covered with policy {#var#}, https://c0i.in/MSWAST/{#var#}. Find your nearest clinic {#var#} -MSWASTH",
        "dlt_id": 1107174185289525526
    },
    183078: {
        "sender": "MSWAST",
        "vars": 4,
        "text": "Dear {#var#} customer {#var#}, you are covered with policy {#var#}, https://c0i.in/MSWAST/{#var#}. Find your nearest clinic https://mswast-map.glitch.me/map2.html  -MSWASTH -MSWASTH",
        "dlt_id": 1107174410935731322
    },
    201352: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "ಆತ್ಮೀಯ {#var#} ಗ್ರಾಹಕರೇ {#var#}, ನೀವು {#var#}ನಲ್ಲಿ M-Swasth ನಿಂದ ಟೆಲಿ ಹೆಲ್ತ್ ಸೇವೆಗಳಿಂದ ಒಳಗೊಳ್ಳಲ್ಪಟ್ಟಿದ್ದೀರಿ. ಚಂದಾದಾರಿಕೆ ಐಡಿ {#var#}. ನಮ್ಮ ವೈದ್ಯರೊಂದಿಗೆ ಸಂಪರ್ಕ ಸಾಧಿಸಲು ನೀವು {#var#} ಗೆ ಕರೆ ಮಾಡಬಹುದು, 24*7 ಅಥವಾ ಲಿಂಕ್‌ನೊಂದಿಗೆ ಮೊಬೈಲ್ ಅಪ್ಲಿಕೇಶನ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201353: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "ప్రియమైన {#var#} వినియోగధారులు {#var#}, మీరు {#var#}లో M-Swasth ద్వారా టెలి హెల్త్ సర్వీసెస్‌తో కవర్ చేయబడ్డారు. సబ్‌స్క్రిప్షన్ ఐడి {#var#}. మీరు మా వైద్యులతో కనెక్ట్ అవ్వడానికి {#var#} కు కాల్ చేయవచ్చు, 24*7 లేదా లింక్‌తో మొబైల్ యాప్‌ను డౌన్‌లోడ్ చేసుకోవచ్చు - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201354: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "அன்புள்ள {#var#} வாடிக்கையாளர் {#var#}, {#var#}இல் M-Swasth வழங்கும் டெலி ஹெல்த் சர்வீசஸ் மூலம் நீங்கள் பாதுகாக்கப்படுகிறீர்கள். சந்தா ஐடி {#var#}. எங்கள் மருத்துவர்களுடன் தொடர்பு கொள்ள {#var#} 24*7 என்ற எண்ணை நீங்கள் அழைக்கலாம் அல்லது https://play.google.com/store/apps/details?id=in.m_insure.patient_app என்ற இணைப்பில் மொபைல் செயலியைப் பதிவிறக்கலாம் -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201355: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "പ്രിയപ്പെട്ട {#var#} ഉപഭോക്താവേ {#var#}, {#var#}ൽ M-Swasth-ന്റെ ടെലി ഹെൽത്ത് സർവീസസ് നിങ്ങൾക്ക് ലഭ്യമാണ്. സബ്‌സ്‌ക്രിപ്‌ഷൻ ഐഡി {#var#}. ഞങ്ങളുടെ ഡോക്ടർമാരുമായി ബന്ധപ്പെടാൻ നിങ്ങൾക്ക് {#var#} 24*7 എന്ന നമ്പറിൽ വിളിക്കാം അല്ലെങ്കിൽ https://play.google.com/store/apps/details?id=in.m_insure.patient_app എന്ന ലിങ്ക് ഉപയോഗിച്ച് മൊബൈൽ ആപ്പ് ഡൗൺലോഡ് ചെയ്യാം -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201356: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "प्रिय {#var#} ग्राहक {#var#}, आप {#var#} में M-Swasth द्वारा टेली हेल्थ सेवाओं के अंतर्गत संरक्षित हैं। आपकी सदस्यता आईडी {#var#} है। आप हमारे डॉक्टरों से 24*7 जुड़ने के लिए {#var#} पर कॉल कर सकते हैं या इस लिंक से मोबाइल ऐप डाउनलोड कर सकते हैं - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    },
    201357: {
        "sender": "MSWAST",
        "vars": 5,
        "text": "Dear {#var#} client {#var#}, you are covered with Tele Health Services by M-Swasth in {#var#}. Subscription Id {#var#}. You can call on {#var#} to get connected with our doctors, 24*7 or download mobile app with the link - https://play.google.com/store/apps/details?id=in.m_insure.patient_app -MSWASTH",
        "dlt_id": 1107172768973504659
    }
}

BASE_URL = "https://www.fast2sms.com/dev/bulkV2"

# ==================== HELPER FUNCTIONS ====================

def need_unicode(txt):
    """Check if text contains non-ASCII characters"""
    return any(ord(c) > 127 for c in txt)

def send_with_retry(payload, api_key, tries=3, base_pause=1.0):
    """Send SMS with retry logic"""
    for n in range(tries):
        try:
            r = requests.post(
                BASE_URL,
                json=payload,
                headers={"authorization": api_key},
                timeout=12
            )
            js = r.json()
            if js.get("return") is True:
                return True, js.get("request_id"), "Success", js
            else:
                err = js.get("message", str(js))
                return False, None, err, js
        except requests.exceptions.Timeout:
            err = "Request timeout"
        except requests.exceptions.RequestException as e:
            err = f"Network error: {str(e)}"
        except Exception as e:
            err = f"Error: {str(e)}"

        if n < tries - 1:
            time.sleep(base_pause * (2**n))

    return False, None, err, {"error": err}


# ==================== MAIN APPLICATION ====================

class SMSSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast2SMS Sender - M-SWASTH")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        # Application state
        self.is_logged_in = False
        self.uploaded_df = None
        self.api_key = ""
        self.last_results = None
        self.current_file_path = None

        # Show login screen
        self.show_login_screen()

    def show_login_screen(self):
        """Display login screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Center frame
        login_frame = tk.Frame(self.root, bg="white", padx=50, pady=50)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(login_frame, text="Fast2SMS Sender", font=("Arial", 24, "bold"),
                bg="white", fg="#2c3e50").pack(pady=20)

        tk.Label(login_frame, text="M-SWASTH Team", font=("Arial", 12),
                bg="white", fg="#7f8c8d").pack(pady=5)

        # Username
        tk.Label(login_frame, text="Username:", font=("Arial", 12),
                bg="white").pack(pady=(30, 5))
        username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
        username_entry.pack(pady=5)
        username_entry.insert(0, "admin")

        # Password
        tk.Label(login_frame, text="Password:", font=("Arial", 12),
                bg="white").pack(pady=(10, 5))
        password_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        password_entry.pack(pady=5)
        password_entry.insert(0, "admin")

        # Error label
        error_label = tk.Label(login_frame, text="", font=("Arial", 10),
                              bg="white", fg="red")
        error_label.pack(pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            if username == "admin" and password == "admin":
                self.is_logged_in = True
                self.show_main_screen()
            else:
                error_label.config(text="Invalid username or password!")

        # Login button
        login_btn = tk.Button(login_frame, text="Login", font=("Arial", 14, "bold"),
                             bg="#3498db", fg="white", padx=30, pady=10,
                             command=login, cursor="hand2")
        login_btn.pack(pady=20)

        # Bind Enter key
        password_entry.bind("<Return>", lambda e: login())

        # Footer
        tk.Label(login_frame, text="Default: admin / admin", font=("Arial", 9, "italic"),
                bg="white", fg="#95a5a6").pack(pady=(20, 0))

    def show_main_screen(self):
        """Display main application screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Top bar
        top_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        top_frame.pack(fill="x", side="top")
        top_frame.pack_propagate(False)

        tk.Label(top_frame, text="Fast2SMS Sender - M-SWASTH",
                font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(side="left", padx=20, pady=15)

        logout_btn = tk.Button(top_frame, text="Logout", font=("Arial", 10),
                              bg="#e74c3c", fg="white", padx=15, pady=5,
                              command=self.logout, cursor="hand2")
        logout_btn.pack(side="right", padx=20)

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Style for tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[20, 10])

        # Create tabs
        self.create_templates_tab()
        self.create_upload_tab()
        self.create_send_tab()
        self.create_logs_tab()

    def logout(self):
        """Logout and return to login screen"""
        self.is_logged_in = False
        self.uploaded_df = None
        self.api_key = ""
        self.last_results = None
        self.show_login_screen()

    def create_templates_tab(self):
        """Create templates viewing tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📋 View Templates")

        # Title
        title_frame = tk.Frame(tab, bg="#3498db", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="Available SMS Templates", font=("Arial", 16, "bold"),
                bg="#3498db", fg="white").pack(pady=12)

        # Create treeview for templates
        tree_frame = tk.Frame(tab, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollbars
        vsb = tk.Scrollbar(tree_frame, orient="vertical")
        hsb = tk.Scrollbar(tree_frame, orient="horizontal")

        # Treeview
        tree = ttk.Treeview(tree_frame, columns=("ID", "Sender", "Vars", "DLT", "Message"),
                           show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        # Configure columns
        tree.heading("ID", text="Template ID")
        tree.heading("Sender", text="Sender")
        tree.heading("Vars", text="Variables")
        tree.heading("DLT", text="DLT ID")
        tree.heading("Message", text="Message Preview")

        tree.column("ID", width=100, anchor="center")
        tree.column("Sender", width=100, anchor="center")
        tree.column("Vars", width=80, anchor="center")
        tree.column("DLT", width=150, anchor="center")
        tree.column("Message", width=600, anchor="w")

        # Add data
        for tid, info in TEMPLATES.items():
            preview = info["text"][:80] + "..." if len(info["text"]) > 80 else info["text"]
            tree.insert("", "end", values=(tid, info["sender"], info["vars"], info["dlt_id"], preview))

        # Pack
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Summary
        summary_frame = tk.Frame(tab, bg="#ecf0f1", height=60)
        summary_frame.pack(fill="x", side="bottom")
        summary_frame.pack_propagate(False)

        tk.Label(summary_frame, text=f"Total Templates: {len(TEMPLATES)}",
                font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=20)

    def create_upload_tab(self):
        """Create file upload tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📁 Upload File")

        # Title
        title_frame = tk.Frame(tab, bg="#27ae60", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="Upload & Preview Data File", font=("Arial", 16, "bold"),
                bg="#27ae60", fg="white").pack(pady=12)

        # Main content
        content_frame = tk.Frame(tab, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Buttons frame
        btn_frame = tk.Frame(content_frame, bg="white")
        btn_frame.pack(fill="x", pady=10)

        # Download sample button
        download_btn = tk.Button(btn_frame, text="📥 Download Sample File",
                                font=("Arial", 12, "bold"), bg="#9b59b6", fg="white",
                                padx=20, pady=10, command=self.download_sample,
                                cursor="hand2")
        download_btn.pack(side="left", padx=5)

        # Upload button
        upload_btn = tk.Button(btn_frame, text="📤 Upload CSV/Excel File",
                              font=("Arial", 12, "bold"), bg="#3498db", fg="white",
                              padx=20, pady=10, command=self.upload_file,
                              cursor="hand2")
        upload_btn.pack(side="left", padx=5)

        # Status label
        self.upload_status_label = tk.Label(btn_frame, text="No file uploaded",
                                           font=("Arial", 11), fg="#7f8c8d", bg="white")
        self.upload_status_label.pack(side="left", padx=20)

        # Preview frame
        preview_frame = tk.Frame(content_frame, bg="white")
        preview_frame.pack(fill="both", expand=True, pady=10)

        tk.Label(preview_frame, text="File Preview:", font=("Arial", 12, "bold"),
                bg="white").pack(anchor="w", pady=5)

        # Treeview for preview
        preview_tree_frame = tk.Frame(preview_frame, bg="white")
        preview_tree_frame.pack(fill="both", expand=True)

        vsb = tk.Scrollbar(preview_tree_frame, orient="vertical")
        hsb = tk.Scrollbar(preview_tree_frame, orient="horizontal")

        self.preview_tree = ttk.Treeview(preview_tree_frame,
                                        yscrollcommand=vsb.set,
                                        xscrollcommand=hsb.set)

        vsb.config(command=self.preview_tree.yview)
        hsb.config(command=self.preview_tree.xview)

        self.preview_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Info frame
        self.info_frame = tk.Frame(content_frame, bg="#ecf0f1", height=80)
        self.info_frame.pack(fill="x", pady=10)
        self.info_frame.pack_propagate(False)

        self.info_label = tk.Label(self.info_frame, text="Upload a file to see statistics",
                                   font=("Arial", 11), bg="#ecf0f1")
        self.info_label.pack(pady=25)

    def download_sample(self):
        """Download sample CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")],
            initialfile="sample_sms_data.csv"
        )

        if file_path:
            columns = ["mobile"] + [f"v{i}" for i in range(1, 11)] + ["template_id"]
            sample_data = pd.DataFrame([
                ["9876543210", "John", "12345", "Health Plus", "ABC123", "1800-XXX-XXX", "", "", "", "", "", "173865"],
                ["9876543211", "Jane", "67890", "Care Pro", "XYZ456", "1800-YYY-YYY", "", "", "", "", "", "201357"]
            ], columns=columns)

            if file_path.endswith('.xlsx'):
                sample_data.to_excel(file_path, index=False, engine='openpyxl')
            else:
                sample_data.to_csv(file_path, index=False)

            messagebox.showinfo("Success", f"Sample file saved to:\n{file_path}")

    def upload_file(self):
        """Upload and process CSV/Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV or Excel file",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            # Load file
            ext = Path(file_path).suffix.lower()
            if ext == ".xlsx":
                df = pd.read_excel(file_path, dtype=str).fillna("")
            else:
                df = pd.read_csv(file_path, dtype=str).fillna("")

            # Normalize columns
            df.columns = [c.strip().lower() for c in df.columns]

            # Ensure required columns exist
            if "mobile" not in df.columns or "template_id" not in df.columns:
                messagebox.showerror("Error", "File must contain 'mobile' and 'template_id' columns!")
                return

            # Ensure v1-v10 columns
            for i in range(1, 11):
                col = f"v{i}"
                if col not in df.columns:
                    df[col] = ""

            # Reorder columns
            df = df[["mobile"] + [f"v{i}" for i in range(1, 11)] + ["template_id"]]

            self.uploaded_df = df
            self.current_file_path = file_path

            # Update preview
            self.update_preview(df)

            # Update status
            self.upload_status_label.config(text=f"✓ File loaded: {Path(file_path).name}", fg="green")

            # Update file status in Send SMS tab
            self.file_status_label.config(
                text=f"✓ File Loaded: {Path(file_path).name} | {len(df)} rows | {df['mobile'].nunique()} unique numbers",
                fg="#27ae60"
            )

            messagebox.showinfo("Success", f"File loaded successfully!\n\nRows: {len(df)}\nFile: {Path(file_path).name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def update_preview(self, df):
        """Update preview treeview with dataframe"""
        # Clear existing
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)

        # Configure columns
        self.preview_tree["columns"] = list(df.columns)
        self.preview_tree["show"] = "headings"

        for col in df.columns:
            self.preview_tree.heading(col, text=col.upper())
            self.preview_tree.column(col, width=80, anchor="center")

        # Add rows (first 100)
        for idx, row in df.head(100).iterrows():
            self.preview_tree.insert("", "end", values=list(row))

        # Update info
        self.info_label.config(
            text=f"Total Rows: {len(df)} | Unique Mobile Numbers: {df['mobile'].nunique()} | Preview showing first 100 rows"
        )

    def create_send_tab(self):
        """Create SMS sending tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📤 Send SMS")

        # Title
        title_frame = tk.Frame(tab, bg="#e67e22", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="Configure & Send SMS", font=("Arial", 16, "bold"),
                bg="#e67e22", fg="white").pack(pady=12)

        # Main content
        content_frame = tk.Frame(tab, bg="white")
        content_frame.pack(fill="both", expand=True, padx=40, pady=30)

        # API Key
        api_frame = tk.LabelFrame(content_frame, text="API Configuration",
                                 font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        api_frame.pack(fill="x", pady=10)

        tk.Label(api_frame, text="Fast2SMS API Key:", font=("Arial", 11),
                bg="white").grid(row=0, column=0, sticky="w", pady=5)

        self.api_key_entry = tk.Entry(api_frame, font=("Arial", 11), width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, padx=10, pady=5)

        # Schedule time
        schedule_frame = tk.LabelFrame(content_frame, text="Schedule (Optional)",
                                      font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        schedule_frame.pack(fill="x", pady=10)

        tk.Label(schedule_frame, text="Schedule Time (YYYY-MM-DD-HH-MM):",
                font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)

        self.schedule_entry = tk.Entry(schedule_frame, font=("Arial", 11), width=30)
        self.schedule_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(schedule_frame, text="Leave blank to send immediately",
                font=("Arial", 9, "italic"), bg="white", fg="#7f8c8d").grid(row=1, column=1, sticky="w")

        # File Status
        file_status_frame = tk.LabelFrame(content_frame, text="File Status",
                                         font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        file_status_frame.pack(fill="x", pady=10)

        self.file_status_label = tk.Label(file_status_frame,
                                          text="⚠️ No file uploaded. Please upload a file first!",
                                          font=("Arial", 11, "bold"), bg="white", fg="#e74c3c")
        self.file_status_label.pack(pady=10)

        # Progress
        progress_frame = tk.LabelFrame(content_frame, text="Progress",
                                      font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        progress_frame.pack(fill="both", expand=True, pady=10)

        self.progress_text = scrolledtext.ScrolledText(progress_frame, height=15,
                                                       font=("Courier", 9), bg="#2c3e50",
                                                       fg="#ecf0f1", wrap=tk.WORD)
        self.progress_text.pack(fill="both", expand=True)
        self.progress_text.insert("1.0", "Ready to send SMS...\n\n")
        self.progress_text.config(state="disabled")

        # Send button
        self.send_btn = tk.Button(content_frame, text="🚀 SEND SMS",
                                 font=("Arial", 14, "bold"), bg="#27ae60", fg="white",
                                 padx=40, pady=15, command=self.send_sms,
                                 cursor="hand2")
        self.send_btn.pack(pady=20)

    def send_sms(self):
        """Send SMS messages"""
        if self.uploaded_df is None or self.uploaded_df.empty:
            messagebox.showerror("Error", "Please upload a file first in the 'Upload File' tab!")
            return

        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your Fast2SMS API key!")
            return

        schedule_time = self.schedule_entry.get().strip()

        # Confirm
        msg = f"Send SMS to {len(self.uploaded_df)} numbers?"
        if schedule_time:
            msg += f"\n\nScheduled for: {schedule_time}"
        else:
            msg += "\n\nSending immediately"

        if not messagebox.askyesno("Confirm", msg):
            return

        self.api_key = api_key
        self.send_btn.config(state="disabled", text="Sending...")

        # Run in thread
        thread = threading.Thread(target=self._send_sms_thread,
                                 args=(self.uploaded_df, api_key, schedule_time))
        thread.daemon = True
        thread.start()

    def _send_sms_thread(self, df, api_key, schedule_time):
        """Send SMS in background thread"""
        self.progress_text.config(state="normal")
        self.progress_text.delete("1.0", tk.END)
        self.progress_text.insert(tk.END, "="*80 + "\n")
        self.progress_text.insert(tk.END, f"Starting SMS sending process...\n")
        self.progress_text.insert(tk.END, f"Total messages: {len(df)}\n")
        self.progress_text.insert(tk.END, "="*80 + "\n\n")
        self.progress_text.config(state="disabled")

        results = []
        success_count = 0
        fail_count = 0
        start_time = datetime.now()

        for idx, row in df.iterrows():
            row_num = idx + 1
            mobile = str(row["mobile"]).strip()

            # Validate template
            try:
                msg_id = int(float(str(row["template_id"]).strip()))
            except:
                status = "FAIL"
                message = f"Invalid template_id: {row['template_id']}"
                results.append({
                    "row": row_num,
                    "mobile": mobile,
                    "template_id": row['template_id'],
                    "status": status,
                    "request_id": "",
                    "message": message,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                fail_count += 1
                self._log_progress(f"Row {row_num} | {mobile} | FAIL | {message}\n")
                continue

            tpl = TEMPLATES.get(msg_id)
            if not tpl:
                status = "FAIL"
                message = f"Template {msg_id} not found"
                results.append({
                    "row": row_num,
                    "mobile": mobile,
                    "template_id": msg_id,
                    "status": status,
                    "request_id": "",
                    "message": message,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                fail_count += 1
                self._log_progress(f"Row {row_num} | {mobile} | FAIL | {message}\n")
                continue

            # Build variables
            nvars = tpl["vars"]
            vals = []
            for i in range(1, nvars + 1):
                val = str(row[f"v{i}"]).strip()
                if val.lower() in {"n/a", "na", "none", "null"}:
                    val = ""
                vals.append(val)
            vars_pipe = "|".join(vals)

            # Build payload
            payload = {
                "route": "dlt",
                "sender_id": tpl["sender"],
                "message": str(msg_id),
                "variables_values": vars_pipe,
                "numbers": mobile,
                "flash": "0"
            }

            if schedule_time:
                payload["schedule_time"] = schedule_time

            if need_unicode(tpl["text"] + vars_pipe):
                payload["language"] = "unicode"

            # Send SMS
            ok, req_id, message, raw = send_with_retry(payload, api_key)

            status = "SUCCESS" if ok else "FAIL"
            if ok:
                success_count += 1
            else:
                fail_count += 1

            results.append({
                "row": row_num,
                "mobile": mobile,
                "template_id": msg_id,
                "status": status,
                "request_id": req_id or "",
                "message": message,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "raw_response": str(raw)
            })

            # Log progress
            self._log_progress(f"Row {row_num} | {mobile} | {status} | {req_id or 'N/A'}\n")

            time.sleep(0.2)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Save results
        self.last_results = pd.DataFrame(results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(os.getcwd(), f"sms_log_{timestamp}.xlsx")
        self.last_results.to_excel(log_path, index=False, engine='openpyxl')

        # Final summary
        self._log_progress("\n" + "="*80 + "\n")
        self._log_progress(f"SENDING COMPLETED!\n")
        self._log_progress(f"Time taken: {duration:.2f} seconds\n")
        self._log_progress(f"Total: {len(df)} | Success: {success_count} | Failed: {fail_count}\n")
        self._log_progress(f"Log saved: {log_path}\n")
        self._log_progress("="*80 + "\n")

        self.send_btn.config(state="normal", text="🚀 SEND SMS")

        # Show completion message
        self.root.after(0, lambda: messagebox.showinfo(
            "Complete",
            f"SMS sending completed!\n\n"
            f"Total: {len(df)}\n"
            f"Success: {success_count}\n"
            f"Failed: {fail_count}\n\n"
            f"Log saved to: {log_path}"
        ))

        # Switch to logs tab
        self.root.after(100, lambda: self.notebook.select(3))

    def _log_progress(self, message):
        """Log progress to text widget"""
        self.progress_text.config(state="normal")
        self.progress_text.insert(tk.END, message)
        self.progress_text.see(tk.END)
        self.progress_text.config(state="disabled")
        self.root.update_idletasks()

    def create_logs_tab(self):
        """Create logs viewing tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="📊 View Logs")

        # Title
        title_frame = tk.Frame(tab, bg="#8e44ad", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="SMS Sending Logs & Statistics", font=("Arial", 16, "bold"),
                bg="#8e44ad", fg="white").pack(pady=12)

        # Buttons
        btn_frame = tk.Frame(tab, bg="white")
        btn_frame.pack(fill="x", padx=20, pady=10)

        refresh_btn = tk.Button(btn_frame, text="🔄 Refresh", font=("Arial", 11, "bold"),
                               bg="#3498db", fg="white", padx=15, pady=8,
                               command=self.refresh_logs, cursor="hand2")
        refresh_btn.pack(side="left", padx=5)

        export_btn = tk.Button(btn_frame, text="💾 Export Log", font=("Arial", 11, "bold"),
                              bg="#27ae60", fg="white", padx=15, pady=8,
                              command=self.export_log, cursor="hand2")
        export_btn.pack(side="left", padx=5)

        retry_btn = tk.Button(btn_frame, text="🔁 Retry Failed SMS", font=("Arial", 11, "bold"),
                             bg="#e74c3c", fg="white", padx=15, pady=8,
                             command=self.retry_failed, cursor="hand2")
        retry_btn.pack(side="left", padx=5)

        # Statistics frame
        stats_frame = tk.LabelFrame(tab, text="Statistics", font=("Arial", 12, "bold"),
                                   bg="white", padx=20, pady=15)
        stats_frame.pack(fill="x", padx=20, pady=10)

        self.stats_label = tk.Label(stats_frame, text="No data available. Send SMS first.",
                                    font=("Arial", 11), bg="white", justify="left")
        self.stats_label.pack(anchor="w")

        # Logs treeview
        logs_frame = tk.Frame(tab, bg="white")
        logs_frame.pack(fill="both", expand=True, padx=20, pady=10)

        vsb = tk.Scrollbar(logs_frame, orient="vertical")
        hsb = tk.Scrollbar(logs_frame, orient="horizontal")

        self.logs_tree = ttk.Treeview(logs_frame,
                                      columns=("Row", "Mobile", "Template", "Status", "Request ID", "Message", "Time"),
                                      show="headings",
                                      yscrollcommand=vsb.set,
                                      xscrollcommand=hsb.set)

        vsb.config(command=self.logs_tree.yview)
        hsb.config(command=self.logs_tree.xview)

        # Configure columns
        self.logs_tree.heading("Row", text="Row")
        self.logs_tree.heading("Mobile", text="Mobile")
        self.logs_tree.heading("Template", text="Template")
        self.logs_tree.heading("Status", text="Status")
        self.logs_tree.heading("Request ID", text="Request ID")
        self.logs_tree.heading("Message", text="Message")
        self.logs_tree.heading("Time", text="Time")

        self.logs_tree.column("Row", width=50, anchor="center")
        self.logs_tree.column("Mobile", width=100, anchor="center")
        self.logs_tree.column("Template", width=80, anchor="center")
        self.logs_tree.column("Status", width=80, anchor="center")
        self.logs_tree.column("Request ID", width=150, anchor="center")
        self.logs_tree.column("Message", width=200, anchor="w")
        self.logs_tree.column("Time", width=150, anchor="center")

        self.logs_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Configure row colors
        self.logs_tree.tag_configure("success", background="#d4edda")
        self.logs_tree.tag_configure("fail", background="#f8d7da")

    def refresh_logs(self):
        """Refresh logs display"""
        # Clear existing
        for item in self.logs_tree.get_children():
            self.logs_tree.delete(item)

        if self.last_results is None or self.last_results.empty:
            self.stats_label.config(text="No data available. Send SMS first.")
            return

        # Update statistics
        total = len(self.last_results)
        success = len(self.last_results[self.last_results["status"] == "SUCCESS"])
        failed = len(self.last_results[self.last_results["status"] == "FAIL"])
        success_rate = (success / total * 100) if total > 0 else 0

        stats_text = f"Total Messages: {total} | Success: {success} ({success_rate:.1f}%) | Failed: {failed}"
        self.stats_label.config(text=stats_text)

        # Add rows
        for _, row in self.last_results.iterrows():
            tag = "success" if row["status"] == "SUCCESS" else "fail"
            self.logs_tree.insert("", "end",
                                 values=(row["row"], row["mobile"], row["template_id"],
                                        row["status"], row["request_id"], row["message"],
                                        row["timestamp"]),
                                 tags=(tag,))

    def export_log(self):
        """Export log to Excel"""
        if self.last_results is None or self.last_results.empty:
            messagebox.showwarning("Warning", "No logs available to export!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"sms_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        if file_path:
            self.last_results.to_excel(file_path, index=False, engine='openpyxl')
            messagebox.showinfo("Success", f"Log exported to:\n{file_path}")

    def retry_failed(self):
        """Retry failed SMS"""
        if self.last_results is None or self.last_results.empty:
            messagebox.showwarning("Warning", "No logs available!")
            return

        failed_df = self.last_results[self.last_results["status"] == "FAIL"]

        if failed_df.empty:
            messagebox.showinfo("Info", "No failed messages to retry!")
            return

        if not messagebox.askyesno("Confirm", f"Retry {len(failed_df)} failed messages?"):
            return

        # Reconstruct dataframe for failed messages
        retry_df = pd.DataFrame()
        retry_df["mobile"] = failed_df["mobile"]
        retry_df["template_id"] = failed_df["template_id"]

        # Add v1-v10 columns (empty for now, user should re-upload with data)
        for i in range(1, 11):
            retry_df[f"v{i}"] = ""

        # Set as uploaded data
        self.uploaded_df = retry_df

        messagebox.showinfo("Info",
                          f"Loaded {len(retry_df)} failed messages.\n\n"
                          "Please note: Variable values (v1-v10) are empty.\n"
                          "You may want to re-upload the original file.\n\n"
                          "Go to 'Send SMS' tab to retry.")

        # Switch to send tab
        self.notebook.select(2)


# ==================== MAIN ====================

def main():
    root = tk.Tk()
    app = SMSSenderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
