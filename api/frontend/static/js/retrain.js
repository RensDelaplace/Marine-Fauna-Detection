// Import WebSocket instance from app.js
import { ws } from './app.js';

// Declare variables
let retrainbutton
let dataPathSpan
let selectDataset
let dataPath
let feedback

// Function to initialize page elements and event listeners
function init(){
    if (window.location.pathname === '/retrain') {
        // Get DOM elements
        retrainbutton = document.getElementById("retrain-button");
        selectDataset = document.getElementById('selectPathBtn');
        feedback = document.getElementById('feedback');
        dataPathSpan = document.getElementById('dataset-path');

        // Add event listeners
        selectDataset.addEventListener('click', choosePath)
        if (retrainbutton) {
            retrainbutton.addEventListener("click", retrain);
            retrainbutton.disabled=true
        }
    }
}

// Function to send command to choose dataset path
function choosePath() {
    let command = { function: "logic_directories_chooseDataset", args: null };
    ws.send(JSON.stringify(command));
}

// Function to set selected directory path and enable retrain button
function setDirectory(path){
    dataPath = path
    dataPathSpan.textContent = 'Dataset path: ' + dataPath;
    enableTrainButton()
}

// Function to enable retrain button
function enableTrainButton(){
    retrainbutton.disabled=false
}

// Function to trigger retraining process and disable retrain button
function retrain() {
    let nameInput = document.getElementById("nameInput").value;
    let numberInput = document.getElementById("numberInput").value;
    
    let name = nameInput || "new"; // Default is "latest"
    let epochs = numberInput || 45; // Default is 45

    // Ensure epochs is within the specified range
    if (isNaN(epochs)) {
        // If not a number, set the value to the minimum
        epochs = document.getElementById("numberInput").min;
    } else if (epochs < document.getElementById("numberInput").min) {
        // If less than minimum, set the value to the minimum
        epochs = document.getElementById("numberInput").min;
    } else if (epochs > document.getElementById("numberInput").max) {
        // If greater than maximum, set the value to the maximum
        epochs = document.getElementById("numberInput").max;
    }
    retrainbutton.disabled=true
    let command = { function: "logic_model_train", args: {name: name, epochs: parseInt(epochs)} };
    ws.send(JSON.stringify(command));
}

// Function to update feedback message
function retrain_feedback(args)
{
 feedback.textContent = args 
}

// Export necessary functions
export {
    retrain,
    init,
    setDirectory,
    retrain_feedback
};