const api = "21cf9c4026d117b68753446ebbe41139";

const iconImg = document.querySelector("#weather-icon");
const loc = document.querySelector("#location");
const desc = document.querySelector(".desc")

const cTemp = document.querySelector(".cAct")
const cMinTemp = document.querySelector(".cMin");
const cMaxTemp = document.querySelector(".cMax");

const fTemp = document.querySelector(".f");
const fMinTemp = document.querySelector(".fMin");
const fMaxTemp = document.querySelector(".fMax");
const SunriseDOM = document.querySelector(".sunrise");
const SunsetDOM = document.querySelector(".sunset");

const lat_info = document.querySelector('#lat_info');
const long_info = document.querySelector('#long_info');

const myClock = document.querySelector('#clock')

function clock() {
    let today = new Date();
    let hours = today.getHours();
    let minutes = today.getMinutes();
    let secs = today.getSeconds();

    myClock.textContent = `${hours}:${minutes}:${secs}`;

    setTimeout(clock, 1000);
}


    window.addEventListener('keypress', () => {
     
            let lat // google maps 1st coordinate
            let long; // google maps 2nd coordinate
        
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                lat = position.coords.latitude;
                long = position.coords.longitude;
                
            
                //lat_info.innerHTML = lat;
                
                const base = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${api}&units=metric&lang=es`;
                fetch(base).then((response) => {
                    return response.json();
                })
                .then((data) => {
                    const currentTemp = data.main.temp;
                    const minTemp = data.main["temp_min"];               
                    const maxTemp = data.main["temp_max"];               
                    console.log(data.main["temp_min"]);                
                    console.log(data.main["temp_max"]);                
                    const place = data.name;
                    const { description, icon} = data.weather[0];
                    const { sunrise, sunset} = data.sys;
                    
                    const iconUrl = `http://openweathermap.org/img/wn/${icon}@2x.png`;
                    
                    lat_info.textContent = `${lat}`
                    long_info.textContent = `${long}`
    
                    const sunriseGMT = new Date(sunrise * 1000);
                    const sunsetGMT = new Date(sunset * 1000);
                    
                    iconImg.src = iconUrl;
                    loc.textContent = `${place}`;
                    desc.textContent = `${description}`;
    
                    cTemp.textContent = `${currentTemp.toFixed(1)} °C`;
                    cMinTemp.textContent = `${minTemp.toFixed(1)} °C`
                    cMaxTemp.textContent = `${maxTemp.toFixed(1)} °C`
    
                    //fTemp.textContent = `${farenheit.toFixed(1)} °F`;
                    fTemp.textContent = `${((currentTemp * 9) / 5 + 32).toFixed(1)} °F`;
                    fMinTemp.textContent = `${((minTemp * 9) / 5 + 32).toFixed(1)} °F`;
                    fMaxTemp.textContent = `${((maxTemp * 9) / 5 + 32).toFixed(1)} °F`;
    
    
                    SunriseDOM.textContent = `${sunriseGMT.toLocaleDateString(), sunriseGMT.toLocaleTimeString()}`
                    SunsetDOM.textContent = `${sunsetGMT.toLocaleDateString(), sunsetGMT.toLocaleTimeString()}`
                })
            })
        }
        }
        
        )
    
clock();


