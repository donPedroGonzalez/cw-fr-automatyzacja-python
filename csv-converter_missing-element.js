
var myString = "Wstaw odpowiednią formę czasownika;Użyj czasownika podanego w nawiasach;Verbes;\r\nJ';45 ans.;ai;avoir\r\nNous;deux enfants.;avons;avoir\r\nVous;mariés ?;êtes;être\r\nMarie et Jean;polonais et italien.;parlent;parler";
var linesArr = myString.split("\r\n");
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
console.log("secondPart: " + secondPart);
console.log("missing element: " + missingElement)
console.log("hints: "+ hints);