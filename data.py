import sqlite3

def create_tables(conn):
    """Creates the necessary tables if they do not exist."""
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Pilot (
            PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT,
            PhoneNumber TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Airport (
            AirportCode TEXT PRIMARY KEY,
            AirportName TEXT NOT NULL,
            City TEXT NOT NULL,
            Country TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Flight (
            FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
            FlightNumber TEXT NOT NULL,
            PilotID INTEGER,
            DepartureAirport TEXT NOT NULL,
            ArrivalAirport TEXT NOT NULL,
            DepartureDate DATE NOT NULL,
            DepartureTime TIME NOT NULL,
            ArrivalDate DATE NOT NULL,
            ArrivalTime TIME NOT NULL,
            FlightStatus TEXT NOT NULL CHECK (FlightStatus IN 
                ('Scheduled', 'Departed', 'Delayed', 'Cancelled', 'Completed')),
            FOREIGN KEY (PilotID) REFERENCES Pilot(PilotID),
            FOREIGN KEY (DepartureAirport) REFERENCES Airport(AirportCode),
            FOREIGN KEY (ArrivalAirport) REFERENCES Airport(AirportCode)
        );
    """)
    conn.commit()

def sample_data():
    conn = sqlite3.connect("FlightManagement.db")
    create_tables(conn)  # Ensure tables are created before inserting data
    cur = conn.cursor()

    # Clear existing data to prevent UNIQUE constraint errors
    cur.execute("DELETE FROM Flight")
    cur.execute("DELETE FROM Pilot")
    cur.execute("DELETE FROM Airport")
    conn.commit()

    # Sample Airports (for a London-based airline with domestic and international routes)
    airports = [
        ('LHR', 'Heathrow Airport', 'London', 'UK'),
        ('LGW', 'Gatwick Airport', 'London', 'UK'),
        ('MAN', 'Manchester Airport', 'Manchester', 'UK'),
        ('EDI', 'Edinburgh Airport', 'Edinburgh', 'UK'),
        ('BFS', 'Belfast International Airport', 'Belfast', 'UK'),
        ('GLA', 'Glasgow Airport', 'Glasgow', 'UK'),
        ('JFK', 'John F. Kennedy International Airport', 'New York', 'USA'),
        ('CDG', 'Charles de Gaulle Airport', 'Paris', 'France'),
        ('AMS', 'Amsterdam Schiphol Airport', 'Amsterdam', 'Netherlands'),
        ('DXB', 'Dubai International Airport', 'Dubai', 'UAE'),
        ('FRA', 'Frankfurt Main Airport', 'Frankfurt', 'Germany'),
        ('MAD', 'Adolfo Suárez Madrid–Barajas Airport', 'Madrid', 'Spain'),
        ('HKG', 'Hong Kong International Airport', 'Hong Kong', 'Hong Kong'),
        ('NRT', 'Narita International Airport', 'Tokyo', 'Japan'),
        ('SIN', 'Changi Airport', 'Singapore', 'Singapore')
    ]

    # Sample Pilots (10 pilots)
    pilots = [
        ('Emma', 'Thompson', 'emma.thompson@example.com', '+447911123456'),
        ('James', 'Wilson', 'james.wilson@example.com', '+447912345678'),
        ('Sophie', 'Davies', 'sophie.davies@example.com', '+447913456789'),
        ('Thomas', 'Harris', 'thomas.harris@example.com', '+447914567890'),
        ('Olivia', 'Clark', 'olivia.clark@example.com', '+447915678901'),
        ('William', 'Lewis', 'william.lewis@example.com', '+447916789012'),
        ('Charlotte', 'Walker', 'charlotte.walker@example.com', '+447917890123'),
        ('Daniel', 'Hall', 'daniel.hall@example.com', '+447918901234'),
        ('Amelia', 'Green', 'amelia.green@example.com', '+447919012345'),
        ('George', 'Adams', 'george.adams@example.com', '+447920123456')
    ]

    # Sample Flights (15 flights, with some duplicate FlightNumbers on different days)
    flights = [
        ('BA101', 1, 'LHR', 'JFK', '2025-10-10', '08:00', '2025-10-10', '11:30', 'Scheduled'),
        ('BA101', 2, 'LHR', 'JFK', '2025-10-11', '08:00', '2025-10-11', '11:30', 'Scheduled'),  
        ('BA202', 5, 'LGW', 'EDI', '2025-10-11', '07:30', '2025-10-11', '09:00', 'Delayed'),
        ('BA202', 6, 'LGW', 'EDI', '2025-10-12', '07:30', '2025-10-12', '09:00', 'Scheduled'),  
        ('BA303', 8, 'LHR', 'CDG', '2025-10-12', '10:15', '2025-10-12', '12:30', 'Scheduled'),
        ('BA404', 9, 'LHR', 'MAN', '2025-10-13', '06:45', '2025-10-13', '07:45', 'Departed'),
        ('BA505', 3, 'LHR', 'DXB', '2025-10-13', '13:00', '2025-10-13', '23:00', 'Scheduled'),
        ('BA606', 4, 'LGW', 'BFS', '2025-10-14', '08:30', '2025-10-14', '09:45', 'Scheduled'),
        ('BA707', 5, 'LHR', 'HKG', '2025-10-14', '18:00', '2025-10-15', '13:30', 'Scheduled'),
        ('BA808', 6, 'LHR', 'GLA', '2025-10-15', '09:00', '2025-10-15', '10:30', 'Scheduled'),
        ('BA909', 10, 'LHR', 'AMS', '2025-10-15', '11:00', '2025-10-15', '13:15', 'Cancelled'),
        ('BA1010', 7, 'LHR', 'NRT', '2025-10-16', '12:00', '2025-10-17', '08:00', 'Scheduled'),
        ('BA1111', 8, 'LHR', 'FRA', '2025-10-16', '14:30', '2025-10-16', '17:00', 'Scheduled'),
        ('BA1212', 9, 'LGW', 'MAD', '2025-10-17', '07:00', '2025-10-17', '10:30', 'Scheduled'),
        ('BA1313', 10, 'LHR', 'SIN', '2025-10-17', '15:45', '2025-10-18', '11:30', 'Scheduled')
    ]

    cur.executemany("INSERT INTO Airport (AirportCode, AirportName, City, Country) VALUES (?, ?, ?, ?)", airports)
    cur.executemany("INSERT INTO Pilot (FirstName, LastName, Email, PhoneNumber) VALUES (?, ?, ?, ?)", pilots)
    cur.executemany("INSERT INTO Flight (FlightNumber, PilotID, DepartureAirport, ArrivalAirport, DepartureDate, DepartureTime, ArrivalDate, ArrivalTime, FlightStatus) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", flights)

    conn.commit()
    print("Sample data inserted successfully.")
    conn.close()

if __name__ == "__main__":
    sample_data()