let classList = ['LT-47', 'LT-12', 'LT-83', 'LT-61', 'LT-90', 'LT-05', 'LT-74', 'LT-33', 'LT-22', 'LT-92'];
let sampleClassList=[
  {'class_number': 'LT-47', 'occupancy_rate_percent': 42},
  {'class_number': 'LT-12', 'occupancy_rate_percent': 68},
  {'class_number': 'LT-83', 'occupancy_rate_percent': 15},
  {'class_number': 'LT-61', 'occupancy_rate_percent': 91},
  {'class_number': 'LT-90', 'occupancy_rate_percent': 54},
  {'class_number': 'LT-05', 'occupancy_rate_percent': 3},
  {'class_number': 'LT-09', 'occupancy_rate_percent': 3},
  {'class_number': 'LT-74', 'occupancy_rate_percent': 77},
  {'class_number': 'LT-33', 'occupancy_rate_percent': 39},
  {'class_number': 'LT-22', 'occupancy_rate_percent': 88},
  {'class_number': 'LT-92', 'occupancy_rate_percent': 21},

]
let sampleData = [
  { name: "John", age: 25, email: "john@example.com" },
  { name: "Alice", age: 30, email: "alice@example.com" },
  { name: "Bob", age: 35, email: "bob@example.com" },
  { name: "Bob", age: 35, email: "bob@example.com" },
  { name: "Bob", age: 35, email: "bob@example.com" },
  { name: "Bob", age: 35, email: "bob@example.com" }
];

function createAndAppendTable(data, containerId) {
  var container = document.getElementById(containerId);
  var table = document.createElement("table");
  table.setAttribute("id", "dataTable");

  var tableHead = document.createElement("thead");
  var headRow = document.createElement("tr");
  Object.keys(data[0]).forEach(function(key) {
      var th = document.createElement("th");
      let finalKey = key.replace(/_/g, ' ').toUpperCase();
      th.textContent = finalKey;
      headRow.appendChild(th);
  });
  tableHead.appendChild(headRow);
  table.appendChild(tableHead);

  var tableBody = document.createElement("tbody");
  data.forEach(function(rowData) {
      var row = document.createElement("tr");
      Object.values(rowData).forEach(function(value) {
          var cell = document.createElement("td");
          cell.textContent = value;
          row.appendChild(cell);
      });
      tableBody.appendChild(row);
  });
  table.appendChild(tableBody);

  container.appendChild(table);
}
function createAndAppendLists(data, containerId) {
  var container = document.getElementById(containerId);
      data.map(value => {
          var listItem = document.createElement("li");
          listItem.textContent = value;
          container.appendChild(listItem);
      });
}
function generateInsights(data,containerId){
  var occupancyRate = data.map(value => value['occupancy_rate_percent']);
  var above50 = occupancyRate.filter(value => value > 50).length;
  let leastOccupied = data.reduce((prev, current) => (prev.occupancy_rate_percent < current.occupancy_rate_percent) ? prev : current);
  let mostOCcupied = data.reduce((prev, current) => (prev.occupancy_rate_percent > current.occupancy_rate_percent) ? prev : current);
  var container = document.getElementById(containerId);
  var insights = document.createElement("div");
  insights.innerHTML = `
  <h4>Highest Occupancy Rate: ${mostOCcupied.occupancy_rate_percent}%</h4>
  <h4>Number of classes with occupancy rate above 50%:  ${above50}</h4>
  <h4>Number of classes with occupancy rate below 50%:  ${occupancyRate.length - above50}</h4>
  `
  container.appendChild(insights);
}

createAndAppendTable(sampleData, "tables");
createAndAppendTable(sampleClassList, "lists");
generateInsights(sampleClassList, "insights")













// SIDEBAR TOGGLE
let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------

// BAR CHART
const barChartOptions = {
  series: [
    {
      data: [53,49,47,44,37,20],
      name: 'Avg Student Present',
    },
  ],
  chart: {
    type: 'bar',
    background: 'transparent',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#2962ff', '#d50000', '#2e7d32', '#ff6d00', '#583cb3' , '#27a5f9'],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: false,
      columnWidth: '40%',
    },
  },
  dataLabels: {
    enabled: false,
  },
  fill: {
    opacity: 1,
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  stroke: {
    colors: ['transparent'],
    show: true,
    width: 2,
  },
  tooltip: {
    shared: true,
    intersect: false,
    theme: 'dark',
  },
  xaxis: {
    // categories: ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],
    // categories: ['Laptop', 'Phone', 'Monitor', 'Headphones', 'Camera'],
    categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    title: {
      style: {
        color: '#f5f7ff',
      },
    },
    axisBorder: {
      show: true,
      color: '#55596e',
    },
    axisTicks: {
      show: true,
      color: '#55596e',
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: {
    title: {
      text: 'Count',
      style: {
        color: '#f5f7ff',
      },
    },
    axisBorder: {
      color: '#55596e',
      show: true,
    },
    axisTicks: {
      color: '#55596e',
      show: true,
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
};

const barChart = new ApexCharts(
  document.querySelector('#bar-chart'),
  barChartOptions
);
barChart.render();

// AREA CHART
const areaChartOptions = {
  series: [
    {
      name: 'Avg. Students in First Shift',
      data: [31, 40, 28, 51, 42, 109],
    },
    {
      name: 'Avg. Students in Second Shift',
      data: [11, 32, 45, 32, 34, 52],
    },
  ],
  chart: {
    type: 'area',
    background: 'transparent',
    height: 350,
    stacked: false,
    toolbar: {
      show: false,
    },
  },
  colors: ['#00ab57', '#d50000'],
  labels: ['Lect-01', 'Lect-02','Lect-03','Lect-04','Lect-05','Lect-06'],
  dataLabels: {
    enabled: false,
  },
  fill: {
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.1,
      shadeIntensity: 1,
      stops: [0, 100],
      type: 'vertical',
    },
    type: 'gradient',
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  markers: {
    size: 6,
    strokeColors: '#1b2635',
    strokeWidth: 3,
  },
  stroke: {
    curve: 'smooth',
  },
  xaxis: {
    axisBorder: {
      color: '#55596e',
      show: true,
    },
    axisTicks: {
      color: '#55596e',
      show: true,
    },
    labels: {
      offsetY: 5,
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: [
    {
      title: {
        text: 'Students in First Shift',
        style: {
          color: '#f5f7ff',
        },
      },
      labels: {
        style: {
          colors: ['#f5f7ff'],
        },
      },
    },
    {
      opposite: true,
      title: {
        text: 'Students in Second Shift',
        style: {
          color: '#f5f7ff',
        },
      },
      labels: {
        style: {
          colors: ['#f5f7ff'],
        },
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    theme: 'dark',
  },
};

const areaChart = new ApexCharts(
  document.querySelector('#area-chart'),
  areaChartOptions
);
areaChart.render();
