/**
 * Sets the background color of #q1-container
 * @param {string} color The background color that #q1-container should change to
 */  
function setBackgroundColor(color) {
    document.getElementById("container").style.backgroundColor = color;
}
document.getElementById("container").onclick = setBackgroundColor;

// RED
function redButtonClicked() {
    setBackgroundColor("#EF476F")
}
document.getElementById("button-red").onclick = redButtonClicked;

// YELLOW
function yellowButtonClicked() {
    setBackgroundColor("yellow")
}
document.getElementById("button-yellow").onclick = yellowButtonClicked;

// GREEN
function greenButtonClicked() {
    setBackgroundColor("#06D6A0")
}
document.getElementById("button-green").onclick = greenButtonClicked;

// LIGHT BLUE
function lightblueButtonClicked() {
    setBackgroundColor("#118AB2")
}

document.getElementById("button-lightblue").onclick = lightblueButtonClicked;

// BLUE
function blueButtonClicked() {
    setBackgroundColor("#073B4C")
}
document.getElementById("button-blue").onclick = blueButtonClicked;

// WHITE
function whiteButtonClicked() {
    setBackgroundColor("white")
}
document.getElementById("button-white").onclick = whiteButtonClicked;

// PINK
function pinkButtonClicked() {
    setBackgroundColor("pink")
}
document.getElementById("button-pink").onclick = pinkButtonClicked;

// ORANGE
function orangeButtonClicked() {
    setBackgroundColor("orange")
}
document.getElementById("button-orange").onclick = orangeButtonClicked;

// AQUA
function aquaButtonClicked() {
    setBackgroundColor("aqua")
}
document.getElementById("button-aqua").onclick = aquaButtonClicked;

// PURPLE
function purpleButtonClicked() {
    setBackgroundColor("purple")
}
document.getElementById("button-purple").onclick = purpleButtonClicked;
