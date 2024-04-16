import sys

from views import student
sys.path.append(r'C:\Users\Uzer\Desktop\python\logBook')
import os

from flask import Flask

from tkinter import *
from views import signIn, student, shared_data

if __name__ == "__main__":

  signIn.SignIn()

  if shared_data.studInfo:

    student.studentHome()