"""All tests for the application"""
import pytest
from datetime import datetime
from unittest.mock import patch, Mock
from requests.exceptions import Timeout, ConnectionError, HTTPError

from webtris_client import (
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
        
    