from django.shortcuts import render
from django.views.generic import (
    View,
    DetailView,
    CreateView
)
from django.contrib import messages
from .models import Post
from .helper_funcs import media_detail_helper
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
    # MOVIES
    all_trending_movie = requests.get('https://api.themoviedb.org/3/trending/movie/day?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f').json()

    # TV SHOWS
    all_trending_tv = requests.get('https://api.themoviedb.org/3/tv/popular?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f&language=en-US&page=1').json()

    def get(self, request):
        top_trending = []
        if self.all_trending_movie and self.all_trending_tv:
            for i in range(15):
                top_trending.append(self.all_trending_movie['results'][i])
                top_trending.append(self.all_trending_tv['results'][i])

        context = {
            'data': top_trending
        }

        return render(request, 'streamNow/home.html', context)

    def post(self, request):
        pass


class MediaDetailView(DetailView):

    model = Post

    def get(self, request, media_type, _id):

        response = requests.get(f'https://api.themoviedb.org/3/{media_type}/{_id}?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f&language=en-US').json()
        posts = self.model.objects.filter(id_media_type=_id)
        print(posts)

        context = {'posts': posts}

        # If there is a response then add values to the context
        # Title, overview, image, rating, genres, maybe similar movies
        if response:
            context = media_detail_helper(response, media_type, _id, context)
        return render(request, 'streamNow/media_detail.html', context)

    # def post(self, request):
    #     pass

class PostCreateView(CreateView):
    model = Post


    fields = ['title', 'content']

    def form_valid(self, form):
        # Grab media_type and_id from the URL
        value = self.request.get_full_path()
        media_type_and_id = value.split("/")[1:-2]
        media_type, _id = media_type_and_id[0], media_type_and_id[1]

        # Add values to the form that are not seen
        form.instance.author = self.request.user
        form.instance.media_type = media_type
        form.instance.id_media_type = _id

        return super().form_valid(form)





    # def get(self, request, media_type, _id):
    #     model = Post
    #
    #     fields = ['title', 'content']
    #
    #     return render(request, 'streamNow/post_form.html')


    # def form_valid(self, form, media_type, _id):
    #     form.instance.author = self.request.user
    #     # form.instance.media_type = self.request
    #     return super().form_valid(form. media_type, _id)


def about(request):
    return render(request, 'streamNow/about.html')

def search(request):
    print('hi from the search')
    return render(request, 'streamNow/search.html')