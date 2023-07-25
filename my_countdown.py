import tkinter as tk
import datetime

class Countdown(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('500x250')  # set initial window size (width x height)
        self.master.title("Your Time Counts")  # set window title
        self.pack(padx=0, pady=25)  # add padding around widgets
        self.create_widgets()
        self.is_paused = False
        self.running = False

    def create_widgets(self):
        self.entry_label = tk.Label(self, text="TIME COUNTDOWN (hours): ")
        self.entry_label.grid(row=0, column=0)  # place label in first row, first column

        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1)  # place entry box in first row, second column

        self.label = tk.Label(self, text="00:00:00", font=('Helvetica', 80))  # set initial text to 00:00:00
        self.label.grid(row=1, column=0, columnspan=3)  # place countdown label in second row, spanning three columns

        self.start = tk.Button(self, text="START", command=self.start_countdown,bg='green',fg='white')
        self.start.grid(row=2, column=0,sticky='ew')  # place START button in third row, first column

        self.pause_resume = tk.Button(self, text="PAUSE", command=self.pause_resume_countdown,bg='red',fg='white')
        self.pause_resume.grid(row=2, column=1,sticky='ew')  # place PAUSE button in third row, second column

        self.reset = tk.Button(self, text="RESET", command=self.reset_countdown,bg='blue',fg='white')
        self.reset.grid(row=2, column=2,sticky='ew')  # place RESET button in third row, third column

    def start_countdown(self):
        self.remaining = int(float(self.entry.get()) * 3600)  # convert input hours to seconds
        self.is_paused = False
        self.running = True
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
        self.remaining = 0
        self.is_paused = False
        self.running = False
        self.pause_resume.configure(text="PAUSE")  # change text back to PAUSE when RESET is pressed
        self.label.configure(text="00:00:00")
        self.entry.delete(0, 'end')

    def countdown(self):
        if self.is_paused or not self.running:
            return
        if self.remaining <= 0:
            self.label.configure(text="Time's up!")
        else:
            hours, remainder = divmod(self.remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label.configure(text="{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds)))
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

root = tk.Tk()
app = Countdown(master=root)
app.mainloop()
