import requests
from requests.exceptions import HTTPError

def get_courses(condition = None):
    url = "http://127.0.0.1:5000/courses"

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
      return False, f"HTTP error occurred: {http_err}"

    except Exception as err:
      return False, f"Other error occurred: {err}"

    else:
      return True, response.json()
