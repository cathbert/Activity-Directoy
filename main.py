# Project details and description
"""
    Author        : Cathbert Mutaurwa
    Project title : Activity Diary
    Duration date : 13/02/2020 -
    Description   : Program for my wife to record her activities and routine
                    exercises.
"""
# Required modules
# ----- import begins ------

import tkinter as tk
from tkinter import Menu
import random
from tkinter import ttk
from resources_and_tools.Database import Database
from resources_and_tools.Database import LoggerEngine
from resources_and_tools.TreeDataView import TreeDataView
from tkinter import messagebox
from datetime import datetime
from subprocess import call
import time

# ----- import ends ------

# Initializing support modules from resources_and_tools library
db = Database()
log = LoggerEngine()


class ActivityDiary(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x500+150+100")
        self.title("Neziswa's Activity Diary")
        self.config(bg='#ff33bb')
        call(["attrib", "+H", "database files"])
        # self.iconbitmap("images/cch_logo.ico")

        self.count = 0

        # time-----------------
        def time_counter(label):
            def counter():
                self.count += 1
                label.config(text=str(datetime.now().strftime("Today\'s date: %d.%m.%Y | Time: %H:%M:%S  ")))
                label.after(1000, counter)

            counter()

        time_label = tk.Label(self, bg='#ff33bb', font=("Verdana", 12))
        time_label.pack()
        time_counter(time_label)

        def on_enter(event):
            time_label["foreground"] = "purple"

        def on_leave(event):
            time_label["foreground"] = "black"

        time_label.bind("<Enter>", on_enter)
        time_label.bind("<Leave>", on_leave)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for i in [MainPage, PassWordPage, HomePage]:
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nwes')

        self.showframe(MainPage)

        # Frame for the main window bottom credit bar
        credit_frame = tk.Frame(self, bg='#ff33bb', relief='groove', bd=1)
        credit_frame.pack(fill='x')

        label = tk.Label(credit_frame, bg='#ff33bb', text='Trademark CCH All rights reserved 2020',
                         font=('Arial', 10, 'bold'))
        label.pack(anchor='center')

    def showframe(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='#ff33bb')
        font = ("Verdana", 14)

        # ------Frame for main title label and logo--------
        logo_label_frame = tk.Frame(self)
        logo_label_frame.pack(side="top", expand=True, anchor="n")

        img_logo = tk.PhotoImage(file="images/ActiveDiaryLogo.png")
        logo = tk.Label(logo_label_frame, image=img_logo)
        logo.image = img_logo
        logo.pack(side="top")
        self.count = 1

        # Inserting Start button
        def login():
            controller.showframe(PassWordPage)

        def on_enter1(event):
            login_button['background'] = '#ff73bb'

        def on_leave1(event):
            login_button['background'] = '#ff33bb'

        def on_enter3(event):
            exit_button['background'] = '#ff73bb'

        def on_leave3(event):
            exit_button['background'] = '#ff33bb'

        start_button_frame = tk.Frame(self, bg='#ff33bb')
        start_button_frame.pack(side="top", expand=True, anchor="n")
        login_button = tk.Button(start_button_frame, width=15, bg='#ff33bb', border=0,
                                 font=font, text="Login", relief='flat', command=login)
        login_button.pack(side="left", expand=True)

        exit_button = tk.Button(start_button_frame, width=15, bg='#ff33bb',
                                font=font, text="Exit", relief='flat', command=exit)
        exit_button.pack(expand=True)

        login_button.bind("<Enter>", on_enter1)
        login_button.bind("<Leave>", on_leave1)

        exit_button.bind("<Enter>", on_enter3)
        exit_button.bind("<Leave>", on_leave3)


class PassWordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='#ff33bb')
        font = ("Verdana", 11)

        # ------Frame for main title label and logo--------
        logo_label_frame = tk.Frame(self)
        logo_label_frame.pack(side="top", expand=True, anchor="n")

        img_logo = tk.PhotoImage(file="images/ActiveDiaryLogo.png")
        logo = tk.Label(logo_label_frame, image=img_logo)
        logo.image = img_logo
        logo.pack(side="top")
        self.count = 1

        # Inserting Start button
        def input_pwd():
            if db.login_user(pwd_entry.get()):
                controller.showframe(HomePage)
                pwd_entry.delete(0, "end")
            elif pwd_entry.get() == '':
                pwd_label.config(text="Entry empty!!!")
                if self.count == 3:
                    messagebox.showwarning("Are you dumb", "If you dont know or forget password"
                                                           " consult system admin")
                    self.count = 1
                self.count += 1
            else:
                pwd_label.config(text="Wrong password!!")
                pwd_entry.delete(0, "end")
                self.count = 1

        start_button_frame = tk.Frame(self, bg='#ff33bb')
        start_button_frame.pack(side="top", expand=True, anchor="n")
        pwd_label = tk.Label(start_button_frame, font=font, fg='turquoise', bg='#ff33bb')
        pwd_label.pack()
        pwd_entry = tk.Entry(start_button_frame, font=font, relief="flat",
                             show="*", justify="center")
        pwd_entry.pack()
        pwd_button = tk.Button(start_button_frame, width=30, bg='#ff33bb',
                               font=font, text="Start", relief='flat', command=input_pwd)
        pwd_button.pack()


'''
class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='#ff33bb')
        font = ("Verdana", 13)

        title = tk.Label(self, text="SignUp", font=("Verdana", 23, "bold"), bg='#ff33bb')
        title.pack()

        # Creating a signup frame
        form_frame = tk.Frame(self, relief='raised', bd=1, bg='#ff33bb', width=100)
        form_frame.pack(expand=True, anchor="n")

        def newuser():
            try:
                db.register_new_user(fname_entry.get(),
                                     lname_entry.get(),
                                     uname_entry.get(),
                                     pwd_entry.get())
                log.log_info(f"New user {uname_entry.get()} created!")
                fname_entry.delete(0, 'end')
                lname_entry.delete(0, 'end')
                uname_entry.delete(0, 'end')
                pwd_entry.delete(0, 'end')
                re_pwd_entry.delete(0, 'end')
                messagebox.showinfo("Success!!", "Successfully created new user")
                controller.showframe(MainPage)
            except Exception as e:
                pass

        # Entry for first name
        fname_entry = tk.Entry(form_frame, font=font, bg='#ff73bb', width=70)
        fname_entry.grid(row=0, column=0)

        # Label for first name
        fname_label = tk.Label(form_frame, text="First Name:", font=font, bg='#ff33bb')
        fname_label.grid(row=1, column=0)

        # Entry for last name
        lname_entry = tk.Entry(form_frame, font=font, bg='#ff73bb', width=70)
        lname_entry.grid(row=2, column=0)

        # Label for last name
        lname_label = tk.Label(form_frame, text="Last Name:", font=font, bg='#ff33bb')
        lname_label.grid(row=3, column=0)

        # Entry for user name
        uname_entry = tk.Entry(form_frame, font=font, bg='#ff73bb', width=15)
        uname_entry.grid(row=4, column=0)

        # Label for user name
        uname_label = tk.Label(form_frame, text="User Name:", font=font, bg='#ff33bb')
        uname_label.grid(row=5, column=0)

        # Entry for password
        pwd_entry = tk.Entry(form_frame, font=font, bg='#ff73bb', width=25, show='-', justify='center')
        pwd_entry.grid(row=6, column=0)

        # label for password
        pwd_label = tk.Label(form_frame, text="Password:", font=font, bg='#ff33bb')
        pwd_label.grid(row=7, column=0)

        # Entry for password re-entry
        re_pwd_entry = tk.Entry(form_frame, font=font, bg='#ff73bb', width=25, show='-', justify='center')
        re_pwd_entry.grid(row=8, column=0)

        # Label for password re-entry
        re_pwd_label = tk.Label(form_frame, text="Re-Type Password:", font=font, bg='#ff33bb')
        re_pwd_label.grid(row=9, column=0)

        def on_enter(event):
            register_button['background'] = '#ff73bb'

        def on_leave(event):
            register_button['background'] = '#ff99dd'

        register_button = tk.Button(form_frame, width=25, bg='#ff99dd', fg='green',
                                    font=("Verdana", 15), text="Register", relief='flat', command=newuser)
        register_button.grid(row=10, column=0)

        register_button.bind("<Enter>", on_enter)
        register_button.bind("<Leave>", on_leave)
'''


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='#ff33bb')
        font = ("Verdana", 11)

        # Page title
        title = tk.Label(self, text="Welcome Nezi", bg='#ff33bb')
        title.pack()


if __name__ == "__main__":
    app = ActivityDiary()
    app.mainloop()

    with open("temporary_files/current_user.txt", 'r') as f:
        if len(f.read()) > 0:
            log.log_user_logout(f"{f.read()} exited out")
        else:
            log.log_user_logout(f"Admin exited out")

    db.clear_temporary()
