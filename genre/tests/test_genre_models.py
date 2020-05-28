from django.test import TestCase
from main.tests.functions import sample_genre, sample_user


class GenreTest(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.genre = sample_genre(self.user)

    def test_genre_str_representation(self):

        self.assertEqual(str(self.genre), self.genre.name)

    def test_name_capital_letter(self):

        self.assertEqual(self.genre.name.title(), self.genre.name)
