# Flask App with Loading Message & Animation

This is a simple Flask app that demonstrates how to display a „loading...” message and/or a spinning graphic while a time-consuming function is executed. The purpose of this is to provide users with feedback while they wait for a process to complete. 

This app has the advantage of not requiring the use of AJAX to display a loading message or spinning graphic. Instead, it leverages the Flask session object to store the user's data while the time-consuming function is executed, and uses Jinja2 templates to display the loading message and/or spinning graphic. This approach simplifies the implementation of the loading feedback and avoids the added complexity of asynchronous requests using AJAX.

## The app has three routes

| Route | Explanation |
| ----- | ----------- |
| / | the home route, which displays a simple form for the user to enter data. |
| /loading | this route is triggered when the user submits the form. It saves the data entered by the user to a session object and displays a loading screen. |
| /results | this route displays the results of the slow loading function applied to the user's data. |

## Dependencies

This app requires the following dependencies:

- Flask
- Flask-Session

## Installation

To install the dependencies, you can use pip:

```text
pip install flask flask-session
```

or:

```text
pip install -r requirements.txt
```

## Running the App

To run the app, navigate to the directory containing the app.py file and run the following command:

```text
python app.py
```

This will start a local web server on <http://localhost:5000>. You can access the app by navigating to this URL in your web browser.

## Notes

- The slow loading function slow_loading_function() is defined at the top of the file. It takes an input string and simulates a time-consuming process by waiting 10 seconds before returning the reversed input string.
- The Flask app is defined below the slow loading function. It uses Flask-Session to save the user's data to a session object and displays a loading message using Jinja2 templates while the slow loading function is executing.
- There are three templates included: index.html for the home page, loading.html for the loading screen, and results.html for the results page.
- The app.run(debug=True) line at the bottom of the file tells Flask to run the app in debug mode, which provides helpful error messages during development. You should remove this line when running the app in production.
