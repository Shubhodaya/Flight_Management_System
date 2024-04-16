import sqlite3
import csv
flights_db = "Databases/flights.db"
flights_db_path = "Databases/flights.csv"

def init_db():
    # Function to initialize the database from the csv database file
    con = sqlite3.connect(flights_db)
    cur = con.cursor()
    # f = open(flights_db_path, 'r')
    # file_content = f.readlines()
    cur.execute("CREATE TABLE Carrier(carrier_name text, full_name text, PRIMARY KEY(carrier_name));")
    con.commit()
    cur.execute("CREATE TABLE Aircraft(tailnum text, carrier_name text, PRIMARY KEY(tailnum), FOREIGN KEY(carrier_name) REFERENCES Carrier(carrier_name));")
    con.commit()
    cur.execute("CREATE TABLE Dates(date_idx text, day text, month text, year text, PRIMARY KEY(date_idx));")
    con.commit()
    cur.execute("CREATE TABLE Flight(flightno text, date_idx text, scheduled_dept_time text, dept_time text, scheduled_arr_time text, arr_time text, air_time text, origin text, dest text, tailnum text, PRIMARY KEY(flightno, date_idx), FOREIGN KEY(date_idx) REFERENCES Dates(date_idx), FOREIGN KEY(tailnum) REFERENCES Aircraft(tailnum));")
    con.commit()
    flight_records = csv.reader(open(flights_db_path, "r"))
    head = True
    i, j=0, 0
    carriers = set()
    aircrafts = set()
    dates = list()
    flights = set()
    for row in flight_records:
        print(j)
        j+=1
        if head:
            head = False
            col_heads = row
            continue
        col_vals = dict(zip(col_heads, row))
        # print(col_vals)
        if col_vals['carrier'] not in carriers:
            carriers.add(col_vals['carrier'])
            cur.execute("INSERT INTO Carrier VALUES(?, ?);", [col_vals['carrier'],col_vals['name']])
            con.commit()
        
        if col_vals['tailnum'] not in aircrafts:
            aircrafts.add(col_vals['tailnum'])
            cur.execute("INSERT INTO Aircraft VALUES(?, ?);", [col_vals['tailnum'], col_vals['carrier']])
            con.commit()
        
        if col_vals['day']+col_vals['month']+col_vals['year'] not in dates:
            dates.append(col_vals['day']+col_vals['month']+col_vals['year'])
            cur.execute("INSERT INTO Dates VALUES(?,?,?,?);", [i,col_vals['day'],col_vals['month'],col_vals['year']])
            con.commit()
            i+=1

        if col_vals['day']+col_vals['month']+col_vals['year']+col_vals['flight'] not in flights:
            flights.add(col_vals['day']+col_vals['month']+col_vals['year']+col_vals['flight'])
            cur.execute("INSERT INTO Flight VALUES(?,?,?,?,?,?,?,?,?,?);", 
                        [col_vals['flight'],dates.index(col_vals['day']+col_vals['month']+col_vals['year'])
                         ,col_vals['sched_dep_time'],col_vals['dep_time'],
                         col_vals['sched_arr_time'],col_vals['arr_time'],col_vals['air_time'],
                         col_vals['origin'], col_vals['dest'], col_vals['tailnum']])
            con.commit()
    con.close()

def ViewAllData():
    con=sqlite3.connect(flights_db)    
    cur=con.cursor()
    cur.execute("SELECT * FROM Flight f inner join Dates d using(date_idx) inner join Aircraft a using(tailnum) inner join Carrier c using(carrier_name)")
    rows=cur.fetchall()
    con.close()
    return rows

def SearchForData(SearchTerms):
    con=sqlite3.connect(flights_db)    
    cur=con.cursor()
    query = "SELECT * FROM Flight f inner join Dates d using(date_idx) inner join Aircraft a using(tailnum) inner join Carrier c using(carrier_name)"
    if len(SearchTerms)!=0:
        query += " WHERE "
        for name, data in SearchTerms.items():
            query+=name+"=\""+data+"\" AND "
        query = query[:-4]
    cur.execute(query)
    rows=cur.fetchall()
    con.close()
    return rows