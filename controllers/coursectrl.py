import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.courses import Courses

obj = Courses()

def load(cond = None):
  if cond is None:
    return obj.read()
  else:
    return obj.read(cond)
