import EmployeeLogin, Login, Map, ShowMenu, ChefA, Manager, Delivery
from tkinter import *
import os.path
import pandas as pd

def main():
    map_tk = Tk()
    map = Map.PickLocation(map_tk)
    map_tk.mainloop()
    menu_path = os.path.join('Database', map.pizza_store, 'Menu.csv')
    complete_menu = pd.read_csv(menu_path, index_col=0)
    if map.employee:
        employee_tk = Tk()
        employee = EmployeeLogin.EmployeeLogin(employee_tk, map.pizza_store)
        employee_tk.mainloop()
        position = employee.identity
        # print(position)
        if position == 'manager':
             root = Tk()
             b = Manager.manager(root, map.pizza_store)
             root.mainloop()
        elif position == 'chef':
            chef_tk = Tk()
            chef = ChefA.Chef(chef_tk, map.pizza_store, employee.username)
            chef_tk.mainloop()
        elif position == 'delivery':
            deliver_tk = Tk()
            deliver = Delivery.Delivery(deliver_tk, employee.username, map.pizza_store)
            deliver_tk.mainloop()
    else:
        customer_tk = Tk()
        customer = Login.Login(customer_tk, map.pizza_store)
        customer_tk.mainloop()
        pending_rating_path = os.path.join('Database', map.pizza_store, 'PendingRating.csv')
        pending_rating = pd.read_csv(pending_rating_path)['Username']
        '''if customer.username in pending_rating:
            rate_tk = Tk()
            rate = Login.Rate(rate_tk, map.pizza_store, customer.username)
            rate_tk.mainloop()'''
        # print([map.store_st, map.store_ave])  # this is the location of the store with row and col
                                              # row = st and col = ave.
                                              # the coordinate is 0 index based instead of 1
        # print([map.start_st - 1, map.start_ave - 1])  # minus one bcos the 0 index based
        # After login customer will rate the pizza, so here we call the
        # Use loop to check the average rating of pizza
        # Then chcek the rating of delivery
        show_menu_tk = Tk()
        show_menu = ShowMenu.ShowMenu(show_menu_tk, customer.username, customer.identity, map.pizza_store,
                                      [map.store_st, map.store_ave], [map.start_st - 1, map.start_ave - 1])
        show_menu_tk.mainloop()


main()
