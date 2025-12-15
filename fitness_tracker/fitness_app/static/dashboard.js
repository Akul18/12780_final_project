document.addEventListener("DOMContentLoaded", () => {
    const chartEl = document.getElementById("chart");
    const exerciseSelect = document.getElementById("exercise-select");
    const metricSelect = document.getElementById("metric-select");
    const exportBtn = document.getElementById("export-selected");
  
    let chart = new Chart(chartEl, {
      type: "line",
      data: {
        labels: [],
        datasets: [{
          label: "weight",
          data: [],
        }]
      }
    });
  
    function buildUrl() {
      const ex = exerciseSelect.value;
      const metric = metricSelect.value;
  
      let url = `/chart-data/?metric=${encodeURIComponent(metric)}`;
      if (ex) url += `&exercise_id=${encodeURIComponent(ex)}`;
      return url;
    }
  
    function loadChart() {
      fetch(buildUrl())
        .then(r => r.json())
        .then(payload => {
          chart.data.labels = payload.labels || [];
          chart.data.datasets[0].data = payload.data || [];
          chart.data.datasets[0].label = payload.metric || metricSelect.value;
          chart.update();
        })
        .catch(() => {
          chart.data.labels = [];
          chart.data.datasets[0].data = [];
          chart.update();
        });
    }
  
    exerciseSelect.addEventListener("change", loadChart);
    metricSelect.addEventListener("change", loadChart);
  
    exportBtn.addEventListener("click", () => {
      const ex = exerciseSelect.value;
      if (ex) {
        window.location.href = `/export.xlsx?exercise_id=${encodeURIComponent(ex)}`;
      } else {
        window.location.href = "/export.xlsx";
      }
    });
  
    loadChart();
  });
  