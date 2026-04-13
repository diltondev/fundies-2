"""All classes for the application"""

from datetime import datetime
from collections.abc import Iterator
from requests import request


API_URL = "https://webtris.nationalhighways.co.uk/api/v1.0"


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

    ENDPOINT = "/reports"  # The endpoint for requesting reports


class DailyReportRequest(ReportRequest):
    """
    A class to be used to make requests to the WebTRIS API's daily report endpoint. This endpoint provides data in fifteen minute intervals.
    A corresponding `TrafficObservation` class is used to support returns. Make a request by calling `.send()`

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
    send() -> `list[TrafficObservation]`
        The send method which makes the call to the API and returns a list of observations. Can raise errors.

    """

    ENDPOINT = f"{ReportRequest.ENDPOINT}/daily"

    _site_id: int

    @property
    def site_id(self) -> int:
        return self._site_id

    @site_id.setter
    def site_id(self, new: int) -> None:
        if not isinstance(new, int):
            raise TypeError("Cannot assign non-int to site_id")
        self._site_id = new

    _date: datetime

    @property
    def date(self) -> datetime:
        return self._date

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

    def send(self) -> list["TrafficObservation"]:
        """
        Sends a request to the WebTRIS API. Gets the `/reports/daiy` endpoint and returns formatted data based on the API's response.

        Returns
        -------
        list[TrafficObservation]
            A list of observations of traffic flow for the day given when initializing the class. site_id, observation_end_datetime, average_speed, and vehicle_count
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
            url=API_URL + DailyReportRequest.ENDPOINT,
            params={
                "sites": self.site_id,
                "start_date": self.date.strftime("%d%m%Y"),
                "end_date": self.date.strftime("%d%m%Y"),
                "page": 1,
                "page_size": 500,
            },
        )
        res.raise_for_status()
        if res.status_code == 204:
            return []
        data = res.json()
        if "Rows" not in data:
            raise ValueError(
                "`Rows` not found in `DailyReportReportRequest.send()`. Required field to form data."
            )
        observation_list: list[TrafficObservation] = []
        for observation in data["Rows"]:
            try:
                observation_list.append(
                    TrafficObservation.from_dict(self.site_id, observation)
                )
            except (ValueError, TypeError):
                # Silently exclude any faulty observations not containing full amounts of data
                continue
        return observation_list

    def __repr__(self):
        return f"DailyReportRequest(site_id={self.site_id}, date={self.date.strftime('%Y-%m-%d')})"

    def __str__(self):
        return f"DailyReportRequest for site {self.site_id} on {self.date.strftime('%Y-%m-%d')}"


class TrafficObservation:
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
    date: datetime
        A datetime.datetime object representing the date of the observation. Hours, minutes, seconds, and microseconds are 0.
    end_time_minutes_in_day: int
        An int representing how many minutes into the day the observation is. For example, 01:15:00 would be 75.
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
    def from_dict(cls, site_id: int, data: dict) -> "TrafficObservation":
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
        ValueError
            If trying to initialize with non-numeric "Avg mph" or "Total Volume"

        Returns
        -------
        DailyReportRequest.TrafficObservation
            A new `FifteenMinutesObservation` containing the data given.
        """
        dt = datetime.fromisoformat(data["Report Date"])
        if "Time Period Ending" not in data:
            raise ValueError(
                "Cannot construct `TrafficObservation` from dict without valid timestamp"
            )

        time: list[int] = [
            int(n) for n in data["Time Period Ending"].split(":")
        ]  # Split "00:11:22" time into int array of [0, 11, 22] for [hour, minute, second]
        dt = dt.replace(
            hour=time[0], minute=time[1], second=time[2], microsecond=0
        )  # Set time of datetime to time given in "Time Period Ending"
        # print(f"making w data: {data}")
        return cls(
            site_name=data.get("Site Name"),
            site_id=site_id,
            end_time=dt,
            average_speed=float(data.get("Avg mph")),
            vehicle_count=int(data.get("Total Volume")),
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
    def site_id(self) -> int:
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
            raise ValueError("Cannot initialize TrafficObservation with no/empty name!")
        self._site_name = site_name

        if not isinstance(site_id, int) or site_id <= 0:
            raise ValueError(
                "Cannot initialize TrafficObservation with no/<=0 site_id!"
            )
        self._site_id = site_id

        if not isinstance(end_time, datetime) or end_time.timestamp() <= 0:
            raise ValueError(
                "Cannot initialize TrafficObservation with no/<=0 end_time!"
            )
        self._observation_end_datetime = end_time

        if not isinstance(average_speed, (int, float)) or average_speed < 0:
            raise ValueError(
                "Cannot initialize TrafficObservation with no/<0 average_speed!"
            )
        self._average_speed = average_speed

        if not isinstance(vehicle_count, int) or vehicle_count < 0:
            raise ValueError(
                "Cannot initialize TrafficObservation with no/<0 vehicle_count!"
            )
        self._vehicle_count = vehicle_count

    def __lt__(self, other: "TrafficObservation") -> bool:
        """
        Less-than operator for TrafficObservation. Compares based on end_datetime.

        Parameters
        ----------
        other : TrafficObservation
            The other observation to compare to

        Returns
        -------
        bool
            True if this observation's end_datetime is less than the other observation's end_datetime, False otherwise
        """
        return self.end_datetime < other.end_datetime

    def __gt__(self, other: "TrafficObservation") -> bool:
        """
        Greater-than operator for TrafficObservation. Compares based on end_datetime.

        Parameters
        ----------
        other : TrafficObservation
            The other observation to compare to

        Returns
        bool
            True if this observation's end_datetime is greater than the other observation's end_datetime, False otherwise
        """
        return self.end_datetime > other.end_datetime

    def __eq__(self, other: object) -> bool:
        """
        Equality operator for TrafficObservation. Compares based on end_datetime.

        Parameters
        ----------
        other : object
            The other observation to compare to

        Returns
        -------
        bool
            True if this observation's end_datetime is equal to the other observation's end_datetime, False otherwise
        """
        return self.end_datetime == other.end_datetime

    def __repr__(self) -> str:
        return f"TrafficObservation(site_name='{self.site_name}', site_id={self.site_id}, end_time='{self.end_datetime.strftime('%Y-%m-%d %H:%M:%S')}', average_speed={self.average_speed}, vehicle_count={self.vehicle_count})"

    def __str__(self) -> str:
        return f"Observation at site {self.site_name} (ID {self.site_id}) on {self.end_datetime.strftime('%Y-%m-%d %H:%M:%S')}: average speed {self.average_speed} mph, vehicle count {self.vehicle_count}"


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
    name: str, readonly
        The name of the site this object corresponds to. Obtained from the API when `.update_data()` is called.
    """

    _observations: list[TrafficObservation]
    _date: datetime
    _site_id: int
    _name: str

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, new: datetime):
        self._date = new
        self.update_data()

    @property
    def site_id(self) -> int:
        return self._site_id

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, site_id: int, date: datetime = datetime.now()):
        self._date = date
        self._site_id = site_id
        self.update_data()

    def get_observations_list(self) -> list[TrafficObservation]:
        """
        Returns a shallow copy of the observations related to this site

        Returns
        -------
        list[TrafficObservation]
            The shallow copy
        """
        return self._observations.copy()

    def update_data(self):
        """
        Makes another call to the API to update the observation data. Called on `__init__` and `@date.setter`
        """
        requestor = DailyReportRequest(site_id=self.site_id, date=self.date)
        self._observations = requestor.send()
        self._observations.sort()
        self._name = (
            self._observations[0].site_name
            if len(self._observations) > 0
            else "Unknown Site"
        )

    def get_average_speed(self) -> float:
        """
        Calculates the average speed over all observations in mph. Weighted based on total vehicle count in each observation.

        Returns
        -------
        float
            The average speed in mph
        """
        total_weighted_speed = sum(
            o.average_speed * o.vehicle_count for o in self._observations
        )
        total_count = sum(o.vehicle_count for o in self._observations)
        return total_weighted_speed / total_count if total_count > 0 else 0.0

    def get_hourly_average_speed(self, hour: int) -> float:
        """
        Calculates the average speed on datapoints where observation.end_datetime.hour == hour
        Weighted based on total vehicle count in each observation.

        Parameters
        ----------
        hour : int
            24 hour (0-23) time to search for

        Returns
        -------
        float
            The average speed in mph for that hour
        """
        if hour < 0 or hour > 23:
            raise ValueError("Hour must be between 0 and 23 inclusive")
        total_weighted_speed = sum(
            o.average_speed * o.vehicle_count
            for o in self._observations
            if o.end_datetime.hour == hour
        )
        total_count = sum(
            o.vehicle_count for o in self._observations if o.end_datetime.hour == hour
        )
        return total_weighted_speed / total_count if total_count > 0 else 0.0

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
        if hour < 0 or hour > 23:
            raise ValueError("Hour must be between 0 and 23 inclusive")
        return sum(
            o.vehicle_count for o in self._observations if o.end_datetime.hour == hour
        )

    def get_peak_hour(self) -> int:
        """
        Gets hour (0-23) where the maximum number of cars were observed
        Returns 0 if there are no observations

        Returns
        -------
        int
            The hour (0-23) with the highest amount of vehicles
        """
        hourly_counts: dict[int:int] = dict()
        for o in self._observations:
            hour = o.end_datetime.hour
            if hour not in hourly_counts:
                hourly_counts[hour] = 0
            hourly_counts[hour] += o.vehicle_count
        return (
            max(hourly_counts.items(), key=lambda x: x[1])[0] if hourly_counts else 0
        )  # Return hour with most vehicles

    def get_records_for_hour(self, hour: int) -> list[TrafficObservation]:
        """
        Gets all records where observation.end_datetime.hour == hour

        Parameters
        ----------
        hour : int
            24 hour (0-23) time to search for

        Raises
        ------
        ValueError
            If hour is not between 0 and 23

        Returns
        -------
        list[TrafficObservation]
            All records in that hour
        """
        if hour < 0 or hour > 23:
            raise ValueError("Hour must be between 0 and 23 inclusive")
        return [o for o in self._observations if o.end_datetime.hour == hour]

    def __getitem__(
        self, key: int | slice
    ) -> TrafficObservation | list[TrafficObservation]:
        return self._observations[key]

    def __len__(self):
        return len(self._observations)

    def __iter__(self) -> Iterator[TrafficObservation]:
        # Guaranteed to be in chronological order due to sorting in `update_data()`
        for o in self._observations:
            yield o

    def __repr__(self) -> str:
        return f"Site(site_id={self.site_id}, name='{self.name}', date='{self.date.strftime('%Y-%m-%d')}', observations={self._observations})"

    def __str__(self) -> str:
        return f"Site {self.site_id} ({self.name}) on {self.date.strftime('%Y-%m-%d')} with {len(self._observations)} observations"
