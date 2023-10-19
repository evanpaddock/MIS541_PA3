import re
import pandas as pd
import numpy as np
from datetime import datetime

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
