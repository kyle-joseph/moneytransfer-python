from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import pymysql
import random
from datetime import *
from datetime import date, timedelta

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, register, Transaction):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.username = StringVar()
        self.password = StringVar()
        self.Start()
    def Start(self):
        canvas = Canvas(self, width=1350, height=690)
        canvas.grid(row=0, column=0, sticky="nsew")
        img = Image.open("bg.png")
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image = canvas.image, anchor = "nw")
        # entry
        uname = Entry(canvas, width=19, font=("Arial", 16), relief=FLAT, bg="#3D3E43", fg="#FFFFFF", textvariable = self.username)
        uname.place(x=575, y=316)
        passw = Entry(canvas, width=19, font=("Arial", 16), relief=FLAT, bg="#3D3E43", fg="#FFFFFF", show="*", textvariable = self.password)
        passw.place(x=575, y=385)
        # buttons

        btnLogin = Button(canvas, text="LOGIN", width=16, height=1, bg="#E7464C", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT, command=lambda: self.testAccount(lblPrompt, uname, passw))
        btnLogin.place(x=592, y=432)
        btnRegister = Button(canvas, text="SIGN UP"
                                          "", width=16, height=1, bg="#E7464C", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT, command=lambda: self.registerClick(lblPrompt, uname, passw))
        btnRegister.place(x=592, y=470)
        lblPrompt = Label(self, bg="#2B2C30", fg="#FFFFFF", font=("Arial", 9, "bold"))


    def data(self):
        accounts = []
        db = pymysql.connect("localhost", "root", "", "dblogin")

        cursor = db.cursor()
        sql = "SELECT * FROM tbllogin"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subaccount = []
                user = row[1]
                passw = row[2]
                subaccount.append(user)
                subaccount.append(passw)
                accounts.append(subaccount)
        except:
            print("Error: unable to fetch data")

        db.close()
        return accounts

    def testAccount(self, lbl, uname, passw):
        accounts = self.data()
        acc = []
        use = self.username.get()
        pas = self.password.get()
        acc.append(use)
        acc.append(pas)
        if acc in accounts:
            lbl.config(text="")
            uname.delete(0, END)
            passw.delete(0, END)
            uname.focus()
            self.controller.show_frame(Transaction)
        elif use == "" and pas == "":
            lbl.place(x=592, y=502)
            lbl.config(text = "Please enter a valid account")
            uname.delete(0, END)
            passw.delete(0, END)
            uname.focus()
        else:
            lbl.place(x=592, y=502)
            lbl.config(text="Please enter a valid account")
            uname.delete(0, END)
            passw.delete(0, END)
            uname.focus()
    def registerClick(self, lbl, uname, passw):
        lbl.config(text="")
        uname.delete(0, END)
        passw.delete(0, END)
        uname.focus()
        self.controller.show_frame(register)

class register(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.username = StringVar()
        self.password = StringVar()
        self.Register()

    def Register(self):
        canvas = Canvas(self, width=1350, height=690)
        canvas.grid(row=0, column=0, sticky="nsew")
        img = Image.open("register.png")
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")
        # entry
        uname = Entry(canvas, width=19, font=("Arial", 16), relief=FLAT, bg="#3D3E43", fg="#FFFFFF",
                      textvariable=self.username)
        uname.place(x=575, y=300)
        passw = Entry(canvas, width=19, font=("Arial", 16), relief=FLAT, bg="#3D3E43", fg="#FFFFFF", show="*",
                      textvariable=self.password)
        passw.place(x=575, y=369)
        # buttons

        btnLogin = Button(canvas, text="SIGN UP", width=16, height=1, bg="#E7464C", fg="#FFFFFF", bd=0,
                          font=("Arial", 12, "bold"), relief=FLAT,
                          command=lambda: self.testAccount(lblPrompt, uname, passw))
        btnLogin.place(x=592, y=416)
        btnCancel = Button(canvas, text="CANCEL", width=7, height=1, bg="#E7464C", fg="#FFFFFF", bd=0,
                          font=("Arial", 12, "bold"), relief=FLAT,
                          command=lambda: self.Cancel(lblPrompt, uname, passw))
        btnCancel.place(x=1200, y=120)
        lblPrompt = Label(self, bg="#2B2C30", fg="#FFFFFF", font=("Arial", 9, "bold"))

    def data(self):
        accounts = []
        db = pymysql.connect("localhost", "root", "", "dblogin")

        cursor = db.cursor()
        sql = "SELECT * FROM tbllogin"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subaccount = []
                user = row[1]
                passw = row[2]
                subaccount.append(user)
                subaccount.append(passw)
                accounts.append(subaccount)
        except:
            print("Error: unable to fetch data")

        db.close()
        return accounts
    def dataInsert(self, use, pas ):
        db = pymysql.connect("localhost", "root", "", "dblogin")

        cur = db.cursor()
        sql = "INSERT INTO tbllogin(ID, Username, Password) VALUES(null, %s, %s)"
        try:
            cur.execute(sql, (use, pas))
            db.commit()
        except:
            print("Error: unable to fetch data")
        db.close()

    def search(self, accounts, user):
        for i in range(len(accounts)):
            if user == accounts[i][0]:
                return True
        return False

    def testAccount(self, lbl, uname, passw):
        accounts = self.data()
        use = self.username.get()
        pas = self.password.get()

        if self.search(accounts, use):
            lbl.place(x=604, y=449)
            lbl.config(text="Username already exist")
            uname.delete(0, END)
            passw.delete(0, END)
            uname.focus()
        elif (use == "" and pas == "") or (use == "" or pas == ""):
            lbl.place(x=592, y=449)
            lbl.config(text="Please enter a valid account")
            uname.delete(0, END)
            passw.delete(0, END)
            uname.focus()
        else:
            self.dataInsert(use, pas)
            uname.delete(0, END)
            passw.delete(0, END)
            uname.focus()
            lbl.config(text="")
            self.controller.show_frame(StartPage)

    def Cancel(self, lbl, uname, passw):
        lbl.config(text="")
        self.controller.show_frame(StartPage)
        uname.delete(0, END)
        passw.delete(0, END)

class Transaction(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.frames = {}
        self.btnSendImage = PhotoImage(file = "btnSend.png")
        self.btnReceiveImage = PhotoImage(file= "btnRec.png")
        self.btnClaimImage = PhotoImage(file = "btnClaimed.png")
        self.btnUnclaimImage = PhotoImage(file = "btnUnclaimed.png")
        self.btnReportImage = PhotoImage(file = "btnReport.png")
        self.Start()

    def Start(self):
        canvas = Canvas(self, width=1350, height=690)
        canvas.grid(row=0, column=0, sticky="nsew")
        img = Image.open("tranbg.png")
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")

        #buttons
        global btnSend, btnReceive, btnClaimed, btnUnclaimed, btnReport, lblTitle
        btnSend = Button(canvas, bg="#E7464C", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT,
                         activebackground = "#E7464C", activeforeground = "#FFFFFF", command=lambda: self.btnClick(1),
                         image = self.btnSendImage)
        btnSend.place(x=2, y=148)
        btnReceive = Button(canvas, bg="#2B2C30", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT,
                            activebackground="#E7464C", activeforeground="#FFFFFF", command=lambda: self.btnClick(2),
                            image=self.btnReceiveImage)
        btnReceive.place(x=2, y=219)
        btnClaimed= Button(canvas, bg="#2B2C30", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT,
                         activebackground="#E7464C", activeforeground="#FFFFFF", command=lambda: self.btnClick(3),
                         image=self.btnClaimImage)
        btnClaimed.place(x=2, y=290)
        btnUnclaimed = Button(canvas, bg="#2B2C30", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT,
                            activebackground="#E7464C", activeforeground="#FFFFFF", command=lambda: self.btnClick(4),
                            image=self.btnUnclaimImage)
        btnUnclaimed.place(x=2, y=361)
        btnReport = Button(canvas, bg="#2B2C30", fg="#FFFFFF", bd=0, font=("Arial", 12, "bold"), relief=FLAT,
                            activebackground="#E7464C", activeforeground="#FFFFFF", command=lambda: self.btnClick(5),
                            image=self.btnReportImage)
        btnReport.place(x=2, y=432)

        lblTitle = Label(canvas, text="SEND MONEY", bg="#E7464C", fg="#F9F4F4", font=("Courier New", 20, "bold"))
        lblTitle.place(x=320, y=19)

        #Display Transactions
        container = Frame(canvas, width=1058, height=613)
        container.place(x=290, y=75)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (Send, Receive, viewClaimed, viewUnclaimed, viewReport):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showTransactionFrame(Send)

    def showTransactionFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    def fetchData(self):
        transactionData = []
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cursor = db.cursor()
        sql = "SELECT * FROM transactions"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subdata = []
                sfname = row[1]
                slname = row[2]
                sNum = row[3]
                rfname = row[4]
                rlname = row[5]
                rNum = row[6]
                cNum = row[7]
                date = row[8]
                charge = row[9]
                amount = row[10]
                totalamount = row[11]
                stat = row[12]
                rDate = row[13]
                eDate = row[14]
                for i in (sfname, slname, sNum, rfname, rlname, rNum, cNum, date, charge, amount, totalamount, stat, rDate, eDatea):
                    subdata.append(i)
                transactionData.append(subdata)
        except:
            print("Error: unable to fetch data")
        db.close()
        return transactionData
    def btnClick(self, clk):
        if clk == 1:
            btnReceive.config(bg="#2B2C30")
            btnClaimed.config(bg="#2B2C30")
            btnUnclaimed.config(bg="#2B2C30")
            btnReport.config(bg="#2B2C30")
            btnSend.config(bg = "#E7464C")
            lblTitle.config(text="SEND MONEY")
            self.showTransactionFrame(Send)
        elif clk == 2:
            btnSend.config(bg="#2B2C30")
            btnClaimed.config(bg="#2B2C30")
            btnUnclaimed.config(bg="#2B2C30")
            btnReport.config(bg="#2B2C30")
            btnReceive.config(bg = "#E7464C")
            lblTitle.config(text="CLAIM MONEY")
            self.showTransactionFrame(Receive)
        elif clk == 3:
            btnSend.config(bg="#2B2C30")
            btnUnclaimed.config(bg="#2B2C30")
            btnReport.config(bg="#2B2C30")
            btnReceive.config(bg="#2B2C30")
            btnClaimed.config(bg="#E7464C")
            lblTitle.config(text="CLAIMED MONEY")
            self.showTransactionFrame(viewClaimed)
        elif clk == 4:
            btnSend.config(bg="#2B2C30")
            btnReport.config(bg="#2B2C30")
            btnReceive.config(bg="#2B2C30")
            btnClaimed.config(bg="#2B2C30")
            btnUnclaimed.config(bg="#E7464C")
            lblTitle.config(text="UNCLAIMED MONEY")
            self.showTransactionFrame(viewUnclaimed)
        elif clk == 5:
            btnSend.config(bg="#2B2C30")
            btnReceive.config(bg="#2B2C30")
            btnClaimed.config(bg="#2B2C30")
            btnUnclaimed.config(bg="#2B2C30")
            btnReport.config(bg="#E7464C")
            lblTitle.config(text="REPORT")
            self.showTransactionFrame(viewReport)

class Send(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, width=1058, height=613)
        self.parent = parent
        self.controller = controller
        self.sfname = StringVar()
        self.slname = StringVar()
        self.sNum = StringVar()
        self.amountToSend = StringVar()
        self.rfname = StringVar()
        self.rlname = StringVar()
        self.rNum = StringVar()
        self.amountToPay = StringVar()
        self.readyToSend = False
        self.voidUpdate()
        self.Start()

    def Start(self):
        canvas = Canvas(self, width=1350, height=690)
        canvas.grid(row=0, column=0, sticky="nsew")
        img = Image.open("SendFrame.png")
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")

        global sfirstname, slastname, sNumber, samount, rfirstname, rlastname, rNumber, payAmount, lblControl,lblCharge,\
        lblpayAmount,lblChange, lblPrompt

        sfirstname = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.sfname)
        sfirstname.place(x = 77, y = 137)
        slastname = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.slname)
        slastname.place(x=77, y=192)
        sNumber = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.sNum)
        sNumber.place(x=77, y=246)
        samount = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.amountToSend)
        samount.place(x=77, y=299)

        rfirstname = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.rfname)
        rfirstname.place(x=77, y=435)
        rlastname = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.rlname)
        rlastname.place(x=77, y=490)
        rNumber = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.rNum)
        rNumber.place(x=77, y=543)

        payAmount = Entry(canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.amountToPay)
        payAmount.place(x=573, y=379)

        lblControl = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 18, "bold"))
        lblControl.place(x=620, y=100)
        lblCharge = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 18, "bold"))
        lblCharge.place(x=620, y=184)
        lblpayAmount = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 18, "bold"))
        lblpayAmount.place(x=620, y=268)
        lblChange = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 18, "bold"))
        lblChange.place(x=620, y=458)
        lblPrompt = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 18, "bold"))
        lblPrompt.place(x=608, y=560)

        btnPrepare = Button(canvas, text="PREPARE", bg="#F99B00", fg="#FFFFFF", bd=0, font=("Courier New", 16, "bold"), relief=FLAT,
                         activebackground="#F99B00", activeforeground="#FFFFFF", height=1, width=8, command=lambda: self.btnPrepareClicked())
        btnPrepare.place(x=610, y=510)
        btnSend = Button(canvas, text="SEND", bg="#00BB27", fg="#FFFFFF", bd=0, font=("Courier New", 16, "bold"),
                            relief=FLAT, activebackground="#00BB27", activeforeground="#FFFFFF", height=1, width=8, command=lambda: self.btnSendClicked())
        btnSend.place(x=740, y=510)
        btnCancel = Button(canvas, text="CANCEL", bg="#E7464C", fg="#FFFFFF", bd=0, font=("Courier New", 16, "bold"),
                         relief=FLAT, activebackground="#E7464C", activeforeground="#FFFFFF", height=1, width=8, command=lambda: self.btnCancelClicked())
        btnCancel.place(x=870, y=510)

    def btnPrepareClicked(self):
        global sfname, slname, sNum, amountToSend, rfname, rlname, rNum, charge, totalAmount, control, dateKarun
        sfname = self.sfname.get()
        slname = self.slname.get()
        sNum = self.sNum.get()
        amounttosend = self.amountToSend.get()
        rfname = self.rfname.get()
        rlname = self.rlname.get()
        rNum = self.rNum.get()
        charge = 0
        totalAmount = 0
        amountToSend = 0
        control = ""
        dateKarun = date.today()
        # test if entries are blank
        notNull = True
        for i in (sfname, slname, sNum, amounttosend, rfname, rlname, rNum):
            if i == "":
                lblPrompt.config(text="Fill in blank info")
                notNull = False
                break
        if notNull:
            if self.testAmountNumber(amounttosend):
                amountToSend = float(amounttosend)
                if amountToSend <= 50000:
                    if amountToSend >= 1:
                        charge = self.Rates(float(amounttosend))
                        totalAmount = float(amounttosend) + charge
                        control = self.controlNumber()
                        lblControl.config(text=control)
                        lblCharge.config(text="Php %.2f" % (charge))
                        lblpayAmount.config(text="Php %.2f" % (totalAmount))
                        lblPrompt.config(text="")
                        self.readyToSend = True
                    else:
                        lblPrompt.config(text="Negative numbers are not allowed")
                        self.readyToSend = False
                else:
                    lblPrompt.config(text="Amount to be sent exceeded the limit")
                    self.readyToSend = False
            else:
                lblPrompt.config(text="Amount to be sent isn't a number")
                self.readyToSend = False
    def btnSendClicked(self):
        amountToPay = self.amountToPay.get()
        change = 0
        if amountToPay != "":
            if self.testAmountNumber(amountToPay):
                if self.readyToSend:
                    amountToPay = float(amountToPay)
                    if not amountToPay < totalAmount:
                        self.readyToSend = False
                        change = amountToPay - totalAmount
                        lblChange.config(text="Php %.2f" % (change))
                        lblPrompt.config(text="Successfully sent money")
                        sfirstname.delete(0, END)
                        slastname.delete(0, END)
                        sNumber.delete(0, END)
                        samount.delete(0, END)
                        rfirstname.delete(0, END)
                        rlastname.delete(0, END)
                        rNumber.delete(0, END)
                        payAmount.delete(0, END)
                        sfirstname.focus()
                        self.insertData()
                    else:
                        lblPrompt.config(text="Amount paid is invalid")
                else:
                    lblPrompt.config(text="Please Click Prepare")
            else:
                lblPrompt.config(text="Enter a valid amount")
        else:
            lblPrompt.config(text="Fill in blank info")
    def btnCancelClicked(self):
        self.readyToSend = False
        sfirstname.delete(0, END)
        slastname.delete(0, END)
        sNumber.delete(0, END)
        samount.delete(0, END)
        rfirstname.delete(0, END)
        rlastname.delete(0, END)
        rNumber.delete(0, END)
        payAmount.delete(0, END)
        lblPrompt.config(text="")
        lblControl.config(text="")
        lblCharge.config(text="")
        lblpayAmount.config(text="")
        sfirstname.focus()
    def voidUpdate(self):
        now = date.today()
        data = self.fetchData()
        for i in range(len(data)):
            expiryDate = data[i][13]
            dateobj = datetime.strptime(expiryDate, "%Y-%m-%d")
            exDate = dateobj.date()
            ctrl = data[i][6]
            if exDate < now:
                db = pymysql.connect("localhost", "root", "", "dblogin")
                cur = db.cursor()
                stat = "Void"
                sql = "UPDATE transactions SET Status = %s WHERE ControlNumber = %s"
                try:
                    cur.execute(sql, (stat, ctrl))
                    db.commit()
                except:
                    print("Error: unable to insert data")
                db.close()
    def insertData(self):
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cur = db.cursor()
        stat = "Unclaimed"
        dat = "None"
        now = date.today()
        edate = now + timedelta(7)

        sql = "INSERT INTO transactions(ID, SenderFirstname, SenderLastname, SenderNumber, ReceiverFirstname, ReceiverLastname, ReceiverNumber, ControlNumber, Date, Charge, Amount, TotalAmount, Status, ReceiveDate, ExpiryDate) VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cur.execute(sql, (sfname, slname, sNum, rfname, rlname, rNum, control, dateKarun, charge, amountToSend, totalAmount, stat, dat, edate))
            db.commit()
        except:
            print("Error: unable to insert data")
        db.close()

    def testAmountNumber(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False
    def fetchData(self):
        transactionData = []
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cursor = db.cursor()
        sql = "SELECT * FROM transactions"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subdata = []
                sfname = row[1]
                slname = row[2]
                sNum = row[3]
                rfname = row[4]
                rlname = row[5]
                rNum = row[6]
                cNum = row[7]
                date = row[8]
                charge = row[9]
                amount = row[10]
                totalamount = row[11]
                stat = row[12]
                rDate = row[13]
                eDate = row[14]
                for i in (sfname, slname, sNum, rfname, rlname, rNum, cNum, date, charge, amount, totalamount, stat, rDate, eDate):
                    subdata.append(i)
                transactionData.append(subdata)
        except:
            print("Error: unable to fetch data")
        db.close()
        return transactionData
    def controlNumber(self):
        data = self.fetchData()
        while True:
            rand = random.randrange(10000, 99999, 1)
            ctrl = "BOSS-" + str(rand)
            if self.linearSearch(data, 6, ctrl) == False:
                return ctrl
                break
    def linearSearch(self, data, key, ctrlNum):
        for i in range(len(data)):
            if data[i][key] == ctrlNum:
                return True
        return False
    def Rates(self, amount):
        rateList = [[1, 100, 2],
                [101, 300, 3],
                [301, 500, 8],
                [501, 700, 10],
                [701, 900, 12],
                [901, 1000, 15],
                [1001, 1500, 20],
                [1501, 2000, 30],
                [2001, 2500, 40],
                [2501, 3000, 50],
                [3001, 3500, 60],
                [3501, 4000, 70],
                [4001, 5000, 90],
                [5001, 7000, 115],
                [7001, 9500, 125],
                [9501, 10000, 140],
                [10001, 14000, 210],
                [14001, 15000, 220],
                [15001, 20000, 250],
                [20001, 30000, 290],
                [30001, 40000, 320],
                [40001, 50000, 345]]
        for i in range(len(rateList)):
            if amount >= rateList[i][0] and amount <= rateList[i][1]:
                rate = rateList[i][2]
                break
            else:
                rate = 0

        return float(rate)

class Receive(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, width=1058, height=613)
        self.parent = parent
        self.controller = controller
        self.ctrlNum = StringVar()
        self.foundkey = None
        self.Start()

    def Start(self):
        canvas = Canvas(self, width=1350, height=690)
        canvas.grid(row=0, column=0, sticky="nsew")
        img = Image.open("ReceiveFrame.png")
        canvas.image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=canvas.image, anchor="nw")

        global lblProm, controlNumber, btnSearch, btnClaim, btnCancel, lblsFirstname, lblsLastname, lblsNumber, lblrFirstname, lblrLastname, lblrNumber, lblAmountToReceive, lblcFirstname, lblcLastname, lblDate, lblStatus
        controlNumber = Entry(canvas, width=30, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949", textvariable=self.ctrlNum)
        controlNumber.place(x=85, y=53)

        btnSearch = Button(canvas, text="SEARCH", bg="#F99B00", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                            relief=FLAT, activebackground="#F99B00", activeforeground="#FFFFFF", height=1, width=8, command=lambda:self.btnSearchClicked())
        btnSearch.place(x=385, y=50)
        btnClaim = Button(canvas, text="CLAIM", bg="#00BB27", fg="#FFFFFF", bd=0, font=("Courier New", 16, "bold"),
                         relief=FLAT, activebackground="#00BB27", activeforeground="#FFFFFF", height=1, width=8, command=lambda: self.btnClaimClicked())
        btnClaim.place(x=660, y=448)
        btnCancel = Button(canvas, text="CANCEL", bg="#E7464C", fg="#FFFFFF", bd=0, font=("Courier New", 16, "bold"),
                           relief=FLAT, activebackground="#E7464C", activeforeground="#FFFFFF", height=1, width=8, command=lambda: self.btnCancelClicked())
        btnCancel.place(x=810, y=448)

        lblsFirstname = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblsFirstname.place(x=90, y=168)
        lblsLastname = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblsLastname.place(x=90, y=225)
        lblsNumber = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblsNumber.place(x=90, y=280)

        lblrFirstname = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblrFirstname.place(x=90, y=415)
        lblrLastname = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblrLastname.place(x=90, y=472)
        lblrNumber = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblrNumber.place(x=90, y=529)

        lblAmountToReceive = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblAmountToReceive.place(x=600, y=120)
        lblStatus = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblStatus.place(x=870, y=120)
        lblcFirstname = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblcFirstname.place(x=600, y=236)
        lblcLastname = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblcLastname.place(x=600, y=304)
        lblDate = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblDate.place(x=600, y=370)
        lblProm = Label(canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 16, "bold"))
        lblProm.place(x=660, y=510)

    def btnSearchClicked(self):
        global data, key, ctrl, found
        ctrl = self.ctrlNum.get()
        data = self.fetchData()
        key = self.linearSearch(data, 6, ctrl)
        found = False
        if key:
            lblsFirstname.config(text=data[self.foundkey][0])
            lblsLastname.config(text=data[self.foundkey][1])
            lblsNumber.config(text=data[self.foundkey][2])
            lblrFirstname.config(text=data[self.foundkey][3])
            lblrLastname.config(text=data[self.foundkey][4])
            lblrNumber.config(text=data[self.foundkey][5])
            lblAmountToReceive.config(text="Php %.2f" % data[self.foundkey][9])
            lblStatus.config(text=data[self.foundkey][11])
            found = True
        else:
            if ctrl == "":
                lblProm.config(text="Fill in control number")
            else:
                lblProm.config(text="Invalid Control Number")
    def btnClaimClicked(self):
        ctr = self.ctrlNum.get()
        if found:
            if data[self.foundkey][11] != "Void":
                if data[self.foundkey][11] == "Unclaimed":
                    lblsFirstname.config(text="")
                    lblsLastname.config(text="")
                    lblsNumber.config(text="")
                    lblrFirstname.config(text="")
                    lblrLastname.config(text="")
                    lblrNumber.config(text="")
                    lblAmountToReceive.config(text="")
                    lblStatus.config(text="")
                    self.updateData()
                    lblcFirstname.config(text=data[self.foundkey][3])
                    lblcLastname.config(text=data[self.foundkey][4])
                    lblDate.config(text=dateNow)
                    lblProm.config(text="Money claimed successfully")
                else:
                    lblProm.config(text="Money already claimed")
            else:
                lblProm.config(text="Transaction already expired")
        else:
            if ctr == "":
                lblProm.config(text="Fill in control number")
            else:
                lblProm.config(text="Invalid Control Number")
            lblsFirstname.config(text="")
            lblsLastname.config(text="")
            lblsNumber.config(text="")
            lblrFirstname.config(text="")
            lblrLastname.config(text="")
            lblrNumber.config(text="")
            lblAmountToReceive.config(text="")
            lblStatus.config(text="")
            self.found = False
    def btnCancelClicked(self):
        controlNumber.delete(0, END)
        lblsFirstname.config(text="")
        lblsLastname.config(text="")
        lblsNumber.config(text="")
        lblrFirstname.config(text="")
        lblrLastname.config(text="")
        lblrNumber.config(text="")
        lblAmountToReceive.config(text="")
        lblStatus.config(text="")
        lblcFirstname.config(text="")
        lblcLastname.config(text="")
        lblDate.config(text="")
        lblProm.config(text="")
        self.found = False

    def updateData(self):
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cur = db.cursor()
        status = "Claimed"
        global dateNow
        dateNow = date.today()

        sql = "UPDATE transactions SET Status = %s WHERE ControlNumber = %s"
        sql2 = "UPDATE transactions SET ReceiveDate = %s WHERE ControlNumber = %s"
        try:
            cur.execute(sql, (status, ctrl))
            cur.execute(sql2, (dateNow, ctrl))
            db.commit()
        except:
            print("Error: unable to update data")
        db.close()

    def linearSearch(self, data, key, ctrlNum):
        for i in range(len(data)):
            if data[i][key] == ctrlNum:
                self.foundkey= i
                return True
        return False
    def fetchData(self):
        transactionData = []
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cursor = db.cursor()
        sql = "SELECT * FROM transactions"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subdata = []
                sfname = row[1]
                slname = row[2]
                sNum = row[3]
                rfname = row[4]
                rlname = row[5]
                rNum = row[6]
                cNum = row[7]
                date = row[8]
                charge = row[9]
                amount = row[10]
                totalamount = row[11]
                stat = row[12]
                rDate = row[13]
                eDate = row[14]
                for i in (sfname, slname, sNum, rfname, rlname, rNum, cNum, date, charge, amount, totalamount, stat, rDate, eDate):
                    subdata.append(i)
                transactionData.append(subdata)
        except:
            print("Error: unable to fetch data")
        db.close()
        return transactionData
class viewClaimed(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, width=1058, height=613, bg="#FFFFFF")
        self.parent = parent
        self.controller = controller
        self.st = ttk.Style()
        self.Start()
    def Start(self):
        self.data = self.fetchData()
        self.tree = ttk.Treeview(self, columns=("Sender", "Receiver", "Amount"))
        self.tree.heading('#0', text='Sender')
        self.tree.heading('#1', text='Receiver')
        self.tree.heading('#2', text='Amount')
        self.tree.heading('#3', text='Control Number')
        self.tree.column("#0", width=264)
        self.tree.column("#1", width=264)
        self.tree.column("#2", width=264)
        self.tree.column("#3", width=245)
        self.tree.grid(row=0, column=0)
        self.st.configure("Treeview", rowheight=54, highlightthickness=0 )
        self.st.configure("Treeview.Heading", font=('Calibri', 15,'bold'))
        ysb = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        ysb.place(x=1041, y=0, height=568)
        self.tree.configure(yscrollcommand=ysb.set)
        btnRef = Button(self, text="REFRESH", bg="#00BB27", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                        relief=FLAT, activebackground="#00BB27", activeforeground="#FFFFFF", height=1, width=8,
                        command=lambda: self.refresh())
        btnRef.place(x=490, y=575)

        for i in range(len(self.data)):
            sender = self.data[i][0] + " " + self.data[i][1]
            rec = self.data[i][3] + " " + self.data[i][4]
            amount = self.data[i][9]
            ctrl = self.data[i][6]
            if self.data[i][11] == "Claimed":
                self.tree.insert("", "end", text=sender, values=(rec, amount, ctrl))
    def refresh(self):
        self.tree.destroy()
        self.Start()
    def fetchData(self):
        transactionData = []
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cursor = db.cursor()
        sql = "SELECT * FROM transactions"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subdata = []
                sfname = row[1]
                slname = row[2]
                sNum = row[3]
                rfname = row[4]
                rlname = row[5]
                rNum = row[6]
                cNum = row[7]
                date = row[8]
                charge = row[9]
                amount = row[10]
                totalamount = row[11]
                stat = row[12]
                rDate = row[13]
                eDate = row[14]
                for i in (sfname, slname, sNum, rfname, rlname, rNum, cNum, date, charge, amount, totalamount, stat, rDate, eDate):
                    subdata.append(i)
                transactionData.append(subdata)
        except:
            print("Error: unable to fetch data")
        db.close()
        return transactionData
class viewUnclaimed(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, width=1058, height=613, bg="#FFFFFF")
        self.parent = parent
        self.controller = controller
        self.st = ttk.Style()
        self.sfname = StringVar()
        self.slname = StringVar()
        self.sNum = StringVar()
        self.amountToSend = StringVar()
        self.rfname = StringVar()
        self.rlname = StringVar()
        self.rNum = StringVar()
        self.ctrlNum = StringVar()
        self.foundkey = None
        self.found = False
        self.Start()

    def Start(self):
        self.data = self.fetchData()
        self.tree = ttk.Treeview(self, columns=("Sender", "Receiver", "Amount"))
        self.tree.heading('#0', text='Sender')
        self.tree.heading('#1', text='Receiver')
        self.tree.heading('#2', text='Amount')
        self.tree.heading('#3', text='Control Number')
        self.tree.column("#0", width=264)
        self.tree.column("#1", width=264)
        self.tree.column("#2", width=264)
        self.tree.column("#3", width=245)
        self.tree.grid(row=0, column=0)
        self.st.configure("Treeview", rowheight=54, highlightthickness=0)
        self.st.configure("Treeview.Heading", font=('Calibri', 15, 'bold'))
        ysb = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        ysb.place(x=1041, y=0, height=568)
        self.tree.configure(yscrollcommand=ysb.set)
        btnRef = Button(self, text="REFRESH", bg="#00BB27", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                        relief=FLAT, activebackground="#00BB27", activeforeground="#FFFFFF", height=1, width=8,
                        command=lambda: self.refresh())
        btnRef.place(x=430, y=575)
        btnUpdate = Button(self, text="UPDATE", bg="#E7464C", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                        relief=FLAT, activebackground="#E7464C", activeforeground="#FFFFFF", height=1, width=8,
                        command=lambda: self.updateData())
        btnUpdate.place(x=550, y=575)

        for i in range(len(self.data)):
            sender = self.data[i][0] + " " + self.data[i][1]
            rec = self.data[i][3] + " " + self.data[i][4]
            amount = self.data[i][9]
            ctrl = self.data[i][6]
            if self.data[i][11] == "Unclaimed":
                self.tree.insert("", "end", text=sender, values=(rec, amount, ctrl))
    def updateData(self):
        self.tree.destroy()
        self.canvas = Canvas(self, width=1350, height=690)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        img = Image.open("UpdateFrame.png")
        self.canvas.image = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")

        global sfirstname, slastname, sNumber, samount, rfirstname, rlastname, rNumber, lblProm

        sfirstname = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                           textvariable=self.sfname)
        sfirstname.place(x=77, y=137)
        slastname = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                          textvariable=self.slname)
        slastname.place(x=77, y=192)
        sNumber = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                        textvariable=self.sNum)
        sNumber.place(x=77, y=246)
        samount = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                        textvariable=self.amountToSend)
        samount.place(x=77, y=299)

        rfirstname = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                           textvariable=self.rfname)
        rfirstname.place(x=77, y=435)
        rlastname = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                          textvariable=self.rlname)
        rlastname.place(x=77, y=490)
        rNumber = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                        textvariable=self.rNum)
        rNumber.place(x=77, y=543)
        ctrlNum = Entry(self.canvas, width=41, font=("Arial", 12), relief=FLAT, bg="#F9F4F4", fg="#494949",
                        textvariable=self.ctrlNum)
        ctrlNum.place(x=561, y=94)
        btnSearch = Button(self.canvas, text="SEARCH", bg="#F99B00", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                           relief=FLAT, activebackground="#F99B00", activeforeground="#FFFFFF", height=1, width=8,
                           command=lambda: self.btnSearchClicked())
        btnSearch.place(x=559, y=140)
        btnSave = Button(self.canvas, text="SAVE", bg="#00BB27", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                           relief=FLAT, activebackground="#00BB27", activeforeground="#FFFFFF", height=1, width=8,
                           command=lambda: self.btnSaveClicked())
        btnSave.place(x=708, y=140)
        btnCancel = Button(self.canvas, text="BACK", bg="#E7464C", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                           relief=FLAT, activebackground="#E7464C", activeforeground="#FFFFFF", height=1, width=8,
                           command=lambda: self.btnCancelClicked())
        btnCancel.place(x=852, y=140)

        lblProm = Label(self.canvas, text="", bg="#F9F4F4", fg="#494949", font=("Arial", 18, "bold"))
        lblProm.place(x=559, y=200)
    def refresh(self):
        self.tree.destroy()
        self.Start()
    def btnSearchClicked(self):
        global data, key, ctrl
        ctrl = self.ctrlNum.get()
        data = self.fetchData()
        key = self.linearSearch(data, 6, ctrl)
        if key:
            sfirstname.delete(0, END)
            slastname.delete(0, END)
            sNumber.delete(0, END)
            samount.delete(0, END)
            rfirstname.delete(0, END)
            rlastname.delete(0, END)
            rNumber.delete(0, END)
            sfirstname.insert(0, data[self.foundkey][0])
            slastname.insert(0, data[self.foundkey][1])
            sNumber.insert(0, data[self.foundkey][2])
            samount.insert(0, data[self.foundkey][9])
            rfirstname.insert(0, data[self.foundkey][3])
            rlastname.insert(0, data[self.foundkey][4])
            rNumber.insert(0, data[self.foundkey][5])
            self.found = True
        else:
            lblProm.config(text="Transaction not found or already claimed")
    def linearSearch(self, data, key, ctrlNum):
        for i in range(len(data)):
            if data[i][key] == ctrlNum and data[i][11] == "Unclaimed":
                self.foundkey= i
                return True
        return False
    def btnCancelClicked(self):
        sfirstname.delete(0, END)
        slastname.delete(0,END)
        sNumber.delete(0, END)
        samount.delete(0, END)
        rfirstname.delete(0, END)
        rlastname.delete(0, END)
        rNumber.delete(0, END)
        self.canvas.destroy()
        self.Start()
    def btnSaveClicked(self):
        control = self.ctrlNum.get()
        sfname = self.sfname.get()
        slname = self.slname.get()
        sNum = self.sNum.get()
        amounttosend = self.amountToSend.get()
        rfname = self.rfname.get()
        rlname = self.rlname.get()
        rNum = self.rNum.get()
        if self.found and(sfname != "" and slname != "" and sNum != "" and amounttosend != "" and rfname != "" and rlname != "" and rNum != ""):

            db = pymysql.connect("localhost", "root", "", "dblogin")

            cur = db.cursor()
            sql = "UPDATE transactions SET SenderFirstname = %s, SenderLastname = %s, SenderNumber = %s, ReceiverFirstname = %s, ReceiverLastname = %s, ReceiverNumber = %s, Amount = %s WHERE ControlNumber = %s"
            try:
                cur.execute(sql, (sfname, slname, sNum, rfname, rlname, rNum, amounttosend, control))
                db.commit()
                lblProm.config(text="Successfully updated transaction")
            except:
                print("Error: unable to update data")
            db.close()
            self.found = False
        else:
            if sfname == "" or slname == "" or sNum == "" or amounttosend == "" or rfname == "" or rlname == "" or rNum == "":
                lblProm.config(text="Fill in blank info")
            else:
                lblProm.config(text="Please click search")
    def fetchData(self):
        transactionData = []
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cursor = db.cursor()
        sql = "SELECT * FROM transactions"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subdata = []
                sfname = row[1]
                slname = row[2]
                sNum = row[3]
                rfname = row[4]
                rlname = row[5]
                rNum = row[6]
                cNum = row[7]
                date = row[8]
                charge = row[9]
                amount = row[10]
                totalamount = row[11]
                stat = row[12]
                rDate = row[13]
                eDate = row[14]
                for i in (sfname, slname, sNum, rfname, rlname, rNum, cNum, date, charge, amount, totalamount, stat,rDate, eDate):
                    subdata.append(i)
                transactionData.append(subdata)
        except:
            print("Error: unable to fetch data")
        db.close()
        return transactionData

class viewReport(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, width=1058, height=613, bg="#FFFFFF")
        self.parent = parent
        self.controller = controller
        self.st = ttk.Style()
        self.searchD = StringVar()
        self.displayAll()
    def Tree(self):
        self.data = self.fetchData()
        self.tree = ttk.Treeview(self, columns=("Sender", "Receiver", "Amount", "Control Number", "Send Date", "Receive Date", "Expiry Date", "Status"))
        self.tree.heading('#0', text='Sender')
        self.tree.heading('#1', text='Receiver')
        self.tree.heading('#2', text='Amount')
        self.tree.heading('#3', text='Control No.')
        self.tree.heading('#4', text='Send Date')
        self.tree.heading('#5', text='Receive Date')
        self.tree.heading('#6', text='Expiry Date')
        self.tree.heading('#7', text='Status')
        self.tree.column("#0", width=130)
        self.tree.column("#1", width=130)
        self.tree.column("#2", width=130)
        self.tree.column("#3", width=129)
        self.tree.column("#4", width=129)
        self.tree.column("#5", width=129)
        self.tree.column("#6", width=129)
        self.tree.column("#7", width=129)
        self.tree.grid(row=0, column=0)
        self.st.configure("Treeview", rowheight=54, highlightthickness=0)
        self.st.configure("Treeview.Heading", font=('Calibri', 15, 'bold'))
        ysb = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        ysb.place(x=1041, y=0, height=568)
        self.tree.configure(yscrollcommand=ysb.set)
    def Start(self):
        global lblsearchDate, searchDate, btnSearch, btnRef, lblError
        lblsearchDate = Label(self, text="Search by date (yyyy-mm-dd): ", font=("Arial", 12), bg="#FFFFFF", fg="#494949")
        lblsearchDate.place(x=150, y=576)
        searchDate = Entry(self, width=30, font=("Arial", 12), bg="#F9F4F4", fg="#494949",
                           textvariable=self.searchD)
        searchDate.place(x=360, y=579)

        btnSearch = Button(self, text="SEARCH", bg="#F99B00", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                        relief=FLAT, activebackground="#F99B00", activeforeground="#FFFFFF", height=1, width=8,
                        command=lambda: self.searchbyDate(self.searchD.get()))
        btnSearch.place(x=650, y=575)
        btnRef = Button(self, text="REFRESH", bg="#00BB27", fg="#FFFFFF", bd=0, font=("Courier New", 12, "bold"),
                        relief=FLAT, activebackground="#00BB27", activeforeground="#FFFFFF", height=1, width=8,
                        command=lambda: self.refresh())
        btnRef.place(x=750, y=575)
        lblError = Label(self, text="", font=("Arial", 10), bg="#FFFFFF",
                              fg="#494949")
        lblError.place(x=850, y=576)

    def displayAll(self):
        self.Tree()
        self.Start()
        for i in range(len(self.data)):
            sender = self.data[i][0] + " " + self.data[i][1]
            rec = self.data[i][3] + " " + self.data[i][4]
            amount = self.data[i][9]
            ctrl = self.data[i][6]
            sdate = self.data[i][7]
            stat = self.data[i][11]
            rdate = self.data[i][12]
            edate = self.data[i][13]
            self.tree.insert("", "end", text=sender, values=(rec, amount, ctrl, sdate, rdate, edate, stat))

    def searchbyDate(self, date):
        self.tree.destroy()
        lblsearchDate.destroy()
        btnSearch.destroy()
        searchDate.destroy()
        btnRef.destroy()
        lblError.destroy()
        self.Tree()
        self.Start()
        isTrue = False

        for i in range(len(self.data)):
            if date == self.data[i][7]:
                sender = self.data[i][0] + " " + self.data[i][1]
                rec = self.data[i][3] + " " + self.data[i][4]
                amount = self.data[i][9]
                ctrl = self.data[i][6]
                sdate = self.data[i][7]
                stat = self.data[i][11]
                rdate = self.data[i][12]
                edate = self.data[i][13]
                self.tree.insert("", "end", text=sender, values=(rec, amount, ctrl, sdate, rdate, edate, stat))
                isTrue = True
                lblError.config(text="")
        else:
            if date == "":
                lblError.config(text="Please enter date")
            elif len(date) < 10 or len(date) > 10:
                lblError.config(text="Invalid date")
            elif isTrue is False:
                lblError.config(text="Date not found")

    def refresh(self):
        searchDate.delete(0, END)
        self.tree.destroy()
        lblsearchDate.destroy()
        btnSearch.destroy()
        btnRef.destroy()
        lblError.destroy()
        searchDate.destroy()
        self.displayAll()

    def fetchData(self):
        transactionData = []
        db = pymysql.connect("localhost", "root", "", "dblogin")
        cursor = db.cursor()
        sql = "SELECT * FROM transactions"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                subdata = []
                sfname = row[1]
                slname = row[2]
                sNum = row[3]
                rfname = row[4]
                rlname = row[5]
                rNum = row[6]
                cNum = row[7]
                date = row[8]
                charge = row[9]
                amount = row[10]
                totalamount = row[11]
                stat = row[12]
                rDate = row[13]
                eDate = row[14]
                for i in (sfname, slname, sNum, rfname, rlname, rNum, cNum, date, charge, amount, totalamount, stat, rDate, eDate):
                    subdata.append(i)
                transactionData.append(subdata)
        except:
            print("Error: unable to fetch data")
        db.close()
        return transactionData


app = App()
app.geometry("1350x690")
app.title("Money Padala")
app.resizable(False, False)
app.mainloop()
