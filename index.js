import 'dotenv/config'
import JupServer from "./src/app.js"
import * as fs from "fs";

try {
    fs.unlinkSync(process.env.DATABASE_FILE_LOCATION);
} catch (err) {}

const jupServer = new JupServer();