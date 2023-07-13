import time
import tkinter as tk
from tkinter import Tk, messagebox
from tkinter import Entry, Button


class Pomodoro(Tk):
    def __init__(self, session=True, session_count=1):
        super().__init__()
        self.geometry("300x200")

        # To set the app to not be able to minimizable and closable until time finishes
        # self.attributes('-fullscreen', True)
        # self.attributes('-topmost', True)
        # self.protocol('WM_DELETE_WINDOW', self.prevent_exit)

        self.session = session
        self.session_count = session_count
        self.long_break = (self.session_count%4==0)
        print("Session Count: ", self.session_count, "; Is session: ", self.session, "; Is long break: ", self.long_break)
        
        self.hours = tk.StringVar()
        self.mins = tk.StringVar()
        self.secs = tk.StringVar()

        if self.session:
            self.title(f"Pomodoro - Session {(self.session_count+1)//2}")
            self.hours.set("00")
            self.mins.set("25")
            self.secs.set("00")
        elif self.long_break:
            self.title(f"Pomodoro - Long Break {(self.session_count+1)//4}")
            self.hours.set("00")
            self.mins.set("15")
            self.secs.set("00")
        else:
            self.title(f"Pomodoro - Break {self.session_count//2}")
            self.hours.set("00")
            self.mins.set("05")
            self.secs.set("00")

        hours_entry = Entry(self, textvariable=self.hours, font=("Arial",18,""), width=3)
        hours_entry.place(x=80,y=20)
        mins_entry = Entry(self, textvariable=self.mins, font=("Arial",18,""), width=3)
        mins_entry.place(x=130,y=20)
        secs_entry = Entry(self, textvariable=self.secs, font=("Arial",18,""), width=3)
        secs_entry.place(x=180,y=20)

        if self.long_break:
            btn = Button(self, text="Start Long Break", command=self.submit)
        elif not self.session:
            btn = Button(self, text='Start Break', command=self.submit)
        else:
            btn = Button(self, text='Start Session', command=self.submit)
        btn.place(x = 70,y = 120)

    def prevent_exit(self):
        pass

    def submit(self):
        self.session = not self.session
        self.countdown()

    @classmethod
    def restart(cls, session, session_count):
        return cls(session, session_count)

    def countdown(self):
        try:
            temp = int(self.hours.get())*3600 + int(self.mins.get())*60 + int(self.secs.get())
        except:
            print("Please input the right value")
            return
        while temp >-1:
            mins,secs = divmod(temp,60)

            hours=0
            if mins >60:
                hours, mins = divmod(mins, 60)

            self.hours.set("{:02d}".format(hours))
            self.mins.set("{:02d}".format(mins))
            self.secs.set("{:02d}".format(secs))

            self.update()
            time.sleep(1)

            if (temp == 0):
                messagebox.askquestion("Time Countdown", "Do you want to continue?", icon="info")
                new_window = self.restart(self.session, self.session_count+1)
                self.destroy()
                new_window.mainloop()
            temp -= 1


if __name__ == "__main__":
    app = Pomodoro(session=True, session_count=1)
    app.mainloop()
