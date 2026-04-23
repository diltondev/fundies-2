from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
import heapq
from webtris_client import Site


class RouteSegment:
    """
    A class to represent a road (edge) with an implied terminus (vertex).

    Attributes
    ----------
    name: str, readonly
        The name of this RouteSegment. Usually to represent the end point of the segment
    sites: list[Site], readonly
        A list of all the sites that are on the road path in this segment. Used to obtain speeds.
    next_segments: list[RouteSegment]
        A list of the next possible segments that originate at the end of this segment.
    date: datetime
        The datetime that this segment is using to calculate speeds. All traffic data will use this date.
        Expensive to set if outside of same 24-hour UTC date as API calls will be made for each site.
    length: float
        The length of this RouteSegment in miles.
    """

    _name: str
    _sites: list[Site]
    next_segments: list["RouteSegment"]
    _date: datetime
    length: float  # in miles

    @property
    def name(self) -> str:
        return self._name

    @property
    def sites(self) -> list[Site]:
        return self._sites.copy()

    def append_site_by_id(self, new_site_id: int) -> None:
        """
        Appends a new site to the internal list of sites by id and updates its date.

        Parameters
        ----------
        new_site_id : int
            The id of the new site to add. Does nothing if site already in this segment.
        """
        if new_site_id in [s.site_id for s in self.sites]:
            return
        new_site = Site(new_site_id, self.date)
        self._sites.append(new_site)

    def remove_site_by_id(self, old_site_id: int) -> None:
        """
        Removes a site on the internal list contained by this segment by its id/

        Parameters
        ----------
        old_site_id : int
            The id of the site to remove.
        """
        self.sites.remove(site for site in self.sites if site.site_id == old_site_id)

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, new_date: datetime):
        # Update Site dates if new date is not in same 24 hour window
        if new_date.date() != self.date.date():
            for site in self._sites:
                site.date = new_date
        self._date = new_date

    def get_average_speed(self) -> float:
        """
        Gets the average speed of all sites on this segment at the internal date and time.

        Returns
        -------
        float
            The average speed in MPH.
        """
        avg_speeds: list[int] = list()
        for site in self.sites:
            observation = None
            for o in site.get_observations_list():
                if o.end_datetime > self.date:
                    observation = o
                    break
            if observation:
                avg_speeds.append(observation.average_speed)
        return sum(avg_speeds) / len(avg_speeds)

    def get_traversal_time(self) -> float:
        """
        Gets the time to traverse this specific route segment.

        Returns
        -------
        float
            The time to traverse this segment in hours.
        """
        return self.length / self.get_average_speed()

    def __repr__(self) -> str:
        """
        A debug-level string representation of a RouteSegment.

        Returns
        -------
        str
            The string representation
        """
        site_ids = [site.site_id for site in self.sites]
        return f"RouteSegment(name= {self.name}, get_traversal_time()={self.get_traversal_time()} ids={site_ids})"

    def __str__(self) -> str:
        """
        A user-presentable representation of a RouteSegment

        Returns
        -------
        str
            The string representation
        """
        return (
            f"{self.name} segment taking {self.get_traversal_time() * 60:.1f} minutes"
        )

    def __init__(self, name: str, site_ids: list[int], date: datetime, length: int):
        """
        Initializes a new instance of a RouteSegment

        Parameters
        ----------
        name : str
            A description of the segment. I.e. "A30 to Heathrow"
        site_ids : list[int]
            A list of WebTRIS sites which are along the segment. Can be initialized to [] and added later though it is recommended to add them at the beginning.
        date : datetime
            The datetime to fetch traffic data for. Date and time components matter.
        length : int
            The length of the segment in miles.
        """
        self._name = name
        self._date = date
        self._sites = list()
        self.next_segments = list()
        self.length = length
        for site_id in site_ids:
            self._sites.append(Site(site_id, self.date))


class RouteSegmentExternal(RouteSegment):
    """
    A class representing a simplified RouteSegment. Contains only pre-filled data.

    Attributes
    ----------
    avg_speed: float
        The pre-set average speed in this segment
    """

    avg_speed: float

    def get_average_speed(self) -> float:
        """
        A simplified version of get_average_speed that simply returns the internal, pre-set speed.

        Returns
        -------
        float
            The average speed in mph
        """
        return self.avg_speed

    def __init__(
        self, name: str, date: datetime, length: int, override_avg_speed: float
    ):
        super().__init__(name, [], date, length)
        self.avg_speed = override_avg_speed


class SearchStrategy(ABC):
    """
    An abstract class which headers the search() method for search strategies to implement.
    """

    @abstractmethod
    def search(self, head: RouteSegment, target: RouteSegment) -> list[RouteSegment]:
        """
        An abstract version of search. Does nothing.

        Parameters
        ----------
        head : RouteSegment
            The origin segment of a route at which searches will start.
        target : RouteSegment
            The target position which searches will try to locate.

        Returns
        -------
        list[RouteSegment]
            An in-order list of RouteSegments which includes `head` and `target` as a route chosen by the search algoritm
        """
        pass


class DepthFirstSearch(SearchStrategy):
    def _dfs_search(
        self, head: RouteSegment, target: RouteSegment, visited: list[RouteSegment]
    ) -> list[RouteSegment]:
        """
        An internal, recursive function for DFS searching.
        """
        visited.append(head)
        if head == target:
            return [head]
        for segment in head.next_segments:
            if segment in visited:
                continue
            p = self._dfs_search(segment, target, visited)
            if p:
                p.append(head)
                return p
        return None

    def search(self, head: RouteSegment, target: RouteSegment) -> list[RouteSegment]:
        """
        Searches RouteSegments for a viable route on a depth-first basis. Searches from low index to high index on `<RouteSegment>.next_segments`

        Parameters
        ----------
        head : RouteSegment
            The origin segment of a route at which searches will start.
        target : RouteSegment
            The target position which searches will try to locate.

        Returns
        -------
        list[RouteSegment]
            An in-order list of RouteSegments which includes `head` and `target` chosen by DFS.
        """
        result = self._dfs_search(head, target, list())
        result.reverse()
        return result


class BreadthFirstSearch(SearchStrategy):
    def search(self, head: RouteSegment, target: RouteSegment) -> list[RouteSegment]:
        """
        Searches RouteSegments for a viable route on a breadth-first basis. Enqueues from low index to high index on `<RouteSegment>.next_segments`


        Parameters
        ----------
        head : RouteSegment
            The origin segment of a route at which searches will start.
        target : RouteSegment
            The target position which searches will try to locate.

        Returns
        -------
        list[RouteSegment]
            An in-order list of RouteSegments which includes `head` and `target` chosen by BFS.
        """
        # Hold the deque as a list of paths to evaluate the segment at the end of the list.
        # Used to be able to return the path at the end.
        q: deque[list[RouteSegment]] = deque([[head]])
        visited: set[RouteSegment] = set()
        while q:
            cur_path = q.popleft()
            # Python refuses to hold an empty deque of lists so empty ones must be skipped
            if len(cur_path) == 0:
                continue
            # Evaluate based on current end of partial route
            cur_node = cur_path[-1]
            if cur_node == target:
                return cur_path
            if cur_node in visited:
                continue
            paths: list[list[RouteSegment]] = [[]]
            for next in cur_node.next_segments:
                new_path = cur_path.copy()
                new_path.append(next)
                paths.append(new_path)
            q.extend(paths)
            visited.add(cur_node)


class DijkstrasAlgoSearch(SearchStrategy):
    def search(self, head: RouteSegment, target: RouteSegment) -> list[RouteSegment]:
        """
        Searches RouteSegments for a viable route based on Dijkstra's Algorithm. Prioritizes to minimize time of commute and does not consider physical length.


        Parameters
        ----------
        head : RouteSegment
            The origin segment of a route at which searches will start.
        target : RouteSegment
            The target position which searches will try to locate.

        Returns
        -------
        list[RouteSegment]
            An in-order list of RouteSegments which includes `head` and `target` chosen by Dijkstra's Algorithm.
        """
        # Hold the min-heap as a list of (time, path) tuples to evaluate the segment at the end of the list.
        # Used to be able to return the path at the end.
        # Python uses the first value in tuples for comparison, so heapq will rank based on traverse time
        paths: list[tuple[float, list[RouteSegment]]] = []
        # Must use [head] here to maintain a list of RouteSegments for a partial Route
        heapq.heappush(paths, (head.get_traversal_time(), [head]))
        visited: set[RouteSegment] = set()
        while paths:
            cur_time, cur_path = heapq.heappop(paths)
            if len(cur_path) == 0:
                continue
            cur_node: RouteSegment = cur_path[-1]
            if cur_node == target:
                return cur_path
            if cur_node in visited:
                continue
            for next in cur_node.next_segments:
                new_path = cur_path.copy()
                new_path.append(next)
                heapq.heappush(paths, (cur_time + next.get_traversal_time(), new_path))
            visited.add(cur_node)