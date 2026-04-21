# ingest/ingest.py

import requests
from pathlib import Path
from loguru import logger
import re


def download(url, datafile: Path):
    datadir = datafile.parent

    if not datadir.exists():
        logger.info(f"Creating directory {datadir}")
        datadir.mkdir(parents=True)

    if not datafile.exists():
        logger.info(f"Downloading {url} to {datafile}")
        response = requests.get(url)
        response.raise_for_status()
        with datafile.open("wb") as f:
            f.write(response.content)
    else:
        logger.info(f"{datafile} already exists, skipping")


def download_main_dataset():
    url = "https://raw.githubusercontent.com/jkingsman/JSON-QAnon/main/posts.json"
    datafile = Path("/app/data/raw/posts.json")
    download(url, datafile)


def download_tanach():
    books = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
        "Judges", "1%20Samuel", "2%20Samuel", "1%20Kings", "2%20Kings",
        "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi"
    ]

    base_dir = Path("/app/data/raw/tanach")

    for book in books:
        url = f"https://www.tanach.us/Server.txt?{book}*&content=Accents"
        filename = re.sub(r"%20", "_", book)
        datafile = base_dir / f"{filename}.txt"
        download(url, datafile)


def main():
    logger.info("Starting ingestion...")
    download_main_dataset()
    download_tanach()
    logger.info("Ingestion complete.")


if __name__ == "__main__":
    main()