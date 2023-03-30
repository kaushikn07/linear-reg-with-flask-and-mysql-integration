from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from flask import Flask, render_template, request, session, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nani",
    database="users"
)

# Create a cursor object to execute MySQL queries
mycursor = mydb.cursor()

# Define routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if the username and password are valid
    mycursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
    account = mycursor.fetchone()

    if account:
        session['username'] = username
        return redirect('/dashboard')
    else:
        message = "Invalid username or password"
        return render_template('login.html', message=message)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect('/')

@app.route('/prediction', methods=['POST'])
def prediction():
    
    dataset = pd.read_csv("Salary_dataset.csv")
    # Separate the features and labels
    x = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=100)
    
    # Train the regression model
    regression_model = LinearRegression()
    regression_model.fit(X_train, y_train)

    
    # Make the prediction using the regression model
    result = regression_model.predict(X_test)[0]
    # Return the prediction result to a new HTML template called result.html
    return render_template('result.html', result=result)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True, host = 'localhost', port = 5000)
