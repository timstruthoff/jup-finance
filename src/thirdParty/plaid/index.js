import { Configuration, PlaidApi, PlaidEnvironments, } from 'plaid';
import { stringify } from 'csv-stringify/sync';
import * as fs from 'fs';

export default class Plaid {

    model;
    constructor() {
        console.log("Plaid")


    }

    attachModel(model) {
        this.model = model;
    }

    async run() {
        const configuration = new Configuration({
            basePath: PlaidEnvironments.development,
            baseOptions: {
                headers: {
                    'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
                    'PLAID-SECRET': process.env.PLAID_SECRET,
                },
            },
        });

        const access_token = process.env.PLAID_ACCESS_TOKEN;

        const plaidClient = new PlaidApi(configuration);

        const accounts_response = await plaidClient.accountsGet({ access_token });
        const accounts = accounts_response.data.accounts;

        console.log(accounts)


        // Provide a cursor from your database if you've previously
        // received one for the Item. Leave null if this is your
        // first sync call for this Item. The first request will
        // return a cursor.
        let cursor = "";

        // New transaction updates since "cursor"
        let added = [];
        let modified = [];
        // Removed transaction ids
        let removed = [];
        let hasMore = true;

        // Iterate through each page of new transaction updates for item
        while (hasMore) {
            const request = {
                access_token: access_token,
                cursor: cursor,
                options: { include_personal_finance_category: true },
            };
            const response = await plaidClient.transactionsSync(request);
            const data = response.data;

            // Add this page of results
            added = added.concat(data.added);
            modified = modified.concat(data.modified);
            removed = removed.concat(data.removed);

            hasMore = data.has_more;

            // Update cursor to the next cursor
            cursor = data.next_cursor;
        }

        // Persist cursor and updated data
        console.log({ added, modified, removed, cursor });

        const output = stringify(added, {
            delimiter: ";",
        });

        fs.writeFileSync("./temp-files/transactions.csv", output)

        // Add Promises to DB
        const addTransactionsPromises = [];

        added.forEach(transaction => {

            // If there is a datetime, format it to fit MySQL DateTime
            const authorized_datetime = transaction.authorized_datetime ? transaction.authorized_datetime.slice(0, 19).replace('T', ' ') : null
            const datetime = transaction.datetime ? transaction.datetime.slice(0, 19).replace('T', ' ') : null;

            addTransactionsPromises.push(
                this.model.createPlaidTransaction({
                    transactionId: transaction.transaction_id,
                    accountId: transaction.account_id,
                    amount: transaction.amount,
                    authorizedDatetime: authorized_datetime,
                    category: transaction.category ? transaction.category[0] : null,
                    datetime: datetime,
                    isoCurrencyCode: transaction.iso_currency_code,
                    name: transaction.name,
                    merchant_name: transaction.merchant_name,
                    paymentChannel: transaction.payment_channel,
                    personalFinanceCategory: transaction.personalFinanceCategory ? transaction.personalFinanceCategory.detailed : null
                })
            );
        })

        setTimeout(() => { }, 100000)

        const result = await Promise.all(addTransactionsPromises)

        console.log("Finished")
    }
}