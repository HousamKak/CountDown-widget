import tkinter as tk
import datetime

class Countdown(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('600x300')  # Increase initial window size
        self.master.title("Your Time Counts")  # Set window title
        self.pack(padx=0, pady=25)  # Add padding around widgets

        # Initialize the time_unit variable before creating widgets
        self.time_unit = tk.StringVar(value="hours")  # Default to hours
        self.after_id = None  # To track scheduled callbacks
        self.create_widgets()

        self.is_paused = False
        self.running = False

        # Disable resizing completely
        self.master.resizable(False, False)
        self.master.maxsize(600, 300)

    def create_widgets(self):
        self.master.configure(bg='#f0f0f0')  # Set a light background color

        self.entry_label = tk.Label(self, text="TIME COUNTDOWN:", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.entry = tk.Entry(self, font=('Arial', 12))
        self.unit_menu = tk.OptionMenu(self, self.time_unit, "hours", "minutes", "seconds")
        self.label = tk.Label(self, text="00:00:00", font=('Helvetica', 48, 'bold'), fg='#333333', bg='#f0f0f0')
        self.start = tk.Button(self, text="START", command=self.start_countdown, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
        self.pause_resume = tk.Button(self, text="PAUSE", command=self.pause_resume_countdown, bg='#FF5722', fg='white', font=('Arial', 12, 'bold'))
        self.reset = tk.Button(self, text="RESET", command=self.reset_countdown, bg='#2196F3', fg='white', font=('Arial', 12, 'bold'))

        self.entry_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.unit_menu.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
        self.label.grid(row=1, column=0, columnspan=3, pady=20, sticky='ew')
        self.start.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.pause_resume.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.reset.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def start_countdown(self):
        # Cancel any pending countdown callbacks
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        # Get time value from entry
        try:
            time_value = float(self.entry.get())
        except ValueError:
            return
        unit = self.time_unit.get()

        # Convert time to seconds
        if unit == "hours":
            self.remaining = int(time_value * 3600)
        elif unit == "minutes":
            self.remaining = int(time_value * 60)
        else:
            self.remaining = int(time_value)

        # Reset states and update buttons
        self.is_paused = False
        self.running = True
        self.start.configure(text="RESTART")
        self.pause_resume.configure(text="PAUSE")

        # Start countdown
        self.countdown()

    def pause_resume_countdown(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_resume.configure(text="PAUSE")
            self.countdown()
        else:
            self.is_paused = True
            self.pause_resume.configure(text="RESUME")

    def reset_countdown(self):
        # Cancel any pending callbacks
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        # Reset all states and UI
        self.running = False
        self.is_paused = False
        self.start.configure(text="START")
        self.pause_resume.configure(text="PAUSE")
        self.label.configure(text="00:00:00")
        self.entry.delete(0, 'end')

    def countdown(self):
        # Cancel previous callback if any
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        if not self.running or self.is_paused:
            return

        if self.remaining <= 0:
            self.running = False
            self.label.configure(text="TIME'S UP!")
            self.start.configure(text="RESTART")
            return

        # Update display
        hours, remainder = divmod(self.remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.remaining -= 1

        # Schedule next tick
        self.after_id = self.after(1000, self.countdown)

if __name__ == '__main__':
    root = tk.Tk()
    app = Countdown(master=root)
    app.mainloop()
