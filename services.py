import sqlite3

class FlightService:
    def __init__(self):
        """Initializes the database connection and ensures tables are created."""
        self.conn = sqlite3.connect("FlightManagement.db")
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Creates Pilot, Airport, and Flight tables if they do not already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pilot (
                PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Email TEXT,
                PhoneNumber TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Airport (
                AirportCode TEXT PRIMARY KEY,
                AirportName TEXT NOT NULL,
                City TEXT NOT NULL,
                Country TEXT NOT NULL
            );
        """)

        self.cursor.execute("""
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
        self.conn.commit()

# Q1. For users to add a new flight 
    def add_new_flight(self):
        """Allows the user to add a new flight by providing required details."""
        print("\n╔═══════════════════════════════╗")
        print("║       Add New Flight          ║")
        print("╚═══════════════════════════════╝")
        print("Enter the flight details below.")
        print("Note: Flight Number (e.g., BA101) can be reused for flights on different days.")
        print("      Pilot ID is optional (press Enter to leave unassigned).")
        try:
            flight_data = (
                input("Flight Number (e.g., BA101): "),
                input("Pilot ID (integer, e.g., 1; optional): ") or None,
                input("Departure Airport Code (e.g., LHR): "),
                input("Arrival Airport Code (e.g., JFK): "),
                input("Departure Date (YYYY-MM-DD, e.g., 2025-10-10): "),
                input("Departure Time (HH:MM in 24-hour format, e.g., 08:00): "),
                input("Arrival Date (YYYY-MM-DD, e.g., 2025-10-10): "),
                input("Arrival Time (HH:MM in 24-hour format, e.g., 11:30): "),
                input("Flight Status (Scheduled, Departed, Delayed, Cancelled, Completed): ")
            )
            self.cursor.execute("""
                INSERT INTO Flight (
                    FlightNumber, PilotID, DepartureAirport, ArrivalAirport,
                    DepartureDate, DepartureTime, ArrivalDate, ArrivalTime,
                    FlightStatus
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, flight_data)
            self.conn.commit()
            print("\nFlight added successfully!")
        except Exception as e:
            print(f"\nError adding flight: {e}")

# Q2. View flights by status
    def view_flights_by_status(self):
        """Displays flights filtered by a specified status."""
        print("\n╔═══════════════════════════════╗")
        print("║     View Flights by Status    ║")
        print("╚═══════════════════════════════╝")
        print("Available statuses: Scheduled, Departed, Delayed, Cancelled, Completed")
        status = input("Enter flight status: ").strip().capitalize()
        self.cursor.execute("""
            SELECT 
                f.FlightID,
                f.FlightNumber,
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS Pilot,
                o.City AS Departure,
                d.City AS Arrival,
                f.DepartureDate,
                f.DepartureTime,
                f.ArrivalDate,
                f.ArrivalTime,
                f.FlightStatus
            FROM Flight f
            LEFT JOIN Pilot p ON f.PilotID = p.PilotID
            JOIN Airport o ON f.DepartureAirport = o.AirportCode
            JOIN Airport d ON f.ArrivalAirport = d.AirportCode
            WHERE f.FlightStatus = ?
            ORDER BY f.DepartureDate, f.DepartureTime
        """, (status,))

        rows = self.cursor.fetchall()

        if rows:
            print(f"\nFlights with Status: {status}")
            print("=" * 110)
            print(f"{'FlightID':<8} | {'Flight':<10} | {'Pilot':<20} | {'From':<15} | {'To':<15} | {'Depart':<10} | {'Time':<8} | {'Arrive':<10} | {'Time':<8}")
            print("-" * 110)
            for row in rows:
                print(f"{row[0]:<8} | {row[1]:<10} | {row[2]:<20} | {row[3]:<15} | {row[4]:<15} | {row[5]:<10} | {row[6]:<8} | {row[7]:<10} | {row[8]:<8}")
            print("=" * 110)
        else:
            print(f"\nNo flights found with status '{status}'.")

# Q3. Update flight status 
    def update_flight_status(self):
        """Updates the status of a flight by its ID."""
        print("\n╔═══════════════════════════════╗")
        print("║      Update Flight Status     ║")
        print("╚═══════════════════════════════╝")
        print("Note: Use Flight ID (unique integer, e.g., 1) to identify the flight.")
        print("Available statuses: Scheduled, Departed, Delayed, Cancelled, Completed")
        flight_id = input("Enter Flight ID (integer, e.g., 1): ")
        new_status = input("Enter new status: ")
        self.cursor.execute("UPDATE Flight SET FlightStatus = ? WHERE FlightID = ?", (new_status, flight_id))
        self.conn.commit()
        print("\nFlight status updated successfully!")

# Q4. Assign a pilot to a flight 
    def assign_pilot_to_flight(self):
        """Assigns a pilot to a flight by their IDs."""
        print("\n╔═══════════════════════════════╗")
        print("║    Assign Pilot to Flight     ║")
        print("╚═══════════════════════════════╝")
        print("Note: Use Flight ID (unique integer, e.g., 1) to identify the flight.")
        flight_id = input("Enter Flight ID (integer, e.g., 1): ")
        pilot_id = input("Enter Pilot ID (integer, e.g., 2): ")
        self.cursor.execute("UPDATE Flight SET PilotID = ? WHERE FlightID = ?", (pilot_id, flight_id))
        self.conn.commit()
        print("\nPilot assigned to flight successfully!")

# Q5. Remove a pilot from a flight 
    def remove_pilot_from_flight(self):
        """Removes the assigned pilot from a flight by its ID."""
        print("\n╔═══════════════════════════════╗")
        print("║   Remove Pilot from Flight    ║")
        print("╚═══════════════════════════════╝")
        print("Note: Use Flight ID (unique integer, e.g., 1) to identify the flight.")
        flight_id = input("Enter Flight ID (integer, e.g., 1): ")
        self.cursor.execute("UPDATE Flight SET PilotID = NULL WHERE FlightID = ?", (flight_id,))
        self.conn.commit()
        print("\nPilot removed from flight successfully!")
        
# Q6. View a pilot schedule
    def view_pilot_schedule(self):
        """Displays the flight schedule for a specific pilot, including their name."""
        print("\n╔═══════════════════════════════╗")
        print("║      View Pilot Schedule      ║")
        print("╚═══════════════════════════════╝")
        pilot_id = input("Enter Pilot ID (integer, e.g., 1): ").strip()

        # Fetch pilot's name
        self.cursor.execute("SELECT FirstName, LastName FROM Pilot WHERE PilotID = ?", (pilot_id,))
        pilot = self.cursor.fetchone()
        pilot_name = f"{pilot[0]} {pilot[1]}" if pilot else "Unknown Pilot"

        self.cursor.execute("""
            SELECT 
                f.FlightID,
                f.FlightNumber,
                f.DepartureDate,
                f.DepartureTime,
                f.ArrivalDate,
                f.ArrivalTime,
                o.City AS Departure,
                d.City AS Arrival,
                f.FlightStatus
            FROM Flight f
            JOIN Airport o ON f.DepartureAirport = o.AirportCode
            JOIN Airport d ON f.ArrivalAirport = d.AirportCode
            WHERE f.PilotID = ?
            ORDER BY f.DepartureDate, f.DepartureTime
        """, (pilot_id,))

        results = self.cursor.fetchall()

        if results:
            print(f"\nFlight Schedule for Pilot: {pilot_name} (ID: {pilot_id})")
            print("=" * 110)
            print(f"{'FlightID':<8} | {'Flight':<10} | {'Depart':<10} | {'Time':<8} | {'Arrive':<10} | {'Time':<8} | {'From':<15} | {'To':<15} | {'Status':<10}")
            print("-" * 110)
            for row in results:
                print(f"{row[0]:<8} | {row[1]:<10} | {row[2]:<10} | {row[3]:<8} | {row[4]:<10} | {row[5]:<8} | {row[6]:<15} | {row[7]:<15} | {row[8]:<10}")
            print("=" * 110)
        else:
            print(f"\nNo flights assigned to pilot ID {pilot_id} ({pilot_name}).")
 
# Q7. Add a new destination to the database     
    def add_destination(self):
        """Allows the user to add a new airport to the database."""
        print("\n╔═══════════════════════════════╗")
        print("║       Add New Airport         ║")
        print("╚═══════════════════════════════╝")
        print("Enter the airport details below.")
        destination_data = (
            input("Airport Code (e.g., LHR): "),
            input("Airport Name (e.g., Heathrow Airport): "),
            input("City (e.g., London): "),
            input("Country (e.g., UK): ")
        )
        try:
            self.cursor.execute("""
                INSERT INTO Airport (AirportCode, AirportName, City, Country)
                VALUES (?, ?, ?, ?)
            """, destination_data)
            self.conn.commit()
            print("\nAirport added successfully!")
        except Exception as e:
            print(f"\nError adding airport: {e}")

# Q8. View flight details with its pilot and destination  
    def view_flight_details(self):
        """Displays detailed information for all flights, including pilot ID and airports."""
        print("\n╔═══════════════════════════════╗")
        print("║      View All Flights         ║")
        print("╚═══════════════════════════════╝")
        self.cursor.execute("""
            SELECT 
                f.FlightID,
                f.FlightNumber,
                f.PilotID,
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS PilotName,
                o.City AS DepartureCity,
                d.City AS ArrivalCity,
                f.FlightStatus
            FROM 
                Flight f
            LEFT JOIN 
                Pilot p ON f.PilotID = p.PilotID
            JOIN 
                Airport o ON f.DepartureAirport = o.AirportCode
            JOIN 
                Airport d ON f.ArrivalAirport = d.AirportCode
        """)
        rows = self.cursor.fetchall()
        if rows:
            print("\nAll Flights")
            print("=" * 100)
            print(f"{'FlightID':<8} | {'Flight':<10} | {'PilotID':<8} | {'Pilot':<20} | {'From':<15} | {'To':<15} | {'Status':<10}")
            print("-" * 100)
            for row in rows:
                pilot_id = str(row[2]) if row[2] is not None else 'None'
                print(f"{row[0]:<8} | {row[1]:<10} | {pilot_id:<8} | {row[3]:<20} | {row[4]:<15} | {row[5]:<15} | {row[6]:<10}")
            print("=" * 100)
        else:
            print("\nNo flights available.")

# Q9. Get a summary of how many flights go to each destination
    def get_flight_summary(self):
        """Provides a summary of the number of flights to each arrival city."""
        print("\n╔═══════════════════════════════╗")
        print("║   Flight Summary by City      ║")
        print("╚═══════════════════════════════╝")
        self.cursor.execute("""
            SELECT 
                d.City,
                COUNT(f.FlightID) AS TotalFlights
            FROM 
                Flight f
            JOIN 
                Airport d ON f.ArrivalAirport = d.AirportCode
            GROUP BY 
                d.City
            ORDER BY 
                TotalFlights DESC
        """)
        results = self.cursor.fetchall()
        if results:
            print("\nFlight Summary by Arrival City")
            print("=" * 45)
            print(f"{'City':<25} | {'Total Flights':<15}")
            print("-" * 45)
            for city, total in results:
                print(f"{city:<25} | {str(total):<15}")
            print("=" * 45)
        else:
            print("\nNo flight summary available.")

# Q10. Delete a flight from the database
    def delete_flight_by_number(self):
        """Deletes a flight by its flight number and departure date after confirmation."""
        print("\n╔═══════════════════════════════╗")
        print("║        Delete Flight          ║")
        print("╚═══════════════════════════════╝")
        print("Note: Flight Number (e.g., BA101) may not be unique; specify Departure Date to identify the flight.")
        flight_number = input("Enter Flight Number (e.g., BA101): ")
        departure_date = input("Enter Departure Date (YYYY-MM-DD, e.g., 2025-10-10): ")

        self.cursor.execute("""
            SELECT FlightID, FlightNumber, DepartureDate, FlightStatus 
            FROM Flight 
            WHERE FlightNumber = ? AND DepartureDate = ?
        """, (flight_number, departure_date))
        flight = self.cursor.fetchone()

        if not flight:
            print(f"\nNo flight found with flight number '{flight_number}' on {departure_date}.")
            return

        print("\nFlight Details:")
        print("-" * 40)
        print(f"Flight ID: {flight[0]}")
        print(f"Flight Number: {flight[1]}")
        print(f"Departure Date: {flight[2]}")
        print(f"Status: {flight[3]}")
        print("-" * 40)
        
        confirm = input("Are you sure you want to delete this flight? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.cursor.execute("DELETE FROM Flight WHERE FlightID = ?", (flight[0],))
            self.conn.commit()
            print("\nFlight deleted successfully!")
        else:
            print("\nDeletion cancelled.")
 
# Q11. View flights assigned to each pilot 
    def view_flights_per_pilot(self):
        """Displays the number of flights assigned to each pilot, including pilot ID."""
        print("\n╔═══════════════════════════════╗")
        print("║ Flights Assigned per Pilot    ║")
        print("╚═══════════════════════════════╝")
        self.cursor.execute("""
            SELECT 
                p.PilotID,
                IFNULL(p.FirstName || ' ' || p.LastName, 'Unassigned') AS Pilot,
                COUNT(f.FlightID) AS FlightCount
            FROM Flight f
            LEFT JOIN Pilot p ON f.PilotID = p.PilotID
            GROUP BY f.PilotID
            ORDER BY FlightCount DESC
        """)
        rows = self.cursor.fetchall()
        if rows:
            print("\nFlights per Pilot")
            print("=" * 55)
            print(f"{'PilotID':<8} | {'Pilot':<25} | {'Flights Assigned':<15}")
            print("-" * 55)
            for row in rows:
                pilot_id = str(row[0]) if row[0] is not None else 'None'
                print(f"{pilot_id:<8} | {row[1]:<25} | {row[2]:<15}")
            print("=" * 55)
        else:
            print("\nNo pilots or flights available.")
    
# Q12. View count of flight for each destination
    def view_flight_count_by_destination(self):
        """Displays the number of flights arriving at each city."""
        print("\n╔═══════════════════════════════╗")
        print("║ Flight Count by Destination   ║")
        print("╚═══════════════════════════════╝")
        self.cursor.execute("""
            SELECT 
                d.City,
                COUNT(f.FlightID) AS FlightCount
            FROM Flight f
            JOIN Airport d ON f.ArrivalAirport = d.AirportCode
            GROUP BY d.City
            ORDER BY FlightCount DESC
        """)
        rows = self.cursor.fetchall()
        if rows:
            print("\nFlight Count by Arrival City")
            print("=" * 45)
            print(f"{'City':<25} | {'Flight Count':<15}")
            print("-" * 45)
            for row in rows:
                print(f"{row[0]:<25} | {row[1]:<15}")
            print("=" * 45)
        else:
            print("\nNo flights or destinations available.")