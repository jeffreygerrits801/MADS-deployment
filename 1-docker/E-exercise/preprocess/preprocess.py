# preprocess/preprocess.py

from pathlib import Path
from loguru import logger
from pandas import json_normalize
import pandas as pd
import json
import re
from datetime import datetime


RAW_FILE = Path("/app/data/raw/posts.json")
OUT_DIR = Path("/app/data/processed")
OUT_FILE = OUT_DIR / "posts.parquet"


def bin_time(time):
    if time < datetime(2017, 12, 1):
        return 0
    elif time < datetime(2018, 1, 1):
        return 1
    elif time < datetime(2018, 8, 10):
        return 2
    elif time < datetime(2019, 8, 1):
        return 3
    else:
        return 4


def remove_url(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', str(text))


def main():
    logger.info("Starting preprocessing...")

    with RAW_FILE.open() as f:
        df = json_normalize(json.load(f)["posts"], sep="_")

    df["time"] = pd.to_datetime(df["post_metadata_time"], unit="s")
    df["bintime"] = df["time"].apply(bin_time)

    df["text"] = df["text"].fillna("").astype(str)
    df["text"] = df["text"].str.replace("\n", " ", regex=False)
    df["text"] = df["text"].apply(remove_url)
    df["text"] = df["text"].str.lower()

    df["size"] = df["text"].str.len()
    df = df[df["size"] > 50].reset_index(drop=True)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_FILE)

    logger.info("Preprocessing complete.")


if __name__ == "__main__":
    main()