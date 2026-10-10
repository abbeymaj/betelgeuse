# Importing packages
from unittest.mock import MagicMock, patch
import pytest
import requests
from src.components.config_entity import SourceDataURL
from src.components.fetch_data import FetchData
from src.exception import CustomException

# Defining the star and Julian date window used across the tests
STAR = "alf Ori"
FROM_JD = 2458800.0
TO_JD = 2458830.0

# Creating a fixture that patches requests.get with a successful response
@pytest.fixture
def mock_get():
    response = MagicMock()
    response.text = "JD|mag\n2458800.5|1.2\n"
    response.raise_for_status.return_value = None
    with patch("src.components.fetch_data.requests.get", return_value=response) as mocked:
        yield mocked

# Verifying that the raw response text is returned unchanged
@pytest.mark.unit
def test_fetch_returns_response_text(mock_get):
    txt = FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD)
    assert txt == "JD|mag\n2458800.5|1.2\n"

# Verifying that the request is sent to the VSX API URL
@pytest.mark.unit
def test_fetch_calls_vsx_url(mock_get):
    FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD)
    args, _ = mock_get.call_args
    assert args[0] == SourceDataURL.url

# Verifying that the query parameters are built from the arguments
@pytest.mark.unit
def test_fetch_sends_expected_params(mock_get):
    FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD, delimiter=";")
    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {
        "view": "api.delim",
        "ident": STAR,
        "fromjd": FROM_JD,
        "tojd": TO_JD,
        "delimiter": ";",
    }

# Verifying that the default delimiter is a pipe
@pytest.mark.unit
def test_fetch_default_delimiter_is_pipe(mock_get):
    FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD)
    _, kwargs = mock_get.call_args
    assert kwargs["params"]["delimiter"] == "|"

# Verifying that a User-Agent header and a timeout are set
@pytest.mark.unit
def test_fetch_sets_user_agent_and_timeout(mock_get):
    FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD)
    _, kwargs = mock_get.call_args
    assert "User-Agent" in kwargs["headers"]
    assert kwargs["timeout"] == 30

# Verifying that an HTTP error status is raised as a CustomException
@pytest.mark.unit
def test_fetch_http_error_raises_custom_exception(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("503 Server Error")
    with pytest.raises(CustomException):
        FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD)

# Verifying that a network failure is raised as a CustomException
@pytest.mark.unit
def test_fetch_connection_error_raises_custom_exception(mock_get):
    mock_get.side_effect = requests.ConnectionError("connection refused")
    with pytest.raises(CustomException):
        FetchData().fetch_photometric_data(STAR, FROM_JD, TO_JD)
