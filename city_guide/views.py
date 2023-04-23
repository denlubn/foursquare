from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from city_guide.models import Place, Question, Comment


class PlaceListView(generic.ListView):
    model = Place


class PlaceDetailView(generic.DetailView):
    model = Place


class PlaceCreateView(generic.CreateView):
    model = Place
    fields = "__all__"
    success_url = reverse_lazy("city_guide:place-list")


class PlaceUpdateView(generic.UpdateView):
    model = Place
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("city_guide:place-detail", args=[self.object.pk])


class PlaceDeleteView(generic.DeleteView):
    model = Place
    success_url = reverse_lazy("city_guide:place-list")


class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ["text"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.place = get_object_or_404(Place, pk=self.kwargs["pk"])
        return super().form_valid(form)

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial["place"] = self.kwargs["pk"]
    #     return initial

    def get_success_url(self):
        return reverse_lazy("city_guide:place-detail", args=[self.kwargs["pk"]])


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ["text", "media_url"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.place = get_object_or_404(Place, pk=self.kwargs["pk"])

        question_pk = self.kwargs.get("question_pk")
        if question_pk:
            form.instance.question = get_object_or_404(Question, pk=question_pk)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("city_guide:place-detail", args=[self.kwargs["pk"]])
