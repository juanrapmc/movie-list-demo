import json
import datetime

from django.core.serializers import serialize
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from movielistapp.forms import MovieForm
from movielistapp.models import Movie


@method_decorator(csrf_exempt, name='dispatch')
class MovieList(View):
    """
    List all movies, or create a new movie entry.
    """
    def get(self, request):
        """
        Returns all movies.
        """
        movies = Movie.objects.filter(is_active=True).order_by('title')
        return HttpResponse(serialize("json", movies),
                            content_type="application/json")

    @csrf_exempt
    def post(self, request):
        """
        Creates a new movie entry.
        """
        form = MovieForm(json.loads(request.body.decode('utf-8')))
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MovieDetails(View):
    """
    Get, update, or delete a specific movie.
    """
    def get(self, request, movie_id):
        """
        Return a specific movie based from id.
        """
        movie = get_object_or_404(Movie, pk=movie_id)
        return HttpResponse(serialize("json", [movie,]),
                            content_type="application/json")

    def put(self, request, movie_id):
        """
        Update movie title of a specific movie based from id.
        """
        movie = get_object_or_404(Movie, pk=movie_id)
        form = MovieForm(json.loads(request.body.decode('utf-8')),
                         instance=movie)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)

    def delete(self, request, movie_id):
        """
        Performs a soft delete - sets is_active movie property to false
        """
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.is_active = False
        movie.save()
        return HttpResponse(status=200)


def likeMovie(request, movie_id):
    """
    Function to handle increment of movie likes.
    """
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.likes += 1
    movie.save()
    return HttpResponse(serialize("json", [movie,]),
                        content_type="application/json")

def getLastSession(request):
    last_session = 0
    try:
        last_session = request.session['last_session']
    except:
        pass
    request.session['last_session'] = datetime.datetime.now().ctime()
    return HttpResponse(last_session)