# tests/test_scrapers.py

import pytest
from unittest import mock
from exprealtyscraper import search_agent as exprealty_search_agent
from zilowscraper import fetchzillow as zillow_fetch_agent

# Correct full MockDriver
class MockDriver:
    def execute(self, command, params=None):
        print("[MockDriver] execute() called.")
        return {}

    def get(self, url):
        print(f"[MockDriver] get() called with url: {url}")

    @property
    def page_source(self):
        return "<html><body>Fake page content with John Doe</body></html>"

    def quit(self):
        print("[MockDriver] quit() called.")

# --- Exprealty Scraper Test ---
@mock.patch('exprealtyscraper.getsource', return_value=(MockDriver(), "<html><body>Fake page content with John Doe</body></html>"))
def test_search_agent_exprealty(mock_getsource):
    agent_name = "John Doe"
    result = exprealty_search_agent(agent_name)
    
    # Now expect result to be a tuple ['', ''] or similar if not found
    assert isinstance(result, list), f"Expected a list (email, phone), got {type(result)}"
    assert len(result) == 2, f"Expected 2 elements (email, phone), got {len(result)}"
    assert all(isinstance(item, str) for item in result), "All items in result should be strings"

# --- Zillow Scraper Test ---
@mock.patch('zilowscraper.requests.get')
def test_fetchzillow_zillow(mock_get):
    class MockResponse:
        def __init__(self, text):
            self.text = text
        def raise_for_status(self):
            pass

    mock_get.return_value = MockResponse("<html><body>Fake Zillow page with John Doe</body></html>")

    agent_name = "John Doe"
    result = zillow_fetch_agent(agent_name)

    # Verify that result is a tuple with 4 elements
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 4, f"Expected 4 elements, got {len(result)}"
    # Verify that all elements are strings
    assert all(isinstance(item, str) for item in result), "All items in result should be strings"
