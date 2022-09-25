// google chart area graph function
function graph(chart_data, total, first, last) {
    google.charts.load('current', { 'packages': ['corechart'] });
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable(chart_data);

        var options = {
            title: 'Generated Views : ' + total + '\n ' + first + ' to ' + last,
            hAxis: { title: 'Date', titleTextStyle: { color: '#333' } },
            vAxis: { minValue: 0 },
            legend: { position: 'none' }
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }
}


// get graph data from python
function queryGraphData(text) {
    req = $.ajax({
        url: '/graph',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ query: text })
    });

    req.done(function (data) {
        graph(data['graph_data'], data['total'], data['first'], data['last'])

    });
}


// get console outputs from python
function queryLogs() {
    req = $.ajax({
        url: '/update',
        type: 'POST',
    });

    req.done(function (data) {
        var i;
        for (i = 1; i < 201; i++) {
            $('#logs-' + i).html(data.console[i - 1]);
        }
        $('#summary_table').html(data.summary);
        $('#video_statistics').html(data.table);
    });
}


// update python logs on page load
$(document).ready(function () {
        queryLogs()
});


// update python logs every 10 seconds
$(document).ready(function () {
    setInterval(function () {
        queryLogs()
    }, 10000);
});


// draw graph on page load for last 7 days
$(document).ready(function () {
    queryGraphData('Last 7 days');
});


// update graph every 5 minutes
$(document).ready(function () {
    setInterval(function () {
        var selText = $('#dropdownMenuButton').text();

        queryGraphData(selText);
    }, 300000);
});


// change graph according to drop down data selected by user
$(".dropdown-menu a").click(function () {
    var selText = $(this).text();
    $(this).parents('.dropdown').find('.dropdown-toggle').html(selText);

    queryGraphData(selText);
});