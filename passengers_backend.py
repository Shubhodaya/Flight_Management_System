import sqlite3
import csv

passengers_db = "Databases/passengers.db"
passengers_db_path = "Databases/passengers.csv"

def init_db():
    
    con = sqlite3.connect(passengers_db)
    cur = con.cursor()
    
 
    cur.execute("CREATE TABLE Continent(continent_code TEXT, continent_name TEXT,PRIMARY KEY(continent_code));")
    con.commit()
    
    cur.execute("CREATE TABLE Passenger(id TEXT, Fname TEXT,Lname TEXT ,gender TEXT, age TEXT, nationality TEXT, PRIMARY KEY(id));")
    con.commit()
    
    cur.execute("CREATE TABLE Country(country_code TEXT, country_name TEXT, continent_code TEXT,PRIMARY KEY(country_code), FOREIGN KEY(continent_code) REFERENCES Continent(continent_code));")
    con.commit()
    
    cur.execute("CREATE TABLE Airport(airport_code TEXT , airport_name TEXT, country_code TEXT, PRIMARY KEY(airport_code), FOREIGN KEY(country_code) REFERENCES Country(country_code));")
    con.commit()

    cur.execute("CREATE TABLE Flight(id TEXT, airport_code TEXT, departure_date TEXT, pilot_name TEXT, status TEXT, PRIMARY KEY(id, airport_code), FOREIGN KEY(id) REFERENCES Passenger(id), FOREIGN KEY(airport_code) REFERENCES Airport(airport_code));")
    con.commit()

    passenger_records = csv.reader(open(passengers_db_path, "r"))
    head = True
    continents = set()
    countries = set()
    passengers = set()
    airports = set()
    flights = set()
    for row in passenger_records:
        if head:
            head = False
            col_heads = row
            continue
        col_vals = dict(zip(col_heads, row))

        if col_vals['continent_code'] not in continents:
            continents.add(col_vals['continent_code'])
            cur.execute("INSERT OR IGNORE INTO Continent VALUES(?, ?);",
                        [col_vals['continent_code'], col_vals['continent_name']])
            con.commit()

        if col_vals['id'] not in passengers:
            passengers.add(col_vals['id'])
            cur.execute("INSERT INTO Passenger VALUES(?, ?, ?, ?, ?,?);", 
                        [col_vals['id'], col_vals['fname'], col_vals['lname'],col_vals['gender'], col_vals['age'], col_vals['nationality']])
            con.commit()

        if col_vals['country_code'] not in countries:
            countries.add(col_vals['country_code'])
            cur.execute("INSERT OR IGNORE INTO Country VALUES(?, ?, ?);",
                        [col_vals['country_code'], col_vals['country_name'], col_vals['continent_code']])
            con.commit()

        if col_vals['airport_code'] not in airports:
            airports.add(col_vals['airport_code'])
            cur.execute("INSERT OR IGNORE INTO Airport VALUES(?, ?, ?);",
                        [col_vals['airport_code'], col_vals['airport_name'], col_vals['country_code']])
            con.commit()
        
        if col_vals['id']+col_vals['airport_code'] not in flights:
            flights.add(col_vals['id']+col_vals['airport_code'])
            cur.execute("INSERT OR IGNORE INTO Flight VALUES(?, ?, ?, ?, ?);",
                        [col_vals['id'], col_vals['airport_code'], col_vals['departure_date'], col_vals['pilot_name'], col_vals['status']])
            con.commit()
    con.close()



def ViewAllPassengers():
    con = sqlite3.connect(passengers_db)
    cur = con.cursor()
    cur.execute("SELECT * FROM Passenger p INNER JOIN Flight f using(id) INNER JOIN Airport a using(airport_code) INNER JOIN Country c using(country_code) INNER JOIN Continent co using(continent_code)")
    rows = cur.fetchall()
    con.close()
    return rows



def SearchPassenger(SearchTerms):
    con = sqlite3.connect(passengers_db)
    cur = con.cursor()
    query = "SELECT * FROM Passenger p INNER JOIN Flight f using(id) INNER JOIN Airport a using(airport_code) INNER JOIN Country c using(country_code) INNER JOIN Continent co using(continent_code)"
    if len(SearchTerms) != 0:
        query += " WHERE "
        for name, data in SearchTerms.items():
            query += name + "=\"" + data + "\" AND "  
        query = query[:-4]
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    return rows