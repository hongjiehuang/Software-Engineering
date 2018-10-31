from tkinter import *
from tkinter import messagebox
import pandas as pd
import os.path
from PIL import Image, ImageTk


class Chef:
    frame_list = []

    def __init__(self, master, store, username):
        self.index = -1
        self.username = username
        self.store = store
        self.master = master
        self.master.title('Menu')
        self.top_frame = Frame(self.master, height=45, width=595, bd=2, relief=SUNKEN)
        self.middle_frame = Frame(self.master, height=370, width=595, bd=2, relief=SUNKEN)
        self.bottom_frame = Frame(self.master, height=45, width=595, bd=2, relief=SUNKEN)
        self.init_menu()
        self.menu_label = Label(self.top_frame, text='MENU')
        self.add_button = Button(self.top_frame, text='Add', command=self.add_event)
        self.prev_button = Button(self.bottom_frame, text='Prev', command=self.prev_event)
        self.next_button = Button(self.bottom_frame, text='Next', command=self.next_event)
        self.top_frame.grid(row=0, column=0)
        self.middle_frame.grid(row=1)
        self.bottom_frame.grid(row=2)
        self.top_frame.grid_propagate(0)
        self.bottom_frame.grid_propagate(0)
        self.middle_frame.grid_propagate(0)
        self.menu_label.grid(row=0, column=0)
        self.add_button.grid(row=0, column=1)
        self.prev_button.grid(row=0, column=0)
        self.next_button.grid(row=0, column=1)

    def init_menu(self):
        menu_path = os.path.join('Database', self.store, 'Menu.csv')
        complete_menu = pd.read_csv(menu_path, index_col=0)
        complete_pizza = pd.read_csv(menu_path)['Pizza']
        for pizza in complete_pizza:
            chef = complete_menu.loc[pizza]['Cook']
            if chef == self.username:
                img_path = complete_menu.loc[pizza]['Source']
                img = ImageTk.PhotoImage(Image.open(img_path))
                pizza_frame = Frame(self.middle_frame, bd=2, relief=SUNKEN)
                pizza_pic = Label(pizza_frame, image=img)
                pizza_pic.image = img
                pizza_pic.grid(row=0, column=0, rowspan=4, sticky=W, padx=(0, 0))
                # ----------------------------------------
                pizza_name = Label(pizza_frame, text=pizza, width=40, anchor=W, justify=LEFT)
                price = complete_menu.loc[pizza]['Price']
                pizza_price = Label(pizza_frame, text='$ %s' % price, width=40, anchor=W, justify=LEFT)
                rating = complete_menu.loc[pizza]['avgrating']
                rating = round(float(rating), 1)
                pizza_rating = Label(pizza_frame, text=rating, width=40, anchor=W, justify=LEFT)
                ingredients = complete_menu.loc[pizza]['Ingredients']
                pizza_ingredient = Label(pizza_frame, text=ingredients, width=40, anchor=W, justify=LEFT)
                name_label = Label(pizza_frame, text='Name: ', width=12)
                price_label = Label(pizza_frame, text='Price: ', width=12)
                rating_label = Label(pizza_frame, text='Rating: ', width=12)
                ingredient_label = Label(pizza_frame, text='Ingredients: ', width=12)
                name_label.grid(row=0, column=1)
                price_label.grid(row=1, column=1)
                rating_label.grid(row=2, column=1)
                ingredient_label.grid(row=3, column=1)
                pizza_name.grid(row=0, column=2)
                pizza_price.grid(row=1, column=2)
                pizza_rating.grid(row=2, column=2)
                pizza_ingredient.grid(row=3, column=2)
                remove_button = Button(pizza_frame, text='Remove', width=10, height=3,
                                       command=lambda p=pizza: self.remove_event(p))
                remove_button.grid(row=0, column=3, rowspan=2)
                modify_button = Button(pizza_frame, text='Modify', width=10, height=3,
                                       command=lambda p=pizza: self.modify_event(p))
                modify_button.grid(row=2, column=3, rowspan=2)
                self.frame_list.append(pizza_frame)
        self.index += 1
        self.frame_list[self.index].grid(row=0, column=0)
        self.index += 1
        self.frame_list[self.index].grid(row=1, column=0)
        self.index += 1
        self.frame_list[self.index].grid(row=2, column=0)

    def remove_event(self, pizza):
        menu_path = os.path.join('Database', self.store, 'Menu.csv')
        complete_menu = pd.read_csv(menu_path, index_col=0)
        complete_pizza = pd.read_csv(menu_path)['Pizza']
        temp = []
        for pizzas in complete_pizza:
            if pizzas != pizza:
                temp.append(pizzas)
        complete_menu.drop([pizza]).to_csv(menu_path, index_label=['Pizza'])
        self.frame_list = []
        for slaves in self.middle_frame.grid_slaves():
            slaves.destroy()
        self.index = -1
        self.init_menu()

    def modify_event(self, pizza):
        def okay_event():
            name = pizza
            price = price_entry.get()
            ingredient = ingredient_entry.get()
            menu_path = os.path.join('Database', self.store, 'Menu.csv')
            complete_menu = pd.read_csv(menu_path, index_col=0)
            complete_menu.loc[name, 'Price'] = price
            complete_menu.loc[name, 'Ingredients'] = ingredient
            complete_menu.to_csv(menu_path)
            #print(complete_menu)
            root.destroy()
            self.frame_list = []
            for slaves in self.middle_frame.grid_slaves():
                slaves.destroy()
            self.index = -1
            self.init_menu()
        root = Tk()
        root.title('Modify')
        mainframe = Frame(root)
        instruction_label = Label(mainframe, text='Please fill in the information to modify the pizza. ')
        instruction_label.grid(row=0, column=0, columnspan=2)
        name_label = Label(mainframe, text='Name: ')
        name_label.grid(row=1, column=0)
        price_label = Label(mainframe, text='Price: ')
        price_label.grid(row=2, column=0)
        ingredient_label = Label(mainframe, text='Ingredients: ')
        ingredient_label.grid(row=3, column=0)
        name_label2 = Label(mainframe, text=pizza)
        name_label2.grid(row=1, column=1)
        price_entry = Entry(mainframe)
        price_entry.grid(row=2, column=1)
        ingredient_entry = Entry(mainframe)
        ingredient_entry.grid(row=3, column=1)
        # initialize the entry button with the original entry
        menu_path = os.path.join('Database', self.store, 'Menu.csv')
        complete_menu = pd.read_csv(menu_path, index_col=0)
        name = pizza
        price = complete_menu.loc[pizza]['Price']
        ingredient = complete_menu.loc[pizza]['Ingredients']
        price_entry.delete(0, END)
        ingredient_entry.delete(0, END)
        price_entry.insert(0, price)
        ingredient_entry.insert(0, ingredient)
        # --------------------------------------------
        ok_button = Button(mainframe, text='Okay',
                           command=okay_event)
        ok_button.grid(row=4, column=0)
        cancel_button = Button(mainframe, text='Cancel', command=root.destroy)
        cancel_button.grid(row=4, column=1)
        mainframe.grid()

    def add_event(self):
        def ok():
            img = img_entry.get()
            if img == 'None':
                img = 'Database/images/default.png'
            data = [[name_entry.get(), img, price_entry.get(), self.username, 'N/A', 'N/A', 'N/A', 'N/A',
                     ingredient_entry.get()]]
            df = pd.DataFrame(data, columns=['Pizza', 'Source', 'Price', 'Cook', 'last1rating', 'last2rating',
                                             'last3rating','avgrating','Ingredients'])
            path = os.path.join('Database', self.store, 'Menu.csv')
            with open(path, 'a') as menu_csv:
                df.to_csv(menu_csv, index=False, header=False)
            messagebox.showinfo('Add', 'Done.')
            root.destroy()
            self.frame_list = []
            for slaves in self.middle_frame.grid_slaves():
                slaves.destroy()
            self.index = -1
            self.init_menu()
        root = Tk()
        root.title('Add Pizza')
        mainframe = Frame(root)
        instruction_label = Label(mainframe, text='Please fill in the information to add the pizza. ')
        instruction_label.grid(row=0, column=0, columnspan=2)
        name_label = Label(mainframe, text='Name: ').grid(row=1, column=0)
        price_label = Label(mainframe, text='Price: ').grid(row=2, column=0)
        ingredient_label = Label(mainframe, text='Ingredients: ').grid(row=3, column=0)
        img_label = Label(mainframe, text='Image Source: ').grid(row=4, column=0)
        ok_button = Button(mainframe, text='ok', command=ok)
        cancel_button = Button(mainframe, text='cancel', command=root.destroy)
        ok_button.grid(row=5, column=0)
        cancel_button.grid(row=5, column=1)
        name_entry = Entry(mainframe)
        name_entry.grid(row=1, column=1)
        price_entry = Entry(mainframe)
        price_entry.grid(row=2, column=1)
        ingredient_entry = Entry(mainframe)
        ingredient_entry.grid(row=3, column=1)
        img_entry = Entry(mainframe)
        img_entry.grid(row=4, column=1)
        img_entry.insert(0, "None")
        mainframe.grid()

    def prev_event(self):
        if self.index - 3 <= -1:
            messagebox.showinfo('Info', 'This is the first page.')
        else:
            for slave in self.middle_frame.grid_slaves():
                slave.grid_forget()
                self.index -= 1
            self.index -= 3
            for i in range(3):
                self.index += 1
                if self.index < len(self.frame_list):
                    self.frame_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.frame_list) - 1

    def next_event(self):
        if self.index + 1 == len(self.frame_list):
            messagebox.showinfo('Info', 'You have reach the last page.')
        else:
            for slave in self.middle_frame.grid_slaves():
                slave.grid_forget()
            for i in range(3):
                self.index += 1
                if self.index < len(self.frame_list):
                    self.frame_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.frame_list) - 1
