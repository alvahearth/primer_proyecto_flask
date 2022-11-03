const required_spending = [
    {
        name: "Plan",
        price: "17000"
    },
    {
        name: "Crunchyroll",
        price: "4300"
    },
    {
        name: "Netflix",
        price: "8320"
    },
    {
        name: "Spotify",
        price: "6290"
    },
    {
        name: "Youtube Premium",
        price: "2490",
    },
    {
        name: "Celular",
        price: "58333"

    },
    {
        name: "Mantención",
        price: "1750"
    },
    {
        name: "UDLA",
        price: "181001"
    }
]

const main_items = document.querySelector("#main-items");
const totalSpend = document.querySelector("#total-spend");

const calc = document.querySelector("#calc");



window.addEventListener("load", () => {
    total = 0;
    const amountToDeduce = required_spending.forEach((item) => {
        total = total + parseInt(item.price);
    });

    const listItems = required_spending.map((item) => {
        return `<li><span class="name">${item.name}</span><span class="price">$${item.price}</span></li>`
    });

    function calculate(n) {

        return n - total
    }

    totalSpend.innerText = `Total: ${total}`
    main_items.innerHTML = listItems.join("");
    
    calc.addEventListener("click", () => {
        //const item1 = document.querySelector("#item1").value; 
        //const item2 = document.querySelector("#item2").value;
        //const item3 = document.querySelector("#item3").value;
        const money = document.querySelector("#current-money").value;

        const finalDigits = calculate(money);
        
        const result = document.querySelector("#result");

        result.innerHTML = finalDigits;
    });
});