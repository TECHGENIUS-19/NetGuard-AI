import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

DATABASE = "data/netguard.db"

connection = sqlite3.connect(DATABASE)

data = pd.read_sql_query(
    "SELECT * FROM traffic",
    connection
)

connection.close()

print("========================================")
print("       NETGUARD AI ANOMALY DETECTOR")
print("========================================")

print("Total traffic records:", len(data))

if len(data) < 10:
    print()
    print("Not enough traffic data for AI detection.")
    print("At least 10 records are required.")
    print()
    print("Current records:", len(data))
    exit()

features = data[
    [
        "source_port",
        "destination_port",
        "packet_size"
    ]
].copy()

features = features.fillna(0)

model = IsolationForest(
    n_estimators=100,
    contamination=0.10,
    random_state=42
)

model.fit(features)

data["prediction"] = model.predict(features)

data["status"] = data["prediction"].map({
    1: "NORMAL",
    -1: "ANOMALY"
})

normal = (data["status"] == "NORMAL").sum()
anomaly = (data["status"] == "ANOMALY").sum()

print()
print("AI ANALYSIS COMPLETED")
print("----------------------------------------")
print("Normal Traffic    :", normal)
print("Anomalous Traffic :", anomaly)

print()
print("TRAFFIC ANALYSIS")
print("----------------------------------------")

for _, row in data.iterrows():

    print(
        row["source_ip"],
        "->",
        row["destination_ip"],
        "|",
        row["protocol"],
        "|",
        row["source_port"],
        "->",
        row["destination_port"],
        "|",
        row["packet_size"],
        "bytes",
        "|",
        row["status"]
    )
