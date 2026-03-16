"""Demonstration on how to use the application"""
from datetime import datetime
from webtris_client import WebTRISClient, Site, FifteenMinuteObservation, DailyReportRequest, SitesRequest

if __name__ == "__main__":
    # Ask for coordinates and date
    latitude = input("Enter the latitude: ")
    try:
        float(latitude)
    except ValueError:
        print("Invalid latitude. Please enter a valid number.")
        exit(1)
    longitude = input("Enter the longitude: ")
    try:
        float(longitude)
    except ValueError:
        print("Invalid longitude. Please enter a valid number.")
        exit(1)
    date_str = input("Enter the date (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
        exit(1)
        
    # Get the site id closest to the coordinates
    sites = SitesRequest().send()
    closest_site = min(sites.sites, key=lambda site: (site.latitude - float(latitude))**2 + (site.longitude - float(longitude))**2)
    site_id = closest_site.id
    print(f"Closest site ID: {site_id}")
        
    # Get the traffic data for the site and date
    site = Site(site_id=site_id, date=date)
    print(f"Site Name: {site.name or 'Unknown Name'}")
    print(f"Average Speed: {site.get_average_speed()} mph")
    print(f"Vehicle Count: {site.get_vehicle_count()}")
    peak_hour = site.get_peak_hour()
    print(f"Peak Hour: {peak_hour} ({site.get_hourly_vehicle_count(peak_hour)} vehicles)")
    
    """
    Example usage:
    Enter the latitude: 51.4087721045577
    Enter the longitude: 0.381354080809833
    Enter the date (YYYY-MM-DD): 2025-03-10
    
    Closest site ID: 14
    Site Name: A2/8392M
    Average Speed: 42.467943045611776 mph
    Vehicle Count: 12431
    Peak Hour: 8 (1094 vehicles)
    """
        
    