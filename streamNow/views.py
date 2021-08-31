from django.shortcuts import render
import requests
import pprint

hardcode_data = [{
    "overview": 'An agoraphobic woman living alone in New York begins spying on her new neighbors only to witness a disturbing act of violence.',
    'title': 'The Woman in the Window',
    'media': 'movie'
    },
    {
    'overview': 'A woman wakes in a cryogenic chamber with no recollection of how she got there, and must find a way out before running out of air.',
    'title': 'Oxygen',
    'media': 'movie'
    }
]

def home(request):

    data = requests.get('https://api.themoviedb.org/3/trending/movie/day?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f').json()
    pprint.pprint(data['results'][0])
    results = []
    # Grab data from response if there is any and get the first ten.
    if data:
        for i in range(9):
            results.append(data['results'][i])
            # pprint.pprint(data['results'][i])
    context = {
        'data': results
    }
    return render(request, 'streamNow/home.html', context)

def about(request):
    return render(request, 'streamNow/about.html')

def search(request):
    print('hi from the search')
    return render(request, 'streamNow/search.html')