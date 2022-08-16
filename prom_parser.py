import json
from datetime import datetime
from pathlib import Path
from matplotlib import pyplot

from pandas import DataFrame, Series, to_numeric


def parse_prom_file(filepath: str) -> DataFrame:
    """Takes a prometheus format file and returns it as a dataframe"""
    with Path(filepath).open("r") as f:
        raw_json = json.load(f)

    df = DataFrame(raw_json["result"][0]["values"], columns=["Time", "Value"])
    df.Time = df.Time.apply(lambda x: datetime.fromtimestamp(x))
    df.Value = to_numeric(df.Value)
    df.set_index("Time")
    print(df.head())
    return df


def parse_prom_file_to_series(filepath: str) -> Series:
    """Takes a prometheus format file and returns it as a series"""
    with Path(filepath).open("r") as f:
        raw_json = json.load(f)

    idx = [datetime.fromtimestamp(i[0]) for i in raw_json["result"][0]["values"]]
    values = [float(i[1]) for i in raw_json["result"][0]["values"]]
    return Series(values, index=idx)


if __name__ == "__main__":
    df = parse_prom_file("./data/data-jan-2022.json")
    df.plot(x="Time", y="Value")
    pyplot.show()
