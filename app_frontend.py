import tkinter as tk
import customtkinter as Ctk
from tkinter import ttk
from tkinter import messagebox
import flights_backend as fbe
import passengers_backend as pbe
import os




def clear_frame(root):
    for widget in root.winfo_children():
        widget.destroy()

class Starting_window():
    def __init__(self, master=None):
        # Constructor for the greeting window
        self.root = master
        self.root.title("Flight Database")
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        self.root.geometry(f"{window_width//3}x{window_height//2}")
        self.root.resizable(width=False, height=False)
        

        if not os.path.isfile("Databases/flights.db"):
            fbe.init_db()
        if not os.path.isfile("Databases/passengers.db"):
            pbe.init_db()

        # Frame
        main_frame = Ctk.CTkFrame(master=self.root)
        main_frame.pack(fill='both', expand=True)
        
 
        title_frame = Ctk.CTkFrame(main_frame, fg_color='transparent')
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0,weight=1)
        title_frame.pack(padx=60)

        query_frame = Ctk.CTkFrame(main_frame, height=200,  fg_color="transparent", border_color="#065e99", border_width=3)
        # query_frame.columnconfigure(0, weight=1)
        # query_frame.columnconfigure(1, weight=1)
        # query_frame.rowconfigure(0, weight=1)
        # query_frame.rowconfigure(1, weight=2)
        query_frame.pack(fill='both', expand=True , padx = 60 , pady=10)

        action_frame = Ctk.CTkFrame(main_frame, height=150, fg_color='transparent')
        # action_frame.columnconfigure(0, weight=5)
        # action_frame.columnconfigure(1, weight=1)
        # action_frame.columnconfigure(2, weight=1)
        action_frame.pack(side='bottom', fill='x')

        # Labels
        self.lbl_title = Ctk.CTkLabel(master=title_frame, text="Flight Enquiry System", font=("Arial", 30))
        self.lbl_title.grid(row=0, column=0, padx=20, pady=20, sticky='nwes')

    
        self.query_title = Ctk.CTkLabel(query_frame, text="What would you like to enquire about?", font=("Arial", 20))
        # self.query_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.query_title.place( anchor="center", relx=0.5, rely=0.2)

        self.v = Ctk.StringVar(query_frame, 'None')
        self.rdiobtn_flight = Ctk.CTkRadioButton(query_frame, text="Flights", value='F', variable=self.v)
        self.rdiobtn_flight.place(anchor="center", relx=0.2, rely=0.6)

        self.rdiobtn_passengers = Ctk.CTkRadioButton(query_frame, text="Passengers", value='P', variable=self.v)
        self.rdiobtn_passengers.place(anchor="center", relx=0.7, rely=0.6)        

        # Buttons
        # self.btn_exit = tk.Button(action_frame, text='Quit', font='Arial 12', command=self.on_closing)
        # self.btn_exit.pack(side='right', fill='y')
        # self.btn_done = tk.Button(action_frame, text='Next', font='Arial 12', command=self.on_done)
        # self.btn_done.pack(side='right', fill='y')

        self.btn_exit = Ctk.CTkButton(action_frame, text='Quit', fg_color="#065e99", border_color="#065e99" , border_width=2, hover_color="#065e99", command=self.on_closing)
        self.btn_exit.place( anchor="center", relx=0.3, rely=0.5)
        self.btn_done = Ctk.CTkButton(action_frame, text='Next',fg_color="#065e99", border_color="#065e99", border_width=2,hover_color="#065e99", command=self.on_done)
        self.btn_done.place( anchor="center", relx=0.7, rely=0.5)

        # Protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Function handling the closing window
        if messagebox.askyesno(title="Quit?", message="Do you want to quit?"):
            self.root.destroy()

    def on_done(self):
        # Function handling actions after pressing done
        if self.v.get()=='None':
            messagebox.showinfo(title="Help", message="Choose one of the options!")
        elif self.v.get()=='F':
            clear_frame(self.root)
            flight_window = Flight_window(self.root)
        elif self.v.get()=='P':
            clear_frame(self.root)
            passenger_window = Passenger_window(self.root)


class Flight_window(Starting_window):
    def __init__(self, master):
        self.root = master
        self.root.title("Flights Enquiry Database")
        self.root.geometry("1260x1260")
        self.root.resizable(width=True, height=True)
        # Your Flight_window code here...
        FlightNo=tk.StringVar()
        Day=tk.StringVar()
        Month=tk.StringVar()
        Year=tk.StringVar()
        SchedDeptTime=tk.StringVar()
        SchedArrTime=tk.StringVar()
        Origin=tk.StringVar()
        Dest=tk.StringVar()
        Tailnum=tk.StringVar()
        CarrierShort=tk.StringVar()
        CarrierName=tk.StringVar()
        headers=['FlightNo', 'Date_Index', 'Scheduled_Dept_Time', 'Dept_Time', 'Scheduled_Arr_Time', 'Arr_Time', 'Air_Time', 'Origin', 'Destination', 'Tail No', 'Day', 'Month', 'Year', 'Carrier_Short', 'Carrier_Name']
        DataList = [FlightNo,Day,Month,Year,SchedDeptTime,SchedArrTime,Origin,Dest,Tailnum,CarrierShort,CarrierName]
        ColNameList = ['flightno', 'day', 'month', 'year', 'scheduled_dept_time', 'scheduled_arr_time', 'origin', 'dest', 'tailnum', "carrier_name", 'full_name']
        
        def viewflightdb():
            for row in fbe.ViewAllData():
                tree.insert('', tk.END, values=row)
        
        def searchflightdb():
            tree.delete(*tree.get_children())
            SearchTerm = {}
            for Name, Data in zip(ColNameList, DataList):
                if Data.get()!='':
                    SearchTerm[Name] = Data.get()
            for row in fbe.SearchForData(SearchTerm):
                tree.insert('', tk.END, values=row)
        
        def flightdatafill(event):
            selected_item = tree.selection()[0]
            info_to_show = 'Data in Record:\n' + '\n'.join([str(a)+": "+str(b) for a, b in zip(headers, tree.item(selected_item)['values'])])
            messagebox.showinfo(title="Selected Record", message=info_to_show)


        # Frames
        main_frame = Ctk.CTkFrame(self.root)
        main_frame.pack(fill='both', expand=True)

        title_frame = Ctk.CTkFrame(main_frame)
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0,weight=1)
        title_frame.pack(fill='x')

        data_frame = Ctk.CTkFrame(main_frame)
        #customtkinter.set_appearance_mode("dark")
        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=7)
        data_frame.rowconfigure(0, weight=1)
        data_frame.pack(fill='both', expand=True)
        data_frame_left = Ctk.CTkFrame(data_frame, width=100, border_color="#065e99", border_width=3 )#bg='white',borderwidth=2, relief='solid'
        #data_frame_left.place( anchor="center", relx=0.5, rely=0.2)

        data_frame_right = Ctk.CTkFrame(data_frame, width=200)
        data_frame_right.grid(row=0, column=1, sticky='nwes', padx=(10, 0))
        data_frame_right.columnconfigure(0, weight=1)  # Set weight of the first column
        data_frame_right.rowconfigure(0, weight=5)  # Set weight of the first row
        data_frame_left.grid(row=0, column=0, sticky='nwes',padx=(10, 0),pady=(10,0))
        # data_frame_right.grid(row=0, column=1, sticky='nwes',padx=(10, 0),pady=(10,0))

        # btn_frame = tk.Frame(main_frame)
        # btn_frame.pack(fill='x', expand=True, side='bottom')

       
        # Labels and Entryboxes
        self.lblTitle = Ctk.CTkLabel(title_frame, text="Flight Enquiry System", font=('Arial', 40),text_color='white',fg_color='#065e99')
        self.lblTitle.grid(row=0, column=0, sticky='nwes' )
        
        # self.lblLeftTitle = tk.Label(data_frame_left, text="Left Portion Title", font='Arial 12 ', fg='black', bg='white')
        # self.lblLeftTitle.grid( row=0, column=0,sticky='w',padx=10)

        # self.lblRightTitle = tk.Label(data_frame_right, text="Right Portion Title", font='Arial 12 bold', fg='black', bg='white')
        # self.lblRightTitle.grid( row=0, column=0,sticky='nesw')

        self.lblFlightno = Ctk.CTkLabel(data_frame_left, text="Flight No: ", pady=3, font=('Arial', 15) )
        self.lblFlightno.grid(row=1, column=0, sticky='w',padx=10,pady=(30,0))
        self.txtFlightno = Ctk.CTkEntry(data_frame_left, textvariable=FlightNo, height= 20,width=200, font=('Helvetica', 15))#, bg='#EEEEEE', fg='black', bd=0.5, relief='solid'
        self.txtFlightno.grid(row=1, column=1, padx=0, pady=(30,0))

        self.lblDay = Ctk.CTkLabel(data_frame_left, text="Day: ", padx=5, pady=3, font=('Arial', 15))
        self.lblDay.grid(row=2, column=0, sticky='w',padx=10) 
        self.txtDay = Ctk.CTkEntry(data_frame_left, textvariable=Day, height= 20,width=200, font=('Helvetica', 15))
        self.txtDay.grid(row=2, column=1, padx=5, pady=3)

        self.lblMonth = Ctk.CTkLabel(data_frame_left, text="Month: ", padx=5, pady=3, font=('Arial', 15))
        self.lblMonth.grid(row=3, column=0, sticky='w',padx=10)
        self.txtMonth = Ctk.CTkEntry(data_frame_left, textvariable=Month, height= 20,width=200, font=('Helvetica', 15))
        self.txtMonth.grid(row=3, column=1, padx=5, pady=3)

        self.lblYear = Ctk.CTkLabel(data_frame_left, text="Year: ", padx=5, pady=3, font=('Arial', 15))
        self.lblYear.grid(row=4, column=0, sticky='w',padx=10)
        self.txtYear = Ctk.CTkEntry(data_frame_left, textvariable=Year, height= 20,width=200, font=('Helvetica', 15))
        self.txtYear.grid(row=4, column=1, padx=5, pady=3)

        self.lblSchedDeptTime = Ctk.CTkLabel(data_frame_left, text="Scheduled Dept Time: ", padx=5, pady=3, font=('Arial', 15))
        self.lblSchedDeptTime.grid(row=5, column=0, sticky='w',padx=10)
        self.txtSchedDeptTime = Ctk.CTkEntry(data_frame_left, textvariable=SchedDeptTime, height= 20,width=200, font=('Helvetica', 15))
        self.txtSchedDeptTime.grid(row=5, column=1, padx=5, pady=3)

        self.lblSchedArrTime = Ctk.CTkLabel(data_frame_left, text="Scheduled Arrival Time: ", padx=5, pady=3, font=('Arial', 15))
        self.lblSchedArrTime.grid(row=6, column=0, sticky='w',padx=10)
        self.txtSchedArrTime = Ctk.CTkEntry(data_frame_left, textvariable=SchedArrTime, height= 20,width=200, font=('Helvetica', 15))
        self.txtSchedArrTime.grid(row=6, column=1, padx=5, pady=3)

        self.lblOrigin = Ctk.CTkLabel(data_frame_left, text="Origin: ", padx=5, pady=3, font=('Arial', 15))
        self.lblOrigin.grid(row=7, column=0, sticky='w',padx=10)
        self.txtOrigin = Ctk.CTkEntry(data_frame_left, textvariable=Origin, height= 20,width=200, font=('Helvetica', 15))
        self.txtOrigin.grid(row=7, column=1, padx=5, pady=3)

        self.lblDest = Ctk.CTkLabel(data_frame_left, text="Destination: ", padx=5, pady=3, font=('Arial', 15))
        self.lblDest.grid(row=8, column=0, sticky='w',padx=10)
        self.txtDest = Ctk.CTkEntry(data_frame_left, textvariable=Dest, height= 20,width=200, font=('Helvetica', 15))
        self.txtDest.grid(row=8, column=1, padx=5, pady=3)

        self.lblTailnum = Ctk.CTkLabel(data_frame_left, text="Tail Number: ", padx=5, pady=3, font=('Arial', 15))
        self.lblTailnum.grid(row=9, column=0, sticky='w',padx=10)
        self.txtTailnum = Ctk.CTkEntry(data_frame_left, textvariable=Tailnum, height= 20,width=100, font=('Helvetica', 15))
        self.txtTailnum.grid(row=9, column=1, padx=5, pady=3)

        self.lblCarrierShort = Ctk.CTkLabel(data_frame_left, text="Carrier Shortform: ", padx=5, pady=3, font=('Arial', 15))

       
        tree = ttk.Treeview(data_frame_right, columns=headers, show='headings')
        tree.grid(row=0, column=0, sticky='nesw')
        tree.bind("<<TreeviewSelect>>", flightdatafill)
        data_frame_right.columnconfigure(0, weight=1)  # Set weight of the first column

        # Set width of each column to 40
        for col in headers:
            tree.heading(col, text=col, anchor=tk.CENTER)
            tree.column(col, width=20, anchor=tk.CENTER)

        # Add vertical scrollbar to the treeview
        sb_vertical = ttk.Scrollbar(data_frame_right, orient='vertical', command=tree.yview)
        sb_vertical.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=sb_vertical.set)


       # Buttons
        self.btnSearch = Ctk.CTkButton(data_frame_left, text="Search",width=25 ,command=searchflightdb,fg_color="#065e99", border_color="#065e99" , border_width=2, hover_color="#065e99")
        self.btnSearch.place( anchor="center", relx=0.3, rely=0.5) # Adjust row and column as needed
        self.btnDisplay = Ctk.CTkButton(data_frame_left, text='Display All',width=15, command=viewflightdb, fg_color="#065e99", border_color="#065e99" , border_width=2, hover_color="#065e99")
        self.btnDisplay.place( anchor="center", relx=0.5, rely=0.5)  # Adjust row and column as needed
        self.btnBack = Ctk.CTkButton(
            data_frame_left,
            text="Go Back",
            width=15,
            command=self.backFunction,
            fg_color="#065e99",
            border_color="#065e99",
            border_width=2,
            hover_color="#065e99",
        )
        self.btnBack.place(anchor="center", relx=0.7, rely=0.5)
    
    def backFunction(self):
        # Function handling actions after pressing back
        clear_frame(self.root)
        Starting_window(self.root)


class Passenger_window(Starting_window):
    def __init__(self, master):
        self.root = master
        self.root.title("Passengers Enquiry Database")
        self.root.geometry("1260x1260")
        self.root.resizable(width=True, height=True)
        
        PassengerId = tk.StringVar()
        FName = tk.StringVar()
        LName = tk.StringVar()
        Gender = tk.StringVar()
        Age = tk.StringVar()
        Nationality = tk.StringVar()
        CountryCode = tk.StringVar()
        CountryName = tk.StringVar()
        AirportCode = tk.StringVar()
        AirportName = tk.StringVar()
        DepartureDate = tk.StringVar()
        ContinentCode = tk.StringVar()
        ContinentName = tk.StringVar()

        headers = ['PassengerId', 'FName', 'Lname', 'Gender', 'Age', 'Nationality', 'Airport_Code', 'Departure_Date', 'Pilot_Name', 'Flight_status', 'Airport_name', 'Country_Code', 'Country_Name', 'Continent_Code', 'Continent_Name']
        DataList = [PassengerId, FName, LName, Gender, Age, Nationality, CountryCode, CountryName, AirportCode, AirportName, DepartureDate, ContinentCode, ContinentName]
        ColNameList = ['id', 'fname', 'lname', 'gender', 'age', 'nationality', 'country_code', 'country_name', 'airport_code', 'airport_name', 'departure_date', 'continent_code', 'continent_name']

        def viewpassengersdb():
            for row in pbe.ViewAllPassengers():
                tree.insert('', tk.END, values=row)
        
        def searchpassengersdb():
            tree.delete(*tree.get_children())
            SearchTerm = {}
            for Name, Data in zip(ColNameList, DataList):
                if Data.get() != '':
                    SearchTerm[Name] = Data.get()
            for row in pbe.SearchPassenger(SearchTerm):
                tree.insert('', tk.END, values=row)
        
        def passengersdatafill(event):
            selected_item = tree.selection()[0]
            info_to_show = 'Data in Record:\n' + '\n'.join([str(a) + ": " + str(b) for a, b in zip(headers, tree.item(selected_item)['values'])])
            messagebox.showinfo(title="Selected Record", message=info_to_show)

        # Frames
        main_frame = Ctk.CTkFrame(self.root)
        main_frame.pack(fill='both', expand=True)

        title_frame = Ctk.CTkFrame(main_frame)
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=1)
        title_frame.pack(fill='x')

        data_frame = Ctk.CTkFrame(main_frame)
        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=7)
        data_frame.rowconfigure(0, weight=1)
        data_frame.pack(fill='both', expand=True)
        data_frame_left = Ctk.CTkFrame(data_frame, width=100, border_color="#065e99", border_width=3)
        data_frame_right = Ctk.CTkFrame(data_frame, width=200)
        data_frame_right.grid(row=0, column=1, sticky='nwes', padx=(10, 0))
        data_frame_right.columnconfigure(0, weight=1)
        data_frame_right.rowconfigure(0, weight=5)
        data_frame_left.grid(row=0, column=0, sticky='nwes', padx=(10, 0), pady=(10, 0))

        # Labels and Entryboxes
        self.lblTitle = Ctk.CTkLabel(title_frame, text="Passengers Enquiry System", font=('Arial', 40), text_color='white', fg_color='#065e99')
        self.lblTitle.grid(row=0, column=0, sticky='nwes')

        self.lblPassengerId = Ctk.CTkLabel(data_frame_left, text="Passenger ID: ", pady=3, font=('Arial', 15))
        self.lblPassengerId.grid(row=0, column=0, sticky='w', padx=10, pady=(30, 0))
        self.txtPassengerId = Ctk.CTkEntry(data_frame_left, textvariable=PassengerId, height=20, width=200, font=('Helvetica', 15))
        self.txtPassengerId.grid(row=0, column=1, padx=0, pady=(30, 0))

        self.lblFName = Ctk.CTkLabel(data_frame_left, text="First Name: ", pady=3, font=('Arial', 15))
        self.lblFName.grid(row=1, column=0, sticky='w', padx=10, pady=3)
        self.txtFName = Ctk.CTkEntry(data_frame_left, textvariable=FName, height=20, width=200, font=('Helvetica', 15))
        self.txtFName.grid(row=1, column=1, padx=0, pady=3)

        self.lblLName = Ctk.CTkLabel(data_frame_left, text="Last Name: ", pady=3, font=('Arial', 15))
        self.lblLName.grid(row=2, column=0, sticky='w', padx=10, pady=3)
        self.txtLName = Ctk.CTkEntry(data_frame_left, textvariable=LName, height=20, width=200, font=('Helvetica', 15))
        self.txtLName.grid(row=2, column=1, padx=0, pady=3)

        self.lblGender = Ctk.CTkLabel(data_frame_left, text="Gender: ", pady=3, font=('Arial', 15))
        self.lblGender.grid(row=3, column=0, sticky='w', padx=10, pady=3)
        self.rdiobtnMale = Ctk.CTkRadioButton(data_frame_left, text="Male", variable=Gender, value='Male')
        self.rdiobtnMale.grid(row=3, column=1, padx=0, pady=3)
        self.rdiobtnFemale = Ctk.CTkRadioButton(data_frame_left, text='Female', variable=Gender, value='Female')
        self.rdiobtnFemale.grid(row=3, column=2, padx=0, pady=3)

        self.lblAge = Ctk.CTkLabel(data_frame_left, text="Age: ", pady=3, font=('Arial', 15))
        self.lblAge.grid(row=4, column=0, sticky='w', padx=10, pady=3)
        self.txtAge = Ctk.CTkEntry(data_frame_left, textvariable=Age, height=20, width=200, font=('Helvetica', 15))
        self.txtAge.grid(row=4, column=1, padx=0, pady=3)
        
        self.lblNationality = Ctk.CTkLabel(data_frame_left, text="Nationality: ", pady=3, font=('Arial', 15))
        self.lblNationality.grid(row=5, column=0, sticky='w', padx=10, pady=3)
        self.txtNationality = Ctk.CTkEntry(data_frame_left, textvariable=Nationality, height=20, width=200, font=('Helvetica', 15))
        self.txtNationality.grid(row=5, column=1, padx=0, pady=3)

        self.lblCountryCode = Ctk.CTkLabel(data_frame_left, text="Country Code: ", pady=3, font=('Arial', 15))
        self.lblCountryCode.grid(row=6, column=0, sticky='w', padx=10, pady=3)
        self.txtCountryCode = Ctk.CTkEntry(data_frame_left, textvariable=CountryCode, height=20, width=200, font=('Helvetica', 15))
        self.txtCountryCode.grid(row=6, column=1, padx=0, pady=3)

        self.lblCountryName = Ctk.CTkLabel(data_frame_left, text="Country Name: ", pady=3, font=('Arial', 15))
        self.lblCountryName.grid(row=7, column=0, sticky='w', padx=10, pady=3)
        self.txtCountryName = Ctk.CTkEntry(data_frame_left, textvariable=CountryName, height=20, width=200, font=('Helvetica', 15))
        self.txtCountryName.grid(row=7, column=1, padx=0, pady=3)

        self.lblAirportCode = Ctk.CTkLabel(data_frame_left, text="Airport Code: ", pady=3, font=('Arial', 15))
        self.lblAirportCode.grid(row=8, column=0, sticky='w', padx=10, pady=3)
        self.txtAirportCode = Ctk.CTkEntry(data_frame_left, textvariable=AirportCode, height=20, width=200, font=('Helvetica', 15))
        self.txtAirportCode.grid(row=8, column=1, padx=0, pady=3)

        self.lblAirportName = Ctk.CTkLabel(data_frame_left, text="Airport Name: ", pady=3, font=('Arial', 15))
        self.lblAirportName.grid(row=9, column=0, sticky='w', padx=10, pady=3)
        self.txtAirportName = Ctk.CTkEntry(data_frame_left, textvariable=AirportName, height=20, width=200, font=('Helvetica', 15))
        self.txtAirportName.grid(row=9, column=1, padx=0, pady=3)

        self.lblDepartureDate = Ctk.CTkLabel(data_frame_left, text="Departure Date: ", pady=3, font=('Arial', 15))
        self.lblDepartureDate.grid(row=10, column=0, sticky='w', padx=10, pady=3)
        self.txtDepartureDate = Ctk.CTkEntry(data_frame_left, textvariable=DepartureDate, height=20, width=200, font=('Helvetica', 15))
        self.txtDepartureDate.grid(row=10, column=1, padx=0, pady=3)

        self.lblContinentCode = Ctk.CTkLabel(data_frame_left, text="Continent Code: ", pady=3, font=('Arial', 15))
        self.lblContinentCode.grid(row=11, column=0, sticky='w', padx=10, pady=3)
        self.txtContinentCode = Ctk.CTkEntry(data_frame_left, textvariable=ContinentCode, height=20, width=200, font=('Helvetica', 15))
        self.txtContinentCode.grid(row=11, column=1, padx=0, pady=3)

        self.lblContinentName = Ctk.CTkLabel(data_frame_left, text="Continent Name: ", pady=3, font=('Arial', 15))
        self.lblContinentName.grid(row=12, column=0, sticky='w', padx=10, pady=3)
        self.txtContinentName = Ctk.CTkEntry(data_frame_left, textvariable=ContinentName, height=20, width=200, font=('Helvetica', 15))
        self.txtContinentName.grid(row=12, column=1, padx=0, pady=3)
        
        tree = ttk.Treeview(data_frame_right, columns=headers, show='headings')
        tree.bind("<<TreeviewSelect>>", passengersdatafill)
        tree.grid(row=0, column=0, sticky='nesw')
        data_frame_right.columnconfigure(0, weight=1)

        # Set width of each column to 40
        for col in headers:
            tree.heading(col, text=col, anchor=tk.CENTER)
            tree.column(col, width=20, anchor=tk.CENTER)

        # Add vertical scrollbar to the treeview
        sb_vertical = ttk.Scrollbar(data_frame_right, orient='vertical', command=tree.yview)
        sb_vertical.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=sb_vertical.set)

        # Buttons
        self.btnSearch = Ctk.CTkButton(data_frame_left, text="Search", width=25, command=searchpassengersdb, fg_color="#065e99", border_color="#065e99", border_width=2, hover_color="#065e99")
        self.btnSearch.place(anchor="center", relx=0.3, rely=0.68)
        self.btnDisplay = Ctk.CTkButton(data_frame_left, text='Display All', width=15, command=viewpassengersdb, fg_color="#065e99", border_color="#065e99", border_width=2, hover_color="#065e99")
        self.btnDisplay.place(anchor="center", relx=0.5, rely=0.68)
        self.btnBack = Ctk.CTkButton(
            data_frame_left,
            text="Go Back",
            width=15,
            command=self.backFunction,
            fg_color="#065e99",
            border_color="#065e99",
            border_width=2,
            hover_color="#065e99",
        )
        self.btnBack.place(anchor="center", relx=0.7, rely=0.68)

    def backFunction(self):
        # Function handling actions after pressing back
        clear_frame(self.root)
        Starting_window(self.root)
      

if __name__ == "__main__":
    root = Ctk.CTk()
   # Ctk.set_appearance_mode("dark")
    window = Starting_window(root)
    root.mainloop()
