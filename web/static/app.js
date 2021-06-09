$(document).ready(function () {

    setInterval(function () {

        req = $.ajax({
            url: '/update',
            type: 'POST',
        });

        req.done(function (data) {

            var i;
            for (i = 1; i < 21; i++) {
                $('#logs-' + i).html(data.console[i - 1]);
            }
        });


    }, 10000);

});

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


$(document).ready(function () {
    req = $.ajax({
        url: '/graph',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ query: "Last 7 days" })
    });

    req.done(function (data) {
        graph(data['graph_data'], data['total'], data['first'], data['last'])

    });
});


$(".dropdown-menu a").click(function () {
    var selText = $(this).text();
    $(this).parents('.dropdown').find('.dropdown-toggle').html(selText);

    req = $.ajax({
        url: '/graph',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ query: selText })
    });

    req.done(function (data) {

        graph(data['graph_data'], data['total'], data['first'], data['last'])

    });
});