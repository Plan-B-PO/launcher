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
