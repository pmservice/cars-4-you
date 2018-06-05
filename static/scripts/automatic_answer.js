
var selectedFace = null



function send_comment() {
    var comment = $("#feedback").val();
    $("#userFeedback").html('User: ' + comment);
    
    document.getElementById("user_comment").innerHTML = comment;

    if(selectedFace.id == "sad"){
        document.getElementById("feedback_comment").innerHTML = "We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue. In the meantime, we’d like to offer you a coupon for a free upgrade on your next rental with us.";
    }
    else {
        document.getElementById("feedback_comment").innerHTML = "Thank you for positive feedback!";
        document.getElementById("coupon").style.display = "none";
    }

    document.getElementById("response_face").src = selectedFace.src;

    document.getElementById("question").style.display = "none";
    document.getElementById("response").style.display = "block";

    // $.ajax({
    //     method: "post",
    //     contentType: "application/json; charset=utf-8",
    //     url: "/analyze",
    //     data: JSON.stringify({ "Ala ma kota": "bezwzglednie" }),
    //     success: function(data) { 
    //         console.log("Response: ");
    //         console.log(data);
    //     },
    //     failure: function(data) { 
    //         console.log("Error Response: ");
    //         console.log(data);
    //     },
    //     dataType: "json"
    // });
    // $.post(
    //     "/analyze",
    //     {"comment": comment},
    //     function(data) {
    //         console.log(data)
    //         // $("#serviceAnswer").html('Car_Rental: ' + data);
    //     }
    // );

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