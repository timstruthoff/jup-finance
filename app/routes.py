from flask import render_template, url_for, request, redirect, make_response
from app import app
from flask import jsonify

from app import dbHandler

@app.route("/", methods = ["POST", "GET"])
def index():
    """
        desc:
            - this function contains the login functionality
            - checks login data with the db using dbHandler
            - connected to index.html using Flask
        param:
            - email: email of the user (requested)
            - password: password of the user (requested)
            - user: key to access user information
            - message: error/confirmation messages
        return:
            - login website (first site)
            - if login is successful: redirects to /dashboard
    """

    #return render_template('dashboard.html', stocksDataList = db.get_stocks_data())
    if request.method == "POST":
        email = str(request.form.get("email", False))
        password = str(request.form.get("password", False))

        user = None

        try:
            user = dbHandler.check_login_password(email, password)
        except Exception as error:
            return render_template(
                "index.html", 
                message = {
                    "type": "error",
                    "text": error
                }
            )

        if user != None:
            session = dbHandler.create_session(user)

            response = make_response(redirect(url_for("dashboard")))
            print(session)
            response.set_cookie("session", session.id)
            return response

    return render_template("index.html", message = None)



@app.route("/register", methods = ["POST", "GET"])
def register():
    """
        desc:
            - this function contains the register functionality
            - creates new user in db using dbHandler
            - connected to register.html using Flask
        param:
            - email: email of the user (requested)
            - password: password of the user (requested)
            - name: username (requested)
            - message: error/confirmation messages
        return:
            - register website
            - if register is successfull: redirects to /dashboard
    """
    
    # If user sends a get request to register url, return the register template including an html form
    if request.method == "GET":
        return render_template("register.html")

    # If user sends a post request, they are trying to add a new user. This data needs to be added to the database
    elif request.method == "POST":
        email = request.form.get("email", False)
        password = request.form.get("password", False)
        name = request.form.get("name", False)
        print ("email:" + str(email))
        print ("password:" + str(password))
        print ("name:" + str(name))
        error = None


        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        elif not name:
            error ="Name is required."
        elif dbHandler.get_user_by_email(email) != None:
            error = "User {} is already registered.".format(password)
            # TODO Render Error

        if error is None:
            user = dbHandler.add_user(name, email, password)

            session = dbHandler.create_session(user)

            response = make_response(redirect(url_for("dashboard")))
            response.set_cookie("session", session.id)
            return response
    
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    """
        desc:
            - this function contains the dashboard functionality
            - connected to dashboard.html using Flask
            - integrates the navbar thorugh the html file
            - can be triggered using navbar
        param:
            - session_id: id for user to access without having to login every execution
            - session_valid: checks if session_id is valid using dbHandler
            - user: key to access user information
            - user_key_figures: contains the figures of a specific user (read out of db using dbHandler)
            - stocksDataList: contains all stocks data
            - message: error/confirmation messages
            - totals assets: equity + assets --> equity value if the user would sell all of his stocks now
            - equity: equity of the user
            - assets: stock assets of the user
            - profit: assets + equity - StartEquity(10.000) --> profit the user would make if he would sell all of his stocks now
            - current_yield: return on capital
        return:
            - dashboard website (main site when logged in)
            - redirects using navbar buttons
    """

    # Session Handling
    session_id = request.cookies.get("session")
    print(f"session: {session_id}")
    session_valid = dbHandler.check_session(session_id)
    
    if not session_valid:
        return redirect(url_for("index"))        

    user = dbHandler.get_user_from_session(session_id)
    if user == None:
        return redirect(url_for("index"))   

    print(f"User {user.username} logged in")

    user_key_figures = dbHandler.get_user_key_figures(user)

    return render_template(
        "dashboard.html", 
        stocksDataList = dbHandler.get_stocks_data(),
        message = None,
        total_assets = user_key_figures["total_assets"],
        equity = user_key_figures["equity"],
        assets = user_key_figures["assets"],
        profit = user_key_figures["profit"],
        current_yield = user_key_figures["current_yield"],
    )



@app.route("/buy", methods = ["POST", "GET"])
def buy():
    """
        desc:
            - this function contains the buy functionality
                - buy button next to each available stock
                - amount field in table header
            - connected to buy.html using Flask
            - integrates the navbar thorugh the html file
            - can be triggered using navbar
        param:
            - session_id: id for user to access without having to login every execution
            - session_valid: checks if session_id is valid using dbHandler
            - user: key to access user information
            - stock_wkn: wkn of the stock that the user want's to be bought
            - amount: how many stocks the user want's to buy
            - stock: contains information about a specific stock
            - user_key_figures: contains the figures of a specific user (read out of db using dbHandler)
            - stocksDataList: contains all stocks data
            - message: error/confirmation messages
            - userStocks: contains all stocks data of the stocks the user has bought
            - equity: equity of the user
            - assets: stock assets of the user
            - profit: assets + equity - StartEquity(10.000) --> profit the user would make if he would sell all of his stocks now
        return:
            - buy website
            - refreshes website after transaction (updates values according to transaction)
            - redirects using navbar buttons
    """

    # Session Handling
    session_id = request.cookies.get("session")
    print(f"session: {session_id}")
    session_valid = dbHandler.check_session(session_id)
    if not session_valid:
        return redirect(url_for("index"))        

    user = dbHandler.get_user_from_session(session_id)
    if user == None:
        return redirect(url_for("index"))   

    print(f"User {user.username} logged in")

    message = None
    
    # runs buy screen
    if request.method == "POST":
        stock_wkn = request.form["name"]
        amount = int(request.form["amount"])

        print(f"wkn: {stock_wkn}, amount: {amount}, user: {user.username}")

        
        message = None

        try:

            stock = dbHandler.get_stock(stock_wkn)

            print(f"Stock: {stock}")

            if stock == None:
                raise Exception(f"The stock with the wkn number {stock_wkn} was not found in the database!")
            
            dbHandler.buy_stock(user, stock, amount)

        except Exception as buying_error:
            message = {
                "type": "error",
                "text": buying_error
            }
        else:
            message = {
                "type": "success",
                "text": f"Successfully bought {amount} stock of {stock.company_name}"
            }


    user_key_figures = dbHandler.get_user_key_figures(user)

    return render_template(
        "buy.html", 
        stocksDataList = dbHandler.get_stocks_data(), 
        message = message, 
        userStocks = dbHandler.get_users_stocks(user),
        equity = user_key_figures["equity"],
        assets = user_key_figures["assets"],
        profit = user_key_figures["profit"]
    )


@app.route("/sell", methods = ["POST", "GET"])
def sell():
    """
        desc:
            - this function contains the sell functionality
                - sell button next to each available stock
                - amount field in table header
            - connected to sell.html using Flask
            - integrates the navbar thorugh the html file
            - can be triggered using navbar
        param:
            - session_id: id for user to access without having to login every execution
            - session_valid: checks if session_id is valid using dbHandler
            - user: key to access user information
            - stock_wkn: wkn of the stock that the user want's to be sold
            - amount: how many stocks the user want's to sell
            - stock: contains information about a specific stock
            - message: error/confirmation messages
            - user_key_figures: contains the figures of a specific user (read out of db using dbHandler)
            - userStocks: contains all stocks data of the stocks the user has bought
            - equity: equity of the user
            - assets: stock assets of the user
            - profit: assets + equity - StartEquity(10.000) --> profit the user would make if he would sell all of his stocks now
        return:
            - sell website
            - refreshes website after transaction (updates values according to transaction)
            - redirects using navbar buttons
    """

    # Session Handling
    session_id = request.cookies.get("session")
    print(f"session: {session_id}")
    session_valid = dbHandler.check_session(session_id)
    if not session_valid:
        return redirect(url_for("index"))        

    user = dbHandler.get_user_from_session(session_id)
    if user == None:
        return redirect(url_for("index"))   

    print(f"User {user.username} logged in")

    message = None

    # For POST requests execute the request contents
    if request.method == "POST":
        # session.permanent=True
        stock_wkn = request.form["name"]
        amount = int(request.form["amount"])

        print(f"wkn: {stock_wkn}, amount: {amount}")

        message = None

        try:

            stock = dbHandler.get_stock(stock_wkn)

            print(f"Stock: {stock}")

            if stock == None:
                raise Exception(f"The stock with the wkn number {stock_wkn} was not found in the database!")
            
            dbHandler.sell_stock(user, stock, amount)

        except Exception as buying_error:
            message = {
                "type": "error",
                "text": buying_error
            }
        else:
            message = {
                "type": "success",
                "text": f"Successfully sold {amount} stock of {stock.company_name}"
            }
            
    user_key_figures = dbHandler.get_user_key_figures(user)

    # For GET requests just return the selling page without doing anything
    return render_template(
        "sell.html", 
        userStocks = dbHandler.get_users_stocks(user), 
        message = message,
        equity = user_key_figures["equity"],
        assets = user_key_figures["assets"],
        profit = user_key_figures["profit"]
    )


@app.route("/history")
def history():
    """
        desc:
            - this function contains the history functionality
                - contains all transactions sorted by date and time of execution
            - connected to history.html using Flask
            - integrates the navbar thorugh the html file
            - can be triggered using navbar
        param:
            - session_id: id for user to access without having to login every execution
            - session_valid: checks if session_id is valid using dbHandler
            - user: key to access user information
            - user_key_figures: contains the figures of a specific user (read out of db using dbHandler)
            - userHistory: contains all transactions the user has executed
            - equity: equity of the user
            - assets: stock assets of the user
            - profit: assets + equity - StartEquity(10.000) --> profit the user would make if he would sell all of his stocks now
        return:
            - history website
            - redirects using navbar buttons
    """

    # Session Handling
    session_id = request.cookies.get("session")
    print(f"session: {session_id}")
    session_valid = dbHandler.check_session(session_id)
    if not session_valid:
        return redirect(url_for("index"))        

    user = dbHandler.get_user_from_session(session_id)
    if user == None:
        return redirect(url_for("index"))   

    print(f"User {user.username} logged in")

    user_key_figures = dbHandler.get_user_key_figures(user)

    # runs history screen
    return render_template(
        "history.html", 
        userHistory = dbHandler.get_user_history(user),
        equity = user_key_figures["equity"],
        assets = user_key_figures["assets"],
        profit = user_key_figures["profit"]
    )


@app.route("/logout")
def logout():
    """
        desc:
            - this function contains the logout functionality
            - can be triggered using navbar
        param:
            - response: contains redirect functionality to /index
        return:
            - redirects to login / index()
            - logs out user (makes session expire)
    """
    # logs out of the application 
    response = make_response(redirect(url_for('index')))
    response.set_cookie('session', '', expires=0)
    return response

@app.route("/reset")
def reset():
    """
        desc:
            - this function contains the reset functionality
                - set's all user related values back to start values
            - can be triggered using navbar
        param:
            - session_id: id for user to access without having to login every execution
            - session_valid: checks if session_id is valid using dbHandler
            - user: key to access user information
        return:
            - redirects to /dashboard
    """
    # Session Handling
    session_id = request.cookies.get("session")
    print(f"session: {session_id}")
    session_valid = dbHandler.check_session(session_id)
    if not session_valid:
        return redirect(url_for("index"))        

    user = dbHandler.get_user_from_session(session_id)
    if user == None:
        return redirect(url_for("index"))   

    print(f"User {user.username} logged in")

    dbHandler.reset_user(user)
    return redirect(url_for("dashboard"))

@app.route("/api/stocks")
def stocks_api():
    """
        desc:
            - This function provides a REST JSON API for getting current stocks information
        return:
            - redirects to /dashboard
    """
    return jsonify(dbHandler.get_stocks_data())

@app.route("/api/user/key-figures")
def user_key_figure_api():
    """
        desc:
            - This function provides a REST JSON API for getting current user key figures
    """

    # Session Handling
    session_id = request.cookies.get("session")
    print(f"session: {session_id}")
    session_valid = dbHandler.check_session(session_id)
    if not session_valid:
        return jsonify({})  

    user = dbHandler.get_user_from_session(session_id)
    if user == None:
        return jsonify({})  

    return jsonify(dbHandler.get_user_key_figures(user))