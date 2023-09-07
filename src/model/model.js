import mysql from 'mysql2/promise'
import * as fs from "fs"

export default class Model {

    databaseConnection;

    constructor() {
        console.log("Plaid")
        this.start.bind(this)
    }

    async start() {

        console.log('Starting server')
        this.databaseConnection = await mysql.createConnection({
            host: process.env.MYSQL_DATABASE_HOST,
            user: process.env.MYSQL_DATABASE_USER,
            password: process.env.MYSQL_DATABASE_PASSWORD
        });
        console.log('Server started')
        
        await this.createDatabase();
        await this.createTables();
    }

    async createDatabase() {
        console.log("Creating Database")
        await this.databaseConnection.execute(`CREATE DATABASE IF NOT EXISTS ${process.env.MYSQL_DATABASE_DATABASE_NAME}`)
        await this.databaseConnection.end()
        this.databaseConnection = await mysql.createConnection({
            host: process.env.MYSQL_DATABASE_HOST,
            user: process.env.MYSQL_DATABASE_USER,
            password: process.env.MYSQL_DATABASE_PASSWORD,
            database: process.env.MYSQL_DATABASE_DATABASE_NAME
        });

    }

    async createTables() {
        console.log('Creating Tables')
        await this.databaseConnection.execute(`CREATE TABLE IF NOT EXISTS transactions (
            id MEDIUMINT NOT NULL AUTO_INCREMENT,
            description MEDIUMTEXT,
            amount DOUBLE,
            datetime DATETIME,
            debit_account_id MEDIUMINT NOT NULL,
            credit_account_id MEDIUMINT NOT NULL,
            PRIMARY KEY (id)
        )`)

        await this.databaseConnection.execute(`CREATE TABLE IF NOT EXISTS plaid_transactions (
            id MEDIUMINT NOT NULL AUTO_INCREMENT,
            plaid_transaction_id TEXT,
            account_id TEXT,
            amount DOUBLE,
            authorized_datetime DATETIME,
            category TEXT,
            datetime DATETIME,
            iso_currency_code TEXT,
            name TEXT,
            payment_channel TEXT,
            personal_finance_category TEXT,
            PRIMARY KEY (id)
        )`)

        await this.databaseConnection.execute(`CREATE TABLE IF NOT EXISTS transactions_plaid_transactions_relation (
            transaction_id MEDIUMINT NOT NULL,
            plaid_transaction_id MEDIUMINT NOT NULL,
            PRIMARY KEY (transaction_id, plaid_transaction_id),
            FOREIGN KEY (transaction_id) REFERENCES transactions(id),
            FOREIGN KEY (plaid_transaction_id) REFERENCES plaid_transactions(id)
        )`)
    }

    async createTransaction({description, amount, datetime, debit_account_id, credit_account_id}) {
        const [results, fields] = await this.databaseConnection.execute(
            'INSERT INTO transactions (description, amount, datetime, debit_account_id, credit_account_id) VALUES (?, ?, ?, ?, ?)',
            [description, amount, datetime, debit_account_id, credit_account_id]
        )

        return results;
    }

    async createPlaidTransaction({
        transactionId, 
        accountId, 
        amount, 
        authorizedDatetime, 
        category, 
        datetime, 
        isoCurrencyCode, 
        name, 
        paymentChannel, 
        personalFinanceCategory
    }) {
        const [results, fields] = await this.databaseConnection.execute(
            `INSERT INTO plaid_transactions (
                plaid_transaction_id,
                account_id,
                amount,
                authorized_datetime,
                category,
                datetime,
                iso_currency_code,
                name,
                payment_channel,
                personal_finance_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                transactionId, 
                accountId, 
                amount, 
                authorizedDatetime, 
                category, 
                datetime, 
                isoCurrencyCode, 
                name, 
                paymentChannel, 
                personalFinanceCategory
            ]
        )

        return results;
    }

    async getLast20Transactions() {
        let [rows, fields] = await this.databaseConnection.execute(`SELECT * FROM transactions
        ORDER BY datetime DESC
        LIMIT 20`)
        return rows;
    }

    async closeDatabase() {
        await this.databaseConnection.close()
    }
}