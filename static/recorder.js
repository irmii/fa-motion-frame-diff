var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");
var buttonCameraOn = document.getElementById("cameraon");
var buttonCameraOff = document.getElementById("cameraoff");
var video=document.getElementById("video");
var placevideo=document.getElementById("videoplace");

buttonStop.disabled = true;
buttonRecord.disabled = true;
buttonCameraOff.disabled = true;

video.style.display = 'none';

buttonCameraOn.onclick = function() {
    buttonCameraOn.disabled = true;
    buttonCameraOff.disabled = false;
    buttonRecord.disabled = false;

    video.style.display = 'flex';

};

buttonCameraOff.onclick = function() {
    buttonCameraOn.disabled = false;
    buttonCameraOff.disabled = true;
    buttonStop.disabled = true;
    buttonRecord.disabled = true;

    video.style.display = 'none';
};

buttonRecord.onclick = function() {
    // var url = window.location.href + "record_status";
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    
    // disable download link
    var downloadLink = document.getElementById("download");
    downloadLink.text = "";
    downloadLink.href = "";

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" }));
};

buttonStop.onclick = function() {
    buttonRecord.disabled = false;
    buttonStop.disabled = true;    

    // XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // enable download link
            var downloadLink = document.getElementById("download");
            downloadLink.text = "Download Video";
            downloadLink.href = "/static/video.mp4";
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false" }));
};


