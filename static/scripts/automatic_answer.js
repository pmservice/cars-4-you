function send_comment() {
    var comment = $("#feedback").val();
    $("#userFeedback").html('User: ' + comment);

    $.post(
        "/comments",
        comment,
        function(data) {
            console.log(data)
            $("#serviceAnswer").html('Car_Rental: ' + data);
        }
    );
}