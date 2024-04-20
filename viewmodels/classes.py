import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from models.Class import Class

obj = Class()

def load(cond = None):
  if cond is None:
    return obj.read()
  else:
    return obj.read(cond)