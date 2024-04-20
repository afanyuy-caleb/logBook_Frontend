import requests
from requests.exceptions import HTTPError

url = "http://127.0.0.1:5000/class_courses"

def get_course_info(condition = None):
    try:
      if condition:
        response = requests.get(
          url,
          params={'condition': condition}
        )
      
      else:
        response = requests.get(url)
          
      response.raise_for_status()

    except HTTPError as http_err:
      return False, f"HTTP error occurred: No record found"

    except Exception as err:
      return False, f"Other error occurred: {err}"

    else:
      return True, response.json()


def update_course_info(json_data):
  try:

    response = requests.post(url, json=json_data)
    response.raise_for_status()

  except HTTPError as http_err:
    return False, f"HTTP error occurred: {http_err}"

  except Exception as err:
    return False, f"Other error occurred: {err}"

  else:
    return True, "Data inserted successfully"
  