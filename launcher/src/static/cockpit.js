function hideOnLoad(id) {
     let details = document.getElementById(id);
     details.open = true;
}

function changeViewOfTasksDetails(id) {
    let details = document.getElementById(id);
    if(details.open){
        details.open = false;
    }
    else {
        details.open = true;
    }
}


document.addEventListener('DOMContentLoaded', function() {
    let ctStatusList = document.getElementsByClassName('ctListElemStatus')
    for (i=0; i<ctStatusList.length; i++) {
        let taskID = ctStatusList[i].id.split('_')[ctStatusList[i].id.split('_').length - 1];
        getTaskStatus(taskID);
    }
}, false);

//document.addEventListener('DOMContentLoaded', checkLogin, false);


function getTaskStatus(task_id) {
    if(task_id) {
        let statusRequest = new XMLHttpRequest;
        statusRequest.responseType = 'json';
        let url = 'https://enigmatic-hollows-51365.herokuapp.com/machine-manager/launcher/computations/'.concat(task_id);
        statusRequest.open('GET', url, true);
        statusRequest.onload = function() {
            let resp = statusRequest.response;
            console.log(resp);
            let statusTextID = 'statusText_'.concat(task_id);
            let statusTextDetailsID = 'statusTextDetails_'.concat(task_id);
            let statusText = document.getElementById(statusTextID);
            let statusTextDetails = document.getElementById(statusTextDetailsID);
            statusText.textContent = resp['status'] == null ? "unknown" : resp['status'];
            statusTextDetails.textContent = resp['status'] == null ? "unknown" : resp['status'];
        };
    statusRequest.send();
    }
}
/*
function checkLogin() {
    let loginField = document.getElementById("userName");
    if (loginField.innerText.split(":")[1] == "None"){
        retakeLogin(loginField)
    }
}

function retakeLogin(loginField) {
    let loginGetter = new XMLHttpRequest;
    let url = "/retake/login/for/user";

    loginGetter.open("GET",url);
    loginGetter.onload = () => {
        let newName = loginGetter.responseText;
        console.log(newName);
        if(newName & newName != "None"){
            let loginText = loginField.innerText.split(":")[0];
            loginField.innerText = loginText + ":" + newName;
        }
    }
}
 */
