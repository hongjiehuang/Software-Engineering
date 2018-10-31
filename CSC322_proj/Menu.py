from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os.path
import pandas as pd


class ShowMenu:
    frame_list = []
    frame_list1= []
    index = -1
    index1 = -1
    order = []
    testing = []

    def __init__(self, master, username, identity, store, start, end):
        self.start = start
        self.end = end
        self.user = username
        self.identity = identity
        self.store = store
        self.master = master
        self.master.title('Menu')
        self.top_frame = Frame(self.master, relief=SUNKEN, bd=5, height=100, width=600)
        self.top_button_frame = Frame(self.master, relief=SUNKEN, bd=5, height=40, width=600)
        self.bottom_button_frame = Frame(self.master, relief=SUNKEN, bd=5, height=40, width=600)
        self.display_frame = Frame(self.master, relief=SUNKEN, bd=5, height=360, width=600)
        self.log_out_button = Button(self.top_button_frame, text='Log Out', command=self.logout_event)
        self.cart_button = Button(self.top_button_frame, text='Cart', command=self.cart_event)
        self.next_button = Button(self.bottom_button_frame, text='Next', command=self.next_event)
        self.prev_button = Button(self.bottom_button_frame, text='Back', command=self.prev_event)
        self.top_frame.grid(row=0, column=0)
        self.top_button_frame.grid(row=1, column=0)
        self.display_frame.grid(row=2, column=0)
        self.bottom_button_frame.grid(row=3, column=0)
        # self.top_frame.grid_propagate(0)
        self.top_button_frame.grid_propagate(0)
        self.initialize_menu(username, identity, store)
        self.display_frame.grid_propagate(0)
        self.bottom_button_frame.grid_propagate(0)
        logo_path = os.path.join('Database', store, 'logo.png')
        img = ImageTk.PhotoImage(Image.open(logo_path))
        image_label = Label(self.top_frame, image=img)
        image_label.image = img
        image_label.grid(row=0, column=0)
        # now grid in the button
        self.log_out_button.grid(row=0, column=0)
        self.cart_button.grid(row=0, column=1)
        self.prev_button.grid(row=0, column=0)
        self.next_button.grid(row=0, column=1)

    def initialize_menu(self, username, identity, store):
        self.frame_list = []
        menu_path = os.path.join('Database', store, 'Menu.csv')
        if identity == 'visitor':
            complete_menu = pd.read_csv(menu_path, index_col=0)
            complete_pizza = pd.read_csv(menu_path).sort_values(by=['avgrating'], ascending=False)['Pizza']
            for pizza in complete_pizza:
                img_path = complete_menu.loc[pizza]['Source']
                img = ImageTk.PhotoImage(Image.open(img_path))
                pizza_frame = Frame(self.display_frame)
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
                add_button = Button(pizza_frame, text='Add', width=10, height=7,
                                    command=lambda p=pizza: self.add_event(p))
                add_button.grid(row=0, column=3, rowspan=4)
                self.frame_list.append(pizza_frame)
        else:
            path = os.path.join('Database', store, 'Users.csv')
            customer_order = pd.read_csv(path, index_col=0)
            first = customer_order.loc[username]['First']
            second = customer_order.loc[username]['Second']
            third = customer_order.loc[username]['Third']
            complete_menu = pd.read_csv(menu_path, index_col=0)
            complete_pizza = pd.read_csv(menu_path)['Pizza']
            # 1
            img_path = complete_menu.loc[first]['Source']
            img = ImageTk.PhotoImage(Image.open(img_path))
            pizza_frame = Frame(self.display_frame)
            pizza_pic = Label(pizza_frame, image=img)
            pizza_pic.image = img
            pizza_pic.grid(row=0, column=0, rowspan=4, sticky=W, padx=(0, 0))
            # ---
            pizza_name = Label(pizza_frame, text=first, width=40, anchor=W, justify=LEFT)
            price = complete_menu.loc[first]['Price']
            if identity == 'vip':
                price = round(float(price) * 0.8, 1)
            else:
                price = round(float(price) * 0.9, 1)
            pizza_price = Label(pizza_frame, text='$ %s' % price, width=40, anchor=W, justify=LEFT)
            rating = complete_menu.loc[first]['avgrating']
            rating = round(float(rating), 1)
            pizza_rating = Label(pizza_frame, text=rating, width=40, anchor=W, justify=LEFT)
            ingredients = complete_menu.loc[first]['Ingredients']
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
            add_button = Button(pizza_frame, text='Add', width=10, height=7,
                                command=lambda p=first: self.add_event(p))
            add_button.grid(row=0, column=3, rowspan=4)
            self.frame_list.append(pizza_frame)
            # 2
            img_path = complete_menu.loc[second]['Source']
            img = ImageTk.PhotoImage(Image.open(img_path))
            pizza_frame = Frame(self.display_frame)
            pizza_pic = Label(pizza_frame, image=img)
            pizza_pic.image = img
            pizza_pic.grid(row=0, column=0, rowspan=4, sticky=W, padx=(0, 0))
            # ---
            pizza_name = Label(pizza_frame, text=second, width=40, anchor=W, justify=LEFT)
            price = complete_menu.loc[second]['Price']
            if identity == 'vip':
                price = round(float(price) * 0.8, 1)
            else:
                price = round(float(price) * 0.9, 1)
            pizza_price = Label(pizza_frame, text='$ %s' % price, width=40, anchor=W, justify=LEFT)
            rating = complete_menu.loc[second]['avgrating']
            rating = round(float(rating), 1)
            pizza_rating = Label(pizza_frame, text=rating, width=40, anchor=W, justify=LEFT)
            ingredients = complete_menu.loc[second]['Ingredients']
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
            add_button = Button(pizza_frame, text='Add', width=10, height=7,
                                command=lambda p=second: self.add_event(p))
            add_button.grid(row=0, column=3, rowspan=4)
            self.frame_list.append(pizza_frame)
            # 3
            img_path = complete_menu.loc[third]['Source']
            img = ImageTk.PhotoImage(Image.open(img_path))
            pizza_frame = Frame(self.display_frame)
            pizza_pic = Label(pizza_frame, image=img)
            pizza_pic.image = img
            pizza_pic.grid(row=0, column=0, rowspan=4, sticky=W, padx=(0, 0))
            # ---
            pizza_name = Label(pizza_frame, text=third, width=40, anchor=W, justify=LEFT)
            price = complete_menu.loc[third]['Price']
            if identity == 'vip':
                price = round(float(price) * 0.8, 1)
            else:
                price = round(float(price) * 0.9, 1)
            pizza_price = Label(pizza_frame, text='$ %s' % price, width=40, anchor=W, justify=LEFT)
            rating = complete_menu.loc[third]['avgrating']
            rating = round(float(rating), 1)
            pizza_rating = Label(pizza_frame, text=rating, width=40, anchor=W, justify=LEFT)
            ingredients = complete_menu.loc[third]['Ingredients']
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
            add_button = Button(pizza_frame, text='Add', width=10, height=7,
                                command=lambda p=third: self.add_event(p))
            add_button.grid(row=0, column=3, rowspan=4)
            self.frame_list.append(pizza_frame)
            for pizza in complete_pizza:
                if pizza != first and pizza != second and pizza != third:
                    img_path = complete_menu.loc[pizza]['Source']
                    img = ImageTk.PhotoImage(Image.open(img_path))
                    pizza_frame = Frame(self.display_frame)
                    pizza_pic = Label(pizza_frame, image=img)
                    pizza_pic.image = img
                    pizza_pic.grid(row=0, column=0, rowspan=4, sticky=W, padx=(0, 0))
                    # ------------------------
                    pizza_name = Label(pizza_frame, text=pizza, width=40, anchor=W, justify=LEFT)
                    price = complete_menu.loc[pizza]['Price']
                    if identity == 'vip':
                        price = round(float(price) * 0.8, 1)
                    else:
                        price = round(float(price) * 0.9, 1)
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
                    add_button = Button(pizza_frame, text='Add', width=10, height=7,
                                        command=lambda p=pizza: self.add_event(p))
                    add_button.grid(row=0, column=3, rowspan=4)
                    self.frame_list.append(pizza_frame)
        self.index += 1
        self.frame_list[self.index].grid(row=0, column=0)
        self.index += 1
        self.frame_list[self.index].grid(row=1, column=0)
        self.index += 1
        self.frame_list[self.index].grid(row=2, column=0)

    def next_event(self):
        if self.index + 1 == len(self.frame_list):
            messagebox.showinfo('Info', 'You have reach the last page.')
        else:
            for slave in self.display_frame.grid_slaves():
                slave.grid_forget()
            for i in range(3):
                self.index += 1
                if self.index < len(self.frame_list):
                    self.frame_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.frame_list) - 1

    def prev_event(self):
        if self.index - 3 <= -1:
            messagebox.showinfo('Info', 'This is the first page.')
        else:
            for slave in self.display_frame.grid_slaves():
                slave.grid_forget()
                self.index -= 1
            self.index -= 3
            for i in range(3):
                self.index += 1
                if self.index < len(self.frame_list):
                    self.frame_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.frame_list) - 1

    def add_event(self, pizza):
        self.order.append(pizza)

    def logout_event(self):
        global status
        status = 'logout'
        self.master.destroy()

    def cart_event(self):
        order = self.order
        print(order)
        frame_list1 = self.frame_list1
        username = self.user
        start = self.start
        end = self.end
        testing = self.testing
        index1 = -1

        def remove_event(pizza):
            order.remove(pizza)
            frame_list1 = []
            for slaves in display_frame.grid_slaves():
                slaves.destroy()
            index1 = -1
            init_display(index1)

        def init_display(index1):
            print(order)
            testing = []
            testingpic = []
            path = os.path.join('Database', self.store, 'Menu.csv')
            complete_menu = pd.read_csv(path, index_col=0)
            for pizza in order:
                order_frame = Frame(display_frame, bd=1, relief=SUNKEN)
                img_path = complete_menu.loc[pizza]['Source']
                img = ImageTk.PhotoImage(Image.open(img_path))
                testingpic.append(img)
                # img = ImageTk.PhotoImage(Image.open(img_path)))
                pizza_label = Label(order_frame, image=img)
                pizza_label.image = img
                pizza_label.grid(row=0, column=0, rowspan=3)
                # 3 group of radio button
                # first group
                size = IntVar()
                testing.append(size) #  This is to prevent GC to kick in
                size_label = Label(order_frame, text='SIZE: ')
                size_label.grid(row=0, column=1)
                Radiobutton(order_frame, text='small', variable=size, value=-2).grid(row=0, column=2)
                Radiobutton(order_frame, text='medium', variable=size, value=0).grid(row=0, column=3)
                Radiobutton(order_frame, text='large', variable=size, value=2).grid(row=0, column=4)
                size.set(0)
                # second group
                dough = IntVar()
                testing.append(dough)
                dough.set(0)
                dough_label = Label(order_frame, text='DOUGH: ').grid(row=1, column=1)
                Radiobutton(order_frame, text='normal', variable=dough, value=0).grid(row=1, column=2)
                Radiobutton(order_frame, text='crispy', variable=dough, value=1).grid(row=1, column=3)
                Radiobutton(order_frame, text='thicken', variable=dough, value=2).grid(row=1, column=4)
                # third group
                topping = IntVar()
                testing.append(topping)
                topping.set(0)
                topping_label = Label(order_frame, text='TOPPING: ').grid(row=2, column=1)
                Radiobutton(order_frame, text='normal', variable=topping, value=0).grid(row=2, column=2)
                Radiobutton(order_frame, text='extra', variable=topping, value=1).grid(row=2, column=3)
                Radiobutton(order_frame, text='flooded', variable=topping, value=3).grid(row=2, column=4)
                #  remove button
                remove_button = Button(order_frame, text='remove', command=lambda p=pizza: remove_event(p))
                # grid in everything
                remove_button.grid(row=1, column=5)
                frame_list1.append(order_frame)
            # grid some of them into the displayframe
            for i in range(5):
                index1 += 1
                if index1 < len(order):
                    frame_list1[index1].grid(row=i, column=0)
                else:
                    index1 = len(order) - 1

        def place_order_event():  # TODO need to work on this
            total = 0
            for intvar in testing:
                total += int(intvar.get())
            data = [[username, str(start[0]), str(start[1]),
                     str(end[0]), str(end[1]), 'none', str(total)]]
            df = pd.DataFrame(data,
                              columns=["Username", "Beginrow", "Begincol", "Endrow", "Endcol", "Delivery", "Total"])
            path = os.path.join('Database', self.store, 'Orders.csv')
            with open(path, 'a') as order_csv:
                df.to_csv(order_csv, index=False, header=False)
            messagebox.showinfo('Success', 'Thank you for placing the order.')
            root.quit()

        def cancel_event():
            root.destroy()

        def next_event():  # TODO need to be modified
            if index1 + 1 == len(frame_list1):
                messagebox.showinfo('Info', 'You have reach the last page.')
            else:
                for slave in display_frame.grid_slaves():
                    slave.grid_forget()
                for i in range(5):
                    index1 += 1
                    if index1 < len(frame_list1):
                        frame_list1[index1].grid(row=i, column=0)
                    else:
                        index1 = len(frame_list1) - 1

        def prev_event():  # TODO need to be modified
            if index1 - 5 <= -1:
                messagebox.showinfo('Info', 'This is the first page.')
            else:
                for slave in display_frame.grid_slaves():
                    slave.grid_forget()
                    index1 -= 1
                index1 -= 5
                for i in range(5):
                    index1 += 1
                    if index1 < len(frame_list1):
                        frame_list1[index1].grid(row=i, column=0)
                    else:
                        index1 = len(frame_list1) - 1

        root = Tk()
        root.title('Shopping Cart')
        up_frame = Frame(root, height=35, width=465, relief=SUNKEN, bd=2)
        display_frame = Frame(root, height=600, width=465)
        down_frame = Frame(root, height=35, width=465, relief=SUNKEN, bd=2)
        close_button = Button(up_frame, text='CLOSE', command=cancel_event)
        checkout_button = Button(up_frame, text='CHECK OUT', command=place_order_event)
        next_button = Button(down_frame, text='NEXT', command=next_event)
        prev_button = Button(down_frame, text='PREV', command=prev_event)
        close_button.grid(row=0, column=0)
        checkout_button.grid(row=0, column=1)
        next_button.grid(row=0, column=1)
        prev_button.grid(row=0, column=0)
        up_frame.grid(row=0, column=0)
        up_frame.grid_propagate(0)
        display_frame.grid(row=1, column=0)
        down_frame.grid(row=2, column=0)
        down_frame.grid_propagate(0)
        init_display(index1)
        display_frame.grid_propagate(0)
        root.mainloop()
        self.frame_list1 = []


a = Tk()
c = ShowMenu(a, 'alan', 'visitor', 'Brotherjohn', [7,2], [3,6])
a.mainloop()
