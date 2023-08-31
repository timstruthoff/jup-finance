'use strict';

import express from 'express';

import sqlite3 from 'sqlite3'
import { open } from 'sqlite'

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';






// this is a top-level await 
(async () => {
    // open the database
    const db = await open({
      filename: 'database.db',
      driver: sqlite3.Database
    })

    // App
    const app = express();
    app.get('/', (req, res) => {
      res.send('Hello World');
    });

    app.listen(PORT, HOST, () => {
      console.log(`Running on http://${HOST}:${PORT}`);
    });

    await db.exec('CREATE TABLE tbl (col TEXT)')
    await db.exec('INSERT INTO tbl VALUES ("test")')

    await db.close()
})()