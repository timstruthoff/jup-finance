import 'dotenv/config'
import JupServer from "./src/app.js"
import * as fs from "fs";


fs.unlinkSync(process.env.DATABASE_FILE_LOCATION);
const jupServer = new JupServer();