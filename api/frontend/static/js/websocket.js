// Object to map function names to their implementations
const functionMap = {};

// Function to register a function with a given name
export function registerFunction(name, func) {
    functionMap[name] = func;
}

// Function to establish a WebSocket connection
export function connectWebSocket() {
    let port = window.location.port
    let ws = new WebSocket(`ws://localhost:${port}/ws`);
    console.log("ws start")
    
    // WebSocket event listener for incoming messages
    ws.addEventListener("message", (event) => {
        const command = JSON.parse(event.data); // Parse received JSON data
        try {
            const func = functionMap[command.function];
            if (typeof func === 'function') {
                func(command.args);
            } else {
                console.error(`Function '${command.function}' not found.`);
            }
        } catch (error) {
            console.error(error);
        }
    });

    return ws;
}
