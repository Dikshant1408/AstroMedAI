import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import datetime

# Import modules from within the src directory
from src import api_handler
from src import risk_model
from src import visualization
from src import report_generator
from src import quiz_mode

# --- Constants & Styles ---
APP_TITLE = "AstroMedAI: Space Health & Radiation Risk"
BG_COLOR = "#2B2B2B"  # Dark gray
FG_COLOR = "#F0F0F0"  # Light text
ACCENT_COLOR = "#6A5ACD" # SlateBlue
BUTTON_COLOR = "#4682B4" # SteelBlue
BUTTON_TEXT_COLOR = "white"
FONT_FAMILY = "Arial"

# Adjusted path for reports and data
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class AstroMedAIGUI:
    def __init__(self, root):
        self.master = root
        root.title("AstroMedAI: Space Health & Radiation Risk")
        root.geometry("1000x700") # Increased window size
        root.configure(bg=BG_COLOR)
        root.resizable(True, True)

        # Set application icon for the window
        # Construct the path to the icon file relative to the script
        # os.path.dirname(__file__) is 'src'
        # os.path.dirname(os.path.dirname(__file__)) is the project root 'astro_med_ai'
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_icon.ico')

        if os.path.exists(icon_path):
            try:
                # For Windows, .ico files are best set with wm_iconbitmap
                self.root.wm_iconbitmap(icon_path)
            except tk.TclError:
                # Fallback or alternative for non-Windows/if .ico isn't working
                # For .png, you'd use PhotoImage and iconphoto
                # Example for .png: photo = tk.PhotoImage(file=icon_path.replace(".ico", ".png"))
                # self.root.iconphoto(False, photo)
                print(f"Warning: Could not set .ico icon directly via wm_iconbitmap. Path: {icon_path}")
        else:
            print(f"Warning: Icon file not found at {icon_path}. Window icon may not display.")

        self._setup_styles()

        # Initialize backend modules
        self.donki_fetcher = api_handler.DONKIFetcher()
        self.risk_calculator = risk_model.SpaceRadiationRiskModel()
        self.data_visualizer = visualization.DataVisualizer()
        self.report_generator = report_generator.PDFReportGenerator()

        self.solar_flare_data = None
        self.geomagnetic_storm_data = None
        self.flare_plot_filepath = None
        self.gst_plot_filepath = None

        self._create_widgets()
        self._setup_drag_and_drop()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam') # Use 'clam' for better customization

        # General frame style
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=(FONT_FAMILY, 10))
        style.configure('TButton', background=BUTTON_COLOR, foreground=BUTTON_TEXT_COLOR, font=(FONT_FAMILY, 10, 'bold'), padding=5, relief='flat')
        style.map('TButton', background=[('active', ACCENT_COLOR)])
        
        # Entry and Combobox styles
        style.configure('TEntry', fieldbackground="#3C3C3C", foreground=FG_COLOR, borderwidth=1, relief='solid')
        style.configure('TCombobox', fieldbackground="#3C3C3C", foreground=FG_COLOR, selectbackground=ACCENT_COLOR, selectforeground=FG_COLOR, borderwidth=1, relief='solid')
        style.map('TCombobox', fieldbackground=[('readonly', '#3C3C3C')], selectbackground=[('readonly', ACCENT_COLOR)])
        
        # Heading labels
        style.configure('Heading.TLabel', font=(FONT_FAMILY, 14, 'bold'), foreground=ACCENT_COLOR, background=BG_COLOR)
        style.configure('SubHeading.TLabel', font=(FONT_FAMILY, 12, 'bold'), foreground=FG_COLOR, background=BG_COLOR)
        
        # Text widget for output
        style.configure('TText', background="#3C3C3C", foreground=FG_COLOR, borderwidth=1, relief='solid')
        
        # Progressbar
        style.configure("TProgressbar", thickness=10, troughcolor="#3C3C3C", background=ACCENT_COLOR)
        style.map("TProgressbar", background=[('active', ACCENT_COLOR)])


    def _create_widgets(self):
        # Main Layout: Three columns
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=2) # Output/Log larger
        self.master.grid_rowconfigure(0, weight=1)

        # --- Left Panel: Mission Parameters ---
        mission_frame = ttk.LabelFrame(self.master, text="Mission Parameters", style='TFrame', padding=15)
        mission_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        mission_frame.grid_columnconfigure(0, weight=1)
        mission_frame.grid_columnconfigure(1, weight=2)
        
        row_idx = 0
        ttk.Label(mission_frame, text="Mission Name:", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.mission_name_entry = ttk.Entry(mission_frame, width=30, style='TEntry')
        self.mission_name_entry.grid(row=row_idx, column=1, sticky="ew", pady=2)
        row_idx += 1

        ttk.Label(mission_frame, text="Duration (Days):", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.duration_entry = ttk.Entry(mission_frame, width=30, style='TEntry')
        self.duration_entry.grid(row=row_idx, column=1, sticky="ew", pady=2)
        self.duration_entry.insert(0, "365") # Default value
        row_idx += 1

        ttk.Label(mission_frame, text="Orbit Type:", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.orbit_type_var = tk.StringVar()
        self.orbit_type_dropdown = ttk.Combobox(mission_frame, textvariable=self.orbit_type_var,
                                                values=["LEO", "GEO", "Lunar Orbit", "Mars Transit"],
                                                state="readonly", style='TCombobox')
        self.orbit_type_dropdown.grid(row=row_idx, column=1, sticky="ew", pady=2)
        self.orbit_type_dropdown.set("LEO") # Default value
        row_idx += 1

        ttk.Label(mission_frame, text="Shielding Level:", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.shielding_var = tk.StringVar()
        self.shielding_dropdown = ttk.Combobox(mission_frame, textvariable=self.shielding_var,
                                               values=["Minimal", "Moderate", "High"],
                                               state="readonly", style='TCombobox')
        self.shielding_dropdown.grid(row=row_idx, column=1, sticky="ew", pady=2)
        self.shielding_dropdown.set("Moderate") # Default value
        row_idx += 1
        
        ttk.Label(mission_frame, text="Crew Size:", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.crew_size_entry = ttk.Entry(mission_frame, width=30, style='TEntry')
        self.crew_size_entry.grid(row=row_idx, column=1, sticky="ew", pady=2)
        self.crew_size_entry.insert(0, "6") # Default value
        row_idx += 1

        ttk.Label(mission_frame, text="Start Date (YYYY-MM-DD):", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.start_date_entry = ttk.Entry(mission_frame, width=30, style='TEntry')
        self.start_date_entry.grid(row=row_idx, column=1, sticky="ew", pady=2)
        self.start_date_entry.insert(0, (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))
        row_idx += 1

        ttk.Label(mission_frame, text="End Date (YYYY-MM-DD):", style='TLabel').grid(row=row_idx, column=0, sticky="w", pady=2)
        self.end_date_entry = ttk.Entry(mission_frame, width=30, style='TEntry')
        self.end_date_entry.grid(row=row_idx, column=1, sticky="ew", pady=2)
        self.end_date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        row_idx += 1

        # Spacer
        ttk.Frame(mission_frame, height=10, style='TFrame').grid(row=row_idx, column=0, columnspan=2)
        row_idx += 1

        ttk.Button(mission_frame, text="Fetch Space Weather Data", command=self._fetch_space_weather, style='TButton').grid(row=row_idx, column=0, columnspan=2, pady=5, sticky="ew")
        row_idx += 1
        ttk.Button(mission_frame, text="Calculate Risk", command=self._calculate_risk, style='TButton').grid(row=row_idx, column=0, columnspan=2, pady=5, sticky="ew")
        row_idx += 1
        ttk.Button(mission_frame, text="Generate Report", command=self._generate_report, style='TButton').grid(row=row_idx, column=0, columnspan=2, pady=5, sticky="ew")
        row_idx += 1
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(mission_frame, orient="horizontal", length=200, mode="determinate", style="TProgressbar")
        self.progress_bar.grid(row=row_idx, column=0, columnspan=2, pady=5, sticky="ew")
        self.progress_label = ttk.Label(mission_frame, text="Ready", style='TLabel')
        self.progress_label.grid(row=row_idx + 1, column=0, columnspan=2, pady=2, sticky="ew")


        # --- Middle Panel: Risk Results & Visualizations ---
        results_frame = ttk.LabelFrame(self.master, text="Risk Assessment & Visualizations", style='TFrame', padding=15)
        results_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(results_frame, text="Overall Radiation Risk:", style='SubHeading.TLabel').pack(pady=(0, 5))
        self.risk_score_label = ttk.Label(results_frame, text="N/A", font=(FONT_FAMILY, 16, 'bold'), foreground=ACCENT_COLOR, background=BG_COLOR)
        self.risk_score_label.pack(pady=(0, 10))
        
        ttk.Label(results_frame, text="Risk Category:", style='SubHeading.TLabel').pack(pady=(0, 5))
        self.risk_category_label = ttk.Label(results_frame, text="N/A", font=(FONT_FAMILY, 16, 'bold'), foreground=ACCENT_COLOR, background=BG_COLOR)
        self.risk_category_label.pack(pady=(0, 10))

        ttk.Label(results_frame, text="Space Weather Data Fetched:", style='SubHeading.TLabel').pack(pady=(10, 5))
        self.flare_count_label = ttk.Label(results_frame, text="Solar Flares: 0", style='TLabel')
        self.flare_count_label.pack(anchor="w", pady=2)
        self.cme_count_label = ttk.Label(results_frame, text="CMEs: 0", style='TLabel')
        self.cme_count_label.pack(anchor="w", pady=2)
        self.gst_count_label = ttk.Label(results_frame, text="Geomagnetic Storms: 0", style='TLabel')
        self.gst_count_label.pack(anchor="w", pady=2)

        ttk.Button(results_frame, text="Show Solar Flare Plot", command=self._show_flare_plot, style='TButton').pack(pady=5, fill="x")
        ttk.Button(results_frame, text="Show Geomagnetic Storm Plot", command=self._show_gst_plot, style='TButton').pack(pady=5, fill="x")
        
        ttk.Label(results_frame, text="Other Features:", style='SubHeading.TLabel').pack(pady=(15, 5))
        ttk.Button(results_frame, text="Launch AstroMed Quiz", command=self._launch_quiz, style='TButton').pack(pady=5, fill="x")
        ttk.Button(results_frame, text="View Reports Folder", command=self._open_reports_folder, style='TButton').pack(pady=5, fill="x")


        # --- Right Panel: Log/Output Console ---
        log_frame = ttk.LabelFrame(self.master, text="Application Log", style='TFrame', padding=10)
        log_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, wrap="word", height=25, width=60, bg="#3C3C3C", fg=FG_COLOR, font=(FONT_FAMILY, 9), relief='flat', borderwidth=0)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        self._log_message("--- AstroMedAI Application Started ---")
        self._log_message("Enter mission details and fetch data.")

    def _setup_drag_and_drop(self):
        # Make the main window a drop target
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self._handle_drop)
        self._log_message("Drag and drop of JSON files enabled.")

    def _handle_drop(self, event):
        filepath = event.data.strip('{}') # Remove braces if present
        if filepath.endswith('.json'):
            self._log_message(f"File dropped: {filepath}")
            self._load_data_from_json(filepath)
        else:
            self._log_message(f"Unsupported file type dropped: {filepath}. Only JSON files are accepted.")
            messagebox.showerror("Invalid File", "Please drop a .json file.")

    def _load_data_from_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Assuming a single JSON might contain both flares and GSTs
            flares = data.get('flares', [])
            gsts = data.get('geomagneticStorms', []) # Using a consistent key name for GSTs

            if flares:
                self.solar_flare_data = flares
                self.flare_count_label.config(text=f"Solar Flares: {len(self.solar_flare_data)} (Loaded from file)")
                self._log_message(f"Loaded {len(flares)} solar flare events from {os.path.basename(filepath)}")
                # Generate plot immediately after loading for visual feedback
                self.flare_plot_filepath = self._generate_plot_for_loaded_data(self.solar_flare_data, 'flares')
            
            if gsts:
                self.geomagnetic_storm_data = gsts
                self.gst_count_label.config(text=f"Geomagnetic Storms: {len(self.geomagnetic_storm_data)} (Loaded from file)")
                self._log_message(f"Loaded {len(gsts)} geomagnetic storm events from {os.path.basename(filepath)}")
                # Generate plot immediately after loading for visual feedback
                self.gst_plot_filepath = self._generate_plot_for_loaded_data(self.geomagnetic_storm_data, 'gsts')

            if not flares and not gsts:
                self._log_message("Dropped JSON file contains no recognized flare or geomagnetic storm data.")
                messagebox.showwarning("No Data", "The dropped JSON file does not contain 'flares' or 'geomagneticStorms' data.")

        except json.JSONDecodeError:
            self._log_message(f"Error: Invalid JSON format in {filepath}")
            messagebox.showerror("File Error", "The selected file is not a valid JSON format.")
        except Exception as e:
            self._log_message(f"Error loading JSON data: {e}")
            messagebox.showerror("File Error", f"An error occurred while loading the file: {e}")

    def _generate_plot_for_loaded_data(self, data, data_type):
        """Helper to generate and save plots for loaded data."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_filename = f"{data_type}_plot_{timestamp}.png"
        plot_path = os.path.join(REPORTS_DIR, plot_filename)
        os.makedirs(REPORTS_DIR, exist_ok=True) # Ensure reports directory exists

        if data_type == 'flares':
            return self.data_visualizer.plot_solar_flares(data, save_path=plot_path)
        elif data_type == 'gsts':
            return self.data_visualizer.plot_geomagnetic_storms(data, save_path=plot_path)
        return None


    def _log_message(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.log_text.insert(tk.END, f"{timestamp} {message}\n")
        self.log_text.see(tk.END) # Scroll to the end

    def _update_progress(self, value, message=""):
        self.progress_bar['value'] = value
        self.progress_label.config(text=message)
        self.master.update_idletasks() # Update GUI immediately

    def _fetch_space_weather(self):
        self._log_message("Fetching space weather data...")
        self._update_progress(0, "Fetching data...")
        
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        try:
            datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
            datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter dates in YYYY-MM-DD format.")
            self._log_message("Error: Invalid date format.")
            self._update_progress(0, "Error")
            return
            
        self.solar_flare_data = self.donki_fetcher.get_solar_flares(start_date_str, end_date_str)
        self.geomagnetic_storm_data = self.donki_fetcher.get_geomagnetic_storms(start_date_str, end_date_str)
        # self.cme_data = self.donki_fetcher.get_coronal_mass_ejections(start_date_str, end_date_str) # Not used in risk model yet

        if self.solar_flare_data is not None:
            self.flare_count_label.config(text=f"Solar Flares: {len(self.solar_flare_data)}")
            self._log_message(f"Fetched {len(self.solar_flare_data)} solar flare events.")
            # Generate plot immediately after fetching
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_filename = f"solar_flares_plot_{timestamp}.png"
            self.flare_plot_filepath = self.data_visualizer.plot_solar_flares(self.solar_flare_data, 
                                                                                save_path=os.path.join(REPORTS_DIR, plot_filename))
        else:
            self.flare_count_label.config(text="Solar Flares: N/A (Error)")
            self.flare_plot_filepath = None
            self._log_message("Failed to fetch solar flare data.")

        if self.geomagnetic_storm_data is not None:
            self.gst_count_label.config(text=f"Geomagnetic Storms: {len(self.geomagnetic_storm_data)}")
            self._log_message(f"Fetched {len(self.geomagnetic_storm_data)} geomagnetic storm events.")
            # Generate plot immediately after fetching
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            plot_filename = f"geomagnetic_storms_plot_{timestamp}.png"
            self.gst_plot_filepath = self.data_visualizer.plot_geomagnetic_storms(self.geomagnetic_storm_data, 
                                                                                    save_path=os.path.join(REPORTS_DIR, plot_filename))
        else:
            self.gst_count_label.config(text="Geomagnetic Storms: N/A (Error)")
            self.gst_plot_filepath = None
            self._log_message("Failed to fetch geomagnetic storm data.")
        
        self.cme_count_label.config(text="CMEs: N/A (Not fetched)") # Placeholder
        
        self._update_progress(100, "Data fetched!")
        self._log_message("Space weather data fetch complete.")

    def _calculate_risk(self):
        self._log_message("Calculating risk...")
        self._update_progress(0, "Calculating risk...")

        try:
            duration_days = int(self.duration_entry.get())
            orbit_type = self.orbit_type_var.get()
            shielding_level = self.shielding_var.get()
            
            # The risk model only needs flare data. CME and GST are for general info/plots.
            risk_score, risk_category = self.risk_calculator.calculate_risk(
                duration_days,
                orbit_type,
                shielding_level,
                self.solar_flare_data # Pass only solar flare data
            )
            
            self.risk_score_label.config(text=f"{risk_score:.2f}%",
                                         foreground=self._get_risk_color(risk_category))
            self.risk_category_label.config(text=risk_category.upper(),
                                            foreground=self._get_risk_color(risk_category))
            self._log_message(f"Risk calculated: {risk_score:.2f}% ({risk_category})")
            self._update_progress(100, "Risk calculated!")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            self._log_message(f"Error calculating risk: {e}")
            self._update_progress(0, "Error")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An unexpected error occurred: {e}")
            self._log_message(f"Unexpected error during risk calculation: {e}")
            self._update_progress(0, "Error")

    def _get_risk_color(self, category):
        if category == "Low":
            return "#28a745"  # Green
        elif category == "Moderate":
            return "#ffc107" # Yellow/Orange
        elif category == "High":
            return "#fd7e14" # Orange-red
        elif category == "Extreme":
            return "#dc3545" # Red
        return FG_COLOR # Default

    def _show_flare_plot(self):
        if self.flare_plot_filepath and os.path.exists(self.flare_plot_filepath):
            self._log_message(f"Opening solar flare plot: {self.flare_plot_filepath}")
            try:
                os.startfile(self.flare_plot_filepath) # Opens file with default viewer
            except Exception as e:
                messagebox.showerror("Error", f"Could not open plot file: {e}")
                self._log_message(f"Error opening flare plot: {e}")
        else:
            messagebox.showinfo("No Plot", "No solar flare plot available. Fetch data first or load from JSON.")
            self._log_message("Cannot show flare plot: file not found or not generated.")

    def _show_gst_plot(self):
        if self.gst_plot_filepath and os.path.exists(self.gst_plot_filepath):
            self._log_message(f"Opening geomagnetic storm plot: {self.gst_plot_filepath}")
            try:
                os.startfile(self.gst_plot_filepath) # Opens file with default viewer
            except Exception as e:
                messagebox.showerror("Error", f"Could not open plot file: {e}")
                self._log_message(f"Error opening GST plot: {e}")
        else:
            messagebox.showinfo("No Plot", "No geomagnetic storm plot available. Fetch data first or load from JSON.")
            self._log_message("Cannot show GST plot: file not found or not generated.")
            
    def _generate_report(self):
        self._log_message("Generating PDF report...")
        self._update_progress(0, "Generating report...")

        try:
            mission_name = self.mission_name_entry.get() if self.mission_name_entry.get() else "Unnamed Mission"
            duration_days = int(self.duration_entry.get())
            orbit_type = self.orbit_type_var.get()
            shielding_level = self.shielding_var.get()
            crew_size = self.crew_size_entry.get()
            start_date_str = self.start_date_entry.get()
            end_date_str = self.end_date_entry.get()
            
            # Re-fetch/re-calculate risk if not done, or use current displayed values
            current_risk_score = self.risk_score_label.cget("text").replace('%', '')
            current_risk_category = self.risk_category_label.cget("text")

            if current_risk_score == "N/A" or not current_risk_score:
                # If risk hasn't been calculated, do it now (or warn user)
                messagebox.showwarning("Missing Data", "Risk not calculated. Please calculate risk before generating report.")
                self._log_message("Report generation aborted: Risk not calculated.")
                self._update_progress(0, "Aborted")
                return
            
            current_risk_score = float(current_risk_score)

            mission_data = {
                "mission_name": mission_name,
                "duration_days": duration_days,
                "orbit_type": orbit_type,
                "shielding_level": shielding_level,
                "crew_size": crew_size,
                "start_date": start_date_str,
                "end_date": end_date_str
            }

            report_filepath = self.report_generator.generate_report(
                mission_data,
                current_risk_score,
                current_risk_category,
                self.flare_plot_filepath,
                self.gst_plot_filepath
            )

            if report_filepath:
                messagebox.showinfo("Report Generated", f"Report saved to:\n{report_filepath}")
                self._log_message(f"Report generated successfully: {report_filepath}")
                self._update_progress(100, "Report generated!")
            else:
                messagebox.showerror("Report Error", "Failed to generate report.")
                self._log_message("Error: Report generation failed.")
                self._update_progress(0, "Error")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input for report: {e}")
            self._log_message(f"Error during report generation (input): {e}")
            self._update_progress(0, "Error")
        except Exception as e:
            messagebox.showerror("Report Error", f"An unexpected error occurred: {e}")
            self._log_message(f"Unexpected error during report generation: {e}")
            self._update_progress(0, "Error")

    def _launch_quiz(self):
        self._log_message("Launching AstroMed Quiz...")
        try:
            quiz_mode.launch_quiz_window(self.master)
            self._log_message("AstroMed Quiz launched.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch quiz: {e}")
            self._log_message(f"Error launching quiz: {e}")
            
    def _open_reports_folder(self):
        self._log_message(f"Opening reports folder: {REPORTS_DIR}")
        os.makedirs(REPORTS_DIR, exist_ok=True) # Ensure it exists before opening
        try:
            os.startfile(REPORTS_DIR) # Opens the folder in file explorer
        except Exception as e:
            messagebox.showerror("Error", f"Could not open reports folder: {e}")
            self._log_message(f"Error opening reports folder: {e}")

def main():
    root = TkinterDnD.Tk() # Use TkinterDnD.Tk() for drag and drop functionality
    app = AstroMedAIGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()