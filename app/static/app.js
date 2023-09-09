class StockRefresher {
    constructor(stockId) {
        this.stockId = stockId;
        this.refresh()

        // docReady(this.setup);

        document.addEventListener("DOMContentLoaded", () => {
            setTimeout(() => {
                this.setup()
            }, 2000)
        });
    }

    setup() {
        this.tableElement = document.getElementById(this.stockId);
        console.log(this.tableElement)

        setInterval(this.refresh.bind(this), 1000)
    }

    refresh() {
        console.log(this.stockId)

        this.getStockData().then((result) => {
            this.refreshDom(result)
        })
    }

    async getStockData() {
        let response = await fetch("/api/stocks");

        if (response.ok) { // if HTTP-status is 200-299
            // get the response body (the method explained below)
            let json = await response.json();
            return json
        } else {
            console.error("HTTP-Error: " + response.status);
        }
    }

    refreshDom(json) {
        for(const [number, stockData] of Object.entries(json)) {

            let element = document.getElementById(stockData.wkn)

            console.log(element)

            if (element != null) {
                

                let children = element.querySelectorAll("td")

                console.log(children)

                let value = parseFloat(stockData.value)

                let nameElement = children[0];
                let wknElement = children[1];
                let valueElement = children[2];
                let changeElement = children[3];

                valueElement.innerHTML = value + "$";
            }
        }
    }
}

function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}  

stockRefresher = new StockRefresher("stockTable")