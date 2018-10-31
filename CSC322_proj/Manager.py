import tkinter
from tkinter import *
from tkinter import messagebox
import pandas as pd
from PIL import Image, ImageTk
import os.path
import random
import csv


class manager:
    def __init__(self, master, store):
        self.store = store
        self.master = master
        self.main_frame = Frame(self.master)
        self.instruction_label = Label(self.main_frame, text = "Manage Employees",fg="black", font=('ariel', 20 ,'bold'),padx = 20,pady =20,anchor="center")
        self.viewEmployeeInfo = Button(self.main_frame, text = "View Employees Information",height = 2, width = 23,command = lambda: self.view(self.store))
        self.viewPendingUserInfo = Button(self.main_frame, text = "View Pending Users Information", height = 2, width = 23, command = lambda: self.ViewPendingUser(self.store))
        self.viewComplaintInfo = Button(self.main_frame, text = "View Complaints", height = 2, width = 23, command = lambda: self.ViewComplaints(self.store))
        self.reviseEmployeeSalary = Button(self.main_frame, text = "Revise Employees Salary", height = 2, width = 23,command = lambda: self.EnterEmployee(self.store))
        self.addEmployee = Button(self.main_frame,text = "Add new Employee",height = 2, width = 23,command = lambda : self.addEmp(self.store))
        self.delectEmployee = Button(self.main_frame, text = "Delete Employee",height = 2, width = 23,command = lambda: self.removeEmployee(self.store))
        self.reviseWarning = Button(self.main_frame, text = "Revise Employee Warning", height = 2, width = 23, command = lambda: self.ReviseWarning(self.store))
        self.randomChooseDeliveryman = Button(self.main_frame, text= "Random Assign Deliveryman",height =2,width=23,command = lambda: self.RandomChoose(self.store))
        self.cancel_button = Button(self.main_frame, text="CANCEL", height = 2, width = 23,command=quit)
        self.main_frame.grid(row = 0, column = 0)
        self.instruction_label.grid(row=0, column=20, columnspan=2,sticky="wens")
        self.viewEmployeeInfo.grid(row = 2, column = 20, columnspan = 2,sticky = W)
        self.viewPendingUserInfo.grid(row = 3, column = 20, columnspan = 2,sticky = W)
        self.viewComplaintInfo.grid(row = 4, column = 20, columnspan = 2, sticky = W)
        self.reviseEmployeeSalary.grid(row =5, column =20, columnspan = 2,sticky = W)
        self.addEmployee.grid(row = 6, column = 20,columnspan = 2,sticky = W)
        self.delectEmployee.grid(row = 7, column =20, columnspan = 2,sticky = W)
        self.reviseWarning.grid(row = 8, column =20, columnspan = 2,sticky = W)
        self.randomChooseDeliveryman.grid(row = 9, column = 20,columnspan = 2, sticky = W)
        self.cancel_button.grid(row = 10, column = 20, columnspan = 2,sticky = W)

        # -——————-----------------------------
        self.frame = Frame(self.master)
        background_path = os.path.join('Database', self.store, 'logo.png')
        img = ImageTk.PhotoImage(Image.open(background_path))
        self.image_label = Label(self.frame, image=img)
        self.image_label.grid(row=0, column=0)
        self.image_label.image = img
        self.frame.grid(row=0, column=1)

    def view(self,store):
        self.root = tkinter.Tk()
        self.store = store
        self.root.title("View Employee Information")
        OpenFile = os.path.join("Database", self.store, "Employees.csv")
        with open(OpenFile, newline="") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(self.root, width=10, height=2, text=row, relief=tkinter.RIDGE)
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        self.cancel_button = Button(self.root, text="CANCEL",command=self.root.destroy)
        self.cancel_button.grid(row = 200, column = 4, columnspan =2)
        self.root.mainloop()

    def EnterEmployee(self,store):
        self.store = store
        self.root = tkinter.Tk()
        self.root.title("Revise Employ Salary")
        self.root.geometry("400x450+20+20")
        self.l = Label(self.root, text="Enter your Employee name")
        self.username_entry = Entry(self.root)
        self.l.pack()
        self.username_entry.pack()

        self.s = Label(self.root, text="Enter new salary")
        self.salary_entry = Entry(self.root)
        self.s.pack()
        self.salary_entry.pack()
        self.b = Button(self.root, text='OK', command=lambda: self.ok_event(self.store))
        self.b.pack()
        self.cancel_button = Button(self.root, text="CANCEL", command=self.root.destroy)
        self.cancel_button.pack()
        self.root.mainloop()

    def validate_identity(self,username,store):
        self.store = store
        FilePath = os.path.join("Database", self.store,"Employees.csv")
        user_list = pd.read_csv(FilePath)
        new_user_list = (user_list.iloc[:,0]).values.tolist()
        if username in new_user_list:
            self.username = username
            return True
        else:
            messagebox.showerror("Error", "Wrong Employee Name.")
            return False

    def ok_event(self,store):
        try:
            self.store = store
            username = self.username_entry.get()
            salary = self.salary_entry.get()
            FilePath = os.path.join("Database", self.store, "Employees.csv")
            user_list = pd.read_csv(FilePath,index_col=0)
            if (user_list.loc[username]["Identity"] == "customer"):
                messagebox.showerror("Error", "It is a customer, not your Empolyee.")
                return False
            if self.validate_identity(username,store):
                user_list.loc[username, "Salary"]= salary
                user_list.to_csv(FilePath)
            self.root.destroy()
            messagebox.showinfo('Dear Manager', 'Congratulation, you have successfully change your employee/s salary.')
        except:
            messagebox.showerror('Error', 'Something wrong')

    def addEmp(self,store):
        self.store = store
        self.root = tkinter.Tk()
        self.root.geometry("400x450+20+20")
        self.root.title("Hiring")
        self.l = Label(self.root, text="Hire a new Employee")
        self.Employee_name_entry = Entry(self.root)
        self.l.pack()
        self.Employee_name_entry.pack()
        self.passW = Label(self.root,text = "Set a password for your Employee")
        self.passW_entry = Entry(self.root)
        self.passW.pack()
        self.passW_entry.pack()
        self.posi = Label(self.root, text="Enter a position")
        self.posi_entry = Entry(self.root)
        self.posi.pack()
        self.posi_entry.pack()
        self.ssn = Label(self.root, text = "Enter Employee SSN")
        self.ssn_entry = Entry(self.root)
        self.ssn.pack()
        self.ssn_entry.pack()
        self.s = Label(self.root, text="Enter a salary")
        self.salary_entry = Entry(self.root)
        self.s.pack()
        self.salary_entry.pack()
        self.w = Label(self.root, text = "Default Warning 0")
        self.w.pack()
        self.b = Button(self.root, text='OK', command=lambda: self.add_people(self.store))
        self.b.pack()
        self.cancel_button = Button(self.root, text="CANCEL", command=self.root.destroy)
        self.cancel_button.pack()
        self.root.mainloop()

    def add_people(self,store):
        try:
            self.store = store
            EmpName = self.Employee_name_entry.get()
            PassWord = self.passW_entry.get()
            posiT = self.posi_entry.get()
            ssn = self.ssn_entry.get()
            salaryE = self.salary_entry.get()
            FilePath = os.path.join("Database", self.store, "Employees.csv")
            usersinfo = pd.read_csv(FilePath)
            userNameinfo = usersinfo["Username"].values.tolist()
            userPasswordinfo = usersinfo["Password"].values.tolist()
            userPositioninfo = usersinfo["Identity"].values.tolist()
            userSSNinfo = usersinfo["ssn"].values.tolist()
            userSalaryinfo = usersinfo["Salary"].values.tolist()
            userWarninginfo = usersinfo["warning"].values.tolist()
            useravgRatinginfo = usersinfo["avgRating"].values.tolist()
            userOneinfo = usersinfo["one"].values.tolist()
            userTwoinfo = usersinfo["two"].values.tolist()
            userThreeinfo = usersinfo["three"].values.tolist()

            workerlist = ["chef", "manager", "deliverman"]
            if EmpName == "" or not EmpName.isalpha():
                messagebox.showerror("Dear Manager", "Invaild Name")
            elif posiT not in workerlist:
                messagebox.showerror("Dear Manager", "Please use the position already exist. eg.chef, deliverman, manager.")
            elif salaryE == "" or int(salaryE) <= 0:
                messagebox.showerror(("Dear Manager", "Invaild salary"))
            else:
                userNameinfo.append(EmpName)
                userPasswordinfo.append(PassWord)
                userPositioninfo.append(posiT)
                userSalaryinfo.append(salaryE)
                userSSNinfo.append(ssn)
                userWarninginfo.append(0)
                if posiT == "deliverman":
                    useravgRatinginfo.append(5)
                    userOneinfo.append(5)
                    userTwoinfo.append(5)
                    userThreeinfo.append(5)
                else:
                    useravgRatinginfo.append(0)
                    userOneinfo.append(0)
                    userTwoinfo.append(0)
                    userThreeinfo.append(0)
                usersinfo = pd.DataFrame({"Username": userNameinfo,
                                      "Password": userPasswordinfo,
                                        "Identity": userPositioninfo,
                                           "ssn": userSSNinfo,
                                            "Salary": userSalaryinfo,
                                            "warning": userWarninginfo,
                                            "avgRating": useravgRatinginfo,
                                            "one":userOneinfo,
                                            "two":userTwoinfo,
                                            "three":userThreeinfo})
                usersinfo = usersinfo[["Username",
                               "Password",
                               "Identity",
                                   "ssn",
                               "Salary",
                                   "warning",
                                   "avgRating",
                                   "one",
                                   "two",
                                   "three"]]
                usersinfo.to_csv(FilePath, mode= 'r+', index= False)
                self.root.destroy()
                messagebox.showinfo('Dear Manager', 'Congratulation, you have successfully added a new employee.')
        except:
            messagebox.showerror('Error', 'Something wrong')

    def removeEmployee(self,store):
        self.store = store
        self.root = tkinter.Tk()
        self.root.geometry("400x450+20+20")
        self.root.title("Firing")
        self.l = Label(self.root, text="Fire An Employee",padx=50, pady=50)
        self.Employee_name_E = Entry(self.root)
        self.l.pack()
        self.Employee_name_E.pack()

        self.b = Button(self.root, text='OK',height = 2, width = 6,command=lambda: self.Remove(self.store))
        self.b.pack()
        self.cancel_button = Button(self.root, text="CANCEL",height = 2, width = 6, command=self.root.destroy)
        self.cancel_button.pack()
        self.root.mainloop()

    def Remove(self, store):
        try:
            self.store = store
            RemoveE = self.Employee_name_E.get()
            FilePath = os.path.join("Database", self.store, "Employees.csv")
            usersinfo = pd.read_csv(FilePath)
            userNameinfo = usersinfo["Username"].values.tolist()
            to_drop = [RemoveE]
            usersinfo = usersinfo[~usersinfo["Username"].isin(to_drop)]
            if RemoveE in userNameinfo:
                usersinfo.to_csv(FilePath,index=False)
                self.root.destroy()
                messagebox.showinfo('Dear Manager', 'Remove your employee successfully! ')
            else:
                self.root.destroy()
                messagebox.showerror("Employee does not exist! ")
        except:
            messagebox.showerror('Error', 'Something wrong')
    def ReviseWarning(self,store):
        self.store = store
        self.root = tkinter.Tk()
        self.root.title("Revise Employ Warning")
        self.root.geometry("400x450+20+20")
        self.l = Label(self.root, text="Enter your Employee name",padx=50, pady=50)
        self.username_entry = Entry(self.root)
        self.l.pack()
        self.username_entry.pack()

        self.s = Label(self.root, text="Edit warning",padx=50, pady=50)
        self.warning_entry = Entry(self.root)
        self.s.pack()
        self.warning_entry.pack()

        self.b = Button(self.root, text='OK', command= lambda: self.ok_event_warning(self.store))
        self.b.pack()
        self.cancel_button = Button(self.root, text="CANCEL", command=self.root.destroy)
        self.cancel_button.pack()
        self.root.mainloop()

    def ok_event_warning(self,store):
        try:
            self.store = store
            username = self.username_entry.get()
            warning = self.warning_entry.get()
            FilePath = os.path.join("Database", self.store, "Employees.csv")
            user_list = pd.read_csv(FilePath,index_col=0)
            if (user_list.loc[username]["Identity"] == "customer"):
                messagebox.showerror("Error", "It is a customer, not your Empolyee.")
                return False
            if self.validate_identity(username,store):
                w = user_list.loc[username, "warning"]
                user_list.loc[username, "warning"] = warning
                user_list.to_csv(FilePath)
            self.root.destroy()
            messagebox.showinfo('Dear Manager', 'Congratulation, you have successfully change your employee/s warning.')
        except:
            messagebox.showerror('Error', 'Something wrong')
    @staticmethod
    def blacklist_customer(store):
        UsePath = os.path.join("Database", store, "Users.csv")
        user_list = pd.read_csv(UsePath, index_col= 0)
        WarnUser = pd.read_csv(UsePath)["Username"].values.tolist()
        for person in WarnUser:
            rate = user_list.loc[person]["Rating"]
            if rate <= 1:
                reachSSN = user_list.loc[person]["ssn"]
                Black_list = pd.read_csv("Database/Blacklist.csv")
                BlackSSN = Black_list["ssn"].values.tolist()
                BlackStore = Black_list["store"].values.tolist()
                BlackSSN.append(reachSSN)
                BlackStore.append(store)
                Black_list = pd.DataFrame({"ssn":BlackSSN,
                                           "store": BlackStore})
                Black_list.to_csv("Database/Blacklist.csv", index= False)
                user_list = user_list.drop([person]).to_csv(UsePath, index_label=["Username"])

    def getDeliveryman(self,store):
        self.store = store
        Employ_path = os.path.join('Database', self.store, "Employees.csv")
        EmployeeFile = pd.read_csv(Employ_path)
        deliverList = EmployeeFile["Username"].values.tolist()

        read = pd.read_csv(Employ_path,index_col=0)
        WhoIsDeliver = []
        for username in deliverList:
            if read.loc[username]["Identity"] == "delivery":
                WhoIsDeliver.append(username)
        return random.choice(WhoIsDeliver)

    def chooseDeliveryman(self,username, store):
        self.store = store
        delivery_path = os.path.join('Database', self.store,"deliver.csv")
        deliver_customer = pd.read_csv(delivery_path, index_col= 0)
        deliver = deliver_customer.loc[username,"man"]

        if deliver == "none":
            man = self.getDeliveryman(self.store)
            deliver_customer.loc[username,"man"] = man
            deliver_customer.to_csv(delivery_path)

    def RandomChoose(self,store):
        self.store = store
        delivery_path = os.path.join('Database', self.store, "deliver.csv")
        deliver_customer = pd.read_csv(delivery_path)
        customer_ssnList = deliver_customer["username"].values.tolist()
        for username in customer_ssnList:
            self.chooseDeliveryman(username,self.store)
        else:
            messagebox.showinfo("Dear manager", "You have successful assigned deliveryman to deliver!")

    def ViewComplaints(self, store):
        self.root = tkinter.Tk()
        self.store = store
        self.root.title("View Complaints Information")
        self.rightDown_frame = Frame(self.root, bd = 2, relief = SUNKEN, width = 500, height = 300)
        self.rightDown_frame.grid(row = 0, column = 0,sticky=N)
        self.rightDown_frame.grid_propagate(0)
        #-----------------------------------------------
        self.viewButtonFrame = Frame(self.root, relief=SUNKEN, width=150, height=100)
        self.viewButtonFrame.grid (row = 1, column = 0)
        self.customer_botton = Button(self.viewButtonFrame, text="View Pizza Comments ", height=2, width=20,
                                      command = lambda: self.viewPizzaComplaint(self.store))
        self.customer_botton.grid(row=0, column=0)

        self.delivery_botton = Button(self.viewButtonFrame, text="View Deliveryman Comments ", height=2, width=20,
                                      command = lambda : self.viewDeliveryComment(self.store))
        self.delivery_botton.grid(row=0, column=1)

        self.chef_botton = Button(self.viewButtonFrame, text="View Store Comments ", height=2, width=20,
                                  command = lambda : self.viewStoreComment(self.store))
        self.chef_botton.grid(row=1, column=0)

        self.clean_botton = Button(self.viewButtonFrame, text="CLEAN ", height=2, width=20, command=self.cleanFrame)
        self.clean_botton.grid(row=1, column=1)

        self.cancel_button = Button(self.viewButtonFrame, text="CANCEL", height=2, width=20, command=self.root.destroy)
        self.cancel_button.grid(row=3, column=0)
        self.root.mainloop()

    def viewPizzaComplaint(self, store):
        self.store = store
        check_complaint_path = os.path.join("Database", store, "Complaint.csv")
        check_complaint = pd.read_csv(check_complaint_path, index_col= 0)
        num_list = pd.read_csv(check_complaint_path)['Num']
        info_label = Label(self.rightDown_frame, width = 55, height = 2, text = "Only Check Previous 7 Comments!",fg = "red")
        info_label.grid(row = 0, column = 0)
        r = 1
        for n in num_list:
            if check_complaint.loc[n]['Identify'] == "pizza":
                pizza = check_complaint.loc[n]['Object']
                pizzaComment = check_complaint.loc[n]["Comment"]
                Pizzacommentlabel = Label(self.rightDown_frame, width=55, height=2,
                                     text={"Pizza": pizza, "Comment": pizzaComment}, relief=RIDGE)
                Pizzacommentlabel.grid(row=r, column=0)
                r = r + 1

    def viewStoreComment(self,store):
        self.store = store
        check_complaint_path = os.path.join("Database", store, "Complaint.csv")
        check_complaint = pd.read_csv(check_complaint_path, index_col=0)
        num_list = pd.read_csv(check_complaint_path)['Num']
        info_label = Label(self.rightDown_frame, width=55, height=2, text="Only Check Previous 7 Comments!",fg = "red")
        info_label.grid(row=0, column=0)
        r = 1
        for n in num_list:
            if check_complaint.loc[n]['Identify'] == "store":
                stores = check_complaint.loc[n]['Object']
                storeComment = check_complaint.loc[n]["Comment"]
                storeCommentlabel = Label(self.rightDown_frame, width = 55, height = 2,
                                          text = {"Store": stores, "Comment": storeComment}, relief = RIDGE)
                storeCommentlabel.grid(row = r, column = 0)
                r = r + 1

    def viewDeliveryComment(self, store):
        self.store = store
        check_complaint_path = os.path.join("Database", store, "Complaint.csv")
        check_complaint = pd.read_csv(check_complaint_path, index_col=0)
        num_list = pd.read_csv(check_complaint_path)['Num']
        info_label = Label(self.rightDown_frame, width=55, height=2, text="Only Check Previous 7 Comments!", fg = "red")
        info_label.grid(row=0, column=0)
        r = 1
        for n in num_list:
            if check_complaint.loc[n]['Identify'] == "delivery":
                delivery = check_complaint.loc[n]['Object']
                deliveryComment = check_complaint.loc[n]["Comment"]
                deliveryCommentlabel = Label(self.rightDown_frame, width = 55, height = 2,
                                             text = {"Deiveryman": delivery, "Comment": deliveryComment}, relief = RIDGE)

                deliveryCommentlabel.grid(row = r, column = 0)
                r = r + 1

    @staticmethod
    def DropPizza(store):
        menupath = os.path.join("Database", store, "Menu.csv")
        Menu = pd.read_csv(menupath, index_col=0)
        pizzaList = pd.read_csv(menupath)["Pizza"].values.tolist()
        for Pizza in pizzaList:
            averageRating = Menu.loc[Pizza]["avgrating"]
            if averageRating < 2:
                getCook = Menu.loc[Pizza]["Cook"]
                EmployeePath = os.path.join("Database", store, "Employees.csv")
                EmployeeFile = pd.read_csv(EmployeePath, index_col=0)
                getWarning = EmployeeFile.loc[getCook]["warning"]
                getWarning = getWarning + 0.5
                EmployeeFile.loc[getCook, "warning"] = getWarning
                EmployeeFile.to_csv(EmployeePath)
                Menu = Menu.drop([Pizza]).to_csv(menupath, index_label=['Pizza'])

    @staticmethod
    def layoffCook(store):
        EmployeePath = os.path.join("Database", store, "Employees.csv")
        EmployeeFile = pd.read_csv(EmployeePath, index_col=0)
        user_list = pd.read_csv(EmployeePath)["Username"].values.tolist()
        for person in user_list:
            getId = EmployeeFile.loc[person, "Identity"]
            if getId == "chef":
                getAvgRate = EmployeeFile.loc[person]["avgRating"]
                getWarning = EmployeeFile.loc[person]["warning"]
                if getWarning > 3:
                    EmployeeFile = EmployeeFile.drop([person]).to_csv(EmployeePath, index_label=['Username'])

    def ViewPendingUser(self, store):
        self.root = tkinter.Tk()
        self.store = store
        self.root.title("View Pending Users Information")
        self.check_frame = Frame(self.root, bd=2, relief=SUNKEN, width=100, height=50)
        OpenFile = os.path.join("Database", self.store, "PendingUsers.csv")
        with open(OpenFile, newline="") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = Label(self.check_frame, width=10, height=2, text=row, relief=RIDGE)
                    label.grid(row=r, column=c)
                    c += 1
                r += 1

        self.check_frame.grid(row = 0, column = 0)
        #--------------------check right-----------------------------------------
        self.right_frame = Frame(self.root, bd = 2, relief = SUNKEN, width = 300, height = 100)
        self.right_frame.grid(row = 1, column = 1,sticky=(N, E, W))
        self.right_frame.grid_propagate(0)
        self.pendingLabel = Label(self.right_frame, text = "Enter Pending Customer SSN: ", height = 2, width = 30)
        self.pendingLabel.grid(row = 0, column = 0)
        self.PendingEntrySSN = Entry(self.right_frame)
        self.PendingEntrySSN.grid(row = 1, column = 0)

        #--------------------check right down--------------------------------------------------
        self.rightDown_frame = Frame(self.root, bd = 2, relief = SUNKEN, width = 400, height = 200)
        self.rightDown_frame.grid(row = 0, column = 1,sticky=N)
        self.rightDown_frame.grid_propagate(0)
        #-----------------------------------------------
        self.viewButtonFrame = Frame(self.root, relief=SUNKEN, width=150, height=100)
        self.viewButtonFrame.grid (row = 2, column = 1)
        self.check_botton = Button(self.viewButtonFrame, text = "CHECK ",height = 2, width = 7, command = lambda :self.check_event(self.store))
        self.check_botton.grid (row = 0 , column = 0)
        self.approve_botton = Button(self.viewButtonFrame, text="APPROVE ", height=2, width=7,command=lambda: self.approvePendingUser(self.store))
        self.approve_botton.grid(row=0, column=1)
        self.clean_botton = Button(self.viewButtonFrame, text="CLEAN ", height=2, width=7,command = self.cleanFrame)
        self.clean_botton.grid(row=0, column=2)
        self.cancel_button = Button(self.viewButtonFrame, text="CANCEL",height = 2, width = 7, command=self.root.destroy)
        self.cancel_button.grid(row=0, column=3)
        self.root.mainloop()



    def approvePendingUser(self, store):
        readPendingPath = os.path.join("Database", store, "PendingUsers.csv")
        readPendingUser = pd.read_csv(readPendingPath, index_col=0)
        getSSN = self.PendingEntrySSN.get()
        getSSN = int(getSSN)
        getUsername = readPendingUser.loc[getSSN]["Username"]
        getPassword = readPendingUser.loc[getSSN]["Password"]
        FilePath = os.path.join("Database", store, "Users.csv")
        usersinfo = pd.read_csv(FilePath)
        userNameinfo = usersinfo["Username"].values.tolist()
        userPasswordinfo = usersinfo["Password"].values.tolist()
        userPositioninfo = usersinfo["Identity"].values.tolist()
        userSSNinfo = usersinfo["ssn"].values.tolist()
        userFirst = usersinfo["First"].values.tolist()
        userSecond = usersinfo["Second"].values.tolist()
        userThird = usersinfo["Third"].values.tolist()
        userRating = usersinfo["Rating"].values.tolist()
        # added
        userOrderMade = usersinfo["OrderMade"].values.tolist()

        userNameinfo.append(getUsername)
        userPasswordinfo.append(getPassword)
        userPositioninfo.append("normal")
        userSSNinfo.append(getSSN)
        userFirst.append("holder")
        userSecond.append("holder")
        userThird.append("holder")
        userRating.append(5)
        userOrderMade.append(0)

        usersinfo = pd.DataFrame({"Username": userNameinfo,
                                  "Password": userPasswordinfo,
                                  "Identity": userPositioninfo,
                                  "ssn": userSSNinfo,
                                  "First": userFirst,
                                  "Second": userSecond,
                                  "Third": userThird,
                                  "Rating": userRating,
                                  "OrderMade": userOrderMade})
        usersinfo = usersinfo[["Username",
                               "Password",
                               "Identity",
                               "ssn",
                               "First",
                               "Second",
                               "Third",
                               "Rating",
                               "OrderMade"]]
        usersinfo.to_csv(FilePath, index=False)
        messagebox.showinfo("Dear Manager", "You have approve the pending visitor to customer")
        readPendingUser.drop([getSSN]).to_csv(readPendingPath, index_label=['ssn'])

    def cleanFrame(self):
        list = self.rightDown_frame.grid_slaves()
        for l in list:
            l.destroy()

    def check_event(self,store):
        goCheck = self.PendingEntrySSN.get()
        storePath = os.path.join("Database/PizzaStores.csv")
        Pizzastore = pd.read_csv(storePath, index_col= 3)
        storeList = pd.read_csv(storePath)["Name"].values.tolist()
        FindPendingPath = os.path.join("Database", store, "PendingUsers.csv")
        readPendingSSNlist = pd.read_csv(FindPendingPath)["ssn"].values.tolist()
        if int(goCheck) not in readPendingSSNlist:
            messagebox.showerror("Dear Manager", "There is not exist such a pending customer. ")
        else:
            r = 0
            for Pstore in storeList:
                FindUserPath = os.path.join("Database", Pstore, "Users.csv")
                UserInfo = pd.read_csv(FindUserPath, index_col= 3)
                readUserSSN = pd.read_csv(FindUserPath)["ssn"].values.tolist()
                if int(goCheck) in readUserSSN:
                    getIdentity = UserInfo.loc[int(goCheck)]["Identity"]
                    getRate = UserInfo.loc[int(goCheck)]["Rating"]
                    Pendinglabel = Label(self.rightDown_frame, width=40, height=2, text = {"Identity":getIdentity,"Rate":getRate,"Store": Pstore}, relief=RIDGE)
                    Pendinglabel.grid(row = r, column = 0)
                    r = r + 1

    @staticmethod
    def promoteOrDemote(store):
        UsePath = os.path.join("Database", store, "Users.csv")
        user_list = pd.read_csv(UsePath, index_col=0)
        WarnUser = pd.read_csv(UsePath)["Username"].values.tolist()
        for person in WarnUser:
            if int(user_list.loc[person]['OrderMade']) <= 3:
                continue
            rate = user_list.loc[person]["Rating"]
            if rate > 4 and int(user_list.loc[person]['OrderMade']) > 3:
                getIdentity = user_list.loc[person, "Identity"]
                if getIdentity == "normal":
                    user_list.loc[person,"Identity"] = 'vip'
                    user_list.to_csv(UsePath)
                if getIdentity == "visitor":
                    user_list.loc[person,"Identity"] = "visitor"
                    user_list.to_csv(UsePath)
                elif getIdentity == "vip":
                    user_list.loc[person,"Identity"] = "vip"
                    user_list.to_csv(UsePath)
            elif rate < 2 and rate > 1 and int(user_list.loc[person]['OrderMade']) > 3:
                getIdentity = user_list.loc[person, "Identity"]
                if getIdentity == "normal":
                    user_list.loc[person, "Identity"] = 'visitor'
                    user_list.to_csv(UsePath)
                if getIdentity == "visitor":
                    user_list.loc[person, "Identity"] = "visitor"
                    user_list.to_csv(UsePath)
                elif getIdentity == "vip":
                    user_list.loc[person, "Identity"] = "normal"
                    user_list.to_csv(UsePath)

    @staticmethod
    def DeliveryPunish(store,username):
        EmployeePath = os.path.join("Database", store, "Employees.csv")
        EmployeeFile = pd.read_csv(EmployeePath, index_col= 0)
        user_list = pd.read_csv(EmployeePath)["Username"].values.tolist()
        for username in user_list:
            getId = EmployeeFile.loc[username, "Identity"]
            if getId == "delivery":
                getAvgRate = EmployeeFile.loc[username]["avgRating"]
                getWarning = EmployeeFile.loc[username]["warning"]
                if getWarning >= 3:
                    EmployeeFile = EmployeeFile.drop([username]).to_csv(EmployeePath, index_label=['Username'])
                if getAvgRate < 2:
                    getWarning = getWarning + 1
                    EmployeeFile.loc[username, "warning"] = getWarning
                    EmployeeFile.to_csv(EmployeePath)


a = Tk()
a.title("Manager Managment")
b = manager(a, 'Brotherjohn')
#manager.DropPizza("Brotherjohn")
#manager.blacklist_customer("Brotherjohn")
#manager.promoteOrDemote("Brotherjohn")
#manager.DeliveryPunish("Brotherjohn","john")
#manager.layoffCook("Brotherjohn")
a.mainloop()
