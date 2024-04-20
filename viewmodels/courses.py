import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.courses import *

def load(cond = None):

  state, data = get_courses(cond)
  
  if state:
    data = [tuple(item.values()) for item in data]
  
  return state, data
