setInterval(async function () {
    const timeRange = document.getElementById('timeRangeSelect').value;
    // Append the time range to the URL
    const response = await fetch(`/monitoring/raw?time_range=${timeRange}`);
    if (!response.ok) return;

    const json_data = await response.json();
    
    for (let i = 0; i < json_data.length; i++) {
        const current_monitor = json_data[i];

        const elm = document.querySelector(`#monitor_frame_${current_monitor['id']}`);
        if (!elm) continue;


        // Assuming sensor_data is an array and you are interested in the first element
        if (current_monitor['sensor_data'] && current_monitor['sensor_data'].length > 0) {
            const sensorData = current_monitor['sensor_data'][0];

            // Make sure to use the correct property names here
            const xAxis = sensorData['x_axis']; // or whatever the correct property name is
            const yAxis = sensorData['y_axis']; // or whatever the correct property name is

            if (xAxis && yAxis) {
                // Update the chart
                const chart = charts[current_monitor['key']];

                chart.data.datasets[0].data = yAxis.map((y, index) => ({ x: xAxis[index], y: y }));
                chart.data.labels = xAxis;
                chart.update();
            }
        }
    }
}, 8000);
