// Import WebSocket instance from app.js
import { ws } from "./app.js";

// Declare variables
let currentResultSpan;
let resultSegment;
let timelineSegment;
let table_body;
let player;

// Initialize video list and index
let video_list = [];
let current_index = 0;

// Function to initialize page elements and event listeners
function init() {
    if (window.location.pathname === '/results') {
        // Get DOM elements
        currentResultSpan = document.getElementById('currentResult');
        resultSegment = document.getElementById('resultSegment');
        timelineSegment = document.getElementById("timelineSegment");
        table_body = document.getElementById('table_body');

        // Resize event listener for adjusting timeline height
        window.addEventListener("resize", function () {
            if (player) {
                timelineSegment.style.height = player.clientHeight + 28 + "px";
            }
        });

        // Previous and Next buttons event listeners
        document.getElementById('prevResult').addEventListener('click', function () {
            changeResult(-1);
        });
        document.getElementById('nextResult').addEventListener('click', function () {
            changeResult(1);
        });

        // Send command to WebSocket for videos
        let command = { function: "logic_videos", args: null };
        ws.send(JSON.stringify(command));
    }
}

// Function to change the current result index
function changeResult(offset) {
    current_index = (current_index + offset + video_list.length) % video_list.length;
    showResult();
}

// Function to set video list received from WebSocket
function setVideos(videos) {
    video_list = videos;
    showResult();
}

// Function to display the current result
function showResult() {
    currentResultSpan.textContent = video_list[current_index];
    let command = { function: "logic_result", args: video_list[current_index][0] };
    ws.send(JSON.stringify(command));
}

// Function to display result segment details
function showResultSegment(result) {
    // Display video or image based on file type
    const videopath = video_list[current_index][1];
    const fullname = videopath.split('/').pop();
    const name = fullname.split('.').shift();
    const extension = fullname.split('.').pop();
    currentResultSpan.textContent = `${name}`;
    if (extension === "mp4" || extension === "avi") {
        displayVideo(videopath, extension);
    } else {
        displayImage(videopath);
    }

    // Display detections in a table
    displayDetections(result['detections']);

    // Set timeline based on timestamps and frame rate
    setTimeline(result['timestamps'], video_list[current_index][2]);
}

// Function to display video
function displayVideo(videopath, extension) {
    resultSegment.innerHTML = '';
    player = document.createElement('video');
    player.setAttribute("class", "fit-image");
    player.setAttribute("controls", "true");
    player.innerHTML = `
        <source src="${videopath}" type="video/${extension}">
        Your browser does not support the video tag.
    `;
    resultSegment.appendChild(player);
}

// Function to display image
function displayImage(videopath) {
    resultSegment.innerHTML = `<img src="${videopath}" alt="Analysed image" class="fit-image">`;
}

// Function to display detections in a table
function displayDetections(detections) {
    table_body.innerHTML = '';
    for (let detection in detections) {
        const row = document.createElement('tr');
        const fish = document.createElement('th');
        fish.setAttribute('scope', 'row');
        fish.setAttribute('class', 'fw-semibold');
        fish.textContent = detection;
        const count = document.createElement('td');
        count.setAttribute('class', 'fw-normal');
        count.textContent = detections[detection];
        row.appendChild(fish);
        row.appendChild(count);
        table_body.appendChild(row);
    }
}

// Function to convert seconds to HH:MM:SS format
function toHHMMSS(sec_num) {
    var hours = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours < 10) {
        hours = "0" + hours;
    }
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    return hours + ':' + minutes + ':' + seconds;
}

// Function to set timeline based on timestamps and frame rate
function setTimeline(timestamps, frame_rate) {
    timelineSegment.innerHTML = "";
    for (let timestamp of timestamps) {
        let secs = Math.floor(timestamp[0] / frame_rate);
        const li = document.createElement('li');
        li.setAttribute("class", "border-top");
        const p = document.createElement('p')
        p.setAttribute("class", "mt-2 mb-1")
        const mark = document.createElement("mark")
        mark.setAttribute("class", "font-monospace rounded-2 fw-bold")
        mark.appendChild(document.createTextNode(toHHMMSS(secs)))
        p.appendChild(mark);
        p.appendChild(document.createTextNode(" " + timestamp[1]))
        li.appendChild(p)
        li.addEventListener('click', function () {
            player.currentTime = secs;
        })
        timelineSegment.appendChild(li)
    }
}

// Export necessary functions
export { init, setVideos, showResultSegment };
