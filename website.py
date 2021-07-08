import calendar
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta

from flask import Flask, jsonify, render_template, request

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

global console
console = []
database = 'database.db'


def create_graph_data(dropdown_text):
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    today = now.date()
    days = False
    number = False
    try:
        number = [int(s) for s in dropdown_text.split() if s.isdigit()][0]
    except:
        pass

    if number:
        if dropdown_text.startswith('Last'):
            days = number
        else:
            month = MONTHS.index(dropdown_text[:-5]) + 1
            year = number
    else:
        month = MONTHS.index(dropdown_text) + 1

    query_days = []

    if days:
        for i in range(days):
            day = today - timedelta(days=i)
            query_days.append(str(day))
        query_days.reverse()

    else:
        num_days = calendar.monthrange(year, month)[1]
        for day in range(1, num_days+1):
            query_days.append(str(date(year, month, day)))

    first_date = query_days[0]
    last_date = query_days[-1]

    graph_data = [['Date', 'Views']]
    total = 0

    try:
        with closing(sqlite3.connect(database, timeout=30)) as connection:
            with closing(connection.cursor()) as cursor:
                for i in query_days:
                    view = cursor.execute(
                        "SELECT view FROM statistics WHERE date = ?", (i,),).fetchall()
                    if view:
                        graph_data.append([i[-2:], view[0][0]])
                        total += view[0][0]
                    else:
                        graph_data.append([i[-2:], 0])
    except:
        pass

    return graph_data, total, first_date, last_date


def create_dropdown_data():
    dropdown = ['Last 7 days', 'Last 28 days', 'Last 90 days']
    now = datetime.now()
    current_year = now.year
    dropdown.append(now.strftime("%B"))

    for _ in range(0, 12):
        now = now.replace(day=1) - timedelta(days=1)
        if current_year == now.year:
            dropdown.append(now.strftime("%B"))
        else:
            dropdown.append(now.strftime("%B %Y"))

    return dropdown


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def start_server(host, port):
    app = Flask(__name__,
                static_url_path='',
                static_folder='web/static',
                template_folder='web/templates')

    @app.route('/')
    def home():
        dropdown = create_dropdown_data()
        return render_template('homepage.html', dropdownitems=dropdown)

    @app.route('/update', methods=['POST'])
    def update():
        return jsonify({'result': 'success', 'console': console[-20:]})

    @app.route('/graph', methods=['GET', 'POST'])
    def graph():
        query = None
        if request.method == 'POST':
            query = request.json['query']
            graph_data, total, first_date, last_date = create_graph_data(query)

            return jsonify({
                'graph_data': graph_data,
                'total': total,
                'first': first_date,
                'last': last_date
            })

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        shutdown_server()
        return 'Server shutting down...'

    app.run(host=host, port=port)


if __name__ == '__main__':
    start_server(host='0.0.0.0', port=5000)
