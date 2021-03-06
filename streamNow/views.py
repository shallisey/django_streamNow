import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from .models import Post
from .helper_funcs import media_detail_helper
import requests
import pprint


API_KEY = settings.TMDB_API_KEY


def home(request):

    data = requests.get(f'https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}').json()
    results = []
    # Grab data from response if there is any and get the first ten.
    if data:
        for i in range(9):
            results.append(data['results'][i])
    context = {
        'data': results,
        'posts': Post.objects.all()
    }
    return render(request, 'streamNow/home.html', context)


class HomePage(View):
    # MOVIES
    all_trending_movie = requests.get(f'https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}').json()

    # TV SHOWS
    all_trending_tv = requests.get(f'https://api.themoviedb.org/3/tv/popular?api_key={API_KEY}&language=en-US&page=1').json()



    def get(self, request):
        top_trending = []
        if self.all_trending_movie and self.all_trending_tv:
            for i in range(15):
                top_trending.append(self.all_trending_movie['results'][i])
                top_trending.append(self.all_trending_tv['results'][i])

        paginator = Paginator(top_trending, 6)
        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)


        context = {
            'data': page_obj
        }

        return render(request, 'streamNow/home.html', context)

    def post(self, request):
        pass


class PostListVIew(ListView):

    model = Post


    def get(self, request, media_type, _id):

        response = requests.get(f'https://api.themoviedb.org/3/{media_type}/{_id}?api_key={API_KEY}&language=en-US').json()
        posts = self.model.objects.filter(id_media_type=_id).order_by('-date_posted')

        # Paginate amount of posts to be seen at one time
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'data': page_obj}

        # If there is a response then add values to the context
        # Title, overview, image, rating, genres, maybe similar movies
        if response:
            context = media_detail_helper(response, media_type, _id, context)
            try:
                watch_providers = requests.get(f'https://api.themoviedb.org/3/{media_type}/{_id}/watch/providers?api_key={API_KEY}').json()['results']['US']
            except KeyError:
                watch_providers = {}
            pprint.pprint(watch_providers)
            if watch_providers:
                if 'buy' in watch_providers:
                    context['buy'] = watch_providers['buy']
                if 'flatrate' in watch_providers:
                    context['stream'] = watch_providers['flatrate']
                if 'rent' in watch_providers:
                    context['rent'] = watch_providers['rent']
                if 'link' in watch_providers:
                    context['tmdb_link'] = watch_providers['link']

        return render(request, 'streamNow/post_list.html', context)

    # def post(self, request):
    #     pass


class UserPostListView(ListView):

    model = Post
    template_name = 'streamNow/user_posts.html'
    context_object_name = 'data'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    fields = ['title', 'content']

    def form_valid(self, form):
        # Grab media_type and_id from the URL
        media_type = self.kwargs['media_type']
        id_media_type = self.kwargs['_id']

        # Add values to the form that are not seen
        form.instance.author = self.request.user
        form.instance.media_type = media_type
        form.instance.id_media_type = id_media_type

        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = ['title', 'content']

    def form_valid(self, form):
        # Grab media_type and_id from the URL
        value = self.request.get_full_path()
        media_type_and_id = value.split("/")[2:-2]
        media_type, _id = media_type_and_id[0], media_type_and_id[1]

        # Add values to the form that are not seen
        form.instance.author = self.request.user
        form.instance.media_type = media_type
        form.instance.id_media_type = _id

        return super().form_valid(form)

    # Test if user is the user of the post they are trying to update.
    # Must be named tesT_func
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/'

    # Test if user is the user of the post they are trying to update.
    # Must be named tesT_func
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False


class SearchForm(ListView):
    template_name = 'streamNow/search_form.html'
    context_object_name = 'data'

    def get_queryset(self):

        query = self.request.GET.get('searchQuery')
        if query:
            print(query)
            tmdb_query = f'https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&language=en-US&query={query}&page=1&include_adult=false'
            r = requests.get(tmdb_query).json()['results']

            paginator = Paginator(r, 4)
            page_number = self.request.GET.get('page')

            page_obj = paginator.get_page(page_number)

            return page_obj
        else:
            print(query, 'Nothing')
            return


def about(request):
    return render(request, 'streamNow/about.html')

# def search(request):
#     print('hi from the search')
#     return render(request, 'streamNow/search_form.html')