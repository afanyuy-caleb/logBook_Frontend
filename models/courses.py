import sqlite3 as sq
from .constants import PATH_TO_DB

class Courses:
  
  table = 'courses'

  def create(self):
    try:

      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()
      
        # Create Courses table
        query = f"CREATE TABLE IF NOT EXISTS {self.table} (course_id INTEGER PRIMARY KEY, course_name varchar(15) UNIQUE, teacher varchar(40))"

        cur.execute(query)
        conn.commit()

        conn.close()
        return True, ''
      
    except sq.Error as err:
      return False, err


  def write(self, list):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        for row in list:
          insert = f"INSERT INTO {self.table} (Courses_id, Courses_name) VALUES (?, ?)"
          cur.execute(insert, row)
          conn.commit()

        conn.close()
      return True, ''

    except sq.Error as err:
      return False, err
  
  def update(self, updateData, condition):
    try:
      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        update_query = f"UPDATE {self.table} set {updateData} WHERE {condition}"

        cur.execute(update_query)
        conn.commit()

        conn.close()

        return True, ''
    
    except sq.Error as err:
      return False, err
  
  def read(self, condition=None):
    try:
       with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()

        if condition is None:
          sel = f"SELECT * FROM {self.table}"
        else:
          sel = f"SELECT * FROM {self.table} WHERE {condition}"

        cur.execute(sel)
        result =  cur.fetchall()

        return True, result
    
    except sq.Error as e:
      return False, e
  
  def delete(self, condition):
    try:
       with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()
     
        query = f"DELETE FROM {self.table} WHERE {condition}"
        cur.execute(query)
        conn.commit()

        return True, ''

    except sq.Error as err:
      return False, err