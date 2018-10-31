from tkinter import *
from tkinter import messagebox
import pandas as pd


class PickLocation:
    store_st = None
    store_ave = None
    start_st = None
    start_ave = None
    pizza_store = None
    employee = False

    def __init__(self, master):
        self.master = master
        self.master.title("Map")
        self.master.resizable(False, False)
        self.instruction_frame = Frame(self.master, height=100, width=700, relief='sunken', bd=3)
        self.instruction_frame.grid(row=0, column=0)
        self.instruction_frame.grid_propagate(False)
        self.left_frame = Frame(self.master, height=500, width=700, relief='sunken', bd=3)
        self.left_frame.grid(row=1, column=0)
        self.left_frame.grid_propagate(False)
        self.right_frame = Frame(self.master, height=600, width=300, relief='sunken', bd=3)
        self.right_frame.grid(row=0, column=1, rowspan=2)
        self.right_frame.grid_propagate(False)
        self.pick_start_label = Label(self.instruction_frame, font=('Times', 18, 'bold'),
                                      text='Please pick a starting location,\n'
                                           'then click okay,\n'
                                           'otherwise please manually enter the address.')
        self.pick_start_label.grid(row=0, column=0, ipadx=120)
        for i in range(10):
            for j in range(10):
                self.button = Button(self.left_frame, text='%sth ave\n%sth st' % (j + 1, i + 1),
                                     command=lambda ave=j, st=i: self.address_event(ave + 1, st + 1))
                self.button.grid(row=i + 3, column=j, ipadx=10, ipady=4)
        self.row_entry = Entry(self.right_frame)
        self.column_entry = Entry(self.right_frame)
        self.row_entry.grid(row=0, column=1, pady=(100, 10))
        self.column_entry.grid(row=1, column=1, pady=(0, 20))
        self.street_label = Label(self.right_frame, text='Street: ', font=('Times', 13, 'bold'))
        self.avenue_label = Label(self.right_frame, text='Avenue: ', font=('Times', 13, 'bold'))
        self.street_label.grid(row=0, column=0, ipadx=45, pady=(100, 10))
        self.avenue_label.grid(row=1, column=0, ipadx=45, pady=(0, 20))
        self.ok_button = Button(self.right_frame, text='OKAY', font=('Times', 13, 'bold'), command=self.okay_event)
        self.quit_button = Button(self.right_frame, text='QUIT', font=('Times', 13, 'bold'), command=quit)
        self.employer_login_button = Button(self.right_frame, text='Employee log in', font=('Times', 13, 'bold'),
                                            command=self.employee_login_event)
        self.ok_button.grid(row=2, column=0, columnspan=2, ipadx=44, pady=(30, 10))
        self.quit_button.grid(row=3, column=0, columnspan=2, ipadx=47, pady=(0, 20))
        self.employer_login_button.grid(row=4, column=0, columnspan=2, ipadx=8)

    def address_event(self, ave, st):
        self.row_entry.delete(0, 'end')
        self.column_entry.delete(0, 'end')
        self.row_entry.insert(0, st)
        self.column_entry.insert(0, ave)
        self.start_ave = ave
        self.start_st = st

    def my_sort(self, store_location):
        answer = []
        for i in range(3):
            my_min = store_location[0]
            for store in store_location:
                my_min_distance = (int(my_min[0]) - int(self.row_entry.get())) ** 2 + \
                                  (my_min[1] - int(self.column_entry.get())) ** 2
                cur_distance = (int(store[0]) - int(self.row_entry.get())) ** 2 + \
                               (store[1] - int(self.column_entry.get())) ** 2
                if cur_distance < my_min_distance:
                    my_min = store
            answer.append(my_min)
            store_location.remove(my_min)
        return answer

    def okay_event(self):
        self.pick_start_label.config(text='Now please pick a pizza store,')
        pizza_store_list = pd.read_csv('Database/PizzaStores.csv')
        pizza_store_name_list = pizza_store_list['Name']
        pizza_store_list = pd.read_csv('Database/PizzaStores.csv', index_col=3)
        temp = []
        for store_name in pizza_store_name_list:
            x = pizza_store_list.loc[store_name]['Row']
            y = pizza_store_list.loc[store_name]['Column']
            temp.append([x, y])
        try:
            temp = self.my_sort(temp)
            # print(temp)
        except:
            messagebox.showerror("Error", "Invalid input")
            return
        for w in self.left_frame.grid_slaves():
            w.grid_forget()
        for i in range(10):
            for j in range(10):
                if [i, j] in temp:
                    self.button = Button(self.left_frame, text='%sth ave\n%sth st' % (j + 1, i + 1),
                                         command=lambda ave=j, st=i: self.store_event(ave, st),
                                         bg='cyan')
                    self.button.grid(row=i + 3, column=j, ipadx=10, ipady=4)
                else:
                    self.button = Button(self.left_frame, text='%sth ave\n%sth st' % (j + 1, i + 1))
                                         # ''',command=lambda ave=j, st=i: self.address_event(ave + 1, st + 1))'''
                    self.button.grid(row=i + 3, column=j, ipadx=10, ipady=4)

    def store_event(self, store_ave, store_st):
        pizza_store_list = pd.read_csv('Database/PizzaStores.csv')
        self.store_ave = store_ave
        self.store_st = store_st
        store = pizza_store_list[(pizza_store_list['Row'] == store_st) & (pizza_store_list['Column'] == store_ave)]
        self.pizza_store = store.iloc[0, 3]
        # self.pizza_store = store
        self.master.destroy()

    def employee_login_event(self):
        self.employee = True
        self.pick_start_label.config(text='Please pick your pizza store,')
        pizza_store_list = pd.read_csv('Database/PizzaStores.csv')
        pizza_store_name_list = pizza_store_list['Name']
        pizza_store_list = pd.read_csv('Database/PizzaStores.csv', index_col=3)
        temp = []
        for store_name in pizza_store_name_list:
            x = pizza_store_list.loc[store_name]['Row']
            y = pizza_store_list.loc[store_name]['Column']
            temp.append([x, y])
        for w in self.left_frame.grid_slaves():
            w.grid_forget()
        for i in range(10):
            for j in range(10):
                if [i, j] in temp:
                    self.button = Button(self.left_frame, text='%sth ave\n%sth st' % (j + 1, i + 1),
                                         command=lambda ave=j, st=i: self.store_event(ave, st),
                                         bg='cyan')
                    self.button.grid(row=i + 3, column=j, ipadx=10, ipady=4)
                else:
                    self.button = Button(self.left_frame, text='%sth ave\n%sth st' % (j + 1, i + 1))
                    self.button.grid(row=i + 3, column=j, ipadx=10, ipady=4)


'''a = Tk()
b = PickLocation(a)
a.mainloop()
print("starting point:")
print(b.start_ave, " ave, ", b.start_st, "st")
print("pizza store's location")
print(b.store_ave + 1, " ave, ", b.store_st + 1, "st")
print()
print(b.pizza_store)'''
