# Repository Structure 
 
## project 
Main directory of project. 
 
- **ML_model:** 
  Bevat `model.py` (interface voor modelinteractie) en `best.pt` (beste modelversie). 
 
- **api:** 
  - **frontend:** 
    - **static:** 
    static js,css and images. 
    - **templates:** 
    html files 
  - **frontend:** 
  all backend logic of the application 
  - **routers:** 
  all routers and enpoints of the API 
     
  - **api_app.py:**  
  core file of backend application 
 
- **datastore:** 
  all things related to the database 
- **ML_model:** 
  Code that runs the models
- **Model testing:** 
  used for testing models 
- **models:** 
  default location of models
- **results:** 
  default location of output videos
- **tests:** 
  unit and integration tests
- **datastore.db:** 
  used database
- **main.py:** 
  application startup script
- **yolov8n.pt:** 
  used for model retraining

 
## test-input 
contains short video's used for testing
 
## Installation guide
 
### how to install using the windows installer: 
 
1. **Download the Installer:** 
    - click here: [Download Installer](http://157.193.171.40:8080/) 
    - choose wildlife1_setup.zip 
    - In case of a warning, ignore the warning and download anyway 
 
2. **Go to the recently downloaded file (defult location is downloads)** 
 
3. **Unzip the files:** 
    - Right click the .zip file. 
    - choose "extract here". 
 
4. **Open recently extracted folder** 
5. **Start the Installer as Administrator:** 
    - Right click  'Marine_Fauna_Detection_Wildlife1_Sprint3_setup.exe' and choose run as administrator
    - In case of a "Windows protected your pc" pop-up, click on "More info" and then on "Run anyway"
6. **Follow the steps of the instalation wizard** 
7. **Starting the Applicatie:** 
    - Search for ‘JDN MARED Maurine Fauna Detection Wildlife1’ (or the custom name chosen in step 7) using the windows search bar. 
    - Start the application as administrator: right click the search result. choose 'Run as administrator'. 
    - In some cases, windows will ask for a password. If you don't know this password, contact your IT-manager. 
    - The startup proces could take some time, be patient even when nothing seems to be happening. 
 
### how to install using gitlab source code: 
 
1. **Clone the GitLab repository :** 
    - Open the git command line in a chosen directory. 
    - run the following code:
    ``` git clone https://gitlab.stud.atlantis.ugent.be/vop2324/wildlife1 ```
    - Log in if needed. 
    - the source code should now be in the chosen directory. 
 
2. **In case your device does not have python, install it using the following installation guide:** [Python Installation guide](https://wiki.python.org/moin/BeginnersGuide/Download) 
 
3. **Making and activating conda environments for dependencies:** 
    - In case you don't have conda, install it using the following installation guide: [Conda installation guide](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). 
    - Open a terminal and navigate to the root folder of the project
    - Create a new environment using the following code:```conda create --name myenv --file spec-file.txt python=3.11``` 
    - to activate the new environment run: `conda activate <env_name>` 
    
5. **Edit the ultralytics-package:** 
    - Navigate to the directory where anaconda is installed (default C:\Program Files or C:\Program Files (x86)\anaconda3). 
    - Go to the folowing directory `Env>*environment name*>lib>site-packages>ultralytics>engine>`. 
    - Open the file `predictor.py`. 
    - On line 363, replace `suffix, fourcc = (".mp4", "avc1") if MACOS else (".avi", "WMV2") if WINDOWS else (".avi", "MJPG")` with `suffix, fourcc = (".mp4", "h264")`. 
 
6. **Start the application:** 
    - With a terminal with the environment active, navigate to the project folder. 
    - Run: `python main.py` 
    - In case of problems with the display of the result video's, run: `pip install opencv-contrib-python av` restart the application. 
 
 
## User manual 
 
### Preparation: 
**Test video's:** short test-videos can be found on Ugent-onedrive https://ugentbe-my.sharepoint.com/:f:/g/personal/rens_delaplace_ugent_be/Er8cSz7iYThDmE8byqJpd8YBiaMZLfn3KPsDwc5OvOAkJg?e=iNtfCb 
 
1. **Navigate to "settings".** 
2. **Choose export path for results.** 
   - under 'Export Destination' choose 'Select Path'. 
   - Navigate to and select a folder where result video's wil be exported to. 
 
3. **Select a model.** 
   - Under 'Current model' click 'Select model'. 
   - Navigate to and select the folder where the model of choice is stored
   
 
**Note:**  
A model is a folder containing the folder ‘weights’ and ‘args.yml’alongside other information about the model. The model must be located in the "models" folder of the project for it to work. The button ‘Select model’ opens this folder. When attempting to select a model outside the folder, an error message wil be displayed. 
 
### Analyse video: 
 
4. **Navigate to "upload".** 
5. **Click ‘Select video’s’ to select the videos you want to analyse.** 
   - make sure the file type (bottom right of the explorer) is set on ‘Videos (*.mp4)’. 
   - Selecteer the videos. 
   - Click ‘Open’. 
   - The selected videos wil be shown in a display window
 
6. **Selected a wrong video?** 
   - You can deselect a video by pressing the cross next to its name in the display window
 
7. **Click ‘Analyse’ to start the analyse procces.** 
   - Wait until the analysis is complete, depending on the video length this can take a long time. 
   - If for any reason you want to cancel the analysis, you can click the abort button to abort all files. Deselecting a file mid analysis will also cancel that video from being analysed without interupting the rest. 
 
**Note:**  
When analysing, you can view the results of videos that have already been completed or the result of previous ones. 
 
### Inspecting the results: 
 
1. **Navigate to "results".** 
2. **Navigate between the videos and watch the results:** 
   - The analysed video will be displayed (depending on the lenght this can take some time)
   - Use the arrows to navigate between results of difrent videos.  
   - For every fish spotted, there will be a list with timestamps of when the fish is on the screen.
   - By clicking one of these timestamps, the video will show the frame where the fish has been spotted. 
   - A list of all fish species and the number spotted in the video is located under the video. 
 
### Retrain the model: 
 
8. **Enable advanced mode:** 
   - If "retrain" is not available on the banner, go to "settings". 
   - Toggle the "advanced mode" button. 
 
9. **Navigate to "retrain".** 
   - Scroll to ‘Make new model’. 
   - Make sure you have an anotated dataset. 
   - Select a dataset by clicking ‘Select path’ and navigate to the dataset of choice. 
   - Select the folder containing ‘Test’, ‘Train’ and ‘Valid’. 
   - Click ‘Select folder’. 
    
10. **Optional:** 
   - Choose a name for the model (standard set to ‘latest’). 
   - Choose number of epochs (standard set to 45). 
 
11. **Click ‘Retrain’ wait until it is done.** 
   - Check the feedback at the bottom of the page. 
   - Once finished, the new model can be found in `/models`. 
 
**Note:**  
If a model with the same name already exists (for example ‘latest’), the new model will receive the name 'latest2’. 
 
 For a more detailed instruction manual, check out the project report 
 
