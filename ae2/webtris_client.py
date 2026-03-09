"""All classes for the application"""
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from requests import request

class TrafficObservation():
    """
    A class which holds data related to a fifteen minute interval of traffic.
    Designed for data in WebTRIS API format.
    """
    
    # Internal storage of properties
    _site_name: str
    _site_id: int
    _observation_end_datetime: datetime
    _average_speed: float
    _vehicle_count: int

    # Exposed read-only public properties
    @property
    def site_name(self) -> str:
        return self._site_name
    @property
    def site_id(self) -> str:
        return self._site_id
    @property
    def observation_end_datetime(self) -> datetime:
        return self._observation_end_datetime
    @property
    def observation_date(self) -> datetime:
        return datetime(self._observation_end_datetime.year, self._observation_end_datetime.month, self._observation_end_datetime.day)
    @property
    def observation_end_time_minutes_in_day(self) -> int:
        return self._observation_end_datetime.hour * 60 + self._observation_end_datetime.minute
    @property
    def average_speed(self) -> float:
        return self._average_speed
    @property
    def vehicle_count(self) -> int:
        return self._vehicle_count
    
    def __init__(self, 
                 site_name: str, 
                 site_id: int, 
                 end_time: datetime, 
                 average_speed: float, 
                 vehicle_count: int):
        """
        Forms a new TrafficObservation instance measuring a fifteen minute interval of traffic.
        
        
        Parameters
        ----------
            site_name: str
                The site name returned in WebTRIS API.
            site_id: int
                The site name returned in WebTRIS API.
            end_time: datetime 
                A datetime.datetime object representing the ending time of the observation. Units smaller than minute should be 0.
            average_speed: float
                A float containing the average speed in miles per hour (mph) of vehicles in the observation time.
            vehicle_count: int
                The int count of all vehicles passing through the observation point.
        Returns
        -------
        TrafficObservation
            A new TrafficObservation object with the given data
        """
        if not isinstance(site_name, str) or site_name == "":
            raise ValueError("Cannot initialize TrafficObservation with no/empty name!")
        self._site_name = site_name
        
        if not isinstance(site_id, int) or site_id <= 0:
            raise ValueError("Cannot initialize TrafficObservation with no/<=0 site_id!")
        self._site_id = site_id
        
        if not isinstance(end_time, datetime) or end_time.timestamp() <= 0:
            raise ValueError("Cannot initialize TrafficObservation with no/<=0 end_time!")
        self._observation_end_datetime = end_time
        
        if not isinstance(average_speed, (int, float)) or average_speed < 0:
            raise ValueError("Cannot initialize TrafficObservation with no/<0 average_speed!")
        self.average_speed = average_speed
        
        if not isinstance(vehicle_count, int) or vehicle_count < 0:
            raise ValueError("Cannot initialize TrafficObservation with no/<0 vehicle_count!")
        vehicle_count = vehicle_count
    
    
class WebTRISClient():
    @staticmethod
    @property
    def API_URL() -> str: "https://webtris.nationalhighways.co.uk/api/v1.0"
    
    class FetchError(Exception):
        def __init__(self, status_code: int, status_message: str = ""):
            super().__init__(f"Recieved a non-okay status when fetching!\nError code: {status_code}\nDetails: {status_message}")
        
        
    
    
class RequestStrategy(ABC):
    """
    An abstract class for request attibute and send method.
    This class is meant to be used as a strategy
    """
    
    @abstractmethod
    @property
    def request(this) -> any:
        pass
    
    @abstractmethod
    def send(this) -> None:
        pass
    
    
class SitesRequest(RequestStrategy):
    """
    A class to request a list of all sites from the /sites endpoint.
    `response` will hold the response in the form of `SitesRequest.Response` after the `send()` method is called.
    
    Attributes
    ----------
    ENDPOINT: str, static
        The endpoint for site requests on the API. This should not be changed.
    response: SitesRequest.Response, readonly
        This is the response from the API on this request. Must call `this.send()` to not recieve None
    
    Methods
    -------
    send() -> None
        Sends a request to the API and stores the response in `response`
    """
    
    @staticmethod
    @property
    def ENDPOINT() -> str: "/sites"     # The endpoint for requesting sites
    
    
    @dataclass(frozen=True)
    class Response():
        """
        The response type specific to the `SitesRequest` request type.
        This class is a frozen dataclass and cannot have its attributes modified.
        
        Attributes
        ----------
        row_count: int, readonly
            The number of rows in the API response. May differ from `len(sites)` due to silent exclusion of faulty data.
        sites: list[Response._Site], readonly
            The list of all sites returned from the API.
        """
        
        @dataclass(frozen=True)
        class _Site():
            """
            A frozen dataclass representing one site in a `SitesRequest.Response`
            
            Attributes
            ----------
            id: int, readonly
                The ID of the site
            name: str, readonly
                A human-readable description of the site's location
            id: str, readonly
                Location id by motorway/markerpost
            longitude: float, readonly
                The longitude of the location
            latitude: float, readonly
                The latitude of the location
            status: str, readonly
                Either "Active" or "Inactive" 
            """
            id: int
            name: str
            description: str
            longitude: float
            latitude: float
            status: str
        
        row_count: int
        sites: list[_Site]
        

    _response: Response | None
    @property 
    def response(this) -> Response | None: 
        return this._response
    
    def send(this) -> None:
        """
        This method sends a request to the sites endpoint. It stores the response in `this._response`.
        Raises errors when request completely fails; silently excludes faulty sites (any missing/invalid fields).
        """
        res = request("GET", WebTRISClient.API_URL + WebTRISClient.SitesRequest.ENDPOINT)
        if not res.ok:
            raise WebTRISClient.FetchError(res.status_code, res.reason)
        data = res.json()
        sites_response = WebTRISClient.SitesRequest.Response(row_count=data["row_count"], sites=[])
        for site in data["sites"]:
            # Check data for validity and silently exclude faulty sites
            if not ("Id" in site and "Name" in site and "Description" in site and "Longitude" in site and "Latitude" in site and "Status" in site):
                continue # Exclude API response sites missing a field
            try:
                _ = int(site["Id"])
            except ValueError:
                continue # Exclude non-numeric or missing ID's
            if site["Name"] == "": continue
            if site["Description"] == "": continue
            if site["Longitude"] == 0.0 or site["Latitude"] == 0.0: continue # Latitude and Longitude are 14-digit precise: won't be at exactly 0.0
            if site["Status"] == "": continue
            sites_response.sites.append(
                WebTRISClient.SitesRequest.Response._Site(
                    id=int(site["Id"]),
                    name=site["Name"],
                    description=site["Description"],
                    longitude=site["Longitude"],
                    latitude=site["Latitude"],
                    status=site["Status"]
                )
            )
        this.response = sites_response    
    
    def __init__(this):
        """
        Returns a new SitesRequest object with no response stored
        """
        this.response = None


class ReportRequest(RequestStrategy):
    pass
        
        
        
             
        
    
    




class Site:
    _id: int
    _name: int
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def id(self) -> str:
        return self._id
    
    def fetchData():
        pass