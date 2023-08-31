import sqlite3 from 'sqlite3'
import { open } from 'sqlite'
import * as fs from "fs"

export default class Model {

    db;

    constructor() {
        console.log("Plaid")
        this.start.bind(this)
    }

    async start() {
        this.db = await open({
            filename: process.env.DATABASE_FILE_LOCATION,
            driver: sqlite3.Database
        })

        await this.createTables();
    }

    async createTables() {
        await this.db.exec(`CREATE TABLE transactions (
            value REAL, 
            datetime TEXT,
            name TEXT,
            plaid_account_id TEXT,
            plaid_category TEXT,
            plaid_currency TEXT,
            plaid_transaction_id TEXT
        )`)
    }

    async createTransaction(value, datetime, name, plaidAccountId, plaidCategory, plaidCurrency, plaidTransactionId) {
        return await this.db.run(
            'INSERT INTO transactions (value, datetime, name, plaid_account_id, plaid_category, plaid_currency, plaid_transaction_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            ...arguments
        )
    }

    async getLast20Transactions() {
        let transactions = await this.db.all(`SELECT * FROM transactions
        ORDER BY datetime DESC
        LIMIT 20`)
        return transactions;
    }

    async closeDatabase() {
        await this.db.close()
    }
}