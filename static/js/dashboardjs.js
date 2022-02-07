feather.replace()
//https://twitter.com/One_div

var modal = document.getElementById("modal");
// Get the card that opens the modal
var card = document.getElementById("card");
var closebtn = document.getElementById("close");

// When the user clicks the card, open the modal 
card.onclick = function() {
    modal.style.display = "block";
  }

// When the user clicks on  (x), close the modal
closebtn.onclick = function() {
    modal.style.display = "none";
  }