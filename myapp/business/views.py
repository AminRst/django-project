from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *
from .urls import *


# Create your views here.
def index(request):
    return render(request, 'business/index.html')


# def cafe_list(request):
#     cafes = Cafe.opened.all()
#     paginator = Paginator(cafes, 2)
#     page_number = request.GET.get('page', 1)
#     try:
#         cafes = paginator.page(page_number)
#     except EmptyPage:
#         cafes = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         cafes = paginator.page(1)
#     context = {
#         'cafes': cafes
#     }
#     return render (request, 'business/list.html', context)

class CafeListView(ListView):
    def get_queryset(self):
        status = self.kwargs.get('status')
        if status == "open_cafe":
            queryset = Cafe.opened.all()
            return queryset
        if status == "close_cafe":
            queryset = Cafe.objects.exclude(status='OP')
            return queryset
        else:
            queryset = Cafe.objects.all()
            return queryset

    context_object_name = 'cafes'
    paginate_by = 5
    template_name = 'Business/list.html'


def cafe_detail(request, id):
    cafe = get_object_or_404(Cafe, id=id, status=Cafe.Status.OPEN)
    comments = cafe.comments.filter(active=True)
    form = CommentForm()
    context = {
        'cafe': cafe,
        'form': form,
        'comments': comments
    }
    return render(request, 'business/detail.html', context)


def out_of_service(request, id):
    cafe = get_object_or_404(Cafe, id=id, status=Cafe.Status.CLOSE)
    context = {
        'cafe': cafe
    }
    return render(request, 'partials/out_of_service.html', context)


# class CafeDetailView(DetailView):
#     model = Cafe
#     template_name = 'Business/detail.html'


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect('business:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def cafe_comment(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id, status=Cafe.Status.OPEN)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.cafe = cafe
        comment.save()
    context = {
        'cafe': cafe,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comment.html', context)


class ContactUsView(FormView):
    form_class = ContactUsForm
    template_name = 'forms/contact-us.html'
    success_url = '/business/success/'

    def form_valid(self, form):
        user = form.save()
        return super(ContactUsView, self).form_valid(form)


class SuccessView(TemplateView):
    template_name = 'forms/contact-us.html'


def city_view(request):
    if request.method == 'POST':
        cafes = []
        form = CitiesForm(request.POST)
        if request.POST['city'] == 'SH':
            cafes = Cafe.opened.filter(city=Cafe.Cities.SHIRAZ)
            # cafe = get_object_or_404(Cafe, city=Cafe.Cities.SHIRAZ, status=Cafe.Status.OPEN)
        elif request.POST['city'] == 'NY':
            cafes = Cafe.opened.filter(city=Cafe.Cities.NEWYORK)
            # cafe = get_object_or_404(Cafe, city=Cafe.Cities.NEWYORK, status=Cafe.Status.OPEN)
        elif request.POST['city'] == 'MN':
            cafes = Cafe.opened.filter(city=Cafe.Cities.MANCHESTER)
            # cafe = get_object_or_404(Cafe, city=Cafe.Cities.MANCHESTER, status=Cafe.Status.OPEN)
        context = {
            'form': form,
            'cafes': cafes
        }
        return render(request, 'partials/city_cafes.html', context)
    else:
        form = CitiesForm()
        return render(request, 'forms/list_of_cities.html', {'form': form})


def cafe_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results1 = (Cafe.opened.annotate(similarity=TrigramSimilarity('name', query))
                        .filter(similarity__gt=0.1))
            results2 = (Cafe.opened.annotate(similarity=TrigramSimilarity('description', query))
                        .filter(similarity__gt=0.1))
            results = (results1 | results2).order_by('-similarity')
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'business/page-search-results.html', context)


# class LoginView():
    # def login(request):
    #     if request.method == 'Post':
    #         form =
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         # Redirect to a success page.
    #         ...
    #     else:
    #         # Return an 'invalid login' error message.
    ...


# class MyLoginView(LoginView):
#     redirect_authenticated_user = True
#
#     def get_success_url(self):
#         return reverse_lazy('tasks')
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))