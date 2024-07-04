import sys, os, shutil, datetime
from datetime import datetime

def get_project_folder():
    # path of main .py or .exe when converted with pyinstaller
    if getattr(sys, 'frozen', False):
        project_path = sys._MEIPASS
    else:
        script_folder = os.path.dirname(os.path.abspath(__file__))
        project_path = os.path.dirname(script_folder)
    return project_path


# define constants to be imported in other file
PROJECT_DIR = get_project_folder()
VIDEO_RESULTS_DIR = os.path.join(PROJECT_DIR,"results")
ML_MODELS_PATH = os.path.join(PROJECT_DIR,"models")

def save_results(save_dir):
    """
    Saves video's / retrained model to folder chosen by user so they dont get lost when temp folder is removed
    """

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    save_dir_with_time = os.path.join(save_dir, current_datetime)

    shutil.move(VIDEO_RESULTS_DIR, save_dir_with_time)

def copy_ML_model(src):

    '''
    Copy files form the selected model (on users device) to temp folder
    '''

    orignal_model_path = os.path.join(ML_MODELS_PATH, "latest")

    # Delete the destination directory if it exists
    if os.path.exists(orignal_model_path):
        shutil.rmtree(orignal_model_path)

    os.makedirs(orignal_model_path)

    # Copy contents from the source to the destination directory
    # for item in os.listdir(src):
    #     src_item = os.path.join(src, item)
    #     dest_item = os.path.join(orignal_model_path, item)
    #     print("moving item to: ",dest_item)
    #     if os.path.isdir(src_item):
    #         shutil.copytree(src_item, dest_item)
    #     else:
    #         shutil.copy2(src_item, dest_item)

    # only copy data needed for html (since it needs to be relative to the html templates)
    # rest of the model (used by python code) can be accessed absolute path
    src_item = os.path.join(src, "confusion_matrix.png")
    dest_item = os.path.join(orignal_model_path, "confusion_matrix.png")
    print("moving item to: ", dest_item)
    shutil.copy(src_item, dest_item)


def save_retrained_model(save_dir, model_name="latest1"):
    """
    Saves video's / retrained model to folder chosen by user so they dont get lost when temp folder is removed
    """

    model = os.path.join(ML_MODELS_PATH, model_name)

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # timestamp so user sees when model was saved
    save_dir_with_time = os.path.join(save_dir, current_datetime)

    # add name entered by user in GUI + "_MLModel" to make clear it a MLModel
    save_dir_model = save_dir_with_time + "_" + model_name + "_MLModel"

    shutil.move(model, save_dir_model)
