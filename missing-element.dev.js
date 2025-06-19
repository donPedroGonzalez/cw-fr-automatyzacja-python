"use strict";

// EXERCICE BODY CREATION
var firstPart, secondPart, missingElement;

window.onload = function () {
  document.getElementById("button").disabled = true;
  var exerciceBody = document.getElementById("exercice-wrapper");
  firstPart = ["Wstaw odpowiednią formę czasownika", "J'", "Nous", "Vous", "Marie et Jean"];
  secondPart = ["Użyj czasownika podanego w nawiasach", "45 ans.", "deux enfants.", "mariés ?", "polonais et italien."];
  missingElement = ["Verbes", "ai", "avons", "êtes", "parlent"];
  hints = ["", "avoir", "avoir", "être", "parler"];
  var myForm = document.createElement("form");
  myForm.setAttribute("id", "myExercice");
  document.getElementById("premiere-consigne").innerText = firstPart[0];
  document.getElementById("deuxieme-consigne").innerText = secondPart[0];
  document.getElementById("footer-cat-info").innerText = missingElement[0];
  var newItemLabel1, newItemLabel2, newItemInput;

  for (var i = 1; i < firstPart.length; i++) {
    newItemLabel1 = document.createElement("label");
    newItemLabel1.setAttribute("for", "item" + i);
    newItemLabel1.innerText = firstPart[i];
    newItemLabel2 = document.createElement("label");
    newItemLabel2.setAttribute("for", "item" + i);
    newItemLabel2.innerText = secondPart[i] + " (" + hints[i] + ")";
    newItemInput = document.createElement("input");
    newItemInput.setAttribute("type", "text");
    newItemInput.setAttribute("name", "item" + i);
    newItemInput.setAttribute("id", "item" + i);
    newItemInput.setAttribute("style", "min-width: 350px; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size:16pt;");
    var paragraph = document.createElement("p");
    paragraph.appendChild(newItemLabel1);
    paragraph.appendChild(newItemInput);
    paragraph.appendChild(newItemLabel2);
    paragraph.setAttribute("id", "par" + i);
    myForm.appendChild(paragraph);
  }

  exerciceBody.appendChild(myForm); // VIRTUAL KEYBOARD

  var inputs = document.getElementById("myExercice").getElementsByTagName("input");
  var keyb = document.getElementById("keyboard");
  var keybKeys = keyb.getElementsByTagName("input");
  var exTitleWindow = document.getElementById("main-window-title");
  var keybReset = document.getElementById("reset-keyboard");

  for (var k = 0; k < inputs.length; k++) {
    inputs[k].addEventListener("onclick", keyboardActivation());
  }

  function keyboardActivation() {
    inputs[k].onclick = function (e) {
      var self = this;
      /*keyb.style.display = "block";*/

      keyb.setAttribute("class", "");
      keybReset.setAttribute("class", "");
      keyb.style.top = Number(e.clientY + -85) + "px";
      console.log("onclick-pageY: " + e.pageY);
      keyb.style.left = Number(e.clientX + 75) + "px";
      keybReset.style.display = "grid";
      keybReset.addEventListener("onclick", keyboardDeactivation());

      for (var m = 0; m < keybKeys.length; m++) {
        var virtualKeyboard = function virtualKeyboard(m, k) {
          keybKeys[m].onclick = function () {
            self.value += this.value;
          };
        };

        keybKeys[m].addEventListener("onclick", virtualKeyboard(m, k));
      }
    };
  }

  function keyboardDeactivation() {
    keybReset.onclick = function () {
      keyb.setAttribute("class", "hidden");
      keybReset.setAttribute("class", "hidden");
    };
  }
};

var inputToFill;
var filledIn; // VERIRFICATION BUTTON ACTIVATION

window.onkeydown = function () {
  for (var i = 1; i < firstPart.length; i++) {
    filledIn = true;
    itemName = "item" + i;
    formToCheck = document.getElementById("myExercice");
    itemToCheck = formToCheck.elements[itemName].value;

    if (!itemToCheck) {
      filledIn = false;
      break;
    }
  }

  if (filledIn === true) {
    document.getElementById("button").disabled = false;
  }
}; // CHECKING ANSWERS


var answer, itemName, itemToCheck, formToCheck, myparagraph, resultWrapper;
var correctNumber = 0;

document.getElementById("button").onclick = function () {
  for (var i = 1; i < firstPart.length; i++) {
    answer = missingElement[i];
    itemName = "item" + i;
    formToCheck = document.getElementById("myExercice");
    itemToCheck = formToCheck.elements[itemName].value;
    console.log("itemToCheck: " + itemToCheck);

    if (itemToCheck !== missingElement[i]) {
      myparagraph = document.createElement("span");
      myparagraph.setAttribute("id", "answer" + i);
      myparagraph.setAttribute("style", "color:red;");
      myparagraph.innerText = " - La réponse correcte : " + missingElement[i];
      document.getElementById("par" + i).appendChild(myparagraph);
    } else {
      myparagraph = document.createElement("span");
      myparagraph.setAttribute("id", "answer" + i);
      myparagraph.setAttribute("style", "color:green;");
      myparagraph.innerText = " - C'est correct, félicitations !";
      document.getElementById("par" + i).appendChild(myparagraph);
      correctNumber++;
    }

    resultWrapper = document.getElementById("result-wrapper");
    resultWrapper.innerText = "Ton résultat : " + correctNumber + " / " + firstPart.length;
    resultWrapper.setAttribute("style", "font-size: larger; color: dark-blue; text-shadow: 0px 0px 3px white;");
  }
};