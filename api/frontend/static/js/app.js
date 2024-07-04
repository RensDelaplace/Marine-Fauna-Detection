import { connectWebSocket, registerFunction } from './websocket.js';
import * as settingFunctions from './settings.js';
import * as retrainFunctions from './retrain.js';
import * as uploadFunctions from './upload.js';
import * as resultFunctions from './results.js';

// Establish WebSocket connection
export const ws = connectWebSocket();
ws.addEventListener("open", initialize);

function initialize(){
    loadPage(window.location.pathname);
}

function loadPage(fileName) {
    fetch(`getHTML${fileName}`)
    .then(response => response.text())
    .then(html => {
        document.getElementById("htmlWindow").innerHTML = html;
    }).then(onPageLoad);
}

// Function to handle page-specific actions after loading
function onPageLoad(){
    // Register functions based on the current page path
    if (window.location.pathname === '/retrain') {
        // Register retrain-related functions
        registerRetrainFunctions();
    } else if (window.location.pathname === '/upload') {
        // Register upload-related functions
        registerUploadFunctions();
    } else if (window.location.pathname === '/settings') {
        // Register settings-related functions
        registerSettingsFunctions();
    } else if (window.location.pathname === '/results') {
        // Register results-related functions
        registerResultsFunctions();
    }
}

// Register retrain-related functions
function registerRetrainFunctions() {
    registerFunction('retrain', retrainFunctions.retrain);
    registerFunction('retrain_setDirectory', retrainFunctions.setDirectory);
    registerFunction('retrain_feedback', retrainFunctions.retrain_feedback);
    retrainFunctions.init.apply();
}

// Register upload-related functions
function registerUploadFunctions() {
    registerFunction('openFile', uploadFunctions.openFile);
    registerFunction('removeFile', uploadFunctions.removeFile);
    registerFunction('analyse', uploadFunctions.analyse);
    registerFunction('upload_showFilePath', uploadFunctions.upload_showFilePath);
    registerFunction('upload_initiateProgress', uploadFunctions.upload_initiateProgress);
    registerFunction('upload_incrementProgress', uploadFunctions.upload_incrementProgress);
    registerFunction('upload_updateProgress', uploadFunctions.upload_updateProgress);
    registerFunction('upload_receiveBusyState', uploadFunctions.upload_receiveBusyState);
    uploadFunctions.init.apply();
}

// Register settings-related functions
function registerSettingsFunctions() {
    registerFunction('settings_setDirectory', settingFunctions.setDirectory);
    registerFunction('settings_setModel', settingFunctions.setModel);
    settingFunctions.init.apply();
}

// Register results-related functions
function registerResultsFunctions() {
    registerFunction('logic_videos', resultFunctions.setVideos);
    registerFunction('logic_result', resultFunctions.showResultSegment);
    resultFunctions.init.apply();
}
