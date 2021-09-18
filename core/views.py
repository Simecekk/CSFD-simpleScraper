from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView

from core.forms import SearchForm
from core.models import Movie, Actor


class HomepageView(TemplateView):
    template_name = 'homepage.html'
    form_class = SearchForm
    
    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            movies = Movie.objects.filter(name__icontains=form.cleaned_data['search_input'])
            actors = Actor.objects.filter(name__icontains=form.cleaned_data['search_input'])
            context = {
                'form': form,
                'movies': movies,
                'actors': actors
            }
            return render(request, 'homepage.html', context=context)
        else:
            # TODO add error messages
            return redirect('homepage.html')


class MovieDetailView(DetailView):
    template_name = 'movie_detail.html'
    queryset = Movie.objects.all()


class ActorDetailView(DetailView):
    template_name = 'actor_detail.html'
    queryset = Actor.objects.all()
