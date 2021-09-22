import typing

from bs4 import BeautifulSoup
import requests

from django.core.management import BaseCommand
from django.db import transaction

from core.models import Movie, Actor


class Command(BaseCommand):
    help = """
        Fetch top 300 movies and actors listed on CSFD: https://www.csfd.cz/zebricky/filmy/nejlepsi/?showMore=1
        and save them to SQL DB.
    """

    @property
    def headers(self):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        return {
            'User-Agent': user_agent
        }

    @staticmethod
    def create_actor(name: str, detail_url: str) -> Actor:
        actor, created = Actor.objects.get_or_create(name=name, detail_url=detail_url)
        return actor

    def get_actors_for_movie(self, movie_detail_url: str) -> typing.List[Actor]:
        actors = []

        movie_detail_html = requests.get(movie_detail_url, headers=self.headers).text
        movie_detail_soup = BeautifulSoup(movie_detail_html, 'html.parser')

        creators = movie_detail_soup.find('div', attrs={'class': 'creators'})
        for creator_category in creators.children:
            headline = creator_category.find('h4')
            if headline is -1 or headline is None:
                continue
            if headline.text == 'Hrají: ':
                actors_tags = creator_category.findAll('a')
                for actor_tag in actors_tags[:-1]:
                    actor_detail_url = 'https://www.csfd.cz' + actor_tag.attrs['href']
                    actor_name = actor_tag.text.strip()
                    actors.append(self.create_actor(actor_name, actor_detail_url))
        return actors

    def create_movie(self, name: str, movie_detail_url: str):
        movie, created = Movie.objects.get_or_create(name=name, detail_url=movie_detail_url)
        if created:
            print(f'Creating movie: {name}')
            # If movie wasn't created, we suppose that it already have all actors connected
            movie.actors.add(*self.get_actors_for_movie(movie_detail_url))

    def handle(self, *args, **options):
        Movie.objects.all().delete()
        Actor.objects.all().delete()
        print('CSFD data import started')

        csfd_url = 'https://www.csfd.cz/zebricky/filmy/nejlepsi/?showMore=1'
        top_movies_html = requests.get(csfd_url, headers=self.headers).text
        soup = BeautifulSoup(top_movies_html, 'html.parser')

        movies = soup.findAll('a', attrs={'class': 'film-title-name'})

        with transaction.atomic():
            for movie in movies:
                name = movie.text.strip()
                detail_url = 'https://www.csfd.cz' + movie.attrs['href']
                self.create_movie(name, detail_url)

        print('CSFD data import finished')
