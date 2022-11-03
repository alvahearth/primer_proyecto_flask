const myClock = document.querySelector('#clock');

function clock() {
    let today = new Date();
    let hours = today.getHours();
    let minutes = today.getMinutes();
    let secs = today.getSeconds();

    myClock.textContent = `${hours}:${addZero(minutes)}:${addZero(secs)}`;
   // myFecha.textContent = `${currentMonth} - ${currentDay}`

    setTimeout(clock, 1000);
}

function addZero(n) {
    return (parseInt(n, 10) < 10 ? '0' : '') + n;
}

clock();


