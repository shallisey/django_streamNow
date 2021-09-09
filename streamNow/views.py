from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import DetailView
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
            context['media_type'] = media_type
            context['_id'] = _id

            # media_type is TV
            if media_type == 'tv':
                context['name'] = response['name']
                context['num_of_episodes'] = response['number_of_episodes']
                context['num_of_seasons'] = response['number_of_seasons']
            # media_type is movie
            else:
                context['name'] = response['original_title']
                context['imdb_id'] = response['imdb_id']

            context['overview'] = response['overview']
            context['poster_path'] = response['poster_path']
            context['backdrop_path'] = response['backdrop_path']
            context['popularity'] = response['popularity']
            context['vote_average'] = response['vote_average']
            context['genres'] = response['genres']
            context['production_companies'] = response['production_companies']
            context['release_date'] = response['release_date']
            context['runtime'] = response['runtime']
            context['revenue'] = '${:,.2f}'.format(response['revenue'])

        if response['homepage']:
            context['homepage'] = response['homepage']
        if response['tagline']:
            context['tagline'] = response['tagline']

        print(context['production_companies'])

        return render(request, 'streamNow/media_detail.html', context)

    def post(self, request):
        pass


def about(request):
    return render(request, 'streamNow/about.html')

def search(request):
    print('hi from the search')
    return render(request, 'streamNow/search.html')