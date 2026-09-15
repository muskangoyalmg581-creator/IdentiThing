async function loadProcesses() {

    const response = await fetch("/api/processes");

    const processes = await response.json();

    let total = processes.length;
    let normal = 0;
    let anomalies = 0;
    let highrisk = 0;

    processes.forEach(process => {

        if (process.status === "NORMAL") {
            normal++;
        }

        else {
            anomalies++;
        }

        if (process.risk >= 80) {
            highrisk++;
        }
    });

    const table = document.getElementById("processTable");

    table.innerHTML = "";

    processes.slice(0, 30).forEach(process => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${process.pid}</td>
            <td>${process.name}</td>
            <td>${process.cpu}</td>
            <td>${process.memory}</td>
            <td class="${process.status === "NORMAL" ? "normal" : "anomaly"}">
                ${process.status}
            </td>
            <td>${process.risk}</td>
        `;

        table.appendChild(row);
    });

    document.getElementById("total").innerText = total;

    document.getElementById("normal").innerText = normal;

    document.getElementById("anomalies").innerText = anomalies;

    document.getElementById("highrisk").innerText = highrisk;
}


async function loadAlerts() {

    const response = await fetch("/api/alerts");

    const alerts = await response.json();

    const table = document.getElementById("alertTable");

    table.innerHTML = "";

    alerts.reverse().forEach(alert => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${alert.timestamp}</td>
            <td>${alert.process_name}</td>
            <td>${alert.cpu_percent}</td>
            <td>${alert.memory_percent}</td>
            <td>${alert.risk_score}</td>
            <td class="anomaly">
                ${alert.severity}
            </td>
        `;

        table.appendChild(row);
    });
}


function updateDashboard() {

    loadProcesses();

    loadAlerts();
}


updateDashboard();

setInterval(updateDashboard, 5000);