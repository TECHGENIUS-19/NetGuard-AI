from flask import Flask, jsonify, render_template_string
import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

DATABASE = "data/netguard.db"


def get_data():

    connection = sqlite3.connect(DATABASE)

    data = pd.read_sql_query(
        "SELECT * FROM traffic ORDER BY id DESC",
        connection
    )

    connection.close()

    return data


def analyze_data(data):

    if len(data) < 10:
        data["status"] = "NORMAL"
        return data

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

    return data


@app.route("/")
def home():

    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

<title>NetGuard AI</title>

<style>

body {
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 0;
    padding: 0;
}

.header {
    background: #111827;
    color: white;
    padding: 20px;
    text-align: center;
}

.header h1 {
    margin: 0;
}

.container {
    width: 90%;
    margin: 30px auto;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card h2 {
    font-size: 32px;
    margin: 10px;
}

.table-box {
    background: white;
    margin-top: 30px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: center;
}

th {
    background: #111827;
    color: white;
}

.normal {
    color: green;
    font-weight: bold;
}

.anomaly {
    color: red;
    font-weight: bold;
}

.status {
    margin-top: 20px;
    text-align: center;
    color: #555;
}

@media(max-width: 800px) {

    .cards {
        grid-template-columns: 1fr;
    }

}

</style>

</head>

<body>

<div class="header">

<h1>NETGUARD AI</h1>

<p>
Intelligent Real-Time Network Traffic Monitoring & Anomaly Detection
</p>

</div>


<div class="container">

<div class="cards">

<div class="card">

<p>Total Traffic</p>

<h2 id="total">0</h2>

</div>


<div class="card">

<p>Normal Traffic</p>

<h2 id="normal">0</h2>

</div>


<div class="card">

<p>Anomalies Detected</p>

<h2 id="anomaly">0</h2>

</div>

</div>


<div class="table-box">

<h2>Recent Network Traffic</h2>

<table>

<thead>

<tr>
<th>Time</th>
<th>Source IP</th>
<th>Destination IP</th>
<th>Protocol</th>
<th>Source Port</th>
<th>Destination Port</th>
<th>Packet Size</th>
<th>Status</th>
</tr>

</thead>

<tbody id="trafficTable">

</tbody>

</table>

</div>


<div class="status">

Dashboard automatically refreshes every 3 seconds.

</div>

</div>


<script>

async function loadDashboard() {

    try {

        const response = await fetch("/api/traffic");

        const data = await response.json();

        document.getElementById("total").innerText = data.total;

        document.getElementById("normal").innerText = data.normal;

        document.getElementById("anomaly").innerText = data.anomaly;


        const table = document.getElementById("trafficTable");

        table.innerHTML = "";


        data.traffic.forEach(row => {

            const tr = document.createElement("tr");

            const statusClass =
                row.status === "ANOMALY"
                ? "anomaly"
                : "normal";


            tr.innerHTML = `
                <td>${row.timestamp}</td>
                <td>${row.source_ip}</td>
                <td>${row.destination_ip}</td>
                <td>${row.protocol}</td>
                <td>${row.source_port}</td>
                <td>${row.destination_port}</td>
                <td>${row.packet_size} bytes</td>
                <td class="${statusClass}">
                    ${row.status}
                </td>
            `;

            table.appendChild(tr);

        });

    }

    catch (error) {

        console.log("Dashboard error:", error);

    }

}


loadDashboard();

setInterval(loadDashboard, 3000);

</script>

</body>

</html>
""")


@app.route("/api/traffic")
def traffic_api():

    data = get_data()

    data = analyze_data(data)

    total = len(data)

    normal = int(
        (data["status"] == "NORMAL").sum()
    )

    anomaly = int(
        (data["status"] == "ANOMALY").sum()
    )

    recent = data.head(20)

    traffic = []

    for _, row in recent.iterrows():

        traffic.append({
            "timestamp": row["timestamp"],
            "source_ip": row["source_ip"],
            "destination_ip": row["destination_ip"],
            "protocol": row["protocol"],
            "source_port": int(row["source_port"]),
            "destination_port": int(row["destination_port"]),
            "packet_size": int(row["packet_size"]),
            "status": row["status"]
        })

    return jsonify({
        "total": total,
        "normal": normal,
        "anomaly": anomaly,
        "traffic": traffic
    })


if __name__ == "__main__":

    print("========================================")
    print("          NETGUARD AI DASHBOARD")
    print("========================================")
    print("Starting Flask server...")
    print("Open: http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
