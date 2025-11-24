"""
Desktop GUI for testing ResuMAX locally
No browser needed - pure desktop app using tkinter
Run with: python desktop_gui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import requests
import json
import os
from pathlib import Path
import threading

# Backend URL
BACKEND_URL = "http://localhost:8080"

class ResuMAXGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ResuMAX - Local Testing")
        self.root.geometry("900x700")

        # State
        self.resume_id = None
        self.parsed_data = None
        self.auth_token = None
        
        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title = ttk.Label(main_frame, text="📄 ResuMAX - Local Testing",
                         font=('Arial', 18, 'bold'))
        title.grid(row=0, column=0, pady=10)
        
        # Auth Section
        auth_frame = ttk.LabelFrame(main_frame, text="Authentication", padding="5")
        auth_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        auth_frame.columnconfigure(1, weight=1)
        
        ttk.Label(auth_frame, text="Firebase Token:").grid(row=0, column=0, padx=5)
        self.token_entry = ttk.Entry(auth_frame)
        self.token_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        ttk.Button(auth_frame, text="Set Token", command=self.set_token).grid(row=0, column=2, padx=5)

        # Section 1: Upload Resume
        upload_frame = ttk.LabelFrame(main_frame, text="1. Upload Resume", padding="10")
        upload_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        upload_frame.columnconfigure(1, weight=1)

        self.file_label = ttk.Label(upload_frame, text="No file selected")
        self.file_label.grid(row=0, column=0, columnspan=2, pady=5)

        ttk.Button(upload_frame, text="Choose PDF/DOCX",
                  command=self.choose_file).grid(row=1, column=0, padx=5)

        self.upload_btn = ttk.Button(upload_frame, text="Upload & Parse",
                                     command=self.upload_resume, state='disabled')
        self.upload_btn.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Section 2: Job Description
        job_frame = ttk.LabelFrame(main_frame, text="2. Job Description", padding="10")
        job_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        job_frame.columnconfigure(0, weight=1)
        job_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.job_text = scrolledtext.ScrolledText(job_frame, height=8, wrap=tk.WORD)
        self.job_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.job_text.insert(1.0, "Paste job description here...")

        # Industry selection
        industry_frame = ttk.Frame(job_frame)
        industry_frame.grid(row=1, column=0, sticky=tk.W, pady=5)

        ttk.Label(industry_frame, text="Industry:").pack(side=tk.LEFT, padx=5)
        self.industry_var = tk.StringVar(value="auto-detect")
        industries = ["auto-detect", "tech", "finance", "healthcare", "marketing", "design", "sales"]
        ttk.Combobox(industry_frame, textvariable=self.industry_var,
                    values=industries, state='readonly', width=15).pack(side=tk.LEFT)

        # Section 3: Optimize
        self.optimize_btn = ttk.Button(main_frame, text="🚀 Optimize Resume",
                                      command=self.optimize_resume, state='disabled')
        self.optimize_btn.grid(row=4, column=0, pady=10)

        # Section 4: Results
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=2)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Status bar
        self.status_var = tk.StringVar(value="Ready - Make sure backend is running on port 8080")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)

        # Initial health check
        self.check_backend()

    def set_token(self):
        token = self.token_entry.get().strip()
        if token:
            self.auth_token = token
            messagebox.showinfo("Auth", "Token set successfully!")
        else:
            messagebox.showwarning("Auth", "Please enter a token")

    def check_backend(self):
        """Check if backend is running"""
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=2)
            if response.status_code == 200:
                self.status_var.set("✅ Backend connected - Ready to test!")
                return True
        except:
            pass

        self.status_var.set("❌ Backend not running - Start with: uvicorn app.main:app --reload")
        return False

    def choose_file(self):
        """Open file dialog to choose resume"""
        filename = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx"), ("All files", "*.*")]
        )

        if filename:
            self.selected_file = filename
            self.file_label.config(text=f"Selected: {os.path.basename(filename)}")
            self.upload_btn.config(state='normal')
            self.results_text.delete(1.0, tk.END)

    def upload_resume(self):
        """Upload resume to backend"""
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Error", "Please select a file first")
            return

        if not self.check_backend():
            messagebox.showerror("Error", "Backend is not running!\n\nStart it with:\nuvicorn app.main:app --reload")
            return
            
        if not self.auth_token:
            messagebox.showerror("Auth Error", "Please set a Firebase ID Token first")
            return

        # Disable button during upload
        self.upload_btn.config(state='disabled')
        self.status_var.set("⏳ Uploading and parsing resume...")

        def upload_thread():
            try:
                with open(self.selected_file, 'rb') as f:
                    files = {'file': (os.path.basename(self.selected_file), f, 'application/pdf')}
                    # data = {'user_id': self.user_id} # No longer needed
                    headers = {"Authorization": f"Bearer {self.auth_token}"}

                    response = requests.post(
                        f"{BACKEND_URL}/upload-resume",
                        files=files,
                        # data=data,
                        headers=headers,
                        timeout=60
                    )

                if response.status_code == 200:
                    result = response.json()
                    self.resume_id = result['resume_id']
                    self.parsed_data = result

                    self.root.after(0, lambda: self.on_upload_success(result))
                else:
                    error_msg = response.text
                    self.root.after(0, lambda: self.on_upload_error(error_msg))

            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self.on_upload_error("Request timed out. Resume parsing is taking too long.\n\nThe model might still be loading (first request takes longer)."))
            except Exception as e:
                self.root.after(0, lambda: self.on_upload_error(str(e)))

        # Run in background thread
        threading.Thread(target=upload_thread, daemon=True).start()

    def on_upload_success(self, result):
        """Handle successful upload"""
        self.status_var.set("✅ Resume uploaded and parsed!")
        self.upload_btn.config(state='normal')
        self.optimize_btn.config(state='normal')

        # Display parsed data
        output = "📋 PARSED RESUME DATA\n" + "="*50 + "\n\n"
        output += f"Resume ID: {result['resume_id']}\n"
        output += f"Bullet Count: {result.get('parsed_data', {}).get('bullet_count', 'N/A')}\n"
        output += f"Sections: {', '.join(result.get('parsed_data', {}).get('sections', []))}\n\n"
        output += "✅ Ready to optimize! Enter job description above and click 'Optimize Resume'."

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, output)

    def on_upload_error(self, error_msg):
        """Handle upload error"""
        self.status_var.set("❌ Upload failed")
        self.upload_btn.config(state='normal')
        messagebox.showerror("Upload Error", f"Failed to upload resume:\n\n{error_msg}")

    def optimize_resume(self):
        """Optimize resume based on job description"""
        if not self.resume_id:
            messagebox.showerror("Error", "Please upload a resume first")
            return

        job_desc = self.job_text.get(1.0, tk.END).strip()
        if not job_desc or job_desc == "Paste job description here...":
            messagebox.showerror("Error", "Please enter a job description")
            return
            
        if not self.auth_token:
            messagebox.showerror("Auth Error", "Please set a Firebase ID Token first")
            return

        # Disable button during processing
        self.optimize_btn.config(state='disabled')
        self.status_var.set("⏳ Optimizing with semantic matching (this may take 30-60 seconds)...")

        def optimize_thread():
            try:
                payload = {
                    # "user_id": self.user_id,
                    "resume_id": self.resume_id,
                    "job_description": job_desc
                }

                industry = self.industry_var.get()
                if industry and industry != "auto-detect":
                    payload["industry"] = industry
                    
                headers = {"Authorization": f"Bearer {self.auth_token}"}

                response = requests.post(
                    f"{BACKEND_URL}/job-description",
                    json=payload,
                    headers=headers,
                    timeout=120  # 2 minutes for optimization
                )

                if response.status_code == 200:
                    result = response.json()
                    self.root.after(0, lambda: self.on_optimize_success(result))
                else:
                    error_msg = response.text
                    self.root.after(0, lambda: self.on_optimize_error(error_msg))

            except requests.exceptions.Timeout:
                self.root.after(0, lambda: self.on_optimize_error("Request timed out. Try again or check backend logs."))
            except Exception as e:
                self.root.after(0, lambda: self.on_optimize_error(str(e)))

        # Run in background thread
        threading.Thread(target=optimize_thread, daemon=True).start()

    def on_optimize_success(self, result):
        """Handle successful optimization"""
        self.status_var.set("✅ Optimization complete!")
        self.optimize_btn.config(state='normal')

        # Display results
        scores = result.get('relevance_scores', {})

        output = "✨ OPTIMIZATION RESULTS\n" + "="*50 + "\n\n"
        output += "📊 SCORES:\n"
        output += f"  Before:  {scores.get('original_score', 'N/A')}%\n"
        output += f"  After:   {scores.get('optimized_score', 'N/A')}%\n"
        output += f"  Improvement: +{scores.get('improvement', 'N/A')}%\n\n"

        if 'industry' in scores:
            output += f"🏢 Industry: {scores['industry'].upper()}\n\n"

        output += "📝 OPTIMIZED BULLETS:\n"
        for i, bullet in enumerate(scores.get('top_bullets', []), 1):
            output += f"{i}. {bullet['text']} (Score: {bullet['score']}%)\n"

        output += f"\n\n{scores.get('message', '')}"

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, output)

    def on_optimize_error(self, error_msg):
        """Handle optimization error"""
        self.status_var.set("❌ Optimization failed")
        self.optimize_btn.config(state='normal')
        messagebox.showerror("Optimization Error", f"Failed to optimize resume:\n\n{error_msg}")


def main():
    root = tk.Tk()
    app = ResuMAXGUI(root)
    root.mainloop()


if __name__ == "__main__":
    print("🚀 Starting ResuMAX Desktop GUI...")
    print("📍 Make sure backend is running: uvicorn app.main:app --reload")
    print("")
    main()
