import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# !Functions
def get_month_year_wordcount_cols(dataframe: pd.DataFrame):
    dataframe["year"] = dataframe.apply(
        lambda row: pd.to_datetime(row["date"]).year, axis=1
    )
    dataframe["month"] = dataframe.apply(
        lambda row: pd.to_datetime(row["date"]).month, axis=1
    )
    dataframe["word_count"] = dataframe.apply(
        lambda row: 0
        if pd.isna(row["comment"])
        else (len(re.findall(r"[\w']+", row["comment"]))),
        axis=1,
    )
    return dataframe


def get_count_rating_by_year(year: pd.DataFrame):
    count_year_df = (
        reviews_df[reviews_df["year"] == year]["rating"]
        .value_counts()
        .fillna(0)
        .astype(int)
    )
    return count_year_df


def merge_dfs(left_df: pd.DataFrame, right_df: pd.DataFrame):
    merged_df = (
        pd.merge(left_df, right_df, on="rating", how="outer").fillna(0).astype(int)
    )
    return merged_df


def get_ticks(df: pd.DataFrame, step: float, min_0: bool = True):
    has_count = df.columns.__contains__("count")

    if has_count:
        min = df["count"].min()
        max = df["count"].max()

    else:
        min = df.values.min()
        max = df.values.max()

    if min_0:
        min = 0

    return np.arange(min, max + (step * 2), step)


def get_columns(list_of_items: list, list_of_items_to_add: list):
    seasonname_year = []
    year_season = []

    season_to_month = {
        "Winter": 1,
        "Winter": 1,
        "Winter": 1,
        "Winter": 1,
        "Summer": 2,
        "Summer": 2,
        "Summer": 2,
        "Summer": 2,
        "Fall": 3,
        "Fall": 3,
        "Fall": 3,
        "Fall": 3,
    }

    for item in list_of_items:
        for item_to_add in list_of_items_to_add:
            seasonname_year.append(f"{item} {item_to_add}")
            year_season.append(f"20{item_to_add}{season_to_month[item]}")

    return seasonname_year, year_season


def add_season_year_col(row):
    month_to_season = {
        1: "Winter",
        2: "Winter",
        3: "Winter",
        4: "Winter",
        5: "Summer",
        6: "Summer",
        7: "Summer",
        8: "Summer",
        9: "Fall",
        10: "Fall",
        11: "Fall",
        12: "Fall",
    }

    season = month_to_season[row["month"]]
    year = str(int(row["year"]))
    seasonname_year = f"{season} {year[2:]}"

    return seasonname_year


# !Read in files to dfs

reviews_df = pd.read_csv("reviews_pa3.txt", sep="\t", index_col="serial_no")
cars_df = pd.read_csv("cars_pa3.txt", sep="#")


# !ADDING COLUMNS

reviews_df = get_month_year_wordcount_cols(reviews_df)
print(reviews_df.to_string(), end="\n\n")

# !DESCRIPTIVE STATISTICS
print("Average Rating:")
print(reviews_df["rating"].describe(), end="\n\n")

print("Average Word Count:")
print(reviews_df["word_count"].describe(), end="\n\n")


# !RATINGS COUNT DISTRIBUTION BY YEAR

count_2019 = get_count_rating_by_year(2019)
count_2020 = get_count_rating_by_year(2020)
count_2021 = get_count_rating_by_year(2021)

df_2019_2020_rating_counts = merge_dfs(count_2019, count_2020)
df_2019_2020_2021_rating_counts = merge_dfs(df_2019_2020_rating_counts, count_2021)

df_2019_2020_2021_rating_counts = df_2019_2020_2021_rating_counts.sort_index()

df_2019_2020_2021_rating_counts.columns = ["count_2019", "count_2020", "count_2021"]

df_2019_2020_2021_rating_counts.plot(kind="bar")

y_ticks = get_ticks(df_2019_2020_2021_rating_counts, 1, True)

plt.title("Number of Ratings by Year")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.yticks(y_ticks)

print(df_2019_2020_2021_rating_counts.to_string(), end="\n\n")

# !AVERAGE WORD COUNT BY YEAR
avg_word_count_year_df = pd.DataFrame(reviews_df.groupby(["year"])["word_count"].mean())
avg_word_count_year_df.columns = ["avg_word_count"]

print(avg_word_count_year_df, end="\n\n")

y_ticks = get_ticks(avg_word_count_year_df, 0.5, True)

avg_word_count_year_df.plot(kind="bar")
plt.legend()
plt.title("Average Word Count by Year")
plt.xlabel("Year")
plt.xticks(rotation=360)
plt.ylabel("Word Count")
plt.yticks(y_ticks)


# !RATINGS COUNT DISTRIBUTION BY SEASONS AND YEARS

seasonname_year, year_season = get_columns(["Winter", "Summer", "Fall"], [19, 20, 21])

rating_count_by_season_year_df = pd.DataFrame(
    {
        "seasonname_year": seasonname_year,
        "year_season": year_season,
    }
).set_index("seasonname_year")

reviews_df = reviews_df.dropna(subset=["rating", "comment"], how="any")
reviews_df = reviews_df[reviews_df["word_count"] != 0]

year_month_rating_counts = pd.DataFrame(
    reviews_df.groupby(["year", "month"])["rating"].value_counts()
).reset_index()


year_month_rating_counts["seasonname_year"] = year_month_rating_counts.apply(
    add_season_year_col, axis=1
)

rating_count_by_season_year_df = (
    pd.merge(
        rating_count_by_season_year_df,
        year_month_rating_counts,
        on="seasonname_year",
        how="left",
    )
    .drop(["year", "month", "rating"], axis=1, inplace=False)
    .fillna(0)
)

rating_count_by_season_year_df = (
    pd.DataFrame(
        rating_count_by_season_year_df.groupby(["seasonname_year", "year_season"])[
            "count"
        ].sum()
    )
    .reset_index()
    .set_index("seasonname_year")
)

rating_count_by_season_year_df["count"] = rating_count_by_season_year_df["count"].apply(
    lambda x: int(x)
)
rating_count_by_season_year_df = rating_count_by_season_year_df.sort_values(
    "year_season"
)

y_ticks = get_ticks(rating_count_by_season_year_df, 1, True)

rating_count_by_season_year_df.plot(kind="line")
plt.title("Number of Reviews by Season and Year")
plt.legend(loc="upper right")
plt.xlabel("Year Season")
plt.xticks(rotation=30)
plt.ylabel("Count")
plt.yticks(y_ticks)

# !AVERAGE YEARLY RATINGS DISTRIBUTION BY CAR