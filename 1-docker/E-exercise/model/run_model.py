# model/run_model.py

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger

from model import TextClustering


DATA_FILE = Path("/app/data/processed/posts.parquet")
OUT_FILE = Path("/app/data/output/clustering.png")


def main():
    logger.info("Starting model step...")

    # load data
    df = pd.read_parquet(DATA_FILE)

    # run model
    clustering = TextClustering()
    X = clustering(df["text"], k=100, batch=True, method="PCA")
    labels = clustering.get_labels(df)

    # plot
    plt.figure(figsize=(10, 10))
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels)

    # save output
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_FILE)

    logger.info(f"Saved result to {OUT_FILE}")


if __name__ == "__main__":
    main()