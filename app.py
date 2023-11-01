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


# Create the columns year, month, word_count by extracting values using the functions above
reviews_df["year"] = reviews_df["date"].apply(extract_year)
reviews_df["month"] = reviews_df["date"].apply(extract_month)
reviews_df["word_count"] = reviews_df["comment"].apply(extract_word_count)

# ! Descriptive Statistics
print("Average Rating: ")
print(reviews_df["rating"].describe(), end="\n\n")

print("Average Word Count: ")
print(reviews_df["word_count"].describe())

# !RATINGS COUNT DISTRIBUTION BY YEAR
# Create three DataFrames for 2019, 2020, and 2021
df_2019 = reviews_df[reviews_df["year"] == 2019]
df_2020 = reviews_df[reviews_df["year"] == 2020]
df_2021 = reviews_df[reviews_df["year"] == 2021]

# Count the rating values for each year
count_2019 = df_2019["rating"].value_counts().fillna(0).astype(int)
count_2020 = df_2020["rating"].value_counts().fillna(0).astype(int)
count_2021 = df_2021["rating"].value_counts().fillna(0).astype(int)

# Merge the three DataFrames on the rating column
df_2019_20_21_rating_years = (
    pd.concat(
        [count_2019, count_2020, count_2021],
        axis=1,
        keys=["count_2019", "count_2020", "count_2021"],
    )
    .fillna(0)
    .sort_index()
)

df_2019_20_21_rating_years.plot(kind="bar")
plt.title("Number of Ratings by Year")
plt.xlabel("Rating")
plt.xticks([0, 1.0, 2.0, 3.0, 4.0, 5.0])
plt.ylabel("Counts")
plt.yticks([0, 1, 2, 3, 4, 5])

# !AVERAGE WORD COUNT BY YEAR
avgword_count_by_year = reviews_df.groupby("year")["word_count"].mean()
avgword_count_by_year = avgword_count_by_year.to_frame()
avgword_count_by_year.columns = ["avg_word_count"]

min = 0.0
max = 5.5
step = 0.5
y_ticks = np.arange(min, max + step, step)

avgword_count_by_year = avgword_count_by_year.sort_index()

avgword_count_by_year.plot(kind="bar", legend=True)
plt.title("Average Word Count by Year")
plt.xlabel("Year")
plt.ylabel("Word Count")
plt.xticks(rotation=360)
plt.yticks(y_ticks)

# !RATINGS COUNT DISTRIBUTION BY SEASONS AND YEARS
reviews_df = reviews_df.dropna(subset=["rating", "comment"], how="any")
reviews_df = reviews_df[reviews_df["word_count"] != 0]

seasonname_year_df = reviews_df.sort_values(["year", "month"])

def get_season_name(row):
    seasons = {
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

    month = seasons[row["month"]]
    year = str(row["year"])
    
    return {'seasonname_year': f"{month} {year[2:]}", 'year_season': f"{year}{row['month']}"}


final_df = seasonname_year_df.apply(get_season_name, axis=1)
final_df = pd.DataFrame(final_df.tolist()).set_index(['seasonname_year'])
count_df = final_df.groupby('seasonname_year')['year_season'].value_counts()

print(final_df.head(10))