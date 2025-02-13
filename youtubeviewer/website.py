"""
MIT License

Copyright (c) 2021-2023 MShawon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import calendar
import sqlite3
import warnings
from contextlib import closing
from datetime import date, datetime, timedelta

from flask import Flask, jsonify, render_template, request
from werkzeug.serving import run_simple

warnings.filterwarnings("ignore", category=Warning)

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

console = []
summary_table = ""
html_table = ""
database = "database.db"


def create_graph_data(dropdown_text):
    """Generate graph data based on dropdown selection."""
    now = datetime.now()
    today = now.date()
    query_days = []

    try:
        days = (
            int([int(s) for s in dropdown_text.split() if s.isdigit()][0])
            if "Last" in dropdown_text
            else None
        )
    except (ValueError, IndexError):
        days = None

    if days:
        query_days = [(today - timedelta(days=i)).isoformat() for i in range(days)]
        query_days.reverse()
    else:
        try:
            if " " in dropdown_text:
                month, year = dropdown_text.rsplit(" ", 1)
                month = MONTHS.index(month) + 1
                year = int(year)
            else:
                month = MONTHS.index(dropdown_text) + 1
                year = now.year
            num_days = calendar.monthrange(year, month)[1]
            query_days = [
                date(year, month, day).isoformat() for day in range(1, num_days + 1)
            ]
        except Exception as e:
            print(f"Error parsing dropdown text '{dropdown_text}': {e}")
            return [], 0, None, None

    graph_data = [["Date", "Views"]]
    total_views = 0

    try:
        with closing(sqlite3.connect(database, timeout=30)) as connection:
            with closing(connection.cursor()) as cursor:
                for query_date in query_days:
                    result = cursor.execute(
                        "SELECT view FROM statistics WHERE date = ?", (query_date,)
                    ).fetchone()
                    views = result[0] if result else 0
                    graph_data.append([query_date[-2:], views])
                    total_views += views
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    return graph_data, total_views, query_days[0], query_days[-1]


def create_dropdown_data():
    """Create dropdown data for the UI."""
    dropdown = ["Last 7 days", "Last 28 days", "Last 90 days"]
    now = datetime.now()
    current_year = now.year

    dropdown.append(now.strftime("%B"))

    for _ in range(12):
        now = now.replace(day=1) - timedelta(days=1)
        dropdown.append(
            now.strftime("%B %Y") if now.year < current_year else now.strftime("%B")
        )

    return dropdown


def shutdown_server():
    """Shut down the Flask server."""
    try:
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            # For newer versions of Werkzeug
            raise RuntimeError("Not running with Werkzeug Server")
        func()
    except Exception as e:
        print(f"Error shutting down server: {e}")


def start_server(host, port, debug=False):
    """Start the Flask server."""
    app = Flask(
        __name__,
        static_url_path="",
        static_folder="web/static",
        template_folder="web/templates",
    )

    @app.route("/")
    def home():
        dropdown = create_dropdown_data()
        return render_template("homepage.html", dropdownitems=dropdown)

    @app.route("/update", methods=["POST"])
    def update():
        return jsonify(
            {
                "result": "success",
                "console": console[:200],
                "summary": summary_table[8:-9],
                "table": html_table[8:-9],
            }
        )

    @app.route("/graph", methods=["GET", "POST"])
    def graph():
        if request.method == "POST":
            try:
                query = request.json.get("query")
                graph_data, total, first_date, last_date = create_graph_data(query)
                return jsonify(
                    {
                        "graph_data": graph_data,
                        "total": total,
                        "first": first_date,
                        "last": last_date,
                    }
                )
            except Exception as e:
                return jsonify({"error": f"Failed to generate graph: {e}"}), 500
        return jsonify({"error": "Invalid request method"}), 405

    @app.route("/shutdown", methods=["POST"])
    def shutdown():
        try:
            shutdown_server()
            return "Server shutting down..."
        except RuntimeError as e:
            return jsonify({"error": str(e)}), 500

    if debug:
        app.run(host=host, port=port, debug=debug)
    else:
        run_simple(host, port, app, threaded=True)


if __name__ == "__main__":
    start_server(host="0.0.0.0", port=5000, debug=True)
