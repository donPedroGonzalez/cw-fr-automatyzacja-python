const fs = require('fs');
const path = require('path');

try {
    const myString = fs.readFileSync(path.join(__dirname, 'JakubGabryel_cw_1.csv'), 'utf-8');
    var linesArr = myString.split("\r\n");
} catch (error) {
    console.error("Error reading file:", error);
}

var firstPart = [];
var secondPart = [];
var missingElement = [];
var hints = [];

for (var i= 0; i < linesArr.length; i++)
{
    var tmpLine = linesArr[i].split(";");
    firstPart[i] = tmpLine[0];
    secondPart[i] = tmpLine[1];
    missingElement[i] = tmpLine[2];
    hints[i] = tmpLine[3];
}

console.log("firstPart: " + firstPart);
console.log("[");
for (item in firstPart){
    console.log("\"", item, "\"");
}
console.log("]");
console.log("secondPart: " + secondPart);
console.log("missing element: " + missingElement)
console.log("hints: "+ hints);