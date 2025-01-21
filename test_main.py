import unittest
from unittest.mock import patch, mock_open
import requests
import json
import pandas as pd

# Assuming the methods are from the module you have
from main import fetch_data, use_mock_data, analyze_data, generate_summary

class TestMainScript(unittest.TestCase):

    # Test for API fetching function
    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.get')
    def test_fetch_data_success(self, mock_get, mock_file):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"userId": 1, "id": 1, "title": "Test", "body": "Test body"}]
        
        # Call the fetch_data function
        fetch_data("https://jsonplaceholder.typicode.com/posts", "data.json", "mock.json")
        
        # Ensure that open was called with the correct file path and mode
        mock_file.assert_called_once_with("data.json", 'w')
        
        # Ensure the write method was called (i.e., data was saved to file)
        mock_file().write.assert_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('requests.get')
    def test_fetch_data_failure_and_mock_fallback(self, mock_get, mock_file):
        # Mock the API request to fail
        mock_get.side_effect = requests.exceptions.RequestException("API request failed")
        
        # Prepare the mock data to return when reading from 'mock.json'
        mock_file.return_value.read.return_value = '''[
            {"userId": 1, "id": 1, "title": "test", "body": "Test body"}
        ]'''

        # Call the fetch_data function
        fetch_data("https://jsonplaceholder.typicode.com/posts", "data.json", "mock.json")
        
        # Ensure that open was called with the correct file path and mode (for mock data)
        mock_file.assert_any_call("mock.json", 'r')
        mock_file.assert_any_call("data.json", 'w')
        
        # Ensure that write method was called (i.e., mock data was written to file)
        mock_file().write.assert_called()

    # Test for data processing logic
    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_data(self, mock_file):
        # Prepare mock data to simulate the content of data.json
        mock_file.return_value.read.return_value = '''[
            {"userId": 1, "id": 1, "title": "test", "body": "Test body"}
        ]'''
        
        # Call the analyze_data function
        total_posts, unique_users, avg_words = analyze_data("data.json")
        
        # Assert that the returned values are correct based on the mock data
        self.assertEqual(total_posts, 1)  # Only 1 post
        self.assertEqual(unique_users, 1)  # Only 1 unique user
        self.assertEqual(avg_words, 2)  # The body "Test body" contains 2 words

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_data_empty_file(self, mock_file):
        # Simulate empty data
        mock_file.return_value.read.return_value = '[]'
        
        # Call the analyze_data function with empty data
        total_posts, unique_users, avg_words = analyze_data("data.json")
        
        # Assert that the values are 0 due to the empty data
        self.assertEqual(total_posts, 0)
        self.assertEqual(unique_users, 0)
        self.assertEqual(avg_words, 0.0)

    @patch('builtins.open', new_callable=mock_open)
    def test_analyze_data_missing_file(self, mock_file):
        # Simulate missing file by not providing any return value
        mock_file.side_effect = FileNotFoundError("File not found.")
        
        # Call the analyze_data function expecting failure
        total_posts, unique_users, avg_words = analyze_data("data.json")
        
        # Assert that the function returns 0 values on error (file not found)
        self.assertEqual(total_posts, 0)
        self.assertEqual(unique_users, 0)
        self.assertEqual(avg_words, 0.0)

    # Test for file generation function
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_summary(self, mock_file):
        # Call the generate_summary function
        generate_summary(10, 5, 3.0, "summary.txt")
        
        # Ensure that open was called with the correct file path and mode for summary
        mock_file.assert_called_once_with("summary.txt", 'w')
        
        # Ensure that write method was called to generate the summary file
        mock_file().write.assert_called()

if __name__ == "__main__":
    unittest.main()
