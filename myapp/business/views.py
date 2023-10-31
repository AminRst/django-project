from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, request, JsonResponse
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
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .urls import *
import json


# Create your views here.
def index(request):
    cafes = Cafe.objects.all()
    return render(request, 'business/index.html', {'cafes': cafes})


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
    return render(request, 'business/detail1.html', context)


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
    template_name = 'business/index.html'


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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('business:index')
                else:
                    return HttpResponse('Your account is not active')
                    # messages.error(request, 'Your account is not active')
            else:
                return HttpResponse('You are not logged in')
    else:
        form = LoginForm()
    return render(request, 'forms/login_page1.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(request.META.get("HTTP_REFERER", "login"))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['email']
            user.save()
            success_message = "ثبت نام شما با موفقیت انجام شد."

            # Account.objects.create(user=user)
            return render(request, 'forms/login_page1.html', {'success_message': success_message})
    else:
        form = UserRegisterForm()
    return render(request, 'forms/login_page1.html', {'form': form})


# def image(request):
#     data = Image.objects.all()
#     print()
#     context = {
#         'data': data
#     }
#     return render(request, "business/list.html", context)


# @login_required()
# def user_profile(request, manager_id, manager):
#     cafes = Cafe.opened.filter(id=manager_id)
#     user = User.objects.get(username=manager)
#     return render(request, 'business/templates/registration/user-profile.html', {'cafes': cafes, 'user': user})


@login_required
def edit_account(request):
    if request.method == 'POST':

        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = UserEditAccount(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = UserEditAccount(instance=request.user.account)
    user = request.user
    saved_cafes = user.saved_cafes.all()
    context = {
        'account_form': account_form,
        'user_form': user_form,
        'saved_cafes': saved_cafes,
    }
    return render(request, 'registration/user-profile.html', context)


@login_required
def panel(request):
    cafes = Cafe.objects.filter(manager=request.user)
    comment = Comment.objects.filter(active=True)
    context = {
        'cafes': cafes,
        'comment': comment,
    }
    return render(request, 'business/panel.html', context)


def edit_cafe(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    if request.method == 'POST':
        form = CreateCafeForm(request.POST, request.FILES, instance=cafe)
        if form.is_valid():
            cafe = form.save(commit=False)
            cafe.manager = request.user
            cafe.save()
            if form.cleaned_data['image1']:
                Image.objects.create(image_file=form.cleaned_data['image1'], cafe=cafe)
            if form.cleaned_data['image2']:
                Image.objects.create(image_file=form.cleaned_data['image2'], cafe=cafe)
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        form = CreateCafeForm(instance=cafe)
    return render(request, 'forms/create-cafe.html', {'form': form, 'cafe': cafe})


def create_cafe(request):
    if request.method == 'POST':
        form = CreateCafeForm(request.POST, request.FILES)
        if form.is_valid():
            cafe = form.save(commit=False)
            cafe.manager = request.user
            cafe.save()
            if form.cleaned_data['image1']:
                Image.objects.create(image_file=form.cleaned_data['image1'], cafe=cafe)
            if form.cleaned_data['image2']:
                Image.objects.create(image_file=form.cleaned_data['image2'], cafe=cafe)
            return redirect('business:panel')
    else:
        form = CreateCafeForm()
        return render(request, 'forms/create-cafe.html', {'form': form})


def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def like_post(request):
    cafe_id = request.POST.get('cafe_id')
    if cafe_id is not None:
        cafe = get_object_or_404(Cafe, id=cafe_id)
        user = request.user

        if user in cafe.likes.all():
            cafe.likes.remove(user)
            liked = False
        else:
            cafe.likes.add(user)
            liked = True

        cafe_likes_count = cafe.likes.count()
        response_data = {
            'liked': liked,
            'likes_count': cafe_likes_count
        }
    else:
        response_data = {'error': 'Invalid cafe_id'}
    return JsonResponse(response_data)


def menu_items_view(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    menu = Menu.objects.get(cafe=cafe)
    sections = Section.objects.filter(menu=menu)
    context = {
        'cafe': cafe,
        'sections': sections,
    }
    return render(request, 'business/cafe_menu.html', context)


class CafeSectionView(ListView):
    def get_queryset(self):
        section = self.kwargs.get('section')
        if section == "drinks":
            sec = Section.objects.filter(name__icontains='نوشیدنی')
            print(sec)
            lst = []
            for i in sec:
                lst.append(i.menu.cafe)
            queryset = Cafe.objects.filter(name__in=lst)
            return queryset
        if section == "food":
            sec = Section.objects.filter(name__icontains='فود')
            print(sec)
            lst = []
            for i in sec:
                lst.append(i.menu.cafe)
            queryset = Cafe.objects.filter(name__in=lst)
            return queryset
        # else:
        #     queryset = Cafe.objects.all()
        #     return queryset

    context_object_name = 'cafes'
    paginate_by = 5
    template_name = 'Business/list.html'


@login_required
@require_POST
def save_cafe(request):
    cafe_id = request.POST.get('cafe_id')
    if cafe_id is not None:
        cafe = Cafe.objects.get(id=cafe_id)
        user = request.user

        if user in cafe.saved_by.all():
            cafe.saved_by.remove(user)
            saved = False
        else:
            cafe.saved_by.add(user)
            saved = True
        return JsonResponse({'saved': saved})

    return JsonResponse({'error': 'Invalid Request'})


def saved_cafes(request):
    user = request.user
    cafes = user.saved_cafes.all()
    return render(request, 'business/saved-cafes.html', {'cafes': cafes})


# @login_required
# def edit_menu(request, cafe_id):
#     cafe = get_object_or_404(Cafe, id=cafe_id)
#     menu = Menu.objects.get(cafe=cafe)
#     section = Section.objects.get(menu=menu)
#     menu_items = MenuItems.objects.filter(section=section)
#     if request.method == 'POST':
#         section_form = EditSectionForm(request.POST, instance=section)
#         MenuItemsFormSet = modelformset_factory(MenuItems, form=EditMenuItemsForm, queryset=menu_items)
#         items_formset = MenuItemsFormSet(request.POST, queryset=menu_items)
#         if section_form.is_valid() and items_form.is_valid():
#             section_form.save()
#             items_form.save()
#
#     # user = request.user
#     else:
#         section_form = EditSectionForm(instance=section)
#         items_form = EditMenuItemsForm(queryset=menu_items)
#
#     context = {
#         'cafe': cafe,
#         'section_form': section_form,
#         'items_form': items_form,
#     }
#     return render(request, 'forms/edit-menu.html', context)


def edit_menu(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    menu = Menu.objects.get(cafe=cafe)
    section = Section.objects.get(menu=menu)
    menu_items = MenuItems.objects.filter(section=section)

    if request.method == 'POST':
        section_form = EditSectionForm(request.POST, instance=section)
        # Create a formset for menu items
        MenuItemsFormSet = modelformset_factory(MenuItems, form=EditMenuItemsForm, extra=0)
        items_formset = MenuItemsFormSet(request.POST, queryset=menu_items)

        if section_form.is_valid() and items_formset.is_valid():
            section_form.save()
            items_formset.save()
            return redirect('business:edit_menu', cafe_id=cafe.id)

    else:
        section_form = EditSectionForm(instance=section)
        # Create a formset for menu items
        MenuItemsFormSet = modelformset_factory(MenuItems, form=EditMenuItemsForm, extra=0)
        items_formset = MenuItemsFormSet(queryset=menu_items)

    context = {
        'cafe': cafe,
        'section_form': section_form,
        'items_formset': items_formset,  # Corrected variable name to reflect it's a formset
    }
    return render(request, 'forms/edit-menu.html', context)

