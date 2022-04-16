feather.replace();
/*//https://twitter.com/One_div

//Get the popup window(modal)
var modal =
    document.getElementById(
        "modal"
    );
console.log(
    modal
);
cards =
    document.querySelectorAll(
        ".card"
    );

//Get the close button
var closebtn =
    document.getElementById(
        "close"
    );

var overlay =
    document.getElementById(
        "overlay  "
    );

for (
    let i = 0; i <
    cards.length; i++
) {
    // When the user clicks the card, open the modal
    cards[
            i
        ].onclick =
        function() {
            modal.style.display =
                "block";
        };
}

// When the user clicks on  (x), close the modal
closebtn.onclick =
    function() {
        modal.style.display =
            "none";
    }; */

var chatbtn=document.getElementsByClassName("chatbotIcon");
var chatframe=document.getElementById("chatbotFrame");

var cross=document.getElementById("cross");
var message =document.getElementById("message-circle");
chatbtn.onclick=function() {popChat()};
var flag=0;

function popChat(){

    if(flag==0){
        cross.style.display ="block";
        message.style.display="none";
        chatframe.style.display ="block";
        flag=1;
    }
    else{
        cross.style.display ="none";
        message.style.display="block";
        chatframe.style.display ="none";
        flag=0;
    }
    

}