feather.replace()
//https://twitter.com/One_div

//Get the popup window(modal)
var modal = document.getElementById("modal");

// Get the card that opens the modal and store it as an array cards
cards=document.querySelectorAll(".card");

//Get the close button
var closebtn = document.getElementById("close");

var overlay=document.getElementById("overlay  ");

for (let i = 0; i < cards.length; i++) 
{
  // When the user clicks the card, open the modal 
  cards[i].onclick = function() 
  {
    modal.style.display = "block";
    // overlay.classList.add('active')
  }
}

// When the user clicks on  (x), close the modal
closebtn.onclick = function() 
{
    modal.style.display = "none";
}