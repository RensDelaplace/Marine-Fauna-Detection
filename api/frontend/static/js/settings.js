// Import WebSocket instance from app.js
import { ws } from './app.js';

// Declare variables
let resultsPathSpan = null;
let outputPath = null;
let modelPathSpan = null;
let advancedToggle = null;

// Initialize settings page elements and event listeners
function init(){
    if (window.location.pathname === '/settings') {
        
        const selectPathBtn = document.getElementById('selectPathBtn');
        advancedToggle = document.getElementById('toggle');
        resultsPathSpan = document.getElementById('results-path');

        selectPathBtn.addEventListener('click', choosePath);
        advancedToggle.addEventListener('change', advanced);

        // Get the value of 'advanced' from the hidden input
        const advancedValue = document.getElementById("advancedSetting").value;

        // Check if 'advanced' is true and set the toggle accordingly
        if (advancedValue == 1 || advancedValue == true) {
            advancedToggle.checked = true; // Toggle inschakelen
        } else {
            advancedToggle.checked = false; // Toggle uitschakelen
        }

        const selectModelBtn = document.getElementById('selectModelBtn');
        modelPathSpan = document.getElementById('model-path');
        selectModelBtn.addEventListener('click', chooseModel);
        
    }
}

// Function to choose output path
function choosePath() {
    let command = { function: "logic_directories_chooseDir", args: null };
    ws.send(JSON.stringify(command));
}

// Function to choose model path
function chooseModel() {
    let command = { function: "logic_directories_chooseModel", args: null };
    ws.send(JSON.stringify(command));
}

// Function to set output directory path
function setDirectory(path){
    outputPath = path
    resultsPathSpan.textContent = 'output Path: ' + outputPath;
}

// Function to set current model path
function setModel(path){
    outputPath = path
    modelPathSpan.textContent = 'Current model: ' + outputPath;
}

// Function to handle toggling advanced mode
function advanced() {
    let command = { function: "logic_advanced_changeMode", args: this.checked };
    ws.send(JSON.stringify(command));
    window.location.href = "/settings";
}

// Export necessary functions
export {setDirectory, setModel, init}