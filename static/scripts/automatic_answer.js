var requestSend = false;

var logoImage = document.getElementById("logoimg")
var textInput = document.getElementById('user-text');
var userComment = document.getElementById("user-comment");
var sadFaceImage = document.getElementById('sad');
var happyFaceImage = document.getElementById('happy');
var responseFace = document.getElementById("response-face");
var sendButton = document.getElementById("send-button");
var feedbackComment = document.getElementById("feedback-comment");
var feedbackTitle = document.getElementById("feedback-title");
var questionBox = document.getElementById("question");
var responseBox = document.getElementById("response");
var sidebar = document.getElementById("sidebar");
var avatarButton = document.getElementById("avatar-button");
var errorPanel = document.getElementById("error-message");
var saveButton = document.getElementById("sidebar-save");
var cancelButton = document.getElementById("sidebar-cancel");
var customerName = document.getElementById("cust-name");
var firstName = document.getElementById("first-name-input");
var secondName = document.getElementById("last-name-input");
var genderInput = document.getElementById("gender-input");
var ageInput = document.getElementById("age-input");
var statusInput = document.getElementById("status-input");
var childrenInput = document.getElementById("children-input");
var carownerInput = document.getElementById("owner-input");
var activeInput = document.getElementById("active-input");

var happyFacePath = "staticImages/thumb_up_notselected.svg";
var happyFaceSelectedPath = "staticImages/thumb_up_selected.svg";
var sadFacePath = "staticImages/thumb_down_notselected.svg";
var sadFaceSelectedPath = "staticImages/thumb_down_selected.svg";


var payloadData = {
    "comment": "",
    "gender": "Male",
    "status": "S",
    "childrens": 2,
    "age": 36,
    "customer": "Active",
    "owner": "Yes",
    "satisfaction": 1
};

var userData = {
    "username": "John",
    "lastname" : "Smith",
    "payload": payloadData
};

var userFirstName = "John";
var userLastName = "Smith";
var gender = "Male";
var age = 36;
var status = "Single";
var children = 2;
var owner = "Yes";
var active = "Active";

var satisfaction = 1;

var selectedFace = null;
var timeout = null;

/* DISABLE NLU */
// textInput.onkeyup = function (e) {
//     clearTimeout(timeout);
//     timeout = setTimeout(get_sentiment, 800);
// };

cancelButton.onclick = function (e) {
    reset_sidebar();
    show_hide_sidebar();
}

saveButton.onclick = function (e) {
    update_customer_name();
    show_hide_sidebar();
}

sadFaceImage.onclick = select_sad;
happyFaceImage.onclick = select_happy;
avatarButton.onclick = function (e) {
    show_hide_sidebar();
}

logoImage.onclick = function (e) {
    console.log("reloding ...");
    location.reload();
}

sendButton.onclick = send_comment;

function send_comment() {
    console.log("--> Sending comment to preproces.");
    var comment = textInput.value;
    userComment.innerHTML = comment;

    if (selectedFace === null) {
        send_with_sentiment(comment);
    }
    else {
        send_request(comment, satisfaction);
    }
}

function send_with_sentiment(text) {
    console.log("Sending request with sentiment: ");
    console.log(text);
    $.post(
        "/analyzesent",
        text,
        function (data) {
            console.log(data)
            if (data === 'negative') {
                send_request(text, 0);
            }
            else {
                send_request(text, 1);
            }
        }
    );
}

function send_request(comment, satisfaction) {
    userData.payload.comment = comment;
    console.log("Sending post request to scoring ...");
    $.ajax({
        method: "POST",
        contentType: "application/json",
        url: "/analyze",
        data: JSON.stringify(userData.payload),
        success: function (data) {
            console.log("Response: ");
            console.log(data);

            update_face(satisfaction);
            feedbackComment.innerHTML = data['client_response'];

            questionBox.style.display = "none";
            responseBox.style.display = "block";
        },
        error: function (data, textStatus, errorThrown) {
            console.log("Error Response: ");
            console.log(data);
            console.log(data['responseText']);
            console.log(textStatus);
            console.log(errorThrown);
            print_error(data['responseText']);
        },
        dataType: "json"
    });
}

function update_face(satisfaction) {
    if (selectedFace != null) {
        responseFace.src = selectedFace.src;
    }
    else if (satisfaction == 1) {
        responseFace.src = happyFaceSelectedPath;
    }
    else {
        responseFace.src = sadFaceSelectedPath;
    }
}

function get_sentiment() {
    var text = textInput.value;
    console.log('Input Value:', text);

    if (text.length > 10) {
        console.log("sending request");
        $.post(
            "/analyzesent",
            text,
            function (data) {
                console.log(data)
                if (data === 'negative') {
                    select_sad();
                }
                else {
                    select_happy();
                }
            }
        );
    }
    else {
        deselect_faces();
    }
}

function select_happy() {
    happyFaceImage.src = happyFaceSelectedPath;
    sadFaceImage.src = sadFacePath;
    selectedFace = happyFaceImage;
    userData.payload.satisfaction = 1;
    sendButton.disabled = false;
}

function select_sad() {
    happyFaceImage.src = happyFacePath;
    sadFaceImage.src = sadFaceSelectedPath;
    selectedFace = sadFaceImage;
    userData.payload.satisfaction = 0;
    sendButton.disabled = false;
}

function deselect_faces() {
    happyFaceImage.src = happyFacePath;
    sadFaceImage.src = sadFacePath;
    sendButton.disabled = true;
}

function print_error(text) {
    errorPanel.innerHTML = String(text);
    errorPanel.style.display = "block";
}

function show_hide_sidebar() {
    if (sidebar.style.display === "none") {
        customerName.innerHTML = userData.username + " " + userData.lastname;
        sidebar.style.display = "block";
    }
    else {
        sidebar.style.display = "none"
    }
}

function update_customer_name() {
    userData.username = firstName.value;
    userData.lastname = secondName.value;
    userData.payload.gender = genderInput.value;
    userData.payload.age = ageInput.value;
    userData.payload.status = statusInput.value;
    userData.payload.childrens = childrenInput.value;
    userData.payload.customer = activeInput.value;
    userData.payload.owner = carownerInput.value;

    console.log(userData);
}

function reset_sidebar() {
    firstName.value = userData.username;
    secondName.value = userData.lastname;
    genderInput.value = userData.payload.gender;
    ageInput.value = userData.payload.age;
    statusInput.value = userData.payload.status;
    childrenInput.value = userData.payload.childrens;
    activeInput.value = userData.payload.customer;
    carownerInput.value = userData.payload.owner;

    console.log(userData);
}
