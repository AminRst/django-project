from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from .models import *
from .forms import *


# Create your views here.
def index(request):
    return HttpResponse('index')


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
    queryset = Cafe.objects.all()
    context_object_name = 'cafes'
    paginate_by = 4
    template_name = 'Business/list.html'


class OpenCafesListView(ListView):
    queryset = Cafe.opened.all()
    context_object_name = 'cafes'
    paginate_by = 2
    template_name = 'Business/list.html'


class CloseCafesListView(ListView):
    queryset = Cafe.objects.exclude(status=Cafe.Status.OPEN)
    context_object_name = 'cafes'
    paginate_by = 2
    template_name = 'Business/list.html'

def cafe_detail(request, id):
    cafe = get_object_or_404(Cafe, id=id, status=Cafe.Status.OPEN)
    context = {
        'cafe': cafe
    }
    return render(request, 'business/detail.html', context)


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
    form = CommentForm(data=require_POST)
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

