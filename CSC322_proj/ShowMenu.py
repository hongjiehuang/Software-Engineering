from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os.path
import pandas as pd


class ShowMenu:
    frame_list = []
    index = -1
    order = []
    cooklist = []

    def __init__(self, master, username, identity, store, start, end, prev_order=None):
        if prev_order is not None:
            self.order = prev_order
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
        # setting optionmenu
        path = os.path.join('Database', store, 'Menu.csv')
        complete_menu = pd.read_csv(path)['Cook']
        self.cheflist = {chef for chef in complete_menu}
        self.cooklist.append('All')
        for chef in self.cheflist:
            self.cooklist.append(chef)
        self.chef = StringVar()
        self.chef.set(self.cooklist[0])
        self.chefoption = OptionMenu(self.top_button_frame, self.chef, *self.cooklist)
        self.chefoption.grid(row=0, column=2)
        self.button_chef = Button(self.top_button_frame, text='Ok', command=self.ok_chef)
        self.button_chef.grid(row=0, column=3)

    def ok_chef(self):
        chef = self.chef.get()
        self.frame_list = []
        for slaves in self.display_frame.grid_slaves():
            slaves.destroy()
        self.index = -1
        if chef != 'All':
            self.initialize_based_chef(self.user, self.identity, self.store, chef)
        else:
            self.initialize_menu(self.user, self.identity, self.store)

    def initialize_based_chef(self, username, identity, store, chef):
        menu_path = os.path.join('Database', store, 'Menu.csv')
        complete_menu = pd.read_csv(menu_path, index_col=0)
        complete_pizza = pd.read_csv(menu_path)['Pizza']
        for pizza in complete_pizza:
            if complete_menu.loc[pizza]['Cook'] == chef:
                img_path = complete_menu.loc[pizza]['Source']
                img = ImageTk.PhotoImage(Image.open(img_path))
                pizza_frame = Frame(self.display_frame)
                pizza_pic = Label(pizza_frame, image=img)
                pizza_pic.image = img
                pizza_pic.grid(row=0, column=0, rowspan=4, sticky=W, padx=(0, 0))
                # ----------------------------------------
                pizza_name = Label(pizza_frame, text=pizza, width=40, anchor=W, justify=LEFT)
                price = complete_menu.loc[pizza]['Price']
                if identity == 'normal':
                    pizza_price = Label(pizza_frame, text='$ %s' % round(float(price) * 0.8, 1), width=40, anchor=W, justify=LEFT)
                elif identity == 'vip':
                    pizza_price = Label(pizza_frame, text='$ %s' % round(float(price) * 0.9, 1), width=40, anchor=W, justify=LEFT)
                else:
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
            #print(first)
            second = customer_order.loc[username]['Second']
            third = customer_order.loc[username]['Third']
            complete_pizza = pd.read_csv(menu_path).sort_values(by=['avgrating'], ascending=False)['Pizza']
            if first == 'holder' or second == 'holder' or third == 'holder':
                #print('hehre')
                first = complete_pizza[0]
                second = complete_pizza[1]
                third = complete_pizza[2]
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

    def cart_event(self):
        global status, shopping_cart
        status = 'cart'
        self.master.withdraw()
        shopping_cart = Toplevel(self.master)
        cart = Cart(shopping_cart, self.order, self.user, self.store, self.master, self.start, self.end)

    def logout_event(self):
        self.master.quit()


class Cart:
    frame_list = []
    status = ''
    testing = []  # keep a bunch of StringVar so those StringVar can be constantly be referenced and prevent GC

    def __init__(self, master, order, username, store, menu, start, end):
        self.start = start
        self.end = end
        self.menu = menu
        self.shopping_cart = master
        self.index = -1
        self.status = status
        self.order = order
        self.username = username
        self.store = store
        self.master = master
        self.master.title('Shopping Cart')
        self.up_frame = Frame(self.master, height=35, width=465, relief=SUNKEN, bd=2)
        self.display_frame = Frame(self.master, height=600, width=465)
        self.down_frame = Frame(self.master, height=35, width=465, relief=SUNKEN, bd=2)
        self.close_button = Button(self.up_frame, text='CLOSE', command=self.cancel_event)
        self.checkout_button = Button(self.up_frame, text='CHECK OUT', command=self.place_order_event)
        self.next_button = Button(self.down_frame, text='NEXT', command=self.next_event)
        self.prev_button = Button(self.down_frame, text='PREV', command=self.prev_event)
        self.close_button.grid(row=0, column=0)
        self.checkout_button.grid(row=0, column=1)
        self.next_button.grid(row=0, column=1)
        self.prev_button.grid(row=0, column=0)
        self.up_frame.grid(row=0, column=0)
        self.up_frame.grid_propagate(0)
        self.display_frame.grid(row=1, column=0)
        self.down_frame.grid(row=2, column=0)
        self.down_frame.grid_propagate(0)
        self.init_display()
        self.display_frame.grid_propagate(0)

    def init_display(self):
        path = os.path.join('Database', self.store, 'Menu.csv')
        complete_menu = pd.read_csv(path, index_col=0)
        for pizza in self.order:
            self.order_frame = Frame(self.display_frame, bd=1, relief=SUNKEN)
            img_path = complete_menu.loc[pizza]['Source']
            img = ImageTk.PhotoImage(Image.open(img_path))
            # img = ImageTk.PhotoImage(Image.open(img_path)))
            self.pizza_label = Label(self.order_frame, image=img)
            self.pizza_label.image = img
            self.pizza_label.grid(row=0, column=0, rowspan=3)
            # 3 group of radio button
            # first group
            size = IntVar()
            self.testing.append(size)  # This is to prevent GC to kick in
            size_label = Label(self.order_frame, text='SIZE: ').grid(row=0, column=1)
            Radiobutton(self.order_frame, text='small', variable=size, value=-2).grid(row=0, column=2)
            Radiobutton(self.order_frame, text='medium', variable=size, value=0).grid(row=0, column=3)
            Radiobutton(self.order_frame, text='large', variable=size, value=2).grid(row=0, column=4)
            size.set(0)
            # second group
            dough = IntVar()
            self.testing.append(dough)
            dough.set(0)
            dough_label = Label(self.order_frame, text='DOUGH: ').grid(row=1, column=1)
            Radiobutton(self.order_frame, text='normal', variable=dough, value=0).grid(row=1, column=2)
            Radiobutton(self.order_frame, text='crispy', variable=dough, value=1).grid(row=1, column=3)
            Radiobutton(self.order_frame, text='thicken', variable=dough, value=2).grid(row=1, column=4)
            # third group
            topping = IntVar()
            self.testing.append(topping)
            topping.set(0)
            topping_label = Label(self.order_frame, text='TOPPING: ').grid(row=2, column=1)
            Radiobutton(self.order_frame, text='normal', variable=topping, value=0).grid(row=2, column=2)
            Radiobutton(self.order_frame, text='extra', variable=topping, value=1).grid(row=2, column=3)
            Radiobutton(self.order_frame, text='flooded', variable=topping, value=3).grid(row=2, column=4)
            #  remove button
            self.remove_button = Button(self.order_frame, text='remove', command=lambda p=pizza: self.remove_event(p))
            # grid in everything
            self.remove_button.grid(row=1, column=5)
            self.frame_list.append(self.order_frame)
        # grid some of them into the displayframe
        for i in range(5):
            self.index += 1
            if self.index < len(self.order):
                self.frame_list[self.index].grid(row=i, column=0)
            else:
                self.index = len(self.order) - 1

    def remove_event(self, pizza):
        self.order.remove(pizza)
        # print(self.order)
        self.frame_list = []
        for slaves in self.display_frame.grid_slaves():
            slaves.destroy()
        self.index = -1
        self.init_display()

    def place_order_event(self):
        if len(self.order) == 0:
            self.master.quit()
        total = 0
        user_path = os.path.join('Database', self.store, 'Users.csv')
        complete_user = pd.read_csv(user_path, index_col=0)
        if self.username != 'visitor':
            if len(self.order) > 2:
                complete_user.loc[self.username, 'First'] = self.order[0]
                complete_user.loc[self.username, 'Second'] = self.order[1]
                complete_user.loc[self.username, 'Third'] = self.order[2]
                complete_user.to_csv(user_path)
            elif len(self.order) > 1:
                complete_user.loc[self.username, 'First'] = self.order[0]
                complete_user.loc[self.username, 'Second'] = self.order[1]
                complete_user.to_csv(user_path)
            elif len(self.order) == 1:
                complete_user.loc[self.username, 'First'] = self.order[0]
                complete_user.to_csv(user_path)
        for intvar in self.testing:
            total += int(intvar.get())
        menu_path = os.path.join('Database', self.store, 'Menu.csv')
        complete_menu = pd.read_csv(menu_path, index_col=0)
        for pizza in self.order:
            total += complete_menu.loc[pizza]['Price']
        if messagebox.askyesno('Confirm', 'The total is %s$' %total):
            path = os.path.join('Database', self.store, 'Orders.csv')
            complete_order = pd.read_csv(path)['key']
            key = 0
            for order in complete_order:
                key = order
            data = [[key + 1, self.username, str(self.start[0]), str(self.start[1]),
                     str(self.end[0]), str(self.end[1]), 'none', str(total), self.order]]
            df = pd.DataFrame(data, columns=['key', "Username", "Beginrow", "Begincol", "Endrow", "Endcol",
                                             "Delivery", "Total", "Order"])
            with open(path, 'a') as order_csv:
                df.to_csv(order_csv, index=False, header=False)
            messagebox.showinfo('Success', 'Thank you for placing the order.')
            self.master.quit()

    def cancel_event(self):
        if messagebox.askyesno('Verify', 'This will erase everything from shopping cart.\n'
                                         'Are you sure you want to quit? '):
            '''self.order = []
            self.shopping_cart.withdraw()
            self.menu.deiconify()
            self.index = -1'''
            self.master.quit()

    def next_event(self):  # TODO need to be modified
        if self.index + 1 == len(self.frame_list):
            messagebox.showinfo('Info', 'You have reach the last page.')
        else:
            for slave in self.display_frame.grid_slaves():
                slave.grid_forget()
            for i in range(5):
                self.index += 1
                if self.index < len(self.frame_list):
                    self.frame_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.frame_list) - 1

    def prev_event(self):  # TODO need to be modified
        if self.index - 5 <= -1:
            messagebox.showinfo('Info', 'This is the first page.')
        else:
            for slave in self.display_frame.grid_slaves():
                slave.grid_forget()
                self.index -= 1
            self.index -= 5
            for i in range(5):
                self.index += 1
                if self.index < len(self.frame_list):
                    self.frame_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.frame_list) - 1


a = Tk()
c = ShowMenu(a, 'alan', 'visitor', 'Brotherjohn', [7,2], [3,6])
a.mainloop()
'''while status == 'cart' or status == 'showmenu':
    print(status)
    if status == 'cart':
        show_cart(order, 'alan', 'Brotherjohn')
    else:
        show_menu('alan', 'visitor', 'Brotherjohn', order)'''
