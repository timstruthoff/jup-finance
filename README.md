# jup-finance

This app attempts to implement the [double-entry bookkeeping system](https://en.wikipedia.org/wiki/Double-entry_bookkeeping) using a relational data model.

## Disclaimer
- This is strictly a **work in progress**. Comments and documentation are incomplete and it's barely a prove of concept.
- I am currently using the (pretty awesesome) [YNAB](https://www.ynab.com/) app for keeping track of expenses but once I have enough free time again I am going to continue this project.

## Getting started

Start the MySQL Docker instance
```
docker run --name jup-finance-database -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:8
```

## Goals
- Keep the data readable; I want to be able to analyze the SQL tables using simple tools like Excel, so I try to minimize complexity in the database schema.

## Limitations
- No split-entries; It is not possible for one debit to go to multiple credits or vice versa. This limitation can be circumvented by using separate entries on both sides.

## Sources
- Great Stack Overflow Answer about implementing Double-Entry bookkeeping in relational data models: [Link](https://stackoverflow.com/questions/59432964/relational-data-model-for-double-entry-accounting)
- https://gist.github.com/NYKevin/9433376


## Better alternatives

- https://beancount.github.io/fava/
- https://beancount.github.io/
- https://github.com/flash-oss/medici
- And [many more](https://github.com/search?q=double+entry&type=repositories)...
