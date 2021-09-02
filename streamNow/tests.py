# from django.test import TestCase

import requests
import json
import pprint

# Create your tests here.
data = requests.get('https://api.themoviedb.org/3/trending/movie/day?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f').json()
pprint.pprint(data)



