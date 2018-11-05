/**
 * @param {string} color The background color that #container should change to
 */  
var light_colors = [];
var multi_clicked = false;
function setBackgroundColor(color) {
    document.getElementById("container").style.backgroundColor = color;
}
document.getElementById("container").onclick = setBackgroundColor;	

// function universe(color) {
//     if (multi_clicked == false) {
//         setBackgroundColor("color");
//         console.log("color");
//         send_data("color");
//     } else {
//         if (document.getElementById("button-" + color).value == "1") {
//             setBackgroundColor("white");
//             let i = 0;
//             for (i = 0; i < light_colors.length; i++) {
//                 if (light_colors[i] == "color") {
//                     light_colors.splice(i, 1);
//                 }
//             }
//             document.getElementById("button-" + color).value = "0";
//         } else {
//             multi_color("color");
//             setBackgroundColor("color");
//             document.getElementById("button-" + color).value = "1";
//         }
//     }
//     console.log(document.getElementById("button-" + color).value);
//     console.log(light_colors);
// }
// document.getElementById("button-"+color).onclick = universe;

// function take_colors(color) {
//     document.getElementById("button-"+color).onclick = universe;
// }

// RED
var redclicked = false;
function redButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("#EF476F");
        console.log("red");
        send_data("red");
    } else {
        if (redclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "red") {
                    light_colors.splice(i, 1);
                }
            }
            redclicked = false;
        } else {
            multi_color("red");
            setBackgroundColor("#EF476F");
            redclicked = true;
        }
    }
    console.log(redclicked);
    console.log(light_colors);
}
document.getElementById("button-red").onclick = redButtonClicked;

// YELLOW
var yellowclicked = false;
function yellowButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("#FFD166");
        console.log("yellow");
        send_data("yellow");
    } else {
        if (yellowclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "yellow") {
                    light_colors.splice(i, 1);
                }
            }
            yellowclicked = false;
        } else {
            multi_color("yellow");
            setBackgroundColor("FFD166");
            yellowclicked = true;
        }
    }
}
document.getElementById("button-yellow").onclick = yellowButtonClicked;	

// GREEN
var greenclicked = false;
function greenButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("#06D6A0");
        console.log("green");
        send_data("green");
    } else {
        if (greenclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "green") {
                    light_colors.splice(i, 1);
                }
            }
            greenclicked = false;
        } else {
            multi_color("green");
            setBackgroundColor("#06D6A0");
            greenclicked = true;
        }
    }
}
document.getElementById("button-green").onclick = greenButtonClicked;	

// LIGHT BLUE
var lightblueclicked = false;
function lightblueButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("#118AB2");
        console.log("lightblue");
        send_data("lightblue");
    } else {
        if (lightblueclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "lightblue") {
                    light_colors.splice(i, 1);
                }
            }
            lightblueclicked = false;
        } else {
            multi_color("lightblue");
            setBackgroundColor("#118AB2");
            lightblueclicked = true;
        }
    }
}
document.getElementById("button-lightblue").onclick = lightblueButtonClicked;	

// BLUE
var blueclicked = false;
function blueButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("#073B4C");
        console.log("blue");
        send_data("blue");
    } else {
        if (blueclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "blue") {
                    light_colors.splice(i, 1);
                }
            }
            blueclicked = false;
        } else {
            multi_color("blue");
            setBackgroundColor("#073B4C");
            blueclicked = true;
        }
    }
}
document.getElementById("button-blue").onclick = blueButtonClicked;	

// WHITE
var whiteclicked = false;
function whiteButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("white");
        console.log("white");
        send_data("white");
    } else {
        if (whiteclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "white") {
                    light_colors.splice(i, 1);
                }
            }
            whiteclicked = false;
        } else {
            multi_color("white");
            setBackgroundColor("white");
            whiteclicked = true;
        }
    }
}
document.getElementById("button-white").onclick = whiteButtonClicked;	

// PINK
var pinkclicked = false;
function pinkButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("pink");
        console.log("pink");
        send_data("pink");
    } else {
        if (pinkclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "pink") {
                    light_colors.splice(i, 1);
                }
            }
            pinkclicked = false;
        } else {
            multi_color("pink");
            setBackgroundColor("pink");
            pinkclicked = true;
        }
    }
}
document.getElementById("button-pink").onclick = pinkButtonClicked;

// ORANGE
var orangeclicked = false;
function orangeButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("orange");
        console.log("orange");
        send_data("orange");
    } else {
        if (aquaclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "orange") {
                    light_colors.splice(i, 1);
                }
            }
            orangeclicked = false;
        } else {
            multi_color("orange");
            setBackgroundColor("orange");
            orangeclicked = true;
        }
    }
}
document.getElementById("button-orange").onclick = orangeButtonClicked;	

// AQUA
let aquaclicked = false;
function aquaButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("aqua");
        console.log("aqua");
        send_data("aqua");
    } else {
        if (aquaclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "aqua") {
                    light_colors.splice(i, 1);
                }
            }
            aquaclicked = false;
        } else {
            multi_color("aqua");
            setBackgroundColor("aqua");
            aquaclicked = true;
        }
    }
}
document.getElementById("button-aqua").onclick = aquaButtonClicked;

// PURPLE
let purpleclicked = false;
function purpleButtonClicked() {
    if (multi_clicked == false) {
        setBackgroundColor("purple");
        console.log("purple");
        send_data("purple");
    } else {
        if (purpleclicked == true) {
            setBackgroundColor("white");
            let i = 0;
            for (i = 0; i < light_colors.length; i++) {
                if (light_colors[i] == "purple") {
                    light_colors.splice(i, 1);
                }
            }
            purpleclicked = false;
        } else {
            multi_color("purple");
            setBackgroundColor("purple");
            purpleclicked = true;
        }
    }
}
document.getElementById("button-purple").onclick = purpleButtonClicked;	

//  OFF
function offButtonClicked() {
    console.log("off");
    send_data("off");
}
document.getElementById("button-off").onclick = offButtonClicked;	

//  FLASH
function onButtonClicked() {
    console.log("on");
    if (multi_clicked == true) {
        send_data("multi on", [200, 200], light_colors);
    } else {
        send_data("on", [200, 200]);
    }
}
document.getElementById("button-on").onclick = onButtonClicked;	

//  FLASH
function flashButtonClicked() {
    console.log("flash");
    if (multi_clicked == true) {
        send_data("multi flash", [200, 200], light_colors);
    } else {
        send_data("flash", [200, 200]);
    }
}
document.getElementById("button-flash").onclick = flashButtonClicked;	

//  BREATHE
function breatheButtonClicked() {
    console.log("breathe");
    if (multi_clicked == true) {
        send_data("multi breathe", [200, 200], light_colors);
    } else {
        send_data("breathe", [200, 200]);
    }
    console.log("Reloading webpage...")
    location.reload()
}
document.getElementById("button-breathe").onclick = breatheButtonClicked;	

// MULTI
function multiButtonClicked() {
    console.log("multi was clicked");
    //send_data("multi");
    multi_clicked = true;
}
document.getElementById("button-multi").onclick = multiButtonClicked;	

function send_data(info, times = [], array = []) {
    console.log("Sending Data");
    var xhr = new XMLHttpRequest();
    var data = new FormData();
    console.log("Info: ", info)
    console.log("Times: ", times)
    console.log("Array: ", array)
    data.append('info', info);
    data.append('times', times);
    data.append('array', array);
    xhr.open("POST", "/", true);
    xhr.send(data);
    console.log(data);
}

// drag bar
$(document).ready(function() {
    M.updateTextFields();
  });

// multi function
function multi_color(color) {
    light_colors.push(color);
}
