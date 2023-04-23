from django.urls import path

from city_guide.views import PlaceListView, PlaceDetailView, PlaceCreateView, PlaceUpdateView, PlaceDeleteView, \
    QuestionCreateView, CommentCreateView

urlpatterns = [

    path("", PlaceListView.as_view(), name="place-list"),
    path("<int:pk>/", PlaceDetailView.as_view(), name="place-detail"),
    path("create/", PlaceCreateView.as_view(), name="place-create"),
    path("<int:pk>/update/", PlaceUpdateView.as_view(), name="place-update"),
    path("<int:pk>/delete/", PlaceDeleteView.as_view(), name="place-delete"),

    path("<int:pk>/question/create/", QuestionCreateView.as_view(), name="question-create"),
    path("<int:pk>/question/<int:question_pk>/comment/", CommentCreateView.as_view(), name="question-comment-create"),
    path("<int:pk>/comment/create/", CommentCreateView.as_view(), name="comment-create"),
]

app_name = "city_guide"
