import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.students import *

def load(cond = None):

  column_list = ['id', 'name', 'Dob', 'gender', 'Tel', 'role_id', 'class_id']

  state, data = get_students(cond)

  if state:
    data_list = []
    for item in data:
        new = {key : item[key] for key in column_list}

        data_list.append(tuple(new.values()))
  
    return state, data_list 
  
  return state, data