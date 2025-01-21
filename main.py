import os
import json

import requests
import pandas as pd


def fetch_data(api_url, output_file, mock_file):
    """
    Fetch data from the API and save it to a file. 
    Use mock data from mock.json if the API fetch fails.
    """
    try:
        print("Fetching data from API...")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        with open(output_file, 'w') as file:
            json.dump(response.json(), file)
        print(f"Data successfully fetched and saved to {output_file}")
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data from API: {error}")
        print("Falling back to mock data...")
        use_mock_data(output_file, mock_file)


def use_mock_data(output_file, mock_file):
    """
    Copy mock data from mock.json to the specified output file.
    """
    try:
        if not os.path.exists(mock_file):
            raise FileNotFoundError(f"Mock data file {mock_file} not found.")

        with open(mock_file, 'r') as mock:
            mock_data = json.load(mock)

        with open(output_file, 'w') as file:
            json.dump(mock_data, file)
        print(f"Mock data successfully used and saved to {output_file}")
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"Error using mock data: {error}")


def analyze_data(input_file):
    """
    Analyze the data file for total posts, unique users, and average words per post.
    """
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File {input_file} does not exist.")

        with open(input_file, 'r') as file:
            data = json.load(file)

        if not data:
            raise ValueError("Data file is empty.")

        df = pd.DataFrame(data)

        # Check for required columns
        if 'userId' not in df or 'body' not in df:
            raise KeyError("Missing required columns in the data.")

        # Calculate metrics
        total_posts = len(df)
        unique_users = df['userId'].nunique()
        avg_words = df['body'].apply(lambda x: len(x.split()) if isinstance(x, str) else 0).mean()

        print("Data analysis complete.")
        return total_posts, unique_users, avg_words

    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as error:
        print(f"Error analyzing data: {error}")
        return 0, 0, 0


def generate_summary(total_posts, unique_users, avg_words, output_file):
    """
    Generate a summary file with analysis results.
    """
    try:
        with open(output_file, 'w') as file:
            file.write(f"Total Posts: {total_posts}\n")
            file.write(f"Unique Users: {unique_users}\n")
            file.write(f"Average Words per Post: {avg_words:.2f}\n")
        print(f"Summary successfully saved to {output_file}")
    except IOError as error:
        print(f"Error writing summary file: {error}")


if __name__ == "__main__":
    API_URL = "https://jsonplaceholder.typicode.com/posts"
    DATA_FILE = "data.json"
    MOCK_FILE = "mock.json"
    SUMMARY_FILE = "summary.txt"

    # Fetch data from API or use mock data
    fetch_data(API_URL, DATA_FILE, MOCK_FILE)

    # Analyze the data
    total_posts, unique_users, avg_words = analyze_data(DATA_FILE)

    # Generate a summary of the analysis
    generate_summary(total_posts, unique_users, avg_words, SUMMARY_FILE)
