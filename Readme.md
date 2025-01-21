# Data Fetch and Analysis Project

This project fetches data from an external API, processes it, and generates insights such as total posts, unique users, and average words per post. In case the API is unavailable, the project can fallback to mock data for analysis.

## Features
1. **Fetch Data from API**: The project fetches data from a public API and stores it in a file (`data.json`).
2. **Mock Data Fallback**: If the API request fails, mock data is used from a local file (`mock.json`).
3. **Data Analysis**: The project analyzes the data for:
   - Total number of posts
   - Unique users who created the posts
   - Average words per post
4. **Generate Summary**: A summary of the analysis is saved to a text file (`summary.txt`).

## Requirements
- Python 3.x
- Requests library
- pandas library

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the main script to fetch data from the API (or use mock data if API fails), analyze it, and generate a summary.
    ```bash
    python main.py
    ```

## Files
- **main.py**: The main script that handles fetching, analyzing, and summarizing data.
- **mock.json**: Mock data used in case the API fetch fails.
- **data.json**: The file where fetched or mock data is saved.
- **summary.txt**: The file where the summary of data analysis is saved.

## Tests
The project includes unit tests that ensure the functionality of data fetching, analysis, and summary generation:
1. **test_fetch_data_success**: Tests fetching data from the API successfully.
2. **test_fetch_data_failure_and_mock_fallback**: Tests using mock data if the API request fails.
3. **test_analyze_data**: Tests the analysis of data.
4. **test_analyze_data_empty_file**: Tests the analysis of an empty data file.
5. **test_analyze_data_missing_file**: Tests handling missing data file.
6. **test_generate_summary**: Tests generating the summary file.

To run tests, use the following command:
```bash
python -m unittest test_main.py
