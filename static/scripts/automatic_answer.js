var selectedFace = null

function send_comment() {
    var comment = $("#feedback").val();
    document.getElementById("user_comment").innerHTML = comment;
    var satisfaction = 0;
    if(selectedFace.id == "sad"){
        satisfaction = 0;
    }
    else {
        satisfaction = 1;
    }    

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
            "owner": "No",
            "satisfaction" : satisfaction
        }),
        success: function (data) {
            console.log("Response: ");
            console.log(data);

            document.getElementById("feedback_comment").innerHTML = data['client_response'];

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