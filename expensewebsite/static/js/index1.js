const log = console.log;

const chartProperties = {
    position: 'absolute',
    width: 1000,
    height: 600,
    timeScale: {
        timeVisible: true,
        secondsVisible: true,
    },
    pane: 0,
};

const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement, chartProperties);
const candleSeries = chart.addCandlestickSeries();

function updateChart(csvFilePath) {
    return fetch(csvFilePath)
        .then(response => response.text())
        .then(data => {
            const rows = data.trim().split('\n');
            const csvData = rows.map(row => row.split(','));
            csvData.shift();
            const first10Rows = csvData.slice(0, 750);

            const transformedData = first10Rows.map(d => {
                return {
                    time: parseFloat(d[0]) / 1000, // Corrected parentheses
                    open: parseFloat(d[1]),
                    high: parseFloat(d[2]),
                    low: parseFloat(d[3]),
                    close: parseFloat(d[4])
                };
            });

            console.log(transformedData);

            return transformedData;
        });
}

function updateChartData() {
    updateChart('static/js/data.csv')
        .then(data => {
            candleSeries.setData(data);
        })
        .catch(error => {
            console.error('Error updating chart:', error);
        });
}

// Call updateChartData initially to populate the chart
updateChartData();

// Add event listener to form submission
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    const symbol = document.getElementById('symbol').value; // Get symbol value from input

    // Get CSRF token from cookies
    const csrftoken = getCookie('csrftoken');

    // Use Fetch API to submit the form data asynchronously
    fetch('http://127.0.0.1:8000/cad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken // Include CSRF token in headers
        },
        body: 'symbol=' + encodeURIComponent(symbol)
    })
    .then(response => {
        if (response.ok) {
            // If form submission is successful, update chart data
            updateChartData();
        } else {
            console.error('Form submission failed:', response.statusText);
        }
    })
    .catch(error => console.error('Error submitting form:', error));
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if cookie name matches the CSRF token cookie name
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}