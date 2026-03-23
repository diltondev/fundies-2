"""Demonstration on how to use the application"""
from datetime import datetime
from webtris_client import Site, TrafficObservation, DailyReportRequest

if __name__ == "__main__":
    site_id = input("Enter a site ID: ")
    try: 
        site_id = int(site_id)
    except ValueError:
        print("Invalid site ID. Please enter a valid integer.")
        exit(1)
    
    date = input("Enter a date (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        exit(1)

    # Get the traffic data for the site and date
    site = Site(site_id=site_id, date=date)
    print(f"Site Name: {site.name or 'Unknown Name'}")
    print(f"Average Speed: {site.get_average_speed()} mph")
    print(f"Vehicle Count: {site.get_vehicle_count()}")
    peak_hour = site.get_peak_hour()
    print(f"Peak Hour: {peak_hour} ({site.get_hourly_vehicle_count(peak_hour)} vehicles)")
    
    """
    Example usage:
    Enter a site ID: 14
    Enter a date (YYYY-MM-DD): 2025-03-10
    
    Site Name: A2/8392M
    Average Speed: 42.467943045611776 mph
    Vehicle Count: 12431
    Peak Hour: 8 (1094 vehicles)
    """
        
    