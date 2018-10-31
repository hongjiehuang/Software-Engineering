from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
import os.path
import time
import Manager


class Delivery:
    # 50% the road will be smooth
    # 30% the road will be busy
    # 20% the road will be closed

    # overall layout
    # ----------------------------------------------
    # |                               |             |
    # |                               |  info_frame |
    # |                               |             |
    # |                               |-------------
    # |                               |             |
    # |          map_frame            |             |
    # |                               | order_frame |
    # |                               |-------------|
    # |                               | button_frame|
    # |                               |             |
    # |                               |             |
    # ----------------------------------------------
    road_condition = []
    button_list = []
    testing = []
    index = -1
    order_press = None

    def __init__(self, master, username, store):
        self.store = store
        self.order_path = os.path.join('Database', self.store, 'Orders.csv')
        self.complete_order = pd.read_csv(self.order_path, index_col=0)
        self.complete_key = pd.read_csv(self.order_path)['key']
        employee_path = os.path.join('Database', self.store, 'Employees.csv')
        complete_employee = pd.read_csv(employee_path, index_col=0)
        warning = complete_employee.loc[username]['warning']
        # --------------------------
        self.master = master
        self.master.title('Delivery')
        self.username = username
        # initialize all the frame
        self.map_frame = Frame(self.master, bd=2, relief=SUNKEN, width=500, height=500)
        self.order_frame = Frame(self.master, bd=2, relief=SUNKEN, width=150, height=300)
        self.info_frame = Frame(self.master, bd=2, relief=SUNKEN, width=150, height=100)
        self.button_frame = Frame(self.master, bd=2, relief=SUNKEN, width=150, height=100)
        # initialize the road condition by calling the function
        self.initialize_road()
        # use label to represent the road onto the map_frame
        for i in range(10):
            for j in range(10):
                if self.road_condition[i][j] == 2:  # green to represent smooth
                    # TODO
                    label_road = Label(self.map_frame, bg='green', bd=2, relief=SUNKEN)
                    label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                elif self.road_condition[i][j] == 5:  # orange represent busy
                    label_road = Label(self.map_frame, bg='orange', bd=2, relief=SUNKEN)
                    label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                else:  # use red represent closed
                    label_road = Label(self.map_frame, bg='red', bd=2, relief=SUNKEN)
                    label_road.grid(row=i, column=j, ipadx=22, ipady=14)
        # the info_frame initially should have nothing
        # simply grid in and initialize the size
        # TODO
        self.info_frame.grid(row=0, column=1)
        # initialize the button frame
        # simply grid in and initialize the size
        # TODO
        self.button_frame.grid(row=2, column=1)
        # initialize the order frame
        # finish the function initialize_order
        # call the function here
        # TODO
        self.initialize_order()
        self.order_frame.grid(row=1, column=1)
        # the button we can have a log out button and a finish deliever button
        # grid in the button
        # implement the log_out_event and finish_deliver_event
        # TODO
        self.logout_button = Button(self.info_frame, text='Log Out', command=self.log_out_event)
        self.finish_button = Button(self.button_frame, text='Finish', command=self.finish_deliver_event)
        self.logout_button.grid(row=3, column=0)
        self.finish_button.grid(row=1, column=0)

        # grid in the mpa
        self.map_frame.grid(row=0, column=0, rowspan=3)
        # gridpropagate
        self.map_frame.grid_propagate(0)
        self.info_frame.grid_propagate(0)
        self.button_frame.grid_propagate(0)
        self.order_frame.grid_propagate(0)
         # -----------------
        self.next_button = Button(self.button_frame, text='next', command=self.next_event)
        self.prev_button = Button(self.button_frame, text='prev', command=self.prev_event)
        self.next_button.grid(row=0, column=1)
        self.prev_button.grid(row=0, column=0)
        self.login_as_label = Label(self.info_frame, text='Log in as: %s' % self.username)
        self.warning_label = Label(self.info_frame, text='warning: %s' % warning)
        self.login_as_label.grid(row=1, column=0)
        self.warning_label.grid(row=2, column=0)
        self.ck = Label(self.info_frame)
        self.clock()

    def clock(self):
        localtime = time.asctime(time.localtime(time.time()))
        self.ck.config(text=localtime)
        self.info_frame.after(1000, self.clock)
        self.ck.grid(row=0, column=0)

    def initialize_road(self):
        for x in range(10):  # initialize the 2d list
            self.road_condition.append([y for y in range(10)])
        for i in range(10):
            for j in range(10):
                p = random.randint(1, 101)
                if p <= 50:  # the road is smooth
                    self.road_condition[i][j] = 2  # 2 minutes
                elif 50 < p <= 80:
                    self.road_condition[i][j] = 5  # 5 minutes
                else:
                    self.road_condition[i][j] = 100

    def initialize_order(self):
        # read the csv based on the username
        # use button and set the text to become the order#
        # use lambda to bind the function 'order_event'
        # so we know when we click the order button which order we are clicking
        # TODO
        self.complete_order = pd.read_csv(self.order_path, index_col=0)
        self.complete_key = pd.read_csv(self.order_path)['key']
        for key in self.complete_key:
            if self.complete_order.loc[key]['Delivery'] == self.username:
                o = key
                c = self.complete_order.loc[key]['Username']
                row = self.complete_order.loc[key]['Endrow']
                col = self.complete_order.loc[key]['Endcol']
                a = str(col) + ' ave ' + str(row) + ' st'
                button = Button(self.order_frame, text='order#: %s\ncustomer: %s\naddress: %s' % (o, c, a),
                                command=lambda i=key: self.order_event(i))
                self.button_list.append(button)
        self.index += 1
        if self.index < len(self.button_list):
            self.button_list[self.index].grid(row=0, column=0)
        else:
            self.index -= 1
        self.index += 1
        if self.index < len(self.button_list):
            self.button_list[self.index].grid(row=1, column=0)
        else:
            self.index -= 1
        self.index += 1
        if self.index < len(self.button_list):
            self.button_list[self.index].grid(row=2, column=0)
        else:
            self.index -= 1

    def order_event(self, order_num):
        # based on order_num we should know everything about the order such as the
        # destination and the total money
        # once the order was clicked display the info in info_frame such as destination, etc
        # the map_frame should now display the shortest route to the destination
        # by calling the function 'find_shortest_path'
        # based on the list return by the function find_shortest_path
        # we reinitialize the map according to the list
        # TODO
        # we can let the info frame to show something or not to
        self.complete_order = pd.read_csv(self.order_path, index_col=0)
        self.complete_key = pd.read_csv(self.order_path)['key']
        self.order_press = order_num
        starti = self.complete_order.loc[order_num]['Beginrow']
        startj  = self.complete_order.loc[order_num]['Begincol']
        endi = self.complete_order.loc[order_num]['Endrow']
        endj = self.complete_order.loc[order_num]['Endcol']
        start = [starti, startj]
        end = [endi, endj]
        path = self.find_shortest_path(start, end)
        # reinitialize the map
        for slaves in self.map_frame.grid_slaves():
            slaves.destroy()
        for i in range(10):
            for j in range(10):
                if [i, j] in path:
                    label_road = Label(self.map_frame, bg='blue', bd=2, relief=SUNKEN)
                    label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                elif [i, j] == start:
                    label_road = Label(self.map_frame, text='store', bg='blue', bd=2, relief=SUNKEN)
                    label_road.grid(row=i, column=j, ipadx=9, ipady=14)
                elif [i, j] == end:
                    label_road = Label(self.map_frame, text='end', bg='blue', bd=2, relief=SUNKEN)
                    label_road.grid(row=i, column=j, ipadx=12, ipady=14)
                else:
                    if self.road_condition[i][j] == 2:  # green to represent smooth
                        # TODO
                        label_road = Label(self.map_frame, bg='green', bd=2, relief=SUNKEN)
                        label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                    elif self.road_condition[i][j] == 5:  # orange represent busy
                        label_road = Label(self.map_frame, bg='orange', bd=2, relief=SUNKEN)
                        label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                    else:  # use red represent closed
                        label_road = Label(self.map_frame, bg='red', bd=2, relief=SUNKEN)
                        label_road.grid(row=i, column=j, ipadx=22, ipady=14)

    def find_shortest_path(self, start, end):
        # return a 2D list [ [i1, j1], [i2, j2], ..., [in, jn] ]
        # where [in, jn] is the coordinate where we will be at after the first step and
        # [i1, j1] is where we at before reaching the destination
        def gen_son(location):
            answer = []
            if 0 <= location[0] + 1 < 10:
                answer.append([location[0] + 1, location[1]])
            if 0 <= location[0] - 1 < 10:
                answer.append([location[0] - 1, location[1]])
            if 0 <= location[1] - 1 < 10:
                answer.append([location[0], location[1] - 1])
            if 0 <= location[1] + 1 < 10:
                answer.append([location[0], location[1] + 1])
            return answer

        def find_min_key(dic):
            min = 1000000000000000
            answer = 1000000000000000
            list_of_key = []
            for key in to_be_visit.keys():
                if to_be_visit.get(key):
                    list_of_key.append(key)
            for key in list_of_key:
                if dic.get(key) <= min:
                    min = dic.get(key)
                    answer = key
            return answer

        to_be_visit = {}  # the expanded node will become False else True
        parent = {}  # keep track of the parent of each node
        cost = {}  # keep track the cost to that node from the start
        s = start[0] * 10 + start[1]  # index of starting point ij
        g = end[0] * 10 + end[1]  # index of destination ij
        for i in range(10):  # initialize the cost, to_be_visit and parent
            for j in range(10):
                index = i * 10 + j
                cost[index] = 1000000000000000
                to_be_visit[index] = True
                parent[index] = 100
        cost[s] = 0  # cost of starting node should be zero
        parent[s] = s  # parent of start is itself
        while parent.get(g) == 100:  # means we still dont find goal yet
            key_to_expand = find_min_key(cost)  # find the node that we are going to expand
            to_be_visit[key_to_expand] = False  # assign False to the expanded node
            key = [int(key_to_expand / 10), key_to_expand % 10]  # ij => [i, j]
            p = gen_son(key)  # get son of [i, j]
            for sons in p:  # p = [[i-1,j], [i+1,j], [i,j+1], [i,j-1]] ;;; sons = [i, j]
                if to_be_visit[sons[0]*10 + sons[1]]:
                    cost_to_parent = cost[key_to_expand]  # cost to parent from start
                    cost_to_sons = cost_to_parent + self.road_condition[sons[0]][sons[1]]  # cost to son = costtoparent + road condition
                    if cost_to_sons <= cost[sons[0] * 10 + sons[1]]:  # if new cost cheaper than prev cost
                        cost[sons[0] * 10 + sons[1]] = cost_to_sons  # chg cost
                        parent[sons[0] * 10 + sons[1]] = key_to_expand  # chg parent
        temp = parent.get(g)
        answer = []
        while temp != s:
            answer.append([int(temp / 10), temp % 10])
            temp = parent.get(temp)
        return answer

    def log_out_event(self):
        self.master.quit()

    def prev_event(self):
        if self.index - 3 <= -1:
            messagebox.showinfo('Info', 'This is the first page.')
        else:
            for slave in self.order_frame.grid_slaves():
                slave.grid_forget()
                self.index -= 1
            self.index -= 3
            for i in range(3):
                self.index += 1
                if self.index < len(self.button_list):
                    self.button_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.button_list) - 1

    def next_event(self):
        if self.index + 1 == len(self.button_list):
            messagebox.showinfo('Info', 'You have reach the last page.')
        else:
            for slave in self.order_frame.grid_slaves():
                slave.grid_forget()
            for i in range(3):
                self.index += 1
                if self.index < len(self.button_list):
                    self.button_list[self.index].grid(row=i, column=0)
                else:
                    self.index = len(self.button_list) - 1

    def finish_deliver_event(self):
        # TODO
        # once finish we reinitialize the order_frame by remove that order
        # we rate the customer
        # read the csv file and put in the rate for customer
        # calculate the avg rating
        if self.order_press == None:
            messagebox.showerror('Error', 'Please select an order first.')
        else:
            key = self.order_press
            username = self.complete_order.loc[key]['Username']
            order = self.complete_order.loc[key]['Order']
            delivery = self.complete_order.loc[key]['Delivery']
            pending_rating_path = os.path.join('Database', self.store, 'PendingRating.csv')
            data = [[key, username, order, delivery]]
            df = pd.DataFrame(data, columns=['OderNum', 'Username', 'Order', 'Delivery'])
            with open(pending_rating_path, 'a') as pending_rating_csv:
                df.to_csv(pending_rating_csv, index=False, header=False)
            messagebox.showinfo('Done', 'Done.')
            self.button_list = []
            for slaves in self.order_frame.grid_slaves():
                slaves.destroy()
            self.index = -1
            # before dropping the order, we need to giv customer rating first
            self.rate_customer()
            self.order_press = None
            # ------------------------------------------------------------------------
            self.complete_order.drop([key]).to_csv(self.order_path, index_label=['key'])
            self.initialize_order()
            for i in range(10):
                for j in range(10):
                    if self.road_condition[i][j] == 2:  # green to represent smooth
                        # TODO
                        label_road = Label(self.map_frame, bg='green', bd=2, relief=SUNKEN)
                        label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                    elif self.road_condition[i][j] == 5:  # orange represent busy
                        label_road = Label(self.map_frame, bg='orange', bd=2, relief=SUNKEN)
                        label_road.grid(row=i, column=j, ipadx=22, ipady=14)
                    else:  # use red represent closed
                        label_road = Label(self.map_frame, bg='red', bd=2, relief=SUNKEN)
                        label_road.grid(row=i, column=j, ipadx=22, ipady=14)

    def rate_customer(self):
        def ok_event():
            user_path = os.path.join('Database', self.store, 'Users.csv')
            order_path = os.path.join('Database', self.store, 'Orders.csv')
            orders = pd.read_csv(order_path, index_col=0)
            users = pd.read_csv(user_path, index_col=0)
            customer_username = orders.loc[self.order_press]['Username']
            times = users.loc[customer_username]['OrderMade']
            cur_rating = users.loc[customer_username]['Rating']
            total = int(times) * int(cur_rating)
            times = int(times) + 1
            rate = int(rating.get())
            avg = (total + rate) / times
            users.loc[customer_username, 'OrderMade'] = times
            users.loc[customer_username, 'Rating'] = avg
            users.to_csv(user_path)
            root.destroy()
            root.quit()
            Manager.manager.promoteOrDemote(self.store)
        root = Tk()
        root.title('Rating')
        mainframe = Frame(root)
        mainframe.grid()
        label1 = Label(mainframe, text='Please give this customer a rating.\n'
                                       'From 1 to 5 and the default is 5.')
        label1.grid(row=0, column=0, columnspan=2)
        # rating.set(5)
        rating = Entry(mainframe, text='5')
        label2 = Label(mainframe, text='rating: ')
        label2.grid(row=1, column=0)
        rating.grid(row=1, column=1)
        #self.testing.append(rating)  # This is to prevent GC to kick in
        ok_button = Button(mainframe, text='Okay', command=ok_event)
        ok_button.grid(row=2, column=0, columnspan=2)
        root.mainloop()


'''a = Tk()
b = Delivery(a, 'ken', 'Brotherjohn')
a.mainloop()'''
#b.rate_customer()
# print(b.find_shortest_path([7,3], [6,1]))
