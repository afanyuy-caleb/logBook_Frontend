import sqlite3 as sq
from .constants import PATH_TO_DB

class Students:
  
  table = 'students'

  def table_create(self):
    try:

      with sq.connect(PATH_TO_DB) as conn:
        cur = conn.cursor()
      
        # Enable foreign key support 
        cur.execute('PRAGMA foreign_keys = ON')

        # Create role table
        query = '''CREATE TABLE IF NOT EXISTS students (
          id INTEGER PRIMARY KEY, 
          name varchar(50) UNIQUE COLLATE NOCASE,
          Dob DATE,
          gender char(2) CHECK(gender IN('M', 'F')),
          Tel varchar(12),
          role_id INTEGER default 2,
          class_id INTEGER,
          FOREIGN KEY(role_id) REFERENCES role(role_id),
          FOREIGN KEY(class_id) REFERENCES role(class_id)
          
        )'''
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
            query = f"INSERT INTO {self.table} VALUES(?, ?, ?, ?, ?, ?, ?)"
            cur.execute(query, row)
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
          query = f"SELECT * FROM {self.table}"
        else:
          query = f"SELECT * FROM {self.table} WHERE {condition}"

        cur.execute(query)
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

    except sq.Error as e:
      return False, e