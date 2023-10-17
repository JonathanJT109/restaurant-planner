import pandas as pd
import matplotlib.pyplot as plt


def read_df(path):
    df = pd.read_csv(path)
    return df


def general_stats(df):
    print(df.describe())
    print(df.info())


def name_and_rating(df):
    plt.bar(df["Name"], df["Rating"])
    plt.xlabel("Restaurant Name")
    plt.ylabel("Rating")
    plt.title("Restaurant Name vs Rating")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("restaurant_name_rating.png", dpi=300)


def name_and_nratings(df):
    plt.bar(df["Name"], df["User Ratings"])
    plt.xlabel("Restaurant Name")
    plt.ylabel("Number of Reviews")
    plt.title("Restaurant Name vs Number of Reviews")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("restaurant_name_nratings.png", dpi=300)


def name_and_price_level(df):
    plt.bar(df["Name"], df["Price Level"])
    plt.xlabel("Restaurant Name")
    plt.ylabel("Price Level")
    plt.title("Restaurant Name vs Price Level")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("restaurant_name_price.png", dpi=300)


def rating_and_nratings(df):
    scale_factor = 1
    plt.scatter(df["Name"], df["Rating"], s=df["User Ratings"] * scale_factor)
    plt.xlabel("Rating")
    plt.ylabel("Number of Reviews")
    plt.title("Restaurant Rating and Number of Reviews")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("restaurant_ratings_and_nratings.png", dpi=300)


def scores_top_10(df):
    df = df.head(10)
    plt.bar(df["Name"], df["Weighted Score"])
    plt.xlabel("Restaurant Name")
    plt.ylabel("Score")
    plt.title("Top 10 Restaurants' Name vs Score")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("10_restaurants_score.png", dpi=300)


def top_10_rated_restaurants(df):
    df = df.head(10)
    plt.bar(df["Name"], df["Rating"])
    plt.xlabel("Restaurant Name")
    plt.ylabel("Rating")
    plt.title("Top 10 Best Rated Restaurants")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("10_restaurants_rating.png", dpi=300)


def rating_vs_nratings(df):
    plt.scatter(df["Rating"], df["User Ratings"])
    plt.xlabel("Rating")
    plt.ylabel("Number of Reviews")
    plt.title("Rating vs Number of Reviews")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("ratings_vs_nratings.png", dpi=300)


def price_vs_nratings(df):
    plt.scatter(df["Price Level"], df["User Ratings"])
    plt.xlabel("Price Level")
    plt.ylabel("Number of Reviews")
    plt.title("Price Level vs Number of Reviews")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("price_vs_nratings.png", dpi=300)


def price_vs_rating(df):
    plt.scatter(df["Price Level"], df["Rating"])
    plt.xlabel("Price Level")
    plt.ylabel("Rating")
    plt.title("Price Level vs Rating")
    plt.xticks(rotation=90, fontsize=6)
    plt.tight_layout()
    plt.savefig("price_vs_rating.png", dpi=300)


def run(df):
    general_stats(df)
    name_and_rating(df)
    name_and_nratings(df)
    rating_and_nratings(df)
    scores_top_10(df)
    rating_vs_nratings(df)
    price_vs_nratings(df)
    price_vs_rating(df)


if __name__ == '__main__':
    data = read_df("./sorted_restaurants.csv")
    run(data)
