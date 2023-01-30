import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("./data.csv")
data["<DATE>"] = pd.to_datetime(data["<DATE>"], format="%d/%m/%Y")


sep_data = data[data["<DATE>"].between("2018-09-05", "2018-09-05")][
    ["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]
]
sep_data.Name = "2018-09-05"

oct_data = data[data["<DATE>"].between("2018-10-05", "2018-10-05")][
    ["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]
]
oct_data.Name = "2018-10-05"

nov_data = data[data["<DATE>"].between("2018-11-07", "2018-11-07")][
    ["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]
]
nov_data.Name = "2018-11-07"

dec_data = data[data["<DATE>"].between("2018-12-05", "2018-12-05")][
    ["<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>"]
]
dec_data.Name = "2018-12-05"


# rename cols
for df in (sep_data, oct_data, nov_data, dec_data):
    df.rename(columns={col: f"{df.Name} {col}" for col in df.columns}, inplace=True)


figures = []
for df in (sep_data, oct_data, nov_data, dec_data):
    figures.append(
        plt.figure(figsize=(15, 10))
    )

    df.boxplot()


plt.show()