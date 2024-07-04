#Imports
from starlette.templating import Jinja2Templates
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
templates_dir = os.path.join(base_dir, "frontend/templates")

print(f"template dir: {templates_dir}")

# region Configure Jinja2
template = Jinja2Templates(directory=templates_dir)