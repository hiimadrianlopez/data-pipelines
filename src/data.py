import os

import pandas as pd
from sqlalchemy import create_engine, text

from src import config


def import_data():
    data_folder = config.RAW_DATA_PATH
    tmp_engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    for file_name in sorted(os.listdir(data_folder)):
        result = tmp_engine.connect().execute(
            text(f"select count(*) from {model_name}")
        )
        if result.fetchone()[0] > 0:
            continue

        df = pd.read_csv(f"{data_folder}/{file_name}")
        model_name = file_name.split(".")[0]
        df.to_sql(model_name, tmp_engine, if_exists="append", index=False)
