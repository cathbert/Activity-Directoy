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
db.get_all_users()
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
                label.config(text=str(datetime.now().strftime("Today\'s date: %d-%m-%Y \nTime: %H:%M:%S  ")))
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
        for i in [MainPage, PassWordPage, SignUpPage, HomePage, AdminPage]:
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

        def sign_up():
            controller.showframe(SignUpPage)

        def on_enter1(event):
            login_button['background'] = '#ff73bb'

        def on_leave1(event):
            login_button['background'] = '#ff33bb'

        def on_enter2(event):
            signing_button['background'] = '#ff73bb'

        def on_leave2(event):
            signing_button['background'] = '#ff33bb'

        def on_enter3(event):
            exit_button['background'] = '#ff73bb'

        def on_leave3(event):
            exit_button['background'] = '#ff33bb'

        start_button_frame = tk.Frame(self, bg='#ff33bb')
        start_button_frame.pack(side="top", expand=True, anchor="n")
        login_button = tk.Button(start_button_frame, width=15, bg='#ff33bb', border=0,
                                 font=font, text="Login", relief='flat', command=login)
        login_button.pack(side="left", expand=True)

        signing_button = tk.Button(start_button_frame, width=15, bg='#ff33bb',
                                   font=font, text="Sign Up", relief='flat', command=sign_up)
        signing_button.pack(side="left", expand=True)

        exit_button = tk.Button(start_button_frame, width=15, bg='#ff33bb',
                                font=font, text="Exit", relief='flat', command=exit)
        exit_button.pack(expand=True)

        login_button.bind("<Enter>", on_enter1)
        login_button.bind("<Leave>", on_leave1)

        signing_button.bind("<Enter>", on_enter2)
        signing_button.bind("<Leave>", on_leave2)

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

            self.count
            if pwd_entry.get() == "1198":
                controller.showframe(AdminPage)
                pwd_entry.delete(0, "end")
            elif db.login_user(pwd_entry.get()):
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


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='#ff33bb')
        font = ("Verdana", 11)

        # Page title

        with open("temporary_files/current_user.txt", "r") as f:
            title = tk.Label(self, text=f"{f.read()} Home Page")
            title.pack()


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='#ff33bb')
        font = ("Verdana", 11)

        # Page title
        title = tk.Label(self, text="Admin Home Page", bg='#513d77', fg="Turquoise", font=("Verdana", 14))
        title.pack()

        # This is the umbrella frame for panel and tree frames
        overall_frame = tk.Frame(self)
        overall_frame.pack(fill='x')

        # This is to hold the panel buttons
        panel_frame = tk.Frame(overall_frame, bg='#513d77')
        panel_frame.pack(expand=True, fill="x")

        # This is to hold the whole database view
        tree_frame = tk.Frame(overall_frame)
        tree_frame.pack(anchor="n", side='top', expand=True, fill="x")

        # add new user panel button
        add_new_user = tk.Button(panel_frame, text="Add New User", fg="turquoise", bg='#513d77',
                                 relief="groove", font=font)
        add_new_user.pack(side='left')

        def delete_row():
            selected_row = tdv1.selection()
            text = tdv1.item(selected_row, 'values')
            try:
                db.delete_user(text[0])
                messagebox.showinfo("Successs!", "User deleted from database")
            except:
                pass
            tdv1.delete(selected_row)

        # Delete user panel button
        delete_user = tk.Button(panel_frame, text="Delete User", fg="turquoise", bg='#513d77',
                                relief="groove", font=font, command=delete_row)
        delete_user.pack(side='left')

        # logout panel button
        logout_btn = tk.Button(panel_frame, text="Logout", fg="gold", bg='#513d77',
                               relief="groove", font=font, command=lambda: controller.showframe(MainPage))
        logout_btn.pack(side='left')

        def callback(event):
            rowid = tdv1.identify_row(event.y)
            column = tdv1.identify_column(event.x)
            selitems = tdv1.selection()
            if selitems:
                selitem = selitems[0]
                text = tdv1.item(selitem, 'values')
                cell = int(column[1]) - 1
                print('Click on row:', rowid[0])
                print('Row data:', text)
                print('Clicked on Cell:', cell)
                print('Cell data:', text[cell])

        def get_row_data():
            selected_row = tdv1.selection()
            prev_item = tdv1.prev(selected_row)
            text = tdv1.item(selected_row, 'values')
            tags = tdv1.item(prev_item, 'tags')
            if tags:
                print(tags[0])
            else:
                pass
            print(text)

        menu = tk.Menu(tree_frame, tearoff=0)
        menu.add_command(label='Print row', command=get_row_data)
        menu.add_command(label='Add', command=None)
        menu.add_command(label='Edit', command=None)
        menu.add_command(label='Delete', command=delete_row)

        def mymenu(event):
            row_id = tdv1.identify_row(event.y)
            tdv1.selection_set(row_id)
            menu.post(event.x_root, event.y_root)

        tree_columns = ['Name', 'Surname', 'Username', 'Password']
        tdv1 = TreeDataView(tree_frame, tree_columns, scrollbar_x=True, scrollbar_y=True, double_click=callback)
        tdv1.pack(fill='both', expand=1)

        # Lets pick a random name, email and company name from the lists then create the email address.

        for item in db.get_all_users():
            name = item[0]
            surname = item[1]
            username = item[2]
            password = item[3]

            # Now lets insert a row with random data into the table.
            new_item = tdv1.insert('', 'end', values=(name, surname, username, password))
            tdv1.table_set_striped(new_item)

        # --configuring background color--
        self.configure(bg='#513d77')


if __name__ == "__main__":
    app = ActivityDiary()
    app.mainloop()

    with open("temporary_files/current_user.txt", 'r') as f:
        if len(f.read()) > 0:
            log.log_user_logout(f"{f.read()} exited out")
        else:
            log.log_user_logout(f"Admin exited out")

    db.clear_temporary()
