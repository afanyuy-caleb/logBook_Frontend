import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.class_courses import *
import views.shared_data as shared

import json

def get_course_details(cond = None):

  state, data = get_course_info(cond) if cond else get_course_info()
  
  if state:
    data = [tuple(item.values()) for item in data]
  
  return state, data


def add_course_details(date, desc = None, img = None, cour_id = None):

  if shared.studInfo:
    studData = shared.studInfo

    if date == "":
      return False, 'Please enter the date'
    else:
      if not desc and not img:
        return False, "Either description or the image must be provided"
    
    # Convert the information into a Dictionary
    courseInfo_Dict = {}

    courseInfo_Dict['date'] = date
    courseInfo_Dict['desc'] = desc
    courseInfo_Dict['img'] = img

    cond = f"course_id = {cour_id} AND class_id = {studData['class_id']}"
    stat, data = get_course_info(cond)

    if stat:

      if data[0]['course_info'] is None:
        infoList = []
        
      else:
        infoList = json.loads(data[0]['course_info'])
      
      infoList.append(courseInfo_Dict)
      json_info = json.dumps(infoList)

      # update the DB
      update_data = {
        'course_id': cour_id,
        'class_id': studData['class_id'],
        'course_info': json_info
        }

      update = update_course_info(update_data)

      if update[0]:
        return True, 'Course Info added successfully'

      else:
        return False, update[1]

    else:
      return False, "No record found"
    
  else:
    return False, "Theres nothing there"

