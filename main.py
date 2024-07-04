if __name__ == "__main__":
    # basic imports
    import multiprocessing
    import signal
    import os
    import sys
    import threading

    # fastapi imports
    from fastapi import Response

    # pyWebview imports
    import webview

    # import the api_app from the api module
    from api.api_app import app

    # make sure no forks of exe are started
    multiprocessing.freeze_support()

    # define used address and port for local webserver
    localhost = "127.0.0.1"
    from random_open_port import random_port
    port = random_port()  # TODO: change to 'random'/unused port


    # region define run and shutdown for fastapi/webserver
    def run_fastapi():
        import uvicorn
        uvicorn.run(app, host=localhost, port=port)


    def shutdown():

        # when frozen (running as exe) move result videos out of temp dir
        if getattr(sys, 'frozen', True):
            from utils.file_manager import save_results
            from datastore.store import DataStore
            datastore = DataStore()
            exportPath = datastore.getSetting("exportPath")
            if not exportPath:
                exportPath = os.path.expanduser("~/Desktop/MARED_Marine_fauna_detection")
            save_results(exportPath)
            # remove results from database when app is closed
            datastore.clearResults()

        os.kill(os.getpid(), signal.SIGTERM)
        return Response(status_code=200, content="Server shutting down...")


    # endregion

    # Start FastAPI app in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    # region pyWebview code
    window = webview.create_window(
        "Marine fauna detection",
        f"http://{localhost}:{port}",
        resizable=True,
        height=700,
        width=1000,
        frameless=False,
        easy_drag=True,
        on_top=False,
        confirm_close=True
    )

    # Add shutdown function so process is killed when window is closed
    window.events.closed += shutdown

    webview.start()
    # endregion

