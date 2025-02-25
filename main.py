import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("src/crawling/brands.csv")
    print(df.head())
