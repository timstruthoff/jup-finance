import Model from "./model/model.js";
import View from "./view/view.js";
import Controller from "./controller/controller.js";

import Plaid from "./thirdParty/plaid/index.js"



export default class JupServer {
    model;
    view;
    controller;
    plaid;

    constructor() {
        console.log("Jup Server!")

        this.model = new Model();
        this.view = new View();
        this.plaid = new Plaid();

        this.controller = new Controller(this.model, this.view, this.plaid);
        this.controller.startApp();
    }
}