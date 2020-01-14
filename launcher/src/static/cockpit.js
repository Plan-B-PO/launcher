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



function getTaskStatus(task_id) {
    let statusRequest = new XMLHttpRequest;
    let url = '/status/'.concat(task_id);
    statusRequest.open('GET', url);
    statusRequest.onload = function() {
        let data = JSON.parse(statusRequest.responseText);
        let statusTextID = 'statusText_'.concat(task_id);
        let statusTextDetailsID = 'statusTextDetails_'.concat(task_id);
        let statusText = document.getElementById(statusTextID);
        let statusTextDetails = document.getElementById(statusTextDetailsID);
        statusText.textContent = data['status'];
        statusTextDetails.textContent = data['status'];
    }
    statusRequest.send();
}
