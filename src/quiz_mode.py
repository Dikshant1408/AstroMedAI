import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import datetime # Import datetime

# --- Quiz Constants & Styles ---
QUIZ_BG_COLOR = "#2B2B2B"   # Dark gray
QUIZ_FG_COLOR = "#F0F0F0"   # Light text
QUIZ_ACCENT_COLOR = "#6A5ACD" # SlateBlue
BUTTON_COLOR = "#4682B4"   # SteelBlue
BUTTON_TEXT_COLOR = "white"

QUESTIONS = [
    {"question": "What is the primary source of radiation risk in deep space?",
     "options": ["Solar Flares", "Galactic Cosmic Rays (GCRs)", "Earth's Van Allen Belts", "Cosmic Microwave Background"],
     "answer": "Galactic Cosmic Rays (GCRs)"},
    {"question": "Which of these is a short-term effect of high radiation exposure?",
     "options": ["Cancer", "Cataracts", "Acute Radiation Syndrome (ARS)", "Genetic Mutations"],
     "answer": "Acute Radiation Syndrome (ARS)"},
    {"question": "What material is commonly explored for radiation shielding in space?",
     "options": ["Lead", "Aluminum", "Water", "Iron"],
     "answer": "Water"},
    {"question": "The NASA DONKI API provides data on what type of space weather?",
     "options": ["Planetary Alignments", "Aurora Activity", "Solar and Geomagnetic Events", "Asteroid Trajectories"],
     "answer": "Solar and Geomagnetic Events"},
    {"question": "What health issue is a long-term concern for astronauts due to radiation?",
     "options": ["Scurvy", "Bone Density Loss", "Cardiovascular Disease", "Muscle Atrophy"],
     "answer": "Cardiovascular Disease"}
]

# Adjusted path for the new structure
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "quiz_highscores.json")

def load_highscores():
    os.makedirs(os.path.dirname(HIGHSCORE_FILE), exist_ok=True) # Ensure data dir exists
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"WARNING: Highscore file {HIGHSCORE_FILE} is corrupt. Starting with empty scores.")
            return {"high_scores": []} 
    return {"high_scores": []}

def save_highscores(scores):
    os.makedirs(os.path.dirname(HIGHSCORE_FILE), exist_ok=True) # Ensure data dir exists
    with open(HIGHSCORE_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

class QuizApp:
    def __init__(self, master_window):
        self.master_window = master_window
        self.quiz_window = tk.Toplevel(master_window)
        self.quiz_window.title("AstroMed Quiz")
        self.quiz_window.geometry("700x550")
        self.quiz_window.configure(bg=QUIZ_BG_COLOR)
        self.quiz_window.transient(master_window) # Set master_window as parent
        self.quiz_window.grab_set() # Make quiz_window modal

        self.current_question = 0
        self.score = 0
        self.highscores = load_highscores()

        self._setup_quiz_styles()
        self._create_widgets()
        self._display_question()

    def _setup_quiz_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('QFrame.TFrame', background=QUIZ_BG_COLOR)
        style.configure('QLabel.TLabel', background=QUIZ_BG_COLOR, foreground=QUIZ_FG_COLOR, font=('Arial', 14))
        style.configure('QRadiobutton.TRadiobutton', background=QUIZ_BG_COLOR, foreground=QUIZ_FG_COLOR, font=('Arial', 12))
        style.map('QRadiobutton.TRadiobutton',
                  background=[('active', QUIZ_BG_COLOR)],
                  foreground=[('active', QUIZ_ACCENT_COLOR)])
        style.configure('QButton.TButton', background=BUTTON_COLOR, foreground=BUTTON_TEXT_COLOR, font=('Arial', 12, 'bold'), padding=8, relief='flat')
        style.map('QButton.TButton', background=[('active', QUIZ_ACCENT_COLOR)])
        style.configure('QHeading.TLabel', background=QUIZ_BG_COLOR, foreground=QUIZ_ACCENT_COLOR, font=('Arial', 18, 'bold'))

    def _create_widgets(self):
        main_frame = ttk.Frame(self.quiz_window, padding=20, style='QFrame.TFrame')
        main_frame.pack(expand=True, fill='both')

        self.question_label = ttk.Label(main_frame, text="", wraplength=600, style='QHeading.TLabel')
        self.question_label.pack(pady=20)

        self.radio_var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(main_frame, text="", variable=self.radio_var, value="", style='QRadiobutton.TRadiobutton')
            rb.pack(anchor="w", pady=5)
            self.option_buttons.append(rb)

        self.feedback_label = ttk.Label(main_frame, text="", style='QLabel.TLabel')
        self.feedback_label.pack(pady=10)

        button_frame = ttk.Frame(main_frame, style='QFrame.TFrame')
        button_frame.pack(pady=20)

        self.submit_button = ttk.Button(button_frame, text="Submit Answer", command=self._check_answer, style='QButton.TButton')
        self.submit_button.pack(side="left", padx=10)

        self.next_button = ttk.Button(button_frame, text="Next Question", command=self._next_question, state=tk.DISABLED, style='QButton.TButton')
        self.next_button.pack(side="left", padx=10)

        self.quit_button = ttk.Button(button_frame, text="Quit Quiz", command=self._quit_quiz, style='QButton.TButton')
        self.quit_button.pack(side="right", padx=10)

        self.score_label = ttk.Label(main_frame, text=f"Score: {self.score}/{len(QUESTIONS)}", style='QLabel.TLabel')
        self.score_label.pack(pady=10)

    def _display_question(self):
        if self.current_question < len(QUESTIONS):
            q_data = QUESTIONS[self.current_question]
            self.question_label.config(text=f"Question {self.current_question + 1}: {q_data['question']}")
            self.radio_var.set("") # Clear selection
            for i, option in enumerate(q_data['options']):
                self.option_buttons[i].config(text=option, value=option)
            self.feedback_label.config(text="")
            self.submit_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
        else:
            self._show_final_score()

    def _check_answer(self):
        selected_answer = self.radio_var.get()
        correct_answer = QUESTIONS[self.current_question]['answer']

        if selected_answer == correct_answer:
            self.score += 1
            self.feedback_label.config(text="Correct!", foreground="green")
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer was: {correct_answer}", foreground="red")
        
        self.score_label.config(text=f"Score: {self.score}/{len(QUESTIONS)}")
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def _next_question(self):
        self.current_question += 1
        self._display_question()

    def _show_final_score(self):
        self.question_label.config(text="Quiz Complete!")
        for rb in self.option_buttons:
            rb.pack_forget() # Hide options
        self.submit_button.pack_forget()
        self.next_button.pack_forget()
        self.feedback_label.config(text="")

        final_message = f"You scored {self.score} out of {len(QUESTIONS)}!\n"
        
        is_highscore = False
        current_scores = self.highscores.get("high_scores", [])
        if not current_scores or self.score > min(s['score'] for s in current_scores) or len(current_scores) < 5: # Top 5
            final_message += "Congratulations, new high score!"
            is_highscore = True
            
        messagebox.showinfo("Quiz Complete", final_message)
        
        if is_highscore:
            self._prompt_for_name()
        else:
            self._display_highscores()
            self._quiz_close_options()

    def _prompt_for_name(self):
        name_window = tk.Toplevel(self.quiz_window)
        name_window.title("Enter Your Name")
        name_window.geometry("300x150")
        name_window.transient(self.quiz_window)
        name_window.grab_set()
        name_window.configure(bg=QUIZ_BG_COLOR)
        
        ttk.Label(name_window, text="Enter your name for the high score:", style='QLabel.TLabel').pack(pady=10)
        name_entry = ttk.Entry(name_window, width=30, style='TEntry') # Using TEntry style from main_app
        name_entry.pack(pady=5)
        
        def save_score():
            player_name = name_entry.get().strip()
            if not player_name:
                player_name = "Anonymous"
            self._add_highscore(player_name, self.score)
            name_window.destroy()
            self._display_highscores()
            self._quiz_close_options()

        ttk.Button(name_window, text="Save Score", command=save_score, style='QButton.TButton').pack(pady=10)
        
        name_window.protocol("WM_DELETE_WINDOW", lambda: [name_window.destroy(), self._quiz_close_options()]) # Handle window close

    def _add_highscore(self, name, score):
        self.highscores["high_scores"].append({"name": name, "score": score, "date": datetime.date.today().strftime("%Y-%m-%d")})
        self.highscores["high_scores"].sort(key=lambda x: x['score'], reverse=True)
        self.highscores["high_scores"] = self.highscores["high_scores"][:5] # Keep top 5
        save_highscores(self.highscores)

    def _display_highscores(self):
        high_score_text = "--- High Scores ---\n"
        for i, entry in enumerate(self.highscores.get("high_scores", [])):
            high_score_text += f"{i+1}. {entry['name']}: {entry['score']} ({entry['date']})\n"
        
        self.feedback_label.config(text=high_score_text, foreground=QUIZ_FG_COLOR)
        self.feedback_label.pack(pady=10) # Repack to ensure visibility


    def _quit_quiz(self):
        if messagebox.askyesno("Quit Quiz", "Are you sure you want to quit the quiz?"):
            self.quiz_window.destroy()
            self.master_window.grab_release() # Release grab

    def _quiz_close_options(self):
        # Options after quiz ends
        play_again_button = ttk.Button(self.quiz_window, text="Play Again", command=self._reset_quiz, style='QButton.TButton')
        play_again_button.pack(pady=5)
        
        back_to_main_button = ttk.Button(self.quiz_window, text="Back to Main Menu", command=self._quit_quiz, style='QButton.TButton')
        back_to_main_button.pack(pady=5)


    def _reset_quiz(self):
        self.current_question = 0
        self.score = 0
        self.radio_var.set("")
        self.feedback_label.config(text="")
        self.score_label.config(text=f"Score: {self.score}/{len(QUESTIONS)}")
        
        # Re-pack widgets that might have been forgotten
        for rb in self.option_buttons:
            rb.pack(anchor="w", pady=5)
        self.submit_button.pack(side="left", padx=10)
        self.next_button.pack(side="left", padx=10)
        
        self._display_question()
        
        # Remove "Play Again" and "Back to Main Menu" buttons if they exist
        for widget in self.quiz_window.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") in ["Play Again", "Back to Main Menu"]:
                widget.destroy()


def launch_quiz_window(parent_window):
    """
    Function to be called from astro_med_ai_gui.py to launch the quiz.
    """
    QuizApp(parent_window)

# This part ensures quiz_mode.py can still be run standalone for testing,
# but it won't interfere when imported by astro_med_ai_gui.py
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Hide the root window as the quiz will open its own Toplevel
    launch_quiz_window(root)
    root.mainloop()