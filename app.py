import sys, os
current_dir = os.getcwd()
sys.path.append(current_dir)

from views import student

from flask import Flask

from tkinter import *
from views import signIn, student, shared_data

if __name__ == "__main__":

  signIn.SignIn()

  if shared_data.studInfo:

    student.studentHome()