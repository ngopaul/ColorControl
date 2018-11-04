/**
 * @param {string} color The background color that #container should change to
 */  
function setBackgroundColor(color) {
    document.getElementById("container").style.backgroundColor = color;
}
document.getElementById("container").onclick = setBackgroundColor;	

// RED
function redButtonClicked() {
    setBackgroundColor("#EF476F");
    console.log("red");
    send_data("red");
}
document.getElementById("button-red").onclick = redButtonClicked;

// YELLOW
function yellowButtonClicked() {
    setBackgroundColor("yellow");
    console.log("yellow");
    send_data("yellow");
}
document.getElementById("button-yellow").onclick = yellowButtonClicked;	

// GREEN
function greenButtonClicked() {
    setBackgroundColor("#06D6A0");
    console.log("green");
    send_data("green")
}
document.getElementById("button-green").onclick = greenButtonClicked;	

// LIGHT BLUE
function lightblueButtonClicked() {
    setBackgroundColor("#118AB2");
    console.log("lightblue");
    send_data("lightblue");
}
document.getElementById("button-lightblue").onclick = lightblueButtonClicked;	

// BLUE
function blueButtonClicked() {
    setBackgroundColor("#073B4C");
    console.log("blue");
    send_data("blue");
}
document.getElementById("button-blue").onclick = blueButtonClicked;	

// WHITE
function whiteButtonClicked() {
    setBackgroundColor("white");
    console.log("white");
    send_data("white");
}
document.getElementById("button-white").onclick = whiteButtonClicked;	

// PINK
function pinkButtonClicked() {
    setBackgroundColor("pink");
    console.log("pink");
    send_data("pink");
}
document.getElementById("button-pink").onclick = pinkButtonClicked;

// ORANGE
function orangeButtonClicked() {
    setBackgroundColor("orange");
    console.log("orange");
    send_data("orange");
}
document.getElementById("button-orange").onclick = orangeButtonClicked;	

// AQUA
function aquaButtonClicked() {
    setBackgroundColor("aqua");
    console.log("aqua");
    send_data("aqua");
}
document.getElementById("button-aqua").onclick = aquaButtonClicked;

// PURPLE
function purpleButtonClicked() {
    setBackgroundColor("purple");
    console.log("purple");
    send_data("purple");
}
document.getElementById("button-purple").onclick = purpleButtonClicked;	


function send_data(color) {
    console.log("Sending Data");
    var xhr = new XMLHttpRequest();
    var data = new FormData();
    data.append('color', color);
    xhr.open("POST", "/", true);
    xhr.send(data);
    console.log(data);
}
