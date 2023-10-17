# Restaurant Planner README

This README provides an overview of the `main.py` script, which is designed to help users plan a two-day restaurant itinerary based on their location, specified radius, and preferred day of the week. It uses the Google Places API to find nearby restaurants, sort them, and generate a restaurant plan.

## Table of Contents

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Functions](#functions)
5. [Example](#example)

## Introduction

The `main.py` script is a Python program that performs the following tasks:

- Reads an API key from a file (default: `key.env`).
- Determines the user's location using the Google Maps API.
- Retrieves nearby restaurants based on user specifications.
- Sorts restaurants based on various factors.
- Generates a two-day restaurant plan.
- Provides directions between the selected restaurants.

## Setup

Before using the script, you need to obtain a Google Places API key. You can place the API key in a file named `key.env`. The script will read the API key from this file. 

Example `key.env` file:
```
YOUR_API_KEY_HERE
```

To install the required dependencies, you can use the following command:
```bash
pip install requirements.txt
```

## Usage

To use the script, simply run it using Python:

```bash
python main.py
```

The script will prompt you for the following information:
- Your location (e.g., a city or address).
- The search radius in kilometers.
- The preferred day of the week for your restaurant plan.

## Functions

The script contains several functions that perform different tasks:

1. `read_api_key_file(path="./key.env")`: Reads the API key from the `key.env` file.

2. `look_for_location(api, location)`: Determines the latitude and longitude of a specified location using the Google Maps API.

3. `nearby_restaurants(api, location, radius, keyword="restaurant")`: Retrieves nearby restaurants based on the given location, radius, and keyword.

4. `sort_restaurants(df)`: Sorts the retrieved restaurants based on a weighted score considering factors like price, user ratings, and ratings.

5. `get_day_of_the_week(day)`: Converts the user-specified day into a numeric value (0 for Sunday, 1 for Monday, etc.).

6. `plan_day(api_key, df, day)`: Generates a restaurant plan for a specific day based on restaurant opening hours.

7. `print_plan(plan, day)`: Prints the generated restaurant plan.

8. `directions(start, waypoint, destination)`: Generates and prints Google Maps directions between selected restaurants.

## Example

After running the script and providing the required inputs, it will generate a two-day restaurant plan and print directions to the selected restaurants.

Please note that the accuracy of the restaurant information and opening hours depends on the data available from the Google Places API. Make sure you have a valid API key with the necessary permissions to access the API.

Enjoy your restaurant exploration with this script!
