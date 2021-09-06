from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from .forms import UserRegisterForm

'''
messages.debug
messages.info
messages.success
messages.warning
messages.error
'''

def register(request):
    # If a the method of the reqeuest is a POST request
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        # Form is valid
        if form.is_valid():
            form.save() 
            # Grab username of the user trying to register.
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login.')
            # After a succesful account creation redirect to homepage of streamNow
            # TODO maybe redirect to users homepage
            return redirect('login')
        else:
            print('FROM THE VALID FORM..........Form waas not valid for some reason.')

    else:
        print('NOT GETTING POSTED.......Form waas not valid for some reason.')
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')
