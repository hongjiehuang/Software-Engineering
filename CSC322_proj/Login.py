from tkinter import *
from tkinter import messagebox
# from PIL import Image, ImageTk
import pandas as pd
import os.path
import Manager


class Login:
    username = ''
    identity = ''
    login = False

    def __init__(self, master, storename):
        self.storename = storename
        self.store_user_path = os.path.join('Database', storename, 'Users.csv')
        self.master = master
        self.master.title('Login')
        self.main_frame = Frame(self.master)
        self.instruction_label = Label(self.main_frame, text="For the returning customer, please log in.\n"
                                                             "If you would like to proceed as visitor, please click "
                                                             "\"VISITOR\".\n"
                                                             "Or register as new customer to become registered customer.\n")
        self.username_label = Label(self.main_frame, text="Username: ")
        self.password_label = Label(self.main_frame, text="Password: ")
        self.username_entry = Entry(self.main_frame)
        self.password_entry = Entry(self.main_frame)
        self.ok_button = Button(self.main_frame, text="OKAY", command=self.ok_event)
        self.register_button = Button(self.main_frame, text="REGISTER", command=self.register)
        self.visitor_button = Button(self.main_frame, text="VISITOR", command=self.visitor_login)
        self.cancel_button = Button(self.main_frame, text="CANCEL", command=quit)
        self.main_frame.grid(row=0, column=0)
        self.instruction_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0)
        self.password_label.grid(row=2, column=0)
        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)
        self.register_button.grid(row=3, column=1)
        self.visitor_button.grid(row=3, column=0)
        self.ok_button.grid(row=4, column=0)
        self.cancel_button.grid(row=4, column=1)

    def validate_identity(self, username, password):
        user_list = pd.read_csv(self.store_user_path, index_col=0)
        try:
            if user_list.loc[username]['Password'] == password:
                self.username = username
                self.identity = user_list.loc[username]['Identity']
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

    def visitor_login(self):
        self.username = 'visitor'
        self.identity = 'visitor'
        self.master.destroy()

    def register(self):

        def cancel_event():
            root.destroy()

        def ok_event(username_e, password_e, ssn_e, tk_root):
            exist = False
            ssn_exist = False
            blacklisted = False
            username = username_e.get()
            password = password_e.get()
            ssn = ssn_e.get()
            if username == '' or password == '' or ssn == '':
                messagebox.showerror('Error', 'Please fill in all the fields.')
                return
            # first check if the ssn appear in blacklist
            ssn = int(ssn)
            blacklist = pd.read_csv('Database/Blacklist.csv')
            blacklist_ssn = blacklist['ssn']
            blacklist = pd.read_csv('Database/Blacklist.csv', index_col=0)
            for entry in blacklist_ssn:
                if int(ssn) == int(entry):
                    blacklisted = True
            if blacklisted:
                messagebox.showerror('Error', 'Sorry, the given ssn is in blacklist by %s.\n'
                                              'If you believe this is a mistake, '
                                              'please contact the store manager.' % (blacklist.loc[ssn]['store']))
                return
            else:
                path = os.path.join('Database', self.storename, 'PendingUsers.csv')
                pending_list = pd.read_csv(path)['ssn']
                if ssn in pending_list:
                    messagebox.showerror('Error', 'You are already in the pending list.\n'
                                                  'Please wait for approval from the store manager.')
                    return
                user_list = pd.read_csv(self.store_user_path)
                username_list = user_list['Username']
                ssn_list = user_list['ssn']
                for user in username_list:
                    if username == user:
                        exist = True
                for entry in ssn_list:
                    if int(ssn) == int(entry):
                        ssn_exist = True
                if exist:
                    messagebox.showerror('Error', 'Username already exist.\n '
                                                  'Please log in or enter another username.')
                    return
                elif ssn_exist:
                    messagebox.showerror('Error', 'SSN already exist.\n'
                                                  'Please try again.')
                    return
                else:
                    data = [[ssn, username, password]]
                    df = pd.DataFrame(data, columns=["ssn", "Username", "Password"])
                    with open(path, 'a') as pending_user_csv:
                        df.to_csv(pending_user_csv, index=False, header=False)
                    messagebox.showinfo('Register', 'Congratulation, you\'ll be notified when approved.')
                    tk_root.destroy()

        root = Tk()
        root.title('Register')
        main_frame = Frame(root)
        instruction_label = Label(main_frame, text='Please enter the following with appropriate values.')
        username_label = Label(main_frame, text='Username: ')
        password_label = Label(main_frame, text='Password: ')
        ssn_label = Label(main_frame, text='SSN: ')
        username_entry = Entry(main_frame)
        password_entry = Entry(main_frame)
        ssn_entry = Entry(main_frame)
        cancel_button = Button(main_frame, text='cancel', command=cancel_event)
        ok_button = Button(main_frame, text='ok', command=lambda: ok_event(username_entry, password_entry, ssn_entry, root))
        main_frame.grid()
        instruction_label.grid(row=0, column=0, columnspan=2)
        username_label.grid(row=1, column=0)
        password_label.grid(row=2, column=0)
        ssn_label.grid(row=3, column=0)
        username_entry.grid(row=1, column=1)
        password_entry.grid(row=2, column=1)
        ssn_entry.grid(row=3, column=1)
        ok_button.grid(row=4, column=0)
        cancel_button.grid(row=4, column=1)
        root.mainloop()


class Rate:
    frame_list = []
    rate_list = []
    complaint = {}
    index = 0

    def __init__(self, master, store, username):
        self.store = store
        self.username = username
        self.pending_rating_path = os.path.join('Database', self.store, 'PendingRating.csv')
        self.menu_path = os.path.join('Database', self.store, 'Menu.csv')
        self.employee_path = os.path.join('Database', self.store, 'Employees.csv')
        self.master = master
        self.master.title('Feedback')
        self.upper_frame = Frame(self.master, height=100, width=500, bd=2, relief=SUNKEN)
        self.middle_frame = Frame(self.master, height=300, width=500, bd=2, relief=SUNKEN)
        self.lower_frame = Frame(self.master, height=100, width=500, bd=2, relief=SUNKEN)
        self.label = Label(self.upper_frame, text='Welcome Back.\n'
                                                  'Your feedback is very important for us.\n'
                                                  'We would love to hear from you.\n'
                                                  'Please leave us the rating from 1 to 5.\n'
                                                  'The default is 5.')
        self.quit_button = Button(self.lower_frame, text='Quit', command=self.quit_event)
        self.skip_button = Button(self.lower_frame, text='Skip', command=self.skip_event)
        # self.okay_button = Button(self.lower_frame, text='Okay')
        self.upper_frame.grid(row=0)
        self.upper_frame.grid_propagate(0)
        self.middle_frame.grid(row=1)
        self.middle_frame.grid_propagate(0)
        self.lower_frame.grid(row=2)
        self.lower_frame.grid_propagate(0)
        self.label.grid(row=0, column=0)
        self.quit_button.grid(row=0, column=0)
        self.skip_button.grid(row=0, column=1)
        self.init_middle()

    def ok_event(self, rate, obj, complaint):
        rate = rate.get()
        complaint = complaint.get()
        # print(rate)
        # print(complaint)
        self.rate_list.append(rate)
        if complaint != 'None':
            self.complaint[obj] = complaint
        for slave in self.middle_frame.grid_slaves():
            slave.grid_remove()
        self.index += 1
        if self.index >= len(self.frame_list):
            employee_list = pd.read_csv(self.employee_path, index_col=0)
            employee_username = pd.read_csv(self.employee_path)['Username']
            for user in employee_username:
                if employee_list.loc[user]['Identity'] == 'manager':
                    manager = user
            customer_list = pd.read_csv(self.pending_rating_path, index_col=1)
            delivery = customer_list.loc[self.username]['Delivery']
            times = float(employee_list.loc[manager]['one'])  # how many times has been rated
            cur_rating = float(employee_list.loc[manager]['avgRating'])
            new_avg = (times * cur_rating + float(self.rate_list[0])) / (times + 1)
            employee_list.loc[manager, 'one'] = times + 1
            employee_list.loc[manager, 'avgRating'] = new_avg
            # ---
            one = float(employee_list.loc[delivery]['two'])
            two = float(employee_list.loc[delivery]['three'])
            thr = float(self.rate_list[1])
            new_avg = (one + two + thr) / 3.0
            employee_list.loc[delivery, 'avgRating'] = new_avg
            employee_list.loc[delivery, 'one'] = one
            employee_list.loc[delivery, 'two'] = two
            employee_list.loc[delivery, 'three'] = thr
            employee_list.to_csv(self.employee_path)
            Manager.manager.DeliveryPunish(self.store) #TODO
            # -----------------------------------------
            i = 2
            pending_pizzas = customer_list.loc[self.username]['Order']
            l = len(pending_pizzas)
            p = pending_pizzas[1:l - 1]
            pending_pizzas = p.split(', ')
            for pizza in pending_pizzas:
                l = len(pizza) - 1
                pizza = pizza[1:l]
                menu = pd.read_csv(self.menu_path, index_col=0)
                one = float(menu.loc[pizza]['last2rating'])
                two = float(menu.loc[pizza]['last3rating'])
                thr = float(self.rate_list[i])
                new_avg = (one + two + thr) / 3.0
                menu.loc[pizza, 'last1rating'] = one
                menu.loc[pizza, 'last2rating'] = two
                menu.loc[pizza, 'last3rating'] = thr
                menu.loc[pizza, 'avgrating'] = new_avg
                menu.to_csv(self.menu_path)
                i += 1
            Manager.manager.DropPizza(self.store)  # this should check if there is any pizza to drop
            Manager.manager.layoffCook(self.store)  # this check any cook needed to be laid off
            # move complaint into complaint csv
            complaint_path = os.path.join('Database', self.store, 'Complaint.csv')
            numbers = pd.read_csv(complaint_path)['Num']
            latest_num = 0
            for number in numbers:
                latest_num = number
            for obj, comm in self.complaint.items():
                latest_num += 1
                data = [[latest_num, obj, comm]]
                df = pd.DataFrame(data, columns=['Num', 'Object', 'Comment'])
                with open(complaint_path, 'a') as complaint_csv:
                    df.to_csv(complaint_csv, index=False, header=False)
            pending_rating = pd.read_csv(self.pending_rating_path, index_col=[0, 1])
            num = pd.read_csv(self.pending_rating_path, index_col=1).loc[self.username]['OrderNum']
            # print(pending_rating.loc[num, self.username]['Order'])
            pending_rating.drop([(num, self.username)]).to_csv(self.pending_rating_path)
            # print(pending_rating['OrderNum'])
            self.master.destroy()
        else:
            self.frame_list[self.index].grid()

    def init_middle(self):
        employee_list = pd.read_csv(self.employee_path, index_col=0)
        employee_username = pd.read_csv(self.employee_path)['Username']
        for user in employee_username:
            if employee_list.loc[user]['Identity'] == 'manager':
                manager = user
        frame = Frame(self.middle_frame)
        label1 = Label(frame, text='Please give a rating to our store.\n'
                                   'what do you think about our store: ')
        comment1 = Label(frame, text='comment: ')
        entry1 = Entry(frame)
        entry1.insert(0, 5)
        comment_entry = Entry(frame)
        comment_entry.insert(0, 'None')
        label1.grid(row=0, column=0)
        comment1.grid(row=1, column=0)
        entry1.grid(row=0, column=1)
        comment_entry.grid(row=1, column=1)
        ok1 = Button(frame, text='Ok',
                     command=lambda r=entry1, o=manager, c=comment_entry: self.ok_event(r, o, c))
        ok1.grid(row=2, column=0, columnspan=2)
        self.frame_list.append(frame)
        # ---------------------------------
        customer_list = pd.read_csv(self.pending_rating_path, index_col=1)
        delivery = customer_list.loc[self.username]['Delivery']
        frame2 = Frame(self.middle_frame)
        label2 = Label(frame2, text='Please rate your last experience\n'
                                    ' with our delivery person: ')
        entry2 = Entry(frame2)
        entry2.insert(0, 5)
        comment2 = Label(frame2, text='comment: ')
        comment2_entry = Entry(frame2)
        comment2_entry.insert(0, 'None')
        label2.grid(row=0, column=0)
        entry2.grid(row=0, column=1)
        comment2.grid(row=1, column=0)
        comment2_entry.grid(row=1, column=1)
        ok2 = Button(frame2, text='Ok',
                     command=lambda r=entry2, o=delivery, c=comment2_entry: self.ok_event(r, o, c))
        ok2.grid(row=2, column=0, columnspan=2)
        self.frame_list.append(frame2)
        # ----------------------------------
        pending_pizzas = customer_list.loc[self.username]['Order']
        l = len(pending_pizzas)
        p = pending_pizzas[1:l-1]
        pending_pizzas = p.split(', ')
        for pizza in pending_pizzas:
            l = len(pizza) - 1
            pizza = pizza[1:l]
            frame_p = Frame(self.middle_frame)
            label_p = Label(frame_p, text='Please rate the taste of our pizza.\n'
                                          'For %s: ' % pizza)
            label_commentp = Label(frame_p, text='comment: ')
            entry_commentp = Entry(frame_p)
            entry_commentp.insert(0, 'None')
            entry_p = Entry(frame_p)
            entry_p.insert(0, 5)
            label_p.grid(row=0, column=0)
            entry_p.grid(row=0, column=1)
            label_commentp.grid(row=1, column=0)
            entry_commentp.grid(row=1, column=1)
            ok_p = Button(frame_p, text='Ok',
                          command=lambda r=entry_p, o=pizza, c=entry_commentp: self.ok_event(r, o, c))
            ok_p.grid(row=2, column=0, columnspan=2)
            self.frame_list.append(frame_p)
        # ----------------------------------
        self.frame_list[self.index].grid()

    def quit_event(self):
        if messagebox.askyesno('Quit', 'Are you sure you want to quit?'):
            self.master.quit()

    def skip_event(self):
        if messagebox.askyesno('Skip', 'Are you sure you want to skip?\n'
                                       'And by default the rest rating will be given 5.'):
            pass


# for testing
'''a = Tk()
b = Login(a, 'Brotherjohn')
a.mainloop()
print(b.username)
print(b.identity)'''
'''a = Tk()
b = Rate(a, 'Brotherjohn', 'hongjie')
a.mainloop()'''
