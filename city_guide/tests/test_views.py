from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from city_guide.models import Place, Question, Comment

PLACE_URL = reverse("city_guide:place-list")


class PublicPlaceTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_retrieve_places(self):
        Place.objects.create(name="Restaurant Lorena's", location="some location", description="some description", image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no")
        Place.objects.create(name="Bosphorus Restaurant", location="some location", description="some description", image_url="https://lh5.googleusercontent.com/p/AF1QipO-7jothJfDK4KjeuU1YjbUCqmRr69oopxiE0RL=w408-h306-k-no")

        response = self.client.get(PLACE_URL)
        places = Place.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["place_list"]), list(places))
        self.assertTemplateUsed(response, "city_guide/place_list.html")

    def test_create_place(self):
        form_data = {
            "name": "Restaurant Lorena's",
            "location": "some location",
            "description": "some description",
            "image_url": "https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no"
        }
        self.client.post(reverse("city_guide:place-create"), data=form_data)
        new_place = Place.objects.get(name=form_data["name"])

        self.assertEqual(new_place.location, form_data["location"])
        self.assertEqual(new_place.description, form_data["description"])
        self.assertEqual(new_place.image_url, form_data["image_url"])

    def test_update_place(self):
        place = Place.objects.create(
            name="Restaurant Lorena's",
            location="some location",
            description="some description",
            image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no",
        )

        form_data = {
            "name": "Restaurant Lorena's",
            "location": "changed location",
            "description": "changed description",
            "image_url": "https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no"
        }

        url = reverse("city_guide:place-update", kwargs={"pk": place.id})
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)

        updated_place = Place.objects.get(id=place.id)
        self.assertEqual(updated_place.location, "changed location")
        self.assertEqual(updated_place.description, "changed description")

    def test_delete_place(self):
        place = Place.objects.create(
            name="Restaurant Lorena's",
            location="some location",
            description="some description",
            image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no",
        )

        url = reverse("city_guide:place-delete", kwargs={"pk": place.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Place.objects.filter(pk=place.pk).exists())


class PublicQuestionTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_for_create(self):
        place = Place.objects.create(
            name="Restaurant Lorena's",
            location="some location",
            description="some description",
            image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no",
        )

        form_data = {
            "text": "some text",
        }
        response = self.client.post(reverse("city_guide:question-create", kwargs={"pk": place.pk}), data=form_data)

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Question.objects.filter(text="some text").exists())


class PrivateQuestionTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_question(self):
        place = Place.objects.create(
            name="Restaurant Lorena's",
            location="some location",
            description="some description",
            image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no",
        )

        form_data = {
            "text": "some text",
        }

        response = self.client.post(reverse("city_guide:question-create", kwargs={"pk": place.pk}), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Question.objects.filter(text="some text").exists())


class PublicCommentTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_for_create(self):
        place = Place.objects.create(
            name="Restaurant Lorena's",
            location="some location",
            description="some description",
            image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no",
        )

        form_data = {
            "text": "some text",
            "media_url": "https://lh5.googleusercontent.com/p/AF1QipMaryxBkzpKEol0A61zISzpWvaMYhI9mXy4HVec=w450-h338-p-k-no"
        }
        response = self.client.post(reverse("city_guide:comment-create", kwargs={"pk": place.pk}), data=form_data)

        self.assertNotEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(text="some text").exists())


class PrivateCommentTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_create_comment(self):
        place = Place.objects.create(
            name="Restaurant Lorena's",
            location="some location",
            description="some description",
            image_url="https://lh5.googleusercontent.com/p/AF1QipNXV1-oyE_A5jiLwLrsWKcOicbKZW-2vdLnNfoX=w426-h240-k-no",
        )

        form_data = {
            "text": "some text",
            "media_url": "https://lh5.googleusercontent.com/p/AF1QipMaryxBkzpKEol0A61zISzpWvaMYhI9mXy4HVec=w450-h338-p-k-no"
        }

        response = self.client.post(reverse("city_guide:comment-create", kwargs={"pk": place.pk}), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(text="some text").exists())
