const log = console.log;

const chartProperties = {
  width: 1500,
  height: 600,
  pane:0,
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
  },


}

const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement, chartProperties);
const candleSeries = chart.addCandlestickSeries();

fetch('static/js/torc5.csv')
  .then(response => response.text())
  .then(data => {
    // Parse the CSV data
    const rows = data.trim().split('\n');
    const csvData = rows.map(row => row.split(','));
    csvData.shift(); // Remove the header row

    // Convert CSV data while handling boolean values correctly
    const transformedData = csvData.map(row => {
      return row.map((element, index) => {
        // Parse boolean values
        if (index === 7 || index === 8) {
          return element.trim().toLowerCase() === 'true';
        }
        // Parse numerical values
        return parseFloat(element.trim());
      });
    });

    // Use the transformedData for further processing or rendering
    console.log(transformedData);

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

    console.log(cdata);

    // Plot candlestick series
    candleSeries.setData(cdata);

    // Plot SMA series
    const smaData = cdata.map(d => ({ time: d.time, value: d.SMA }));
    const smaSeries = chart.addLineSeries({ color: 'green', lineWidth: 1 });
    smaSeries.setData(smaData);
    const EmaData = cdata.map(d => ({ time: d.time, value: d.EMA }));
    const EmaSeries = chart.addLineSeries({ color: 'red', lineWidth: 1 });
    EmaSeries.setData(EmaData);
    console.log(EmaData);
    console.log(smaData);
    const EmaData1 = cdata.map(d => ({ time: d.time, value: d.long }));
    console.log(EmaData1);
    const EmaData11 = cdata.map(d => ({ time: d.time, value: d.rsi }));
    console.log(EmaData11);

    // Set markers
    candleSeries.setMarkers(cdata.filter((d)=>d.long || d.short).map(d => {
      return d.long ? { time: d.time, position: 'belowBar', color: 'green', shape: 'arrowUp', text: 'LONG' } : { time: d.time, position: 'aboveBar', color: 'red', shape: 'arrowUp', text: 'short' };
    }));
    const rsi_series=chart.addLineSeries({
    color:'purple',
    linewidth:1,
    pane:1,

    });
    rsi_series.setData(EmaData11)
  })
  .catch(err => log(err));