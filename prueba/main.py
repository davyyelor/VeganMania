import time
from flask import Flask, session, request, render_template
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysupersecretkey"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


def slow_loading_function(input_string: str):
    """Simulates a time consuming process (wait 10 seconds and return a reversed string)"""

    time.sleep(10)
    return input_string[::-1]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/loading", methods=["POST"])
def loading():
    if request.method == "POST":
        # We'll use a session object to save the data sent by the user for processing
        session["user_data"] = request.form.get("user_data")
        return render_template("loading.html")


@app.route("/results")
def results():
    # Finally, use the user data in some intensive process
    processed_data = slow_loading_function(session["user_data"])
    return render_template("results.html", processed_data=processed_data)


if __name__ == "__main__":
    app.run(debug=True)
