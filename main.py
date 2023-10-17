import pandas as pd
import requests
import urllib.parse

# TODO: Analysis
# TODO: Documentation
# TODO: README


def read_api_key_file(path="./key.env"):
    api_key_file = open(path, "r")
    API_KEY = api_key_file.read()
    api_key_file.close()
    return API_KEY


def look_for_location(api, location):
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "fields": "geometry",
        "input": location,
        "inputtype": "textquery",
        "key": api,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") == "OK":
            candidates = data.get("candidates")
            # print(candidates)
            latitude = candidates[0]["geometry"]["location"]["lat"]
            longitude = candidates[0]["geometry"]["location"]["lng"]
            return f"{latitude},{longitude}"

    except requests.exceptions.RequestException as e:
        print("Error:", e)

    print("Defaulting to Indianapolis, IN")
    return "39.7684,-86.1581"


def nearby_restaurants(api, location, radius, keyword="restaurant"):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {"location": location, "radius": radius, "keyword": keyword, "key": api}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") == "OK":
            results = data.get("results")
            restaurants = []

            for place in results:
                # Details about the place
                id = place.get("place_id")
                name = place.get("name")
                address = place.get("vicinity")
                latitude = place["geometry"]["location"]["lat"]
                longitude = place["geometry"]["location"]["lng"]
                types = place.get("types")

                # Ratings and Price
                rating = place.get("rating", 0)
                user_ratings = place.get("user_ratings_total", 0)
                price_level = place.get("price_level", 0)

                # Other Details
                website = place.get("website", "N/A")
                maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

                restaurants.append(
                    {
                        "ID": id,
                        "Name": name,
                        "Address": address,
                        "Latitude": latitude,
                        "Longitude": longitude,
                        "Types": types,
                        "Rating": rating,
                        "User Ratings": user_ratings,
                        "Price Level": price_level,
                        "Maps Link": maps_link,
                        "Website": website,
                    }
                )
            restaurants_df = pd.DataFrame(restaurants)
            return restaurants_df

        else:
            print("Error: Unable to fetch data from Google Places API")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return pd.DataFrame()


def sort_restaurants(df):
    min_nratings = df["User Ratings"].min()
    max_nratings = df["User Ratings"].max()
    min_price = df["Price Level"].min()
    max_price = df["Price Level"].max()
    min_rating = df["Rating"].min()
    max_rating = df["Rating"].max()

    rating_weight = 0.8
    user_ratings_weight = 0.6
    price_level_weight = -0.3

    price = (df["Price Level"] - min_price) / (max_price - min_price)
    num_ratings = (df["User Ratings"] - min_nratings) / (max_nratings - min_nratings)
    ratings = (df["Rating"] - min_rating) / (max_rating - min_rating)

    df["Weighted Score"] = (
        price * price_level_weight
        + num_ratings * user_ratings_weight
        + ratings * rating_weight
    )

    sorted_df = df.sort_values(by=["Weighted Score"], ascending=False)
    sorted_df = sorted_df.reset_index(drop=True)

    return sorted_df


def get_day_of_the_week(day):
    week = {
        "sunday": 0,
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6,
    }

    return week[day.lower()]


def plan_day(api_key, df, day):
    breakfast = lunch = dinner = False
    i = 0
    plan = []
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    hours = {
        "breakfast": 800,
        "lunch": 1100,
        "dinner": 1500,
    }

    while i < len(df):
        place_id = df["ID"][i]
        params = {"place_id": place_id, "key": api_key}

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") == "OK":
                result = data.get("result")
                opening_hours = result.get("opening_hours")
                periods = opening_hours.get("periods")

                period = periods[day % len(periods)]
                try:
                    open_time = int(period["open"]["time"])
                    close_time = int(period["close"]["time"])
                except KeyError:
                    open_time = 2400
                    close_time = 2400

                if (
                    open_time <= hours["breakfast"] or close_time <= hours["lunch"]
                ) and not breakfast:
                    plan.append(
                        {
                            "id": place_id,
                            "name": df["Name"][i],
                            "address": df["Address"][i],
                            "maps_link": df["Maps Link"][i],
                            "website": df["Website"][i],
                            "lat": result["geometry"]["location"]["lat"],
                            "lng": result["geometry"]["location"]["lng"],
                        }
                    )
                    breakfast = True
                elif (
                    open_time <= hours["lunch"] or close_time <= hours["dinner"]
                ) and not lunch:
                    plan.append(
                        {
                            "id": place_id,
                            "name": df["Name"][i],
                            "address": df["Address"][i],
                            "maps_link": df["Maps Link"][i],
                            "website": df["Website"][i],
                        }
                    )
                    lunch = True
                elif open_time <= hours["dinner"] and not dinner:
                    plan.append(
                        {
                            "id": place_id,
                            "name": df["Name"][i],
                            "address": df["Address"][i],
                            "maps_link": df["Maps Link"][i],
                            "website": df["Website"][i],
                        }
                    )
                    dinner = True

        except requests.exceptions.RequestException as e:
            print("Error:", e)

        if breakfast and lunch and dinner:
            break
        i += 1

    for i in plan:
        df = df[df.ID != i["id"]]

    df = df.reset_index(drop=True)

    return plan, df


def print_plan(plan, day):
    print("-" * 20)
    print(day.upper())
    print("-" * 20)
    print()

    for i, j in enumerate(plan):
        if i == 0:
            print("--Breakfast--")
        elif i == 1:
            print("--Lunch--")
        elif i == 2:
            print("--Dinner--")
        print(f"{j['name']}")
        print(f"Address: {j['address']}")
        print(f"Maps Link: {j['maps_link']}")
        if j["website"] != "N/A":
            print(f"Website: {j['website']}")
        print()


def directions(start, waypoint, destination):
    url = "https://www.google.com/maps/dir/?api=1"

    params = {
        "origin": f"{start}",
        "destination": f"{destination}",
        "waypoints": f"{waypoint}",
    }

    url = f"{url}&{urllib.parse.urlencode(params)}"
    print(url)


if __name__ == "__main__":
    api_key = read_api_key_file()

    user_location = input("Enter your location: ")
    user_radius = input("Enter the radius (in km): ")
    user_day = input("Enter the day of the week: ")
    radius = int(user_radius) * 1000

    location = look_for_location(api_key, user_location)
    restaurants = nearby_restaurants(api_key, location, radius)
    sorted_restaurants = sort_restaurants(restaurants)
    sorted_restaurants.to_csv("sorted_restaurants.csv")
    day = get_day_of_the_week(user_day)

    first_day, df = plan_day(api_key, sorted_restaurants, day)
    second_day, df = plan_day(api_key, df, (day + 1))

    print_plan(first_day, "First Day")
    print_plan(second_day, "Second Day")

    directions(
        first_day[0]["address"], first_day[1]["address"], first_day[2]["address"]
    )
