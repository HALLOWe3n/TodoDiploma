import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.views.generic import DetailView, View

from todo.forms import RegistrationForm, TodoForm
from todo.models import Todo, Profile
from todo.utils import send_mail


ReviewForm = None


def home(request, status=None):
    if request.user.profile.is_admin():
        todos = Todo.objects.filter(
            assignee__profile__domain=request.user.profile.domain
        )
    else:
        todos = Todo.objects.filter(Q(assignee=request.user) | Q(assignor=request.user))
    if status:
        todos = todos.filter(status=status)
    context = {"todos": todos, "user": request.user}
    return render(request, "todo/home.html", context)


def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("todo:login"))
    return render(request, "todo/registration_form.html", {"form": form})


def add_or_update_task(request, pk=None):
    task = get_object_or_404(Todo, pk=pk) if pk else None
    form = TodoForm(request.user, request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect(reverse("todo:home"))
    return render(request, "todo/task_form.html", {"form": form})


def pending_requests(request):
    pending_requests = Profile.objects.filter(
        is_approved=False, domain=request.user.profile.domain
    )
    return render(
        request, "todo/pending_requests.html", {"pending_requests": pending_requests}
    )


def approve_request(request, pk):
    user_profile = get_object_or_404(Profile, user__id=pk)
    user_profile.is_approved = True
    user_profile.save()
    send_mail(
        subject="Request Approved",
        body="%s has approved your registration request" % request.user.email,
        to=user_profile.user.email,
    )
    return redirect("todo:pending_requests")


def request_task_to_job(request, pk):
    user_profile = get_object_or_404(Profile, user__id=pk)
    if user_profile.is_approved:
        task = Todo.objects.get(pk=pk)
        task.status = Todo.ACTIVE
        task.save()


def request_set_timer(pk_task):
    task = Todo.objects.get(pk=pk_task)
    # set timer start
    task.time = datetime.datetime.now()
    task.save()


class TaskTodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "todo/task.html"


class TaskTodoWorkingDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "todo/working_task.html"


class TaskTodoDoneDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    form_class = ReviewForm
    template_name = "todo/done_task.html"


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "profile/profile.html")
