"""All tests for the application"""
import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from requests.exceptions import Timeout, ConnectionError, HTTPError

from webtris_client import (
    Site,
    WebTRISClient,
    SitesRequest,
    ReportRequest,
    DailyReportRequest,
    FifteenMinuteObservation,
)

@pytest.fixture
def mock_sites_success_response():
    response = Mock(status_code=200)
    response.json.return_value = {
        "row_count": 3,
        "sites": [
            {"Id": "10", "Name": "Site 1", "Description": "A site", "Longitude": 1.0, "Latitude": 1.0, "Status": "active"},
            {"Id": "20", "Name": "Site 2", "Description": "Another site", "Longitude": 2.0, "Latitude": 2.0, "Status": "inactive"},
            {"Id": "30", "Name": "Site 3", "Description": "Yet another site", "Longitude": 3.0, "Latitude": 3.0, "Status": "active"},
        ]
    }
    return response

@pytest.fixture
def mock_sites_invalid_json_responses():
    response = Mock(status_code=200)
    response.json.return_value = {
        "row_count": 1,
        "sites": [
            {"Id": "10", "Name": "Site 1", "Description": "A site with valid data", "Longitude": 1.0, "Latitude": 1.0, "Status": "active"},
            {"Id": "Not an int", "Name": "Site 2", "Description": "A site with invalid ID", "Longitude": 2.0, "Latitude": 2.0, "Status": "inactive"},
            {"Id": "30", "Name": "", "Description": "A site with empty name", "Longitude": 3.0, "Latitude": 3.0, "Status": "active"},
            {"Id": "40", "Name": "Site 4", "Description": "", "Longitude": 4.0, "Latitude": 4.0, "Status": "active"},
            {"Id": "50", "Name": "Site 5", "Description": "A site with invalid coordinates", "Longitude": 0.0, "Latitude": 0.0, "Status": "active"},
            {"Id": "60", "Name": "Site 6", "Description": "A site with empty status", "Longitude": 6.0, "Latitude": 6.0, "Status": ""},
        ]
        }
    return response


class TestSitesRequest:
    def test_static(self):
        assert SitesRequest.ENDPOINT == "/sites"
    
    def test_from_dict(self, mock_sites_success_response):
        data = mock_sites_success_response.json()
        response = SitesRequest.SitesResponse.from_dict(data)
        assert len(response.sites) == 3
        assert response.sites[0].id == 10
        assert response.sites[0].name == "Site 1"
        assert response.sites[0].description == "A site"
        assert response.sites[0].longitude == 1.0
        assert response.sites[0].latitude == 1.0
        assert response.sites[0].status == "active"
        assert response.sites[2].id == 30
        
    def test_from_dict_faulty_data(self, mock_sites_invalid_json_responses):
        data = mock_sites_invalid_json_responses.json()
        response = SitesRequest.SitesResponse.from_dict(data)
        assert len(response.sites) == 1
        assert response.sites[0].id == 10
    
    @patch('requests.Session.send')
    def test_success(self, mock_send, mock_sites_success_response):
        mock_send.return_value = mock_sites_success_response
        request = SitesRequest()
        response = request.send()
        assert len(response.sites) == 3
        assert response.sites[0].id == 10
        assert response.sites[0].name == "Site 1"
        assert response.sites[0].description == "A site"
        assert response.sites[0].longitude == 1.0
        assert response.sites[0].latitude == 1.0
        assert response.sites[0].status == "active"
        assert response.sites[2].id == 30
    
    @patch('requests.Session.send')
    def test_timeout(self, mock_send):
        mock_send.side_effect = Timeout("Request timed out")
        request = SitesRequest()
        with pytest.raises(Timeout):
            request.send()
            
    @patch('requests.Session.send')
    def test_connection_error(self, mock_send):
        mock_send.side_effect = ConnectionError("Connection error occurred")
        request = SitesRequest()
        with pytest.raises(ConnectionError):
            request.send()
            
    @patch('requests.Session.send')
    def test_invalid_json(self, mock_send, mock_sites_invalid_json_responses):
        mock_send.return_value = mock_sites_invalid_json_responses
        request = SitesRequest()
        response = request.send()
        assert len(response.sites) == 1
        assert response.sites[0].id == 10
    
    @patch('requests.Session.send')
    def test_500_error(self, mock_send):
        mock_response = Mock(status_code=500, reason="Internal Server Error")
        mock_send.return_value = mock_response
        request = SitesRequest()
        with pytest.raises(HTTPError) as exc_info:
            request.send()
        assert exc_info.value.status_code == 500
        assert exc_info.value.reason == "Internal Server Error"
        
    @patch('requests.Session.send')
    def test_404_error(self, mock_send):
        mock_response = Mock(status_code=404, reason="Not Found")
        mock_send.return_value = mock_response
        request = SitesRequest()
        with pytest.raises(HTTPError) as exc_info:
            request.send()
        assert exc_info.value.status_code == 404
        assert exc_info.value.reason == "Not Found"
    
    
class TestReportRequest:
    
    def test_endpoint_assert(self):
        assert ReportRequest.ENDPOINT == "/reports"
    
    

@pytest.fixture
def mock_fifteen_minute_observation_data():
    return {
        "Site Name": "M25/4876A",
        "Report Date": "2025-03-10T00:00:00",
        "Time Period Ending": "00:14:00",
        "Time Interval": "0",
        "0 - 520 cm": "136",
        "521 - 660 cm": "11",
        "661 - 1160 cm": "12",
        "1160+ cm": "13",
        "0 - 10 mph": "",
        "11 - 15 mph": "",
        "16 - 20 mph": "",
        "21 - 25 mph": "",
        "26 - 30 mph": "",
        "31 - 35 mph": "",
        "36 - 40 mph": "",
        "41 - 45 mph": "",
        "46 - 50 mph": "",
        "51 - 55 mph": "",
        "56 - 60 mph": "",
        "61 - 70 mph": "",
        "71 - 80 mph": "",
        "80+ mph": "",
        "Avg mph": "66",
        "Total Volume": "172"
    }
    
 
    
@pytest.fixture
def mock_daily_report_response():
    response = Mock(status_code=200)
    response.json.return_value = {
        "Header": {
            "row_count": 96,
            "start_date": "10032025",
            "end_date": "10032025",
            "links": []
        },
        "Rows": [
            {
            "Site Name": "M25/4876A",
            "Report Date": "2025-03-10T00:00:00",
            "Time Period Ending": "00:14:00",
            "Time Interval": "0",
            "0 - 520 cm": "136",
            "521 - 660 cm": "11",
            "661 - 1160 cm": "12",
            "1160+ cm": "13",
            "0 - 10 mph": "",
            "11 - 15 mph": "",
            "16 - 20 mph": "",
            "21 - 25 mph": "",
            "26 - 30 mph": "",
            "31 - 35 mph": "",
            "36 - 40 mph": "",
            "41 - 45 mph": "",
            "46 - 50 mph": "",
            "51 - 55 mph": "",
            "56 - 60 mph": "",
            "61 - 70 mph": "",
            "71 - 80 mph": "",
            "80+ mph": "",
            "Avg mph": "66",
            "Total Volume": "172"
            },
            {
            "Site Name": "M25/4876A",
            "Report Date": "2025-03-10T00:00:00",
            "Time Period Ending": "00:29:00",
            "Time Interval": "1",
            "0 - 520 cm": "95",
            "521 - 660 cm": "10",
            "661 - 1160 cm": "11",
            "1160+ cm": "20",
            "0 - 10 mph": "",
            "11 - 15 mph": "",
            "16 - 20 mph": "",
            "21 - 25 mph": "",
            "26 - 30 mph": "",
            "31 - 35 mph": "",
            "36 - 40 mph": "",
            "41 - 45 mph": "",
            "46 - 50 mph": "",
            "51 - 55 mph": "",
            "56 - 60 mph": "",
            "61 - 70 mph": "",
            "71 - 80 mph": "",
            "80+ mph": "",
            "Avg mph": "65",
            "Total Volume": "136"
            },
        ]
    }
    return response

@pytest.fixture
def mock_daily_report_invalid_json_response():
    response = Mock(status_code=200)
    response.json.return_value = {
        "Header": {
            "row_count": 2,
            "start_date": "10032025",
            "end_date": "10032025",
            "links": []
        },
        "Rows": [
            {
                # Normal row for control
            "Site Name": "M25/4876A",
            "Report Date": "2025-03-10T00:00:00",
            "Time Period Ending": "00:14:00",
            "Time Interval": "0",
            "0 - 520 cm": "136",
            "521 - 660 cm": "11",
            "661 - 1160 cm": "12",
            "1160+ cm": "13",
            "0 - 10 mph": "",
            "11 - 15 mph": "",
            "16 - 20 mph": "",
            "21 - 25 mph": "",
            "26 - 30 mph": "",
            "31 - 35 mph": "",
            "36 - 40 mph": "",
            "41 - 45 mph": "",
            "46 - 50 mph": "",
            "51 - 55 mph": "",
            "56 - 60 mph": "",
            "61 - 70 mph": "",
            "71 - 80 mph": "",
            "80+ mph": "",
            "Avg mph": "66",
            "Total Volume": "172"
                
            },
            {
            "Site Name": "M25/4876A",
            "Report Date": "2025-03-10T00:00:00",
            "Time Period Ending": "00:29:00",
            "Time Interval": "1",
            "0 - 520 cm": "136",
            "521 - 660 cm": "11",
            "661 - 1160 cm": "12",
            "1160+ cm": "13",
            "0 - 10 mph": "",
            "11 - 15 mph": "",
            "16 - 20 mph": "",
            "21 - 25 mph": "",
            "26 - 30 mph": "",
            "31 - 35 mph": "",
            "36 - 40 mph": "",
            "41 - 45 mph": "",
            "46 - 50 mph": "",
            "51 - 55 mph": "",
            "56 - 60 mph": "",
            "61 - 70 mph": "",
            "71 - 80 mph": "",
            "80+ mph": "",
            # Missing Avg mph and Total Volume fields
            },
            {
            "Site Name": "M25/4876A",
            "Report Date": "2025-03-10T00:00:00",
            # Missing Time Period Ending field
            "Time Interval": "2",
            "0 - 520 cm": "95",
            "521 - 660 cm": "10",
            "661 - 1160 cm": "11",
            "1160+ cm": "20",
            "0 - 10 mph": "",
            "11 - 15 mph": "",
            "16 - 20 mph": "",
            "21 - 25 mph": "",
            "26 - 30 mph": "",
            "31 - 35 mph": "",
            "36 - 40 mph": "",
            "41 - 45 mph": "",
            "46 - 50 mph": "",
            "51 - 55 mph": "",
            "56 - 60 mph": "",
            "61 - 70 mph": "",
            "71 - 80 mph": "",
            "80+ mph": "",
            "Avg mph": "65",
            "Total Volume": "136"
            },
        ]
    }
    return response
   
@pytest.fixture
def normal_fifteen_minute_observation():
    return FifteenMinuteObservation(
        site_name="M25/4876A",
        site_id=1,
        end_time=datetime(2025, 3, 10, 0, 14, 0),
        average_speed=66.2,
        vehicle_count=172
    )

class TestFifteenMinuteObservation:
    def test_from_dict_success(self, mock_fifteen_minute_observation_data):
        site_id = 1
        data = mock_fifteen_minute_observation_data
        observation = FifteenMinuteObservation.from_dict(site_id, data)
        assert observation.site_name == "M25/4876A"
        assert observation.site_id == site_id
        assert observation.end_datetime == datetime(2025, 3, 10, 0, 14, 0)
        assert observation.date == datetime(2025, 3, 10)
        assert observation.end_time_minutes_in_day == 14
        assert observation.average_speed == 66
        assert observation.vehicle_count == 172
    
    def test_from_dict_faulty_types(self, mock_fifteen_minute_observation_data):
        site_id = 1
        data = mock_fifteen_minute_observation_data            
        data["Avg mph"] = "not an int"
        with pytest.raises(ValueError):
            FifteenMinuteObservation.from_dict(site_id, data)
        data["Avg mph"] = "66"
        data["Total Volume"] = "not an int"
        with pytest.raises(ValueError):
            FifteenMinuteObservation.from_dict(site_id, data)
        data["Total Volume"] = "172"
        del data["Time Period Ending"]
        with pytest.raises(ValueError):
            FifteenMinuteObservation.from_dict(site_id, data)
            
    def test_from_dict_faulty_date(self, mock_fifteen_minute_observation_data):
        site_id = 1
        data = mock_fifteen_minute_observation_data            
        data["Report Date"] = "not a date"
        with pytest.raises(ValueError):
            FifteenMinuteObservation.from_dict(site_id, data)
        data["Report Date"] = "2025-03-10T00:00:00"
        data["Time Period Ending"] = "not a time"
        with pytest.raises(ValueError):
            FifteenMinuteObservation.from_dict(site_id, data)
            
    def test_changing_attributes(self, normal_fifteen_minute_observation):
        observation = normal_fifteen_minute_observation
        with pytest.raises(AttributeError):
            observation.site_name = "New Site Name"
        with pytest.raises(AttributeError):
            observation.site_id = 2
        with pytest.raises(AttributeError):
            observation.end_datetime = datetime(2025, 3, 10, 0, 29, 0)
        with pytest.raises(AttributeError):
            observation.average_speed = 70.5
        with pytest.raises(AttributeError):
            observation.vehicle_count = 200
        assert observation.site_name == "M25/4876A"
        assert observation.site_id == 1
        assert observation.end_datetime == datetime(2025, 3, 10, 0, 14, 0)
        assert observation.average_speed == 66.2
        assert observation.vehicle_count == 172
        
        
    def test_date(self, normal_fifteen_minute_observation):
        observation = normal_fifteen_minute_observation
        assert observation.date == datetime(2025, 3, 10)
        assert observation.date.year == 2025
        assert observation.date.month == 3
        assert observation.date.day == 10
        assert observation.date.hour == 0
        assert observation.date.minute == 0
        assert observation.date.second == 0
        assert observation.date.microsecond == 0
        observation._observation_end_datetime = datetime(2025, 3, 11, 0, 14, 0)
        assert observation.date == datetime(2025, 3, 11)
        assert observation.date.year == 2025
        assert observation.date.month == 3
        assert observation.date.day == 11
        assert observation.date.hour == 0
        assert observation.date.minute == 0
        assert observation.date.second == 0
        assert observation.date.microsecond == 0
        
    def test_end_time_minutes_in_day(self, normal_fifteen_minute_observation):
        observation = normal_fifteen_minute_observation
        assert observation.end_time_minutes_in_day == 14
        expected_minutes = observation.end_datetime.hour * 60 + observation.end_datetime.minute
        assert observation.end_time_minutes_in_day == expected_minutes
        observation._observation_end_datetime = datetime(2025, 3, 10, 1, 15, 0)
        assert observation.end_time_minutes_in_day == 75
    
    
class TestDailyReportRequest:
    
    def test_endpoint_assert(self):
        assert DailyReportRequest.ENDPOINT == "/reports/daily"
        
    def test_protected_properties(self):
        rr = DailyReportRequest(1, datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
        with pytest.raises(TypeError, match="site_id"):
            rr.site_id = "string, not int type"
        rr.site_id = 2
        assert rr.site_id == 2
        with pytest.raises(TypeError, match="date"):
            rr.date = "string, not datetime type"
        rr.date = datetime(2026, 1, 2)
        assert rr.date.year == 2026
        assert rr.date.month == 1
        assert rr.date.day == 2
    
    @patch('requests.Session.send')
    def test_success(self, mock_send, mock_daily_report_response):
        mock_send.return_value = mock_daily_report_response
        rr = DailyReportRequest(1, datetime(2025, 3, 10))
        response = rr.send()
        assert len(response) == 2
        assert response[0].site_name == "M25/4876A"
        assert response[0].end_datetime == datetime(2025, 3, 10, 0, 14, 0)
        assert response[0].end_time_minutes_in_day == 14
        assert response[0].average_speed == 66
        assert response[0].vehicle_count == 172
        assert response[1].end_time_minutes_in_day == 29

    @patch('requests.Session.send')
    def test_invalid_json(self, mock_send, mock_daily_report_invalid_json_response):    
        mock_send.return_value = mock_daily_report_invalid_json_response
        rr = DailyReportRequest(1, datetime(2025, 3, 10))
        response = rr.send()
        assert len(response) == 1
        assert response[0].site_name == "M25/4876A"
        assert response[0].end_datetime == datetime(2025, 3, 10, 0, 14, 0)
        assert response[0].end_time_minutes_in_day == 14
        assert response[0].average_speed == 66
        assert response[0].vehicle_count == 172
        
        
@pytest.fixture
@patch('webtris_client.DailyReportRequest.send')
def normal_site(report_request_send_mock):
    report_request_send_mock.return_value = [
        FifteenMinuteObservation(
            site_name="M25/4876A",
            site_id=1,
            end_time=datetime(2025, 3, 10, 0, 14, 0),
            average_speed=66.2,
            vehicle_count=172
        ),
        FifteenMinuteObservation(
            site_name="M25/4876A",
            site_id=1,
            end_time=datetime(2025, 3, 10, 0, 29, 0),
            average_speed=65.0,
            vehicle_count=136
        ),
        FifteenMinuteObservation(
            site_name="M25/4876A",
            site_id=1,
            end_time=datetime(2025, 3, 10, 0, 44, 0),
            average_speed=64.5,
            vehicle_count=150
        ),
        FifteenMinuteObservation(
            site_name="M25/4876A",
            site_id=1,
            end_time=datetime(2025, 3, 10, 0, 59, 0),
            average_speed=64.0,
            vehicle_count=100
        ),
        FifteenMinuteObservation(
            site_name="M25/4876A",
            site_id=1,
            end_time=datetime(2025, 3, 10, 1, 14, 0),
            average_speed=60.0,
            vehicle_count=100
        )
    ]
    return Site(1, datetime(2025, 3, 10))

@patch('webtris_client.DailyReportRequest.send')
class TestSite:
    
    def test_get_set_attributes(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        site: Site = normal_site
        assert site.site_id == 1
        assert site.date.year == 2025
        assert site.date.month == 3
        assert site.date.day == 10
        site.date =  datetime(2025, 3, 11)
        assert site.date == datetime(2025, 3, 11)
        
    
    def test_get_observations_list(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        observations = normal_site.get_observations_list()
        assert len(observations) == 5
        assert observations[0].site_name == "M25/4876A"
        assert observations[0].end_datetime == datetime(2025, 3, 10, 0, 14, 0)
        assert observations[0].end_time_minutes_in_day == 14
        assert observations[0].average_speed == 66.2
        assert observations[0].vehicle_count == 172
        assert observations[1].end_time_minutes_in_day == 29
        assert observations[2].end_time_minutes_in_day == 44
        assert observations[3].end_time_minutes_in_day == 59
        assert observations[4].end_time_minutes_in_day == 74
        
    def test_get_average_speed(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        average_speed = normal_site.get_average_speed()
        total_weighted_speed = 66.2 * 172 + 65.0 * 136 + 64.5 * 150 + 64.0 * 100 + 60.0 * 100
        total_count = 172 + 136 + 150 + 100 + 100
        expected_average_speed = total_weighted_speed / total_count
        assert average_speed == expected_average_speed
        
    def test_get_average_speed_no_observations(self, mock_report_request_send):
        mock_report_request_send.return_value = []
        site = Site(1, datetime(2025, 3, 10))
        average_speed = site.get_average_speed()
        assert average_speed == 0.0
        
    def test_get_hourly_average_speed(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        hourly_average_speed = normal_site.get_hourly_average_speed(0)
        total_weighted_speed = 66.2 * 172 + 65.0 * 136 + 64.5 * 150 + 64.0 * 100
        total_count = 172 + 136 + 150 + 100
        expected_hourly_average_speed = total_weighted_speed / total_count
        assert hourly_average_speed == expected_hourly_average_speed
        
    def test_get_hourly_average_speed_no_observations(self, mock_report_request_send):
        mock_report_request_send.return_value = []
        site = Site(1, datetime(2025, 3, 10))
        hourly_average_speed = site.get_hourly_average_speed(0)
        assert hourly_average_speed == 0.0
        
    def test_get_vehicle_count(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        vehicle_count = normal_site.get_vehicle_count()
        expected_vehicle_count = 172 + 136 + 150 + 100 + 100
        assert vehicle_count == expected_vehicle_count
        
    def test_get_vehicle_count_no_observations(self, mock_report_request_send):
        mock_report_request_send.return_value = []
        site = Site(1, datetime(2025, 3, 10))
        vehicle_count = site.get_vehicle_count()
        assert vehicle_count == 0
        
    def test_get_hourly_vehicle_count(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        hourly_vehicle_count = normal_site.get_hourly_vehicle_count(0)
        expected_hourly_vehicle_count = 172 + 136 + 150 + 100
        assert hourly_vehicle_count == expected_hourly_vehicle_count
        
    def test_get_hourly_vehicle_count_no_observations(self, mock_report_request_send):
        mock_report_request_send.return_value = []
        site = Site(1, datetime(2025, 3, 10))
        hourly_vehicle_count = site.get_hourly_vehicle_count(0)
        assert hourly_vehicle_count == 0
        
    def test_get_peak_hour(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        peak_hour = normal_site.get_peak_hour()
        assert peak_hour == 0
        normal_site._observations.append(
            FifteenMinuteObservation(
                site_name="M25/4876A",
                site_id=1,
                end_time=datetime(2025, 3, 10, 11, 14, 0),
                average_speed=60.0,
                vehicle_count=20000
            )
        )
        peak_hour = normal_site.get_peak_hour()
        assert peak_hour == 11
        
    def test_get_peak_hour_no_observations(self, mock_report_request_send):
        mock_report_request_send.return_value = []
        site = Site(1, datetime(2025, 3, 10))
        peak_hour = site.get_peak_hour()
        assert peak_hour == 0
        
    def test_get_records_for_hour(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        records_for_hour = normal_site.get_records_for_hour(0)
        assert len(records_for_hour) == 4
        for record in records_for_hour:
            assert record.end_datetime.hour == 0
        records_for_hour = normal_site.get_records_for_hour(1)
        assert len(records_for_hour) == 1
        assert records_for_hour[0].end_datetime.hour == 1
        
    def test_get_records_for_hour_with_no_observations(self, mock_report_request_send):
        mock_report_request_send.return_value = []
        site = Site(1, datetime(2025, 3, 10))
        records_for_hour = site.get_records_for_hour(0)
        assert len(records_for_hour) == 0
        
    def test_get_records_for_hour_out_of_range(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        with pytest.raises(ValueError):
            normal_site.get_records_for_hour(24)
        with pytest.raises(ValueError):
            normal_site.get_records_for_hour(-1)
   
    def test_site_len(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        assert len(normal_site) == 5         
   
    def test_site_getitems(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        assert normal_site[0].site_name == "M25/4876A"
        assert normal_site[0].end_datetime == datetime(2025, 3, 10, 0, 14, 0)
        assert normal_site[0].end_time_minutes_in_day == 14
        assert normal_site[0].average_speed == 66.2
        assert normal_site[0].vehicle_count == 172
        
    def test_site_getitems_out_of_range(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        with pytest.raises(IndexError):
            normal_site[5]
        with pytest.raises(IndexError):
            normal_site[-6]
        
    def test_site_iter(self, mock_report_request_send, normal_site):
        mock_report_request_send.return_value = normal_site.get_observations_list()
        for observation in normal_site:
            assert observation.site_name == "M25/4876A"
            assert observation.end_datetime.hour == 0 or observation.end_datetime.hour == 1
            assert observation.site_id == 1
        
    