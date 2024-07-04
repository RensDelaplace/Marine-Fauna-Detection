# Imports
from datastore.store import DataStore

# Get datastore instance
ds = DataStore()

# Change advanced setting to args
# Called from frond end
async def logic_advanced_changeMode(args):
    ds.setSetting('advanced', args)
        
