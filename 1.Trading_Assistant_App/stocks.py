#STOCK VALUE AI PREDICTOR
#REQUIRES UNDERLYING MYSQL DB - ALTER CREDENTIALS IN QUERY_DB AND UPDATE_DB FUNCTIONS AS NEEDED
#HTML TEMPLATES REQUIRED, SHOULD BE PUT IN FOLDER ALONGSIDE PYTHON FILE /TEMPLATES/*

#------------------------------------------------
#GENERAL CODE
#------------------------------------------------
#-----SHARED LIBRARIES-----
import pandas as pd 
import datetime
import mysql.connector
import warnings
#-----SHARED FUNCTIONS/CODE-----
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARMA',
                        FutureWarning)
warnings.filterwarnings('ignore', 'statsmodels.tsa.arima_model.ARIMA',
                        FutureWarning)

#-----CORE FUNCTIONS FOR SQL ACCESS-----
#Function to read data from database
def query_db(query):
    db = mysql.connector.connect(
        host="INSERT IP",
        user="INSERT USER",
        password="INSERT PASSWORD",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return(result)

#Function to write data to database
def update_db(query):
    db = mysql.connector.connect(
        host="INSERT IP",
        user="INSERT USER",
        password="INSERT PASSWORD",
        database="financial_data"
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

#------------------------------------------------
#AI MODELLING/PREDICTOR CODE
#------------------------------------------------
#-----LIBRAIRES FOR AI MODELLING/PREDICTOR-----
import numpy as np 
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

#-----RETURN ACTIVE PRODUCTS-----
def active_products(target_date):
    query = "SELECT product FROM product_values WHERE record_date = '{}'"
    query = query.format(target_date)
    results = query_db(query)
    return(results)

#-----DATA PULL-----
def data_pull(product_id, date):
    query = "SELECT product, record_date , close_value, open_value FROM product_values WHERE product = {} AND record_date < '{}' ORDER BY record_date ASC"
    query = query.format(str(product_id), date)
    raw_results = query_db(query)
    df = pd.DataFrame(columns = ["product", "record_date", "close_value", "open_value"])
    for row in raw_results:
        df = df.append(pd.Series([row[0], row[1], row[2], row[3]], index = df.columns), ignore_index = True)
    return(df)

#-----PREDICT NEXT DAY VALUE-----
def predict_next_day(product, date):
    df = data_pull(product, date)
    count = 1
    df["open_value"].plot()
    training_data = []
    while (count < df.shape[0]):
        training_data = training_data + [df.loc[count, "open_value"],]
        count = count + 1
    model = ARIMA(training_data, order=(4, 1, 1))
    fitted_model = model.fit()
    prediction = fitted_model.forecast()[0][0]
    prediction = round(prediction, 2)
    return(prediction)

#-----GENERATE HIGHLIGHTS-----
def generate_highlights(date):
    products = active_products(date)
    query = "SELECT open_value FROM product_values WHERE product = {} AND record_date = '{}'"
    products_with_return = ()
    for product in products:
        prediction = predict_next_day(product, date)
        query_result = query_db((query.format(product, date)))
        value = None
        for item in query_result:
            value = item[0]
        profit = prediction - value
        print(profit)
        if(profit > 0):
            products_with_return = products_with_return + ((product, profit))
    return(products_with_return)

#------------------------------------------------
#FLASK WEB APP CODE
#------------------------------------------------

#-----LIBRARIES FOR FLASK-----
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, PasswordField, HiddenField, DateField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional
from waitress import serve

#Establish flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "ASDSDFDFGHFGJHJKL"
bootstrap = Bootstrap(app)

#-----FLASK SPECIFIC FUNCTIONS-----
def select_values(table, value):
    query = 'SELECT id, {} FROM {} ORDER BY {} ASC'
    query = query.format(value, table, value)
    results = query_db(query)
    options = []
    for row  in results:
        tup = [(row[0], row[1])]
        options = options + tup
    return(options)

def message_build (statement, var):
    string = "{}: {} \n"
    string = string.format(statement, var)
    return(string)

#-----SET FORMS FOR PAGES-----

#Form to provide return to dashboard button
class ReturnDashboardForm(FlaskForm):
    dashboard_return= SubmitField("Return to Dashboard")

#Form for stock query page
class StockQueryForm(FlaskForm):
    product = StringField("Product")
    submit = SubmitField("Find Product Details")

#Form for stock calculator
class StockCalculatorForm(FlaskForm):
    desired_total_return = DecimalField("Total Profit", validators=[Optional()])
    number_shares = IntegerField("Given Number of shares", validators=[Optional()])
    investment = DecimalField("Investment", validators=[Optional()])
    submit = SubmitField("Calculate")

#-----PAGES-----
#LOGIN PAGE
@app.route('/')
def login():
    return redirect(url_for('home'))

#HOMEPAGE
@app.route('/home', methods=["GET","POST"])
def home():
    form = StockQueryForm()
    if form.validate_on_submit():
        product = str(form.product.data)
        query = "SELECT product.id, product_name, financial_exchange.exchange_name, start_date, end_date FROM product LEFT JOIN financial_exchange ON product.financial_exchange = financial_exchange.id WHERE product_name LIKE '%{}%' "
        query = query.format(product)
        session["query"] = query
        return redirect(url_for('stock_results'))
    #Render homepage based on index_form.html template
    return render_template("index_form.html", heading="Homepage", form=form, messages="Welcome to the SolFinTech next day trader system! \n This AI augmented system is designed to allow traders to make next day trades with minimal risk due to AI prediction of product values. \n Search for a stock code to get started:")

#PREDICT BASED ON STOCK
@app.route('/stock_predict', methods=["GET","POST"])
def stock_predict():
    form = StockQueryForm()
    if form.validate_on_submit():
        product = str(form.product.data)
        query = "SELECT product.id, product_name, financial_exchange.exchange_name, start_date, end_date FROM product LEFT JOIN financial_exchange ON product.financial_exchange = financial_exchange.id WHERE product_name LIKE '%{}%' "
        query = query.format(product)
        session["query"] = query
        return redirect(url_for('stock_results'))
    return render_template("index_form.html", form=form, heading="Specific Stock Prediction", messages="Please enter a stock code below to search for a product:")

#STOCK SEARCH RESULTS
@app.route('/stock_results', methods=["GET","POST"])
def stock_results():
    #Pull in variables
    query = session["query"]
    print(query)
    data = query_db(query)
    data_tuple = []
    for row in data:
        new_tuple = [(str(row[1]), str(row[2]), str(row[3]), str(row[4]), "/stock_prediction/id-" + str(row[0]) + ";Predict Tomorrows Value")]
        data_tuple = data_tuple + new_tuple
    heading_tuple = ("Product Name", "Financial Exchange", "Earliest Date", "Most Recent Date", "")
    return render_template("table_button.html", heading="Stocks Search Results", table_headings=heading_tuple, data_collection=data_tuple)

#STOCK NEXT DAY PREDICTION
@app.route('/stock_prediction/id-<id>', methods=["GET","POST"])
def stock_prediction(id):
    form = StockCalculatorForm()
    today = datetime.datetime(2020, 11, 25)
    today_query = "SELECT open_value FROM product_values WHERE product = {} AND record_date = '{}'"
    today_query = today_query.format(id, today.strftime("%Y-%m-%d"))
    raw_today_value = query_db(today_query)
    for row in raw_today_value:
        today_value = float(row[0])
    predicted_value = predict_next_day(id, today.strftime("%Y-%m-%d"))
    profit = round((predicted_value - today_value),2)
    tup = ["Today's Value", "Tomorrow's Predicted Value", "Return"]
    row = ((str(today_value)), (str(predicted_value)), (str(profit)) + " Per share")
    counter = 0
    message = ""
    while(counter < 3):
        message = message + message_build(tup[counter], row[counter])
        counter = counter + 1
    message = message.split('\n')
    if form.validate_on_submit():
        try:
            desired_profit = float(form.desired_total_return.data)
        except:
            desired_profit = ""
        try:
            number_of_shares = int(form.number_shares.data)
        except:
            number_of_shares = ""
        try:
            investment = float(form.investment.data)
        except:
            investment = ""
        if((desired_profit == "") and (number_of_shares == "")):
            no_shares = round(investment / today_value)
            rate_profit = round((no_shares * profit), 2)
            session["calculations"] = (("Number of shares owned", no_shares), ("Return on shares owned", rate_profit))
        elif((investment == "") and (desired_profit == "")):
            rate_profit = round((number_of_shares * profit), 2)
            value_of_shares = round((number_of_shares * today_value), 2)
            session["calculations"] = (("Return on shares owned", rate_profit), ("Value of shares owned at todays price", value_of_shares))
        elif((investment == "") and (number_of_shares == "")):
            no_shares_required = round(desired_profit / profit)
            investment_required = round((no_shares_required * today_value),2)
            session["calculations"] = (("No. of Shares required", no_shares_required), ("Cost of investment", investment_required))
        return (redirect('/calculation_details/id-' + str(id)))
    return render_template("index_multiline_button_form.html", heading="Stock Predictions", messages=message, form=form, link='/stock_results', button_text="Return to Search Results")

#CALCULATION DETAILS
@app.route('/calculation_details/id-<id>', methods=["GET","POST"])
def calculation_details(id):
    calculation_results = session["calculations"]
    session["calculations"] = None
    message = ""
    for item in calculation_results:
        message = message + message_build(item[0], item[1])
    message = message.split('\n')
    return render_template("index_multiline_button.html", heading="Calculation Results", messages=message, link="/stock_prediction/id-" + str(id), button_text="Return to stock details")

serve(app, host="0.0.0.0", port=8080, threads=1)