from flask import render_template, url_for, request, redirect, make_response
from app import app
from flask import jsonify

from app import dbHandler

@app.route("/stock", methods = ["POST"])
def add_stock():

    company_name = request.form.get("company_name", False)
    current_value = request.form.get("current_value", False)
    error = None


    if not company_name:
        error = "company_name is required."
    elif not current_value:
        error = "current_value is required."

    if error is None:
        stock = dbHandler.add_stock(company_name, current_value)

        
        return jsonify(stock)
    
    return jsonify(error)

@app.route("/stock", methods = ["GET"])
def get_stocks():

    stock_id = request.form.get("id", False)
    error = None
    
    if not stock_id:
        return jsonify(dbHandler.get_all_stocks())
    else:
        return jsonify()