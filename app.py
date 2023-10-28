import re
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

cars_df = pd.read_csv("./cars_pa3.txt", sep="#")
reviews_df = pd.read_csv("./reviews_pa3.txt", sep="\t")


def extract_year(date_str):
    date_object = datetime.strptime(date_str, "%m-%d-%Y")
    return date_object.year


def extract_month(date_str):
    date_object = datetime.strptime(date_str, "%m-%d-%Y")
    return date_object.month


def extract_word_count(comment):
    if pd.isna(comment):
        return 0
    return len(re.findall(r"[\w']+", comment))


reviews_df["year"] = reviews_df["date"].apply(extract_year)
reviews_df["month"] = reviews_df["date"].apply(extract_month)
reviews_df["word_count"] = reviews_df["comment"].apply(extract_word_count)

print("Average Rating: ")
print(reviews_df["rating"].describe(), end="\n\n")

print("Average Word Count: ")
print(reviews_df["word_count"].describe())


# extract_ratingCountSeries(rating_Series)
def get_year_rating_df(df):
    year_rating_df = df.groupby(["year"])["rating"].value_counts()
    year_rating_df = year_rating_df.to_frame()
    year_rating_df.columns = ["count"]
    year_rating_df = year_rating_df.reset_index()
    return year_rating_df


year_rating_df = get_year_rating_df(reviews_df)


def get_rating_year_sp(my_df, year):
    my_df_year = my_df[year_rating_df["year"] == year]
    my_df_year = my_df_year.drop(["year"], axis=1)
    my_df_year.columns = ["rating", "count_" + str(year)]

    return my_df_year


# year_rating_df_2019 = get_rating_year_sp(reviews_df, 2019)
# year_rating_df_2020 = get_rating_year_sp(reviews_df, 2020)
# year_rating_df_2021 = get_rating_year_sp(reviews_df, 2021)

df_pivot = (
    year_rating_df.pivot(index="rating", columns="year", values="count")
    .fillna(0)
    .astype("int")
)

print(df_pivot)

# plt.hist(df_pivot)
# plt.title("Number of Ratings by Year")
# plt.xlabel("Rating")
# plt.xticks([1.0, 2.0, 3.0, 4.0, 5.0])
# plt.ylabel("Counts")
# plt.yticks([0, 1, 2, 3, 4, 5])
# plt.show()

df_pivot.plot(kind="bar", legend=True)

# Set the labels for x and y axes
plt.xlabel("Rating")
plt.xticks([0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
plt.ylabel("Count")
plt.yticks([0, 1, 2, 3, 4, 5])

# Show the legend
plt.legend(title="Year")
plt.title("Number of Rating by Year")

# Show the plot
plt.show()
