feather.replace()
//https://twitter.com/One_div

//Get the popup window(modal)
var modal = document.getElementById("modal");

// Get the card that opens the modal and store it as an array cards
cards=document.querySelectorAll(".card");

//Get the close button
var closebtn = document.getElementById("close");

//Get content of Modal class
var modalTitle=document.getElementById("modal-title");
var modalSub=document.getElementById("modal-sub");
var modalTime=document.getElementById("modal-time");

//Get content of card class
var cardHeader=document.getElementById("card-header");
var cardBody=document.getElementById("card-body");
var cardTime=document.getElementById("btn-time");

var overlay=document.getElementById("overlay  ");

for (let i = 0; i < cards.length; i++) 
{
  // When the user clicks the card, open the modal 
  cards[i].onclick = function() 
  {
    modal.style.display = "block";
    // overlay.classList.add('active')
    // modalContent[0].innerText=cardContent[0].innerText
    // console.log(modalSub.innerText,cardBody.innerText,modalTime.innerText,cardTime.innerText)
    // modalTitle.innerText=cardHeader.innerText;
    // modalSub.innerText= "Subject: " +cardBody.innerText;
    // modalTime.innerText="Time: "+cardTime.innerText;
    
  }
}

// When the user clicks on  (x), close the modal
closebtn.onclick = function() 
{
    modal.style.display = "none";
}