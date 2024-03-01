const log = console.log;

const chartProperties = {
    position: 'absolute',
    width: 1000,
    height: 600,
    timeScale: {
        timeVisible: true,
        secondsVisible: false,
    },
    pane: 0,
};

const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement, chartProperties);
const candleSeries = chart.addCandlestickSeries();

// Function to update the chart with new data
function updateChart(csvFilePath) {
    fetch(csvFilePath)
        .then(response => response.text())
        .then(data => {
            const rows = data.trim().split('\n');
            const csvData = rows.map(row => row.split(','));
            csvData.shift();
            console.log(csvData)

            const transformedData = csvData.map(row => {
                return row.map((element, index) => {
                    if (index === 7 || index === 8) {
                        return element.trim().toLowerCase() === 'true';
                    }
                    return parseFloat(element.trim());
                });
            });

            const cdata = transformedData.map(d => ({
                time: d[0],
                open: parseFloat(d[1]),
                high: parseFloat(d[2]),
                low: parseFloat(d[3]),
                close: parseFloat(d[4]),
                SMA: parseFloat(d[5]),
                EMA: parseFloat(d[6]),
                long: String(d[7]).toLowerCase() === 'true',
                short: String(d[8]).toLowerCase() === 'true',
                rsi: parseFloat(d[9])
            }));

            candleSeries.setData(cdata);

            const smaData = cdata.map(d => ({ time: d.time, value: d.SMA }));
            const smaSeries = chart.addLineSeries({ color: 'green', lineWidth: 1 });
            smaSeries.setData(smaData);

            const EmaData = cdata.map(d => ({ time: d.time, value: d.EMA }));
            const EmaSeries = chart.addLineSeries({ color: 'red', lineWidth: 1 });
            EmaSeries.setData(EmaData);

            candleSeries.setMarkers(cdata.filter((d)=>d.long || d.short).map(d => {
                return d.long ? { time: d.time, position: 'belowBar', color: 'green', shape: 'arrowUp', text: 'LONG' } : { time: d.time, position: 'aboveBar', color: 'red', shape: 'arrowUp', text: 'short' };
            }));

            const rsi_series=chart.addLineSeries({color:'purple',linewidth:1,pane:0});
            rsi_series.setData(cdata.map(d => ({ time: d.time, value: d.rsi })));
        })
        .catch(err => log(err));
}

// Function to force chart update


// Call the function to display initial chart data
updateChart('static/js/torc5.csv');


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
            // If form submission is successful, update chart with new data
            updateChart('static/js/torc5.csv');

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

// Function to download raw CSV data
