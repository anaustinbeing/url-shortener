from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from .models import URL
from .forms import URLForm
from .schema import CreateURL

# Create your views here.
def home_view(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            entered_url = URL(original_url=form.cleaned_data['url'])
            is_already_available = entered_url.save()
            url = is_already_available if is_already_available else URL.objects.latest('created_at')
            shortened_url = 'http://' + request.get_host() + '/' + url.url_hash
            form = URLForm()
            return render(request, 'shorty/home.html', {'form': form, 'url': shortened_url})
    else:
        form = URLForm()

    return render(request, 'shorty/home.html', {'form': form, 'url': None})

def redirect_view(request, url_hash):
    url = get_object_or_404(URL, url_hash=url_hash)
    url.clicked()
    return redirect(url.original_url)

def details_view(request):
    queryset = URL.objects.all()
    return render(request, 'shorty/details.html', {'details': queryset.order_by('created_at'), 'request': request})