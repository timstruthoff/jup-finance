CREATE TABLE User (
    userID integer (4) UNIQUE NOTNULL,
    username varchar (20) DEFAULT 'User' NOTNULL,
    email varchar (50) UNIQUE NOTNULL,
    password varchar (50) NOTNULL,
    PRIMARY KEY (userID)
)
CREATE TABLE Transactions (
   transactionID integer (4) UNIQUE NOTNULL,
   type {buy|sell} NOTNULL,
   timestamp CURRENT_TIMESTAMP NOTNULL,
   FOREIGN KEY (userID) REFERENCES User(userID),
   FOREIGN KEY (stockID) REFERENCES Stock(stockID),
   PRIMARY KEY (transactionID)
)
CREATE TABLE UserCapital (
  id integer (4) UNIQUE NOTNULL,
  balance decimal (6.2) default '1000.00' NOTNULL,
  stockassets decimal (6.2) default '0.00' NOTNULL,
  FOREIGN KEY (userID) REFERENCES User(userID),
  PRIMARY KEY (id)
)
CREATE TABLE Stock (
  stockID integer (4) UNIQUE NOTNULL,
  company_name varchar (50) NOTNULL,
  current_value decimal (6.2),
  changerate decimal (1.4), 
  PRIMARY KEY (stockID)
)
CREATE TABLE StockValue (
  timestamp CURRENT_TIMESTAMP NOTNULL,
  FOREIGN KEY (stockID) REFERENCES Stock(stockID),
  value decimal (6.2) NOTNULL,
  CONSTRAINT name UNIQUE (timestamp, stockID),
  PRIMARY KEY (timestamp, stockID)
)
CREATE TABLE StockShare (
  shareID integer (4) UNIQUE NOTNULL,
  shareamount integer DEFAULT '0' NOTNULL,
  FOREIGN KEY (stockID) REFERENCES Stock(stockID),
  FOREIGN KEY (userID) REFERENCES User(userID),
  PRIMARY KEY (shareID)
)
CREATE TABLE StockShareValue (
  valueID integer (4) UNIQUE NOTNULL,
  sharevalue decimal (6.2) DEFAULT '0.00' NOTNULL,
  FOREIGN KEY (shareID) REFERENCES StockShare(shareID),
  FOREIGN KEY (stockID) REFERENCES Stock(stockID),
  FOREIGN KEY (capitalID) REFERENCES UserCapital(capitalID),
  PRIMARY KEY (valueID)
)