export default class Controller {

    model;
    view;
    plaid;

    constructor(model, view, plaid) {
        this.model = model;
        this.view = view;
        this.plaid = plaid;
    }

    async startApp() {
        await this.model.start();
        await this.model.executeTestCommands();
        await this.plaid.run();
        await this.shutdown();
    }

    async testModel() {
        await this.model.executeTestCommands();
    }

    async shutdown() {
        await this.model.closeDatabase();
    }
}