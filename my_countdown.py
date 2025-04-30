import tkinter as tk
from tkinter import ttk
import datetime

def format_time(seconds: int) -> str:
    """
    Convert seconds into HH:MM:SS format.
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

class Countdown(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Your Time Counts")
        self.pack(padx=0, pady=10, fill='x')

        # Tracking attributes
        self.session_start = None
        self.pause_start = None
        self.total_pause = 0
        self.history = []
        self.original_seconds = 0
        self.after_id = None
        self.session_recorded = False  # to prevent duplicate records

        # Countdown state
        self.time_unit = tk.StringVar(value="hours")
        self.session_name_var = tk.StringVar()
        self.is_paused = False
        self.running = False
        self.history_visible = False

        self.create_widgets()

    def create_widgets(self):
        self.master.configure(bg='#f0f0f0')

        # Input row: countdown and unit
        self.entry_label = tk.Label(self, text="TIME COUNTDOWN:", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.entry = tk.Entry(self, font=('Arial', 12))
        self.unit_menu = tk.OptionMenu(self, self.time_unit, "hours", "minutes", "seconds")

        self.entry_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.unit_menu.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        # Input row: session name
        self.name_label = tk.Label(self, text="Session Name:", font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.name_entry = tk.Entry(self, textvariable=self.session_name_var, font=('Arial', 12))
        self.name_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew', columnspan=2)

        # Timer display
        self.label = tk.Label(self, text="00:00:00", font=('Helvetica', 48, 'bold'), fg='#333333', bg='#f0f0f0')
        self.label.grid(row=2, column=0, columnspan=3, pady=10)

        # Control buttons
        self.start = tk.Button(self, text="START", command=self.start_countdown,
                               bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'))
        self.pause_resume = tk.Button(self, text="PAUSE", command=self.pause_resume_countdown,
                                      bg='#FF5722', fg='white', font=('Arial', 12, 'bold'))
        self.reset = tk.Button(self, text="RESET", command=self.reset_countdown,
                               bg='#2196F3', fg='white', font=('Arial', 12, 'bold'))

        self.start.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        self.pause_resume.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        self.reset.grid(row=3, column=2, padx=5, pady=5, sticky='ew')

        for i in range(3):
            self.columnconfigure(i, weight=1)

        # Analytics frame
        analytics_frame = tk.Frame(self, bg='#f0f0f0')
        analytics_frame.grid(row=4, column=0, columnspan=3, pady=5, sticky='ew')
        analytics_frame.columnconfigure(0, weight=1)
        analytics_frame.columnconfigure(1, weight=1)
        analytics_frame.columnconfigure(2, weight=0)

        self.label_active = tk.Label(analytics_frame, text="Active: 00:00:00",
                                     font=('Arial', 10), bg='#f0f0f0')
        self.label_paused = tk.Label(analytics_frame, text="Paused: 00:00:00",
                                     font=('Arial', 10), bg='#f0f0f0')
        self.history_btn = tk.Button(analytics_frame, text="History", command=self.toggle_history,
                                     bg='#607D8B', fg='white', font=('Arial', 10, 'bold'))

        self.label_active.grid(row=0, column=0, padx=5, sticky='w')
        self.label_paused.grid(row=0, column=1, padx=5, sticky='w')
        self.history_btn.grid(row=0, column=2, padx=10)

        # History frame (hidden by default)
        self.history_frame = tk.Frame(self, bg='#ffffff')
        self.history_frame.grid(row=5, column=0, columnspan=3, sticky='nsew')
        self.history_frame.grid_remove()

        cols = ('name', 'start', 'length', 'active', 'paused')
        self.tree = ttk.Treeview(self.history_frame, columns=cols, show='headings', height=6)
        for col, text in zip(cols, ('Name', 'Start', 'Length', 'Active', 'Paused')):
            width = 150 if col == 'start' else 100
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor='center')
        vsb = ttk.Scrollbar(self.history_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        # Clear history button
        self.clear_btn = tk.Button(self.history_frame, text="Clear History", command=self.clear_history,
                                   bg='#D32F2F', fg='white', font=('Arial', 10, 'bold'))
        self.clear_btn.grid(row=1, column=0, columnspan=2, pady=5)

        self.history_frame.columnconfigure(0, weight=1)
        self.history_frame.rowconfigure(0, weight=1)

    def start_countdown(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        try:
            time_value = float(self.entry.get())
        except ValueError:
            return
        unit = self.time_unit.get()
        if unit == "hours":
            seconds = int(time_value * 3600)
        elif unit == "minutes":
            seconds = int(time_value * 60)
        else:
            seconds = int(time_value)

        self.remaining = seconds
        self.original_seconds = seconds
        self.session_recorded = False  # reset record flag

        now = datetime.datetime.now()
        self.session_start = now
        self.total_pause = 0
        self.pause_start = None

        self.is_paused = False
        self.running = True
        self.start.configure(text="RESTART")
        self.pause_resume.configure(text="PAUSE")

        self.countdown()

    def pause_resume_countdown(self):
        if not self.running:
            return
        now = datetime.datetime.now()
        if self.is_paused:
            self.is_paused = False
            self.pause_resume.configure(text="PAUSE")
            if self.pause_start:
                self.total_pause += (now - self.pause_start).total_seconds()
                self.pause_start = None
            self.countdown()
        else:
            self.is_paused = True
            self.pause_resume.configure(text="RESUME")
            self.pause_start = now

    def reset_countdown(self):
        if self.session_start and not self.session_recorded:
            self._record_session()

        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        self.running = False
        self.is_paused = False
        self.session_start = None
        self.pause_start = None
        self.total_pause = 0
        self.label.configure(text="00:00:00")
        self.label_active.configure(text="Active: 00:00:00")
        self.label_paused.configure(text="Paused: 00:00:00")
        self.entry.delete(0, 'end')
        self.session_name_var.set("")
        self.start.configure(text="START")
        self.pause_resume.configure(text="PAUSE")

    def countdown(self):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

        if not self.running or self.is_paused:
            return

        if self.remaining <= 0:
            self.label.configure(text="TIME'S UP!")
            self.running = False
            self.start.configure(text="RESTART")
            self._record_session()
            return

        self.label.configure(text=format_time(self.remaining))
        self.remaining -= 1

        now = datetime.datetime.now()
        elapsed = (now - self.session_start).total_seconds()
        active_time = elapsed - self.total_pause
        self.label_active.configure(text=f"Active: {format_time(active_time)}")
        self.label_paused.configure(text=f"Paused: {format_time(self.total_pause)}")

        self.after_id = self.after(1000, self.countdown)

    def _record_session(self):
        if self.session_recorded:
            return
        self.session_recorded = True

        end_time = datetime.datetime.now()
        total_time = (end_time - self.session_start).total_seconds()
        paused = self.total_pause
        active = total_time - paused

        self.history.append({
            "name": self.session_name_var.get() or "",
            "start": self.session_start,
            "length": self.original_seconds,
            "active": int(active),
            "paused": int(paused)
        })

    def toggle_history(self):
        if self.history_visible:
            self.history_frame.grid_remove()
            self.history_visible = False
        else:
            for i in self.tree.get_children():
                self.tree.delete(i)
            for sess in self.history:
                self.tree.insert('', 'end', values=(
                    sess['name'],
                    sess['start'].strftime("%Y-%m-%d %H:%M:%S"),
                    format_time(sess['length']),
                    format_time(sess['active']),
                    format_time(sess['paused'])
                ))
            self.history_frame.grid()
            self.history_visible = True

    def clear_history(self):
        self.history.clear()
        for i in self.tree.get_children():
            self.tree.delete(i)

if __name__ == '__main__':
    root = tk.Tk()
    app = Countdown(master=root)
    app.mainloop()
