# Deppentreff Stock Exchange

Not everyone has the capability to buy stock in a real stock exchange. 
This application is supposed to simulate buying and selling stocks. 


## Install the neccessary modules

- Install python
- pip install bs4
- pip install lxml
- pip install flask
- pip install Flask-SQLAlchemy
- pip install bcrypt
- pip install flask-migrate
- pip install python-dotenv

## Start the application

You can start the app with the following command

```
flask run
```

Then access the website by opening [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Database
When there is a change to the database structure, this change needs to be tracked using the Alembic framework.
After you made a change run:
```
flask db -migrate "description of the change"
```
and then apply this change by running
```
flask db upgrade
```