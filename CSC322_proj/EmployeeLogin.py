from tkinter import *
from tkinter import messagebox
import pandas as pd
import os.path


class EmployeeLogin:
    username = None
    identity = None

    def __init__(self, master, storename):
        self.storename = storename
        self.store_employee_path = os.path.join('Database', storename, 'Employees.csv')
        self.master = master
        self.master.title('Employee Login')
        self.main_frame = Frame(self.master)
        self.instruction_label = Label(self.main_frame, text="\nEnter your username and password.\n")
        self.username_label = Label(self.main_frame, text="Username: ")
        self.password_label = Label(self.main_frame, text="Password: ")
        self.username_entry = Entry(self.main_frame)
        self.password_entry = Entry(self.main_frame)
        self.ok_button = Button(self.main_frame, text="OKAY", command=self.ok_event)
        self.cancel_button = Button(self.main_frame, text="CANCEL", command=quit)
        self.main_frame.grid(row=0, column=0)
        self.instruction_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0)
        self.password_label.grid(row=2, column=0)
        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)
        self.ok_button.grid(row=3, column=0)
        self.cancel_button.grid(row=3, column=1)

    def validate_identity(self, username, password):
        employee_list = pd.read_csv(self.store_employee_path, index_col=0)
        try:
            if employee_list.loc[username]['Password'] == password:
                self.username = username
                self.identity = employee_list.loc[username]['Identity']
                return True
            else:
                messagebox.showerror("Error", "Wrong password.")
                return False
        except:
            messagebox.showerror("Error", "Wrong username.")
            return False

    def ok_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.validate_identity(username, password):
            self.master.destroy()


# for testing
'''a = Tk()
b = EmployeeLogin(a, 'Brotherjohn')
a.mainloop()
print(b.username)
print(b.identity)'''
