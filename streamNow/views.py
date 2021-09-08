from django.shortcuts import render
from django.views.generic import View, DetailView
from .models import Post
import requests
import pprint



def home(request):

    data = requests.get('https://api.themoviedb.org/3/trending/movie/day?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f').json()
    results = []
    # Grab data from response if there is any and get the first ten.
    if data:
        for i in range(9):
            results.append(data['results'][i])
            # pprint.pprint(data['results'][i])
    context = {
        'data': results,
        'posts': Post.objects.all()
    }
    pprint.pprint(context['posts'])
    return render(request, 'streamNow/home.html', context)


class HomePage(View):
    all_trending = requests.get('https://api.themoviedb.org/3/trending/movie/day?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f').json()

    def get(self, request):
        top_trending = []
        if self.all_trending:
            for i in range(9):
                top_trending.append(self.all_trending['results'][i])

        context = {
            'data': top_trending
        }

        return render(request, 'streamNow/home.html', context)

    def post(self, request):
        pass


class MediaDetailView(DetailView):

    def get(self, request, media_type, _id):
        response = requests.get(f'https://api.themoviedb.org/3/{media_type}/{_id}?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f&language=en-US').json()
        context = {}

        # If there is a response then add values to the context
        # Title, oveview, image, rating, genres, maybe similar movies
        if response:
            print(response)




        return render(request, 'streamNow/media_detail.html', context)

    def post(self, request):
        pass


def about(request):
    return render(request, 'streamNow/about.html')

def search(request):
    print('hi from the search')
    return render(request, 'streamNow/search.html')