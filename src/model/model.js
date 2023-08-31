import sqlite3 from 'sqlite3'
import { open } from 'sqlite'

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
    }

    async executeTestCommands() {
        await this.db.exec('CREATE TABLE tbl (col TEXT)')
        await this.db.exec('INSERT INTO tbl VALUES ("test")')
    }

    async closeDatabase() {
        await this.db.close()
    }
}