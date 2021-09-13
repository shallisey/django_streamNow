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
from django.core.paginator import Paginator
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

        response = requests.get(f'https://api.themoviedb.org/3/{media_type}/{_id}?api_key=3fe16ac899ef8daf40c2fb35b0a90b5f&language=en-US').json()
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
        value = self.request.get_full_path()
        media_type_and_id = value.split("/")[2:-2]
        media_type, _id = media_type_and_id[0], media_type_and_id[1]

        # Add values to the form that are not seen
        form.instance.author = self.request.user
        form.instance.media_type = media_type
        form.instance.id_media_type = _id

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





def about(request):
    return render(request, 'streamNow/about.html')

def search(request):
    print('hi from the search')
    return render(request, 'streamNow/search.html')