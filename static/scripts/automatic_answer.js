var selectedFace = null

function send_comment() {
    var comment = $("#feedback").val();
    document.getElementById("user_comment").innerHTML = comment;

    // if(selectedFace.id == "sad"){
    //     document.getElementById("feedback_comment").innerHTML = "We’re sorry that you were unhappy with your experience with Cars4U. We will open a case to investigate the issue. In the meantime, we’d like to offer you a coupon for a free upgrade on your next rental with us.";
    //     document.getElementById("coupon").style.display = "block";
    // }
    // else {
    //     document.getElementById("feedback_comment").innerHTML = "Thank you for positive feedback!";

    // }    

    $.ajax({
        method: "POST",
        contentType: "application/json",
        url: "/analyze",
        data: JSON.stringify({
            "comment": comment,
            "gender": "Female",
            "status": "S",
            "childrens": "2",
            "age": "30",
            "customer": "Active",
            "owner": "No"
        }),
        success: function (data) {
            console.log("Response: ");
            console.log(data);

            document.getElementById("feedback_comment").innerHTML = data['area'] + "<br>Action: " + data['action'];

            if(data['action'] == "Voucher"){
                document.getElementById("coupon").style.display = "block";
            }

            document.getElementById("response_face").src = selectedFace.src;

            document.getElementById("question").style.display = "none";
            document.getElementById("response").style.display = "block";

            console.log("Should be changed!");
        },
        error: function (data, textStatus, errorThrown) {
            console.log("Error Response: ");
            console.log(data);
            console.log(textStatus);
            console.log(errorThrown);
        },
        dataType: "json"
    });

    $.post(
        "/comments",
        comment,
        function (data) {
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