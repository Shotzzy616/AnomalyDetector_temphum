let myChart; // Declare the chart variable globally

function fetchWeatherData() {
    $.ajax({
        url: '/latest_data',
        method: 'GET',
        success: function(data) {
            const time = data.Timestamp;
            const temperature = data['Temperature (°C)'];
            const humidity = data['Humidity (%)'];
            const lpg = data['lpg'];
            const co = data['co'];
            const smoke = data['smoke'];
            const prediction = data.Prediction;

            $('#temperature').text(temperature);
            $('#humidity').text(humidity);
            $('#lpg').text(lpg);
            $('#co').text(co);
            $('#smoke').text(smoke);
            $('#prediction').text(prediction === 1 ? 'Normal' : 'Anomaly');
        },
        error: function() {
            $('#weather-data').html('<strong>Error fetching data.</strong>');
        }
    });
}

$(document).ready(function() {
    fetchWeatherData(); // Initial fetch
    setInterval(fetchWeatherData, 5000);  // Fetch data every 5 seconds

    // Event listener for list-group-item clicks
    $('.graph-btn').click(function () {
        const type = $(this).data('type');
        fetchData(type);
    });

    function fetchData(type) {
        $.get('/get_data', function (data) {
            const labels = data.map(item => item.Timestamp);
            const values = data.map(item => item[type]);

            // Show the chart and render it
            $('#myChart').show();
            renderChart(labels, values, type);
        });
    }

    function renderChart(labels, data, label) {
        // Destroy the previous chart if it exists
        if (myChart) {
            myChart.destroy();
        }

        const ctx = document.getElementById('myChart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
