eel.expose(updateImageSrc);
function updateImageSrc(val) {
    let elem = document.getElementById('previewimg');
    elem.src = "data:image/png;base64," + val;
}

function startStream() {
    eel.startStream();
    document.getElementById('startstop').innerHTML = 'Stop Stream';
}

function closeBrowser(){
    printInfo('We here homie')
    eel.close();
    printInfo('We there homie')
}

function printInfo(info) {
    //document.getElementById('info').innerHTML = info;
}

function showTab(event,tabType){

    var tabs;

    tabs = document.getElementsByClassName("tabcontent");
    for(var i = 0; i<tabs.length; i++){
        tabs[i].style.display="none";
    }
    

    document.getElementById(tabType).style.display = "block";
    //event.currentTarget.className +=" active";
}

function showButton(buttonType){

    var buttons;

    buttons = document.getElementsByClassName("buttonExplain");
    for(var i = 0; i<buttons.length; i++){
        buttons[i].style.display="none";
    }
    

    document.getElementById(buttonType).style.display = "block";
    //event.currentTarget.className +=" active";
}

function changeFGColor(event){
    printInfo("Foreground"+event.target.value);
    eel.setFGColor(event.target.value);
}

function changeBGColor(event){
    printInfo("Background"+event.target.value);
    eel.setBGColor(event.target.value);
}

function handleKeyboard(event){
    //printInfo(event.target.innerHTML)
    //document.getElementById("textbox").append(event.target.innerHTML)
    if(event.target.className.includes("keyboard__key")){
        printInfo(event.target.innerHTML);
        let currentString = document.getElementById("textinput").value
        let carretPos = document.getElementById("textinput").selectionStart
        if(event.target.innerHTML == "Space") {
            document.getElementById("textinput").value = currentString.substring(0,carretPos) + " " + currentString.substring(carretPos)
        } else if (event.target.innerHTML == "Backspace") {
            document.getElementById("textinput").value = currentString.substring(0,carretPos-1) + currentString.substring(carretPos)
        } else {
            document.getElementById("textinput").value = currentString.substring(0,carretPos) + event.target.innerHTML + currentString.substring(carretPos)
        }
    }
    else{
        printInfo("aint no KEY DOG")
    }
}

eel.expose(updateStatus)
function updateStatus(cvStatus, btStatus, frameTime) {
    let fps = frameTime.toString();

    document.getElementById("cvstatus").innerHTML = "CV Status: " + cvStatus;
    document.getElementById("btstatus").innerHTML = "Bluetooth: " + btStatus;
    document.getElementById("framerate").innerHTML = "FPS: "+ fps;
}

