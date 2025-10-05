from services import FlightService

def main():
    """Main entry point for the Flight Management System."""
    service = FlightService()

    while True:
        print("\n╔═════════════════════════════════════════════╗")
        print("║         Flight Management System             ║")
        print("╚═════════════════════════════════════════════╝")
        print("Welcome! Select an option from the menu below.")
        print("Note: FlightID is a unique integer (e.g., 1).")
        print("      FlightNumber (e.g., BA101) can be reused for different days.")
        print("=" * 47)
        print("  1. Add a New Flight")
        print("  2. View Flights by Status")
        print("  3. Update Flight Status")
        print("  4. Assign Pilot to Flight")
        print("  5. Remove Pilot from Flight")
        print("  6. View Pilot Schedule")
        print("  7. Add New Airport")
        print("  8. View All Flights with Details")
        print("  9. Flight Summary by Destination")
        print(" 10. Delete Flight")
        print(" 11. Flights Assigned per Pilot")
        print(" 12. Flight Count by Destination")
        print("  0. Exit System")
        print("=" * 47)

        choice = input("\nEnter your choice (0-12): ").strip()

        if choice == '1':
            service.add_new_flight()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '2':
            service.view_flights_by_status()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '3':
            service.update_flight_status()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '4':
            service.assign_pilot_to_flight()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '5':
            service.remove_pilot_from_flight()
            print("\nAction completed.")
            print("=" * 20)
            
        elif choice == '6':
            service.view_pilot_schedule()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '7':
            service.add_destination()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '8':
            service.view_flight_details()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '9':
            service.get_flight_summary()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '10':
            service.delete_flight_by_number()
            print("\nAction completed.")
            print("=" * 20)

        elif choice == '11':
            service.view_flights_per_pilot()
            print("\nAction completed.")
            print("=" * 20)
            
        elif choice == '12':
            service.view_flight_count_by_destination()
            print("\nAction completed.")
            

        elif choice == '0':
            print("\nThank you for using the Flight Management System.")
            break

        else:
            print("\nInvalid choice. Please enter a number between 0 and 12.")

        # Prompt to continue or exit
        again = input("\nReturn to menu? (yes/no): ").strip().lower()
        if again != 'yes':
            print("\nThank you for using the Flight Management System.")
            break

if __name__ == "__main__":
    main()