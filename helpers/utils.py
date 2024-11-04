# helpers/utils.py

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlite3


def get_books(url: str) -> list:
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    books = soup.find_all("article")
    return books


def scrape_page(books: list, results: list) -> list:
    for book in books:
        base = "http://books.toscrape.com/"
        title = book.find("a").find("img")["alt"]
        price = book.find("p", class_="price_color").text[2:]
        image_link = base + book.find("a").find("img")["src"]
        book_link = base + book.find("a")["href"]
        result = {
            "title": title,
            "price": price,
            "book_link": book_link,
            "image_link": image_link,
        }
        results.append(result)
    return results


def save_to_sqlite3(df: pd.DataFrame) -> None:
    # create a connection
    conn = sqlite3.connect("../../project_template2/data/MovieScrape.db")
    df.to_sql("movies", conn, if_exists="replace", index=False)
    data = pd.read_sql("select * from movies", conn)
    conn.commit()
    conn.close()
    print("saved to sql")
