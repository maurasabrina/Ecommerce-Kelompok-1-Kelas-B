from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from . forms import  ProfileUpdateForm   
from django.contrib.auth.decorators import login_required



def is_pelanggan(user):
    return user.is_authenticated and user.is_pelanggan


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'dashboard/profile.html', {'form': form})



@user_passes_test(is_pelanggan)
def dashboard_profile(request):
    user = request.user
    return render(request, 'dashboard/profile.html', {'user': user})


@user_passes_test(is_pelanggan)
def pelanggan(request):
    user = request.user
    return render(request, 'dashboard/pelanggan.html', {'user': user})
    