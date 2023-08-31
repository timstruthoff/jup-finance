import express from 'express';

export default class View {

    app;

    constructor() {
        this.app = express();
        this.setupRoutes();
        this.listen();
    }

    setupRoutes() {
        this.app.get('/', (req, res) => {
            res.send('Hello World');
        });
    }

    listen() {
        this.app.listen(process.env.WEBVIEW_PORT, process.env.WEBVIEW_HOST, () => {
            console.log(`Running on http://${process.env.WEBVIEW_HOST}:${process.env.WEBVIEW_PORT}`);
        });
    }
}