<script>
let lineChart, barChart, overviewLineChart, overviewBarChart;

/* ---------- TABS ---------- */
function openTab(id) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.getElementById(id).classList.add("active");
    event.target.classList.add("active");
}

/* ---------- DATA ---------- */
const compactness = [0.62,0.66,0.70,0.74,0.78,0.82,0.86,0.90,0.94,0.98];
const heating = [36,32,28,24,20,17,14,12,10,9];
const cooling = [28,25,22,19,16,14,12,10,9,8];

const features = [
    "Relative Compactness","Overall Height","Glazing Area",
    "Surface Area","Wall Area","Roof Area","Glazing Dist","Orientation"
];
const importance = [95,90,82,75,70,62,35,12];

/* ---------- LINE CHART ---------- */
function createLineChart(canvasId) {
    return new Chart(document.getElementById(canvasId), {
        type: "line",
        data: {
            labels: compactness,
            datasets: [
                { label: "Heating Load", data: heating, borderColor: "#f97316", tension: 0.4 },
                { label: "Cooling Load", data: cooling, borderColor: "#3b82f6", tension: 0.4 }
            ]
        },
        options: { responsive: true }
    });
}

/* ---------- BAR CHART ---------- */
function createBarChart(canvasId) {
    return new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: features,
            datasets: [{
                data: importance,
                backgroundColor: "#6366f1",
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: "y",
            plugins: { legend: { display: false } }
        }
    });
}

/* ---------- INIT ---------- */
window.onload = () => {
    overviewLineChart = createLineChart("overviewLineChart");
    overviewBarChart = createBarChart("overviewBarChart");

    lineChart = createLineChart("lineChart");
    barChart = createBarChart("barChart");
};
</script>
