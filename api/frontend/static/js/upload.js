// Import WebSocket instance from app.js
import { ws } from './app.js';

// Declare variables
var command;
var path_list
var fileSelectFeedback
var fileButton
var progressList
var buttonContainer

// Initialize settings page elements and event listeners
function init(){
    if (window.location.pathname === '/upload') {
        fileButton = document.getElementById("fileButton");
        fileSelectFeedback = document.getElementById("fileSelectFeedback");
        buttonContainer = document.getElementById("button-container")
        fileButton.addEventListener("click", openFile);
        progressList = document.getElementById("progressList")
        ws.send(JSON.stringify({function:"logic_files_clearFiles",args:null}));
        disableButton()
        reloadPage()        
    }
}

// Function to receive backend busy state
// Called from backend
function upload_receiveBusyState(args){
    swapButton(!args)
}

// Function to querry the backend for most recent changes
function reloadPage(){
    ws.send(JSON.stringify({function:"logic_files_updateUpload",args:null}))
    ws.send(JSON.stringify({function:"logic_progress_updateFrontendProgress",args:null}));
    ws.send(JSON.stringify({function:"logic_model_getBusyState",args:null}));
}

// Function to ask backend to open file explorer
function openFile() {
    command = { function: "logic_files_addFiles", args: null };
    ws.send(JSON.stringify(command));
}

// Function to ask backend to remove file from list
function removeFile(event){
    event.stopPropagation();
    var index = event.target.getAttribute("index")
    command={function:"logic_files_removeFiles",args:index}
    ws.send(JSON.stringify(command));
    command={function:"logic_progress_removeProgress",args:index}
    ws.send(JSON.stringify(command));
    reloadPage()
}

// Function that swaps button function
function swapButton(setAnalyse){
    buttonContainer.innerHTML=""
    var button = document.createElement("button")
    button.setAttribute("type","button")
    if(setAnalyse){
        button.setAttribute("id","button")
        button.innerHTML="Analyse"
        button.addEventListener("click", analyse);
    }else{
        button.setAttribute("id","button")
        button.innerHTML="Abort"
        button.addEventListener("click", abort)
    }
    buttonContainer.appendChild(button)
}

// Function that dissables the button
function disableButton(){
    var button = document.getElementById("button")
    if(button!=null)
        button.disabled=true 
}

// Function that enables the button
function enableButton(){
    var button = document.getElementById("button")
    if(button!=null)
        button.disabled=false
}

// Function displaying selected file info
// Called from backend
function upload_showFilePath(paths) {
  // Clear existing content
  path_list = paths
  document.getElementById("column-0").innerHTML = "";
  document.getElementById("column-1").innerHTML = "";

    // Change button if needed
    if(paths.length==0)
    {disableButton()}
    else{enableButton()}

    // Make display element for all files
    for (var index in paths) {
        var short = paths[index].split(/\\|\//).pop();
        var li = document.createElement("li");
        li.setAttribute("class", "list-group-item");

        // Create a div to hold video name and remove button
        var contentDiv = document.createElement("div");
        contentDiv.setAttribute("class", "d-flex justify-content-between align-items-center");

        // Display the video name
        var name = document.createElement("p");
        name.innerHTML = short;
        contentDiv.appendChild(name);

        // Create the remove button
        var bt = document.createElement("button");
        bt.setAttribute("type", "button");    
        bt.setAttribute("class", "remove-button");
        bt.setAttribute("index", index);
        bt.setAttribute("aria-hidden", "true");
        bt.innerHTML = "&times;";
        bt.addEventListener("click", (event) => {
            removeFile(event)
        }, { capture: true });

        // Append the remove button to the div
        contentDiv.appendChild(bt);

        // Append the div to the list item or any other container
        // For example, assuming 'li' is your list item:
        li.appendChild(contentDiv);

        // Append the div to the list item
        li.appendChild(contentDiv);

        // Decide which column to add the video to
        var columnId = (index % 2 === 0) ? "column-0" : "column-1";
        document.getElementById(columnId).appendChild(li);
        ws.send(JSON.stringify({function:"logic_model_getBusyState",args:null}));
    }
}

// Function that calls backend to start analysing selected files
function analyse(){
    command={function:"logic_model_analyse",args:path_list}
    ws.send(JSON.stringify(command));
    disableButton()
    
    
}

// Function that calls backend to abort analysing
function abort(){
    ws.send(JSON.stringify({function:"logic_model_abort",args:null}));
    disableButton()
    for(var bar of document.getElementsByClassName("progress-bar")){
        bar.setAttribute("class","progress-bar bg-canceled")
    }
}

// Function updating progressbar displays
// Called from backend
function upload_updateProgress(args){
    var ul = document.getElementById("progressList")
    // clear all progressbars
    ul.innerHTML=""
    for(var p of args){
        var progress = JSON.parse(p)
        create_progressbar(progress.index,progress.value,progress.max,progress.label,ul)
    }
    ws.send(JSON.stringify({function:"logic_model_getBusyState",args:null}));
}

// Function creating new progressbar
function create_progressbar(index,value,maxValue,name,parent){
    // Create list element
    var li = document.createElement("li")
    // Create progress bar title
    var h = document.createElement("h6")
    h.innerHTML=name
    li.appendChild(h)
    // Create progress bar itself
    var bar= document.createElement("div")
    bar.setAttribute("class","progress")
    li.setAttribute("id",`progressbar${index}`)
    // Create inside of progress bar
    var bardiv = document.createElement("div")
    bardiv.setAttribute("class","progress-bar bg-danger")
    bardiv.setAttribute("role","progressbar")
    bardiv.setAttribute("aria-valuemin",0)
    bardiv.setAttribute("aria-valuemax",maxValue)
    bardiv.setAttribute("aria-valuenow",value)
    bardiv.setAttribute("style","width:"+(value*100/maxValue).toFixed(2)+"%")
    bar.appendChild(bardiv)
    var barspan = document.createElement("span")
    barspan.setAttribute("class", "progress-label");
    barspan.innerHTML=(value*100/maxValue).toFixed(2)+"%"
    li.appendChild(bar)
    li.appendChild(barspan)
    parent.appendChild(li)
    //if bar is full -> make it green
    if(parseInt(value)>=parseInt(maxValue)){
        bardiv.setAttribute("class","progress-bar bg-success")
    }
}

// Export necessary functions
export { openFile, removeFile, analyse, upload_showFilePath,upload_updateProgress,upload_receiveBusyState, init };
