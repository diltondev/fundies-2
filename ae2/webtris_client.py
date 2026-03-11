"""All classes for the application"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import math
from collections.abc import Iterator
from requests import request


class WebTRISClient:
    @staticmethod
    @property
    def API_URL() -> str:
        "https://webtris.nationalhighways.co.uk/api/v1.0"

    class FetchError(Exception):
        def __init__(self, status_code: int, status_message: str = ""):
            super().__init__(
                f"Recieved a non-okay status when fetching!\nError code: {status_code}\nDetails: {status_message}"
            )


class SitesRequest:
    """
    A class to request a list of all sites from the /sites endpoint.
    `response` will hold the response in the form of `SitesRequest.Response` after the `send()` method is called.

    Attributes
    ----------
    ENDPOINT: str, static
        The endpoint for site requests on the API. This should not be changed.

    Methods
    -------
    send() -> `SitesRequest.SitesResponse`
        Sends a request to the API and returns the response. Throws errors if `not status.ok`. Otherwise silently excludes deformed data.
    """

    @staticmethod
    @property
    def ENDPOINT() -> str:
        "/sites"  # The endpoint for requesting sites

    @dataclass(frozen=True)
    class SitesResponse:
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
        class _Site:
            """
            A frozen dataclass representing one site in a `SitesRequest.Response`

            Attributes
            ----------
            id: int, readonly
                The ID of the site
            name: str, readonly
                A human-readable description of the site's location
            description: str, readonly
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

        @classmethod
        def from_dict(cls, data: dict) -> "SitesRequest.SitesResponse":
            sites_response = cls(row_count=data["row_count"], sites=[])
            for site in data["sites"]:
                # Check data for validity and silently exclude faulty sites
                if not (
                    "Id" in site
                    and "Name" in site
                    and "Description" in site
                    and "Longitude" in site
                    and "Latitude" in site
                    and "Status" in site
                ):
                    continue  # Exclude API response sites missing a field
                try:
                    _ = int(site["Id"])
                except ValueError:
                    continue  # Exclude non-numeric or missing ID's
                if site["Name"] == "":
                    continue
                if site["Description"] == "":
                    continue
                if site["Longitude"] == 0.0 or site["Latitude"] == 0.0:
                    continue  # Latitude and Longitude are 14-digit precise: won't be at exactly 0.0
                if site["Status"] == "":
                    continue
                sites_response.sites.append(
                    WebTRISClient.SitesRequest.Response._Site(
                        id=int(site["Id"]),
                        name=site["Name"],
                        description=site["Description"],
                        longitude=site["Longitude"],
                        latitude=site["Latitude"],
                        status=site["Status"],
                    )
                )
                return sites_response

    def send(this) -> SitesResponse:
        """
        This method sends a request to the sites endpoint. It stores the response in `this._response`.
        Raises errors when request completely fails; silently excludes faulty sites (any missing/invalid fields).
        """
        res = request(
            "GET", WebTRISClient.API_URL + WebTRISClient.SitesRequest.ENDPOINT
        )
        if not res.ok:
            raise WebTRISClient.FetchError(res.status_code, res.reason)
        data = res.json()
        sites_response = SitesRequest.SitesResponse.from_dict(data)
        return sites_response

    def __init__(this):
        """
        Returns a new SitesRequest object
        """


class ReportRequest:
    """
    A class to request a list of traffic observations aggregated at different scales from the /reports endpoint.\
    This class must be subclassed to implement methods and return types as each level of aggregation returns different data.
    Aggregation levels are daily, monthly, and annualy. Only daily has been implemented. 
    
    
    
    Attributes
    ----------
    ENDPOINT: str, static
        The endpoint for site requests on the API. This should not be changed.
    """

    @staticmethod
    @property
    def ENDPOINT() -> str:
        "/reports"  # The endpoint for requesting reports


class DailyReportRequest(ReportRequest):
    """
    A class to be used to make requests to the WebTRIS API's daily report endpoint. This endpoint provides data in fifteen minute intervals.
    A corresponding `FifteenMinuteObservation` class is used to support returns. Make a request by calling `.send()`

    Attributes
    ----------
    ENDPOINT: str, static, readonly
        The endpoint used to make requests to the API. Do not change this.
    site_id: int
        The ID of the site this object handles. All requests using this object will be made using `site_id`
    date: datetime
        The datetime object representing what day requests should be made to. Strips hours, minutes, seconds, and microseconds on assignment for comparability.

    Methods
    -------
    send() -> `list[FifteenMinuteObservation]`
        The send method which makes the call to the API and returns a list of observations. Can raise errors.

    """

    @property
    @staticmethod
    def ENDPOINT() -> str:
        f"{ReportRequest.ENDPOINT}/daily"

    _site_id: int

    @property
    def site_id(self) -> int:
        self._site_id

    @site_id.setter
    def site_id(self, new: int) -> None:
        if not isinstance(new, int):
            raise TypeError("Cannot assign non-int to site_id")
        self._site_id = new

    _date: datetime

    @property
    def date(self) -> datetime:
        self._date

    @date.setter
    def date(self, new: datetime) -> None:
        if not isinstance(new, datetime):
            raise TypeError("Cannot assign non-datetime to date")
        self._date = new.replace(
            hour=0, minute=0, second=0, microsecond=0
        )  # Ignore time and set to midnight of date
        
    def __init__(
        self,
        site_id: int,
        date: datetime,
    ):
        self.site_id = site_id
        self.date = date

    def send(self) -> list["FifteenMinuteObservation"]:
        """
        Sends a request to the WebTRIS API. Gets the `/reports/daiy` endpoint and returns formatted data based on the API's response.

        Returns
        -------
        list[FifteenMinuteObservation]
            A list of observations of traffic flow for the day given when initializing the class. site_name, site_id, observation_end_datetime, average_speed, and vehicle_count
            can be relied upon in those observations as they will otherwise be excluded.

        Raises
        ------
        WebTRISClient.FetchError
            Raised in the case that the fetch does not return a res.ok
        ValueError
            Raised if "Rows" not in returned data dictionary
        """

        res = request(
            method="GET",
            url=WebTRISClient.API_URL + DailyReportRequest.ENDPOINT,
            params={
                "sites": self.site_id,
                "start_date": self.date.strftime("%Y%m%d"),
                "end_date": self.date.strftime("%Y%m%d"),
                "page": 1,
                "page_size": 500,
            },
        )
        if not res.ok:
            raise WebTRISClient.FetchError(res.status_code, res.reason)
        data = res.json()
        if "Rows" not in data:
            raise ValueError(
                "`Rows` not found in `DailyReportReportRequest.send()`. Required field to form data."
            )
        observation_list: list[FifteenMinuteObservation] = []
        for observation in data["Rows"]:
            try:
                observation_list.append(
                    FifteenMinuteObservation.from_dict(observation)
                )
            except ValueError:
                # Silently exclude any faulty observations not containing full amounts of data
                continue
        
class FifteenMinuteObservation:
    """
    A class to represent a fifteen minute measurement of traffic data from the WebTRIS API.


    Attributes
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

    Raises
    ------
    ValueError
        If trying to initialize with no/empty `name`
    ValueError
        If trying to initialize with no/<=0 `id`
    ValueError
        If trying to initialize with no/<=0 `end_time`
    ValueError
        If trying to initialize with no/<0 `average_speed`
    ValueError
        If trying to initialize with no/<0 `vehicle_count`
    """

    @classmethod
    def from_dict(
        cls, site_id: int, data: dict
    ) -> "DailyReportRequest.FifteenMinuteObservation":
        """
        Creates a new `FifteenMinutesObservation` object using key-value dictionary in the format provided by WebTRIS API.

        Parameters
        ----------
        data : dict
            Data in the format:
            "Site Name": "7001/1",
            "Report Date": "2025-03-07T00:00:00",
            "Time Period Ending": "00:14:00",
            "Avg mph": "66",
            "Total Volume": "7"

        Raises
        ------
        ValueError
            If trying to initialize with no/empty "Time Period Ending"

        Returns
        -------
        DailyReportRequest.FifteenMinuteObservation
            A new `FifteenMinutesObservation` containing the data given.
        """
        dt = datetime.fromisoformat(data["Report Date"])
        if "Time Period Ending" not in data:
            raise ValueError(
                "Cannot construct `FifteenMinuteObservation` from dict without valid timestamp"
            )
        time: list[int] = [
            int(n) for n in data["Time Period Ending"].split(":")
        ]  # Split "00:11:22" time into int array of [0, 11, 22] for [hour, minute, second]
        dt.hour = time[0]
        dt.minute = time[1]
        dt.second = time[2]

        return cls(
            site_name=data.get("Site Name"),
            site_id=site_id,
            end_time=dt,
            average_speed=data.get("Avg mph"),
            vehicle_count=data.get("Total Volume"),
        )
        
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
    def end_datetime(self) -> datetime:
        return self._observation_end_datetime

    @property
    def date(self) -> datetime:
        return datetime(
            self._observation_end_datetime.year,
            self._observation_end_datetime.month,
            self._observation_end_datetime.day,
        )

    @property
    def end_time_minutes_in_day(self) -> int:
        return (
            self._observation_end_datetime.hour * 60
            + self._observation_end_datetime.minute
        )

    @property
    def average_speed(self) -> float:
        return self._average_speed

    @property
    def vehicle_count(self) -> int:
        return self._vehicle_count

        
    def __init__(
        self,
        site_name: str,
        site_id: int,
        end_time: datetime,
        average_speed: float,
        vehicle_count: int,
    ):
        if not isinstance(site_name, str) or site_name == "":
            raise ValueError(
                "Cannot initialize FifteenMinuteObservation with no/empty name!"
            )
        self._site_name = site_name

        if not isinstance(site_id, int) or site_id <= 0:
            raise ValueError(
                "Cannot initialize FifteenMinuteObservation with no/<=0 site_id!"
            )
        self._site_id = site_id

        if not isinstance(end_time, datetime) or end_time.timestamp() <= 0:
            raise ValueError(
                "Cannot initialize FifteenMinuteObservation with no/<=0 end_time!"
            )
        self._observation_end_datetime = end_time

        if not isinstance(average_speed, (int, float)) or average_speed < 0:
            raise ValueError(
                "Cannot initialize FifteenMinuteObservation with no/<0 average_speed!"
            )
        self.average_speed = average_speed

        if not isinstance(vehicle_count, int) or vehicle_count < 0:
            raise ValueError(
                "Cannot initialize FifteenMinuteObservation with no/<0 vehicle_count!"
            )
        vehicle_count = vehicle_count

        
        
class Site:
    """
    A class to represent one traffic camera and corresponding data in WebTRIS.
    Objects can be indexed into to reach FifteenMinuteObeservation elements. A shallow copy can be obtained instead via `.get_observations_list()` 

    Attributes
    ----------
    date: datetime
        The date on which the observations are recorded. May have errounious hours, minutes, and seconds. Calls `.update_data()` on change.
    site_id: int, readonly
        The site identifier which this object corresponds to.
    """
    
    _observations: list[FifteenMinuteObservation]
    _date: datetime
    _site_id: int
    
    @property
    def date(self) -> datetime: self._date
    @date.setter
    def date(self, new: datetime):
        self._date = new
        self.update_data()
    
    @property
    def site_id(self) -> int: self._site_id
    
    def __init__(self, site_id: int, date: datetime = datetime.now()):
        self._date = date
        self._site_id = site_id
        self.update_data()
        
    def get_observations_list(self) -> list[FifteenMinuteObservation]:
        """
        Returns a shallow copy of the observations related to this site

        Returns
        -------
        list[FifteenMinuteObservation]
            The shallow copy
        """
        self._observations.copy()
        
    def update_data(self):
        """
         Makes another call to the API to update the observation data. Called on `__init__` and `@date.setter`
        """
        requestor = DailyReportRequest(site_id=self.site_id, date=self.date)
        self._observations = requestor.send()
        self._observations.sort(key=lambda o: o.end_time_minutes_in_day)
    
    def get_average_speed(self) -> float:
        """
        Calculates the average speed over all observations in mph

        Returns
        -------
        float
            The average speed in mph
        """
        return sum(o.average_speed for o in self._observations) / len(self._observations)
    
    def get_hourly_average_speed(self, hour: int) -> float:
        """
        Calculates the average speed on datapoints where observation.end_datetime.hour == hour

        Parameters
        ----------
        hour : int
            24 hour (0-23) time to search for

        Returns
        -------
        float
            The average speed in mph for that hour
        """
        return sum(o.average_speed for o in self._observations if o.end_datetime.hour == hour) / len(self._observations)
    
    def get_vehicle_count(self) -> int:
        """
        Calculates total number of vehicles through all observations

        Returns
        -------
        int
            The total vehicle count over all observations
        """
        return sum(o.vehicle_count for o in self._observations) 
    
    def get_hourly_vehicle_count(self, hour: int) -> int:
        """
        Calculates total number of vehicles through all observations where observation.end_datetime.hour == hour

        Parameters
        ----------
        hour : int
            24 hour (0-23) time to search for 

        Returns
        -------
        int
            The total vehicle count over that hour
        """
        return sum(o.vehicle_count for o in self._observations if o.end_datetime.hour == hour)
    
    def get_peak_hour(self) -> int:
        """
        Gets hour (0-23) where the maximum number of cars were observed

        Returns
        -------
        int
            The hour (0-23) with the highest amount of 
        """
        hourly_counts: dict[int: int] = dict()
        for o in self._observations:
            hour = o.end_datetime.hour
            if hour not in hourly_counts:
                hourly_counts[hour] = 0
            hourly_counts[hour] += o.vehicle_count
        return max(hourly_counts.items(), key=lambda x: x[1])[0] # Return hour with most vehicles
    
    def get_records_for_hour(self, hour: int) -> list[FifteenMinuteObservation]:
        """
        Gets all records where observation.end_datetime.hour == hour

        Parameters
        ----------
        hour : int
            24 hour (0-23) time to search for 

        Returns
        -------
        list[FifteenMinuteObservation]
            All records in that hour
        """
        return [o for o in self._observations if o.end_datetime.hour == hour]
    
    def __getitem__(self, key: int | slice) -> FifteenMinuteObservation | list[FifteenMinuteObservation]:
        return self._observations[key]

    def __len__(self):
        return len(self._observations)
    
    def __iter__(self) -> Iterator[FifteenMinuteObservation]:
        for o in self._observations:
            yield o
