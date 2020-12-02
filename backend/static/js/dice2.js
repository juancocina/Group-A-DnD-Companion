/*roll.js
* Copyright (C) 2019  Jake Bauer
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

/* stringRoll()
 * @brief This function rolls dice based on the input from the text-field
 */
function stringRoll() {
    let rollString = document.getElementById("inputString").value;
    let result = 0;
    let numRolls, die, operation, modifier, resultStr = "";

    // Parse values from string
    try {
        numRolls = rollString.match(/\d+d/ig)[0];
        numRolls = numRolls.substring(0, numRolls.length-1);
        die = rollString.match(/d\d+/ig)[0];
        die = die.substring(1);
    }
    catch(err) {
        console.log(err);
        alert("Invalid text input! See example for proper string format.");
        return;
    }
    try {
        operation = rollString.match(/[\+\-]/ig)[0];
        modifier = rollString.match(/\d+$/ig)[0];
    }
    catch(TypeError) {
        // Ignore missing operation or modifier strings
    }

    // Conduct rolls
    for (let i = 0; i < numRolls; i++) {
	let intermediate = Math.floor((Math.random()*die)+1);
	if (i == numRolls-1) {
	    // If it's the last roll, don't add a + symbol to the string
            resultStr += intermediate;
	}
	else {
            resultStr += intermediate + " + ";
	}
	result += intermediate;
    }
    // Finalize the result string
    resultStr += " = " + result;
    if (numRolls == 1) {
        resultStr = result;
    }
    // Apply the modifier
    resultStr = "d"+ die + ": " + resultStr;
    if (operation === '-') {
        result = Number(result) - Number(modifier);
        resultStr += " - " + modifier + " = " + result;
    }
    else if (operation === '+') {
        result = Number(result) + Number(modifier);
        resultStr += " + " + modifier + " = " + result;
    }
    // Add the result to the history box
    let hist = document.getElementById("history-text");
    hist.innerHTML = (resultStr + "\n") + hist.innerHTML;
}

/* roll()
 * @brief This function rolls the dice according to which button was pressed
 * @input Element The button representing which dice to roll
 */
function roll(element) {
    let btnId = (element.id).substring(1);
    let numRolls = document.getElementById(('num'+btnId)).value;
    let modifier = document.getElementById(('mod'+btnId)).value;
    let result = 0;
    let resultStr = "";
    // Conduct rolls
    for (let i = 0; i < numRolls; i++) {
	let intermediate = Math.floor((Math.random()*btnId)+1);
	if (i == numRolls-1) {
	    // If it's the last roll, don't add a + symbol to the string
            resultStr += intermediate;
	}
	else {
            resultStr += intermediate + " + ";
	}
	result += intermediate;
    }
    // Finalize the result string
    resultStr += " = " + result;
    if (numRolls == 1) {
        resultStr = result;
    }
    // Apply the modifier
    result = Number(result) + Number(modifier);
    resultStr = "d"+ btnId + ": " + resultStr;
    if (modifier < 0) {
        resultStr += " - " + Math.abs(modifier) + " = " + result;
    }
    else if (modifier > 0) {
        resultStr += " + " + modifier + " = " + result;
    }
    // Show the result as a number in the die's row
    document.getElementById(("d"+btnId+"result")).innerHTML = result;
    // Add the result to the history box
    let hist = document.getElementById("history-text");
    hist.innerHTML = (resultStr + "\n") + hist.innerHTML;
}

/* clear_history()
 * @brief This function clears the history box, restting it back to default
 *          values while also clearing results and input boxes.
 */
function clear_history() {
    let results = document.getElementsByTagName("p");
    for (let i = 0; i < Object.keys(results).length; i++) {
        element = results[i];
	if (element.getAttribute("class") == "field") {
	    element.innerHTML = "0";
	}
    }
    let inputs = document.getElementsByTagName("input");
    for (let i = 0; i < Object.keys(inputs).length; i++) {
	element = inputs[i];
	if (element.getAttribute("type") == "number") {
	    if (element.getAttribute("min")) {
	        element.value = 1;
	    }
	    else {
	        element.value = 0;
	    }
	}
    }
    let hist = document.getElementById("history-text");
    hist.innerHTML = "-------&#13;&#10;History";
}
