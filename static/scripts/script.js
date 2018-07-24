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
var modelSidebar = document.getElementById("sidebar-models");
var errorPanel = document.getElementById("error-message");
var saveButton = document.getElementById("sidebar-save");
var cancelButton = document.getElementById("sidebar-cancel");
var saveModelButton = document.getElementById("sidebar-model-save");
var cancelModelButton = document.getElementById("sidebar-model-cancel");
var customerName = document.getElementById("cust-name");
var firstName = document.getElementById("first-name-input");
var secondName = document.getElementById("last-name-input");
var genderInput = document.getElementById("gender-input");
var ageInput = document.getElementById("age-input");
var statusInput = document.getElementById("status-input");
var childrenInput = document.getElementById("children-input");
var carownerInput = document.getElementById("owner-input");
var activeInput = document.getElementById("active-input");
var areaSelection = document.getElementById("area-input");
var nluSelection = document.getElementById("nlu-input");
var happyFacePath = "staticImages/thumb_up.svg";
var happyFaceSelectedPath = "staticImages/thumb_up_on.svg";
var sadFacePath = "staticImages/thumb_down.svg";
var sadFaceSelectedPath = "staticImages/thumb_down_on.svg";
var deploymentSelected = false;



var payloadData = {
    "comment": "",
    "gender": "Male",
    "status": "S",
    "childrens": 2,
    "age": 36,
    "customer": "Active",
    "owner": "Yes",
    "satisfaction": -1
};

var userData = {
    "username": "John",
    "lastname" : "Smith",
    "payload": payloadData
};

cancelButton.onclick = function (e) {
    reset_sidebar();
    show_hide_sidebar();
}

saveButton.onclick = function (e) {
    update_customer_name();
    show_hide_sidebar();
}

cancelModelButton.onclick = function(e){
    show_hide_model_sidebar();
}

saveModelButton.onclick = function(e) {
    show_hide_model_sidebar();
    update_models();
}

sadFaceImage.addEventListener('click', select_sad);
happyFaceImage.addEventListener('click', select_happy);

document.getElementById("avatar-button").addEventListener('click', show_hide_sidebar);
document.getElementById("user-welcome").addEventListener('click', show_hide_sidebar);
document.getElementById("logout-button").addEventListener('click', function() { location.reload(); });

document.getElementById("model-button").addEventListener('click', show_hide_model_sidebar);

check_deployments();

logoImage.onclick = function (e) {
    location.reload();
}

sendButton.onclick = function (e) {
    console.log("--> sendButton.onclick():");
    var comment = textInput.value;
    userComment.innerHTML = comment;

    if (userData.payload.satisfaction === -1) {
        send_with_sentiment(comment);
    }
    else {
        send_request(comment);
    }
}

function send_with_sentiment(text) {
    console.log("--> send_with_sentiment(): ");
    console.log(text);
    $.post(
        "/analyzesent",
        text,
        function (data) {
            console.log(data)
            if (data === 'negative') {
                userData.payload.satisfaction = 0;
                send_request(text);
            }
            else {
                userData.payload.satisfaction = 1;
                send_request(text);
            }
        }
    );
}

function get_area_deployments() {
    console.log("--> get_area_deployments(): ");
    $.get(
        "/areadeployments",
        function (data) {
            areaSelection.innerHTML = "";
            if (data['deployments'].length == 0){
                var opt = document.createElement('option');
                opt.value = "< no deployments >";
                opt.innerHTML = "< no deployments >";
                areaSelection.appendChild(opt);
            }
            else{
                areaSelection.innerHTML = "";

                data['deployments'].forEach(element => {
                    console.log(element);
                    var opt = document.createElement('option');
                    opt.value = element;
                    opt.innerHTML = element;
                    areaSelection.appendChild(opt);
                }); 
            }
        }
    );
}

function get_action_deployments() {
    console.log("--> get_action_deployments(): ");
    $.get(
        "/actiondeployments",
        function (data) {
            nluSelection.innerHTML = "";
            if (data['deployments'].length == 0){
                var opt = document.createElement('option');
                opt.value = "< no deployments >";
                opt.innerHTML = "< no deployments >";
                nluSelection.appendChild(opt);
            }
            else{
                data['deployments'].forEach(element => {
                    console.log(element);
                    var opt = document.createElement('option');
                    opt.value = element;
                    opt.innerHTML = element;
                    nluSelection.appendChild(opt);
                }); 
            }
        }
    );
}


function check_deployments(){
    get_area_deployments();
    get_action_deployments();

    console.log("--> check_deployments(): ");
    $.get(
        "/checkdeployments",
        function (data) {
            if (data){
                sendButton.disabled = false;
            }
            else{
                sendButton.disabled = true;
                sendButton.title = "There is no deployments available."
            }
        }
    );
}

function send_request(comment) {
    userData.payload.comment = comment;
    console.log("--> send_request():");
    $.ajax({
        method: "POST",
        contentType: "application/json",
        url: "/analyze",
        data: JSON.stringify(userData.payload),
        success: function (data) {
            console.log("response: ");
            console.log(data);

            update_face(userData.payload.satisfaction);
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

function update_models() {
    console.log(areaSelection.value);
    console.log(nluSelection.value);

    var models_payload = {"area": areaSelection.value, "action": nluSelection.value}

    console.log("--> update_models():");
    $.ajax({
        method: "POST",
        contentType: "application/json",
        url: "/updatemodels",
        data: JSON.stringify(models_payload),
        success: function (data) {
            console.log("response: ");
            console.log(data);

        },
        error: function (data, textStatus, errorThrown) {
            console.log("Error Response: ");
            console.log(data);
        },
        dataType: "json"
    });

}

function update_face(satisfaction) {
    if (satisfaction == 1) {
        responseFace.src = happyFaceSelectedPath;
    }
    else {
        responseFace.src = sadFaceSelectedPath;
    }
}

function select_happy() {
    happyFaceImage.src = happyFaceSelectedPath;
    sadFaceImage.src = sadFacePath;
    userData.payload.satisfaction = 1;
    sendButton.disabled = false;

    check_deployments();
}

function select_sad() {
    happyFaceImage.src = happyFacePath;
    sadFaceImage.src = sadFaceSelectedPath;
    userData.payload.satisfaction = 0;
    sendButton.disabled = false;

    check_deployments();
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
    if(modelSidebar.style.display === "block"){
        show_hide_model_sidebar();
    }
    if (sidebar.style.display === "none") {
        customerName.innerHTML = userData.username + " " + userData.lastname;
        sidebar.style.display = "block";
    }
    else {
        sidebar.style.display = "none"
    }

    check_deployments();
}

function show_hide_model_sidebar() {
    if(sidebar.style.display === "block"){
        show_hide_sidebar();
    }
    if (modelSidebar.style.display === "none") {
        modelSidebar.style.display = "block";
    }
    else {
        modelSidebar.style.display = "none"
    }

    check_deployments();
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

    document.getElementById("user-welcome").value = "Welcome, " + firstName.value + "!";

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


/* DISABLE NLU */
// var timeout = null;
// textInput.onkeyup = function (e) {
//     clearTimeout(timeout);
//     timeout = setTimeout(get_sentiment, 800);
// };
// function get_sentiment() {
//     var text = textInput.value;
//     console.log('Input Value:', text);

//     if (text.length > 10) {
//         console.log("sending request");
//         $.post(
//             "/analyzesent",
//             text,
//             function (data) {
//                 console.log(data)
//                 if (data === 'negative') {
//                     select_sad();
//                 }
//                 else {
//                     select_happy();
//                 }
//             }
//         );
//     }
//     else {
//         deselect_faces();
//     }
// }