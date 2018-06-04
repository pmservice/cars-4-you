
var selectedFace = null



function send_comment() {
    var comment = $("#feedback").val();
    $("#userFeedback").html('User: ' + comment);
    
    document.getElementById("user_comment").innerHTML = comment;

    if(selectedFace.id == "very_sad"){
        document.getElementById("feedback_comment").innerHTML = "We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue. In the meantime, we’d like to offer you a coupon for a free upgrade on your next rental with us.";
    }
    else {
        document.getElementById("feedback_comment").innerHTML = "Thank you for positive feedback!";
        document.getElementById("coupon").style.display = "none";
    }

    document.getElementById("response_face").src = selectedFace.src;

    document.getElementById("question").style.display = "none";
    document.getElementById("response").style.display = "block";


    $.post(
        "/comments",
        comment,
        function(data) {
            console.log(data)
            // $("#serviceAnswer").html('Car_Rental: ' + data);
        }
    );
}


function change_image(elmnt) {
    var button = document.getElementById("send_button");
    button.disabled = false;

    if (selectedFace != null){
        var selectedId = selectedFace.id;
        console.log("staticImages/" + selectedId + ".svg");
        selectedFace.src = "staticImages/" + selectedId + ".svg";
    }
    elmnt.src = "staticImages/selected_" + elmnt.id + ".svg";
    selectedFace = elmnt;  
}