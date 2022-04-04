import random

from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse
from .models import comment, poster, order, WishList
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, SigninForm, CommentForm, PosterForm, OrderForm, ForgotPasswordForm, ChangePasswordForm
import requests
from urllib.parse import urlencode
from django.core.mail import send_mail
from django.views import View

TMDB_API_KEY = "850248f75917ae33a4baa0eee7b334cf"


# Create your views here.
class Movies(View):
    type = "movie"
    time_window = "day"
    header = "Top results of the Day "
    currentPage = "home"

    def get(self, request):
        trendings = requests.get(
            f"https://api.themoviedb.org/3/trending/{self.type}/{self.time_window}?api_key={TMDB_API_KEY}&language=en-US")
        return render(request, '../templates/movies_list.html', {"data": trendings.json(), "type": "movie_details",
                                                                 "header": self.header,
                                                                 "currentPage": self.currentPage})


class Trending(Movies):
    # movie_list = Movies.objects.all().order_by('-release_date')[:10]
    type = "movie"
    time_window = "week"
    header = "Trending movies of the week "
    currentPage = "trending"


def now_playing(request):
    currentPage = "nowplaying"
    data = requests.get(
        f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}")
    return render(request, '../templates/results.html', {
        "data": data.json(),
        "type": "movie_details",
        "currentPage": currentPage
    })


def top_rated(request):
    currentPage = "toprated"
    data = requests.get(
        f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=en-US")
    return render(request, '../templates/results.html', {
        "data": data.json(),
        "type": "movie_details",
        "currentPage": currentPage
    })


@login_required(login_url='/signin/')
def wishlist(request):
    # data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    # title = data.json()["title"]
    currentPage = "wishlist"
    items = reversed(WishList.objects.filter(user_id=request.user))
    print(items)
    res = []
    for idx, movie in enumerate(items):
        if idx == 5:
            break
        res.append(requests.get(
            f"https://api.themoviedb.org/3/movie/{movie.movie_id}?api_key={TMDB_API_KEY}&language=en-US").json())

    return render(request, '../templates/wishlist.html', {
        "title": "test",
        "items": res,
        "currentPage": currentPage
    })
    # return render(request, '../templates/add_to_wishlist.html')


@login_required(login_url='/signin/')
def add_to_wishlist(request, movie_id):
    # print(request)
    # print(movie_id)
    # movie_id = request.GET.get('movie_id')
    if movie_id and WishList.objects.filter(movie_id=movie_id, user=request.user).count() == 0:
        WishList.objects.create(movie_id=movie_id, user=request.user).save()
        # WishList.objects.filter(movie_id=movie_id,user=request.user).delete()
    # data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    return redirect("/wishlist/")


@login_required(login_url='/signin/')
def delete_from_wishlist(request, movie_id):
    # print(request)
    # print(movie_id)
    # movie_id = request.GET.get('movie_id')
    if movie_id:
        # WishList.objects.create(movie_id=movie_id,user=request.user).save()
        WishList.objects.filter(movie_id=movie_id, user=request.user).delete()
    # data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    # return render(request, "../templates/add_to_wishlist.html", {
    #     "data": data.json(),
    #     "type": "movie_details",
    return redirect("/wishlist/")


def movie_details(request, movie_id):
    # movie_detail = Movies.objects.filter(tmdbid=movie_id) | Movies.objects.filter(id=movie_id)
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    recommendations = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")
    if 'recently_browsed' in request.session:
        if movie_id in request.session['recently_browsed']:
            request.session['recently_browsed'].remove(movie_id)
        request.session['recently_browsed'].insert(0, movie_id)
        if len(request.session['recently_browsed']) > 5:
            request.session['recently_browsed'].pop()
    else:
        request.session['recently_browsed'] = [movie_id]
    request.session.modified = True
    return render(request, "../templates/movie_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "movie_details",
    })


def search(request):
    # Get the query from the search box
    query = request.GET.get('q')
    # If the query is not empty
    if query:

        # Get the results from the API

        # data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
        data = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
    else:
        # return HttpResponse("Please enter a search query")
        return redirect('/')

    # Render the template
    return render(request, '../templates/results.html', {
        "data": data.json(),
        "type": "movie_details",
    })


def signup(request):
    msg = ''
    if request.method == "POST":
        filled_form = SignupForm(request.POST)
        if filled_form.is_valid():
            if filled_form.cleaned_data['password'] == filled_form.cleaned_data['confirmpassword']:
                user = User.objects.create_user(filled_form.cleaned_data['name'], filled_form.cleaned_data['email'],
                                                filled_form.cleaned_data['password'])
                login(request, user)
                # request.session.set_expiry(600)
                return redirect('/')
            else:
                msg = "Passwords don't match"
    new = SignupForm()
    return render(request, '../templates/Signup.html', {'SignupForm': new, 'msg': msg})


def signin(request):
    currentPage = "signin"
    msg = ''
    if request.method == "POST":
        filled_form = SigninForm(request.POST)
        if filled_form.is_valid():
            user = authenticate(request, username=filled_form.cleaned_data['name'],
                                password=filled_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # return render(request, '../templates/base_code.html')
                # request.session.set_expiry(600)
                # print(request.session.get_expiry_age())
                nexturl = request.GET.get('next', '/')
                return redirect(nexturl)
            else:
                msg = 'Wrong Combo. Try Again !!'
    new = SigninForm()
    return render(request, '../templates/Signin.html', {'SigninForm': new, 'msg': msg, "currentPage": currentPage})


def signout(request):
    currentPage = "signout"
    logout(request)
    return redirect('/signin/')


def comments(request, movie_id):
    if request.method == "POST":
        user = request.user
        if not request.user.is_authenticated:
            # return HttpResponse("Need to login to post comments")
            base_url = '/signin/'  # 1 /signin/
            query_string = urlencode(
                {'next': '/movie_details/' + str(movie_id) + '/comments/'})  # 2 /movie_details/634649/
            url = '{}?{}'.format(base_url, query_string)  # 3 /signin/?next=movie_details/634649/comments
            return redirect(url)  # 4
        else:
            form = CommentForm(request.POST)
            # return HttpResponse('<p>'+ str(form)+'</p>')
            if form.is_valid():
                comment(comment=form.cleaned_data['comment'], user=user, movie_id=movie_id,
                        rating=form.cleaned_data['rating']).save()
                # form.save()
            return redirect(f"/movie_details/{movie_id}/comments/")
    else:
        data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
        title = data.json()["title"]

        comments = reversed(comment.objects.filter(movie_id=movie_id))

        return render(request, "../templates/comments.html", {
            "title": title,
            "comments": comments,
        })


def posters(request):
    currentPage = "posters"
    if request.method == "POST":
        user = request.user
        if not request.user.is_authenticated:
            # return HttpResponse("Need to login to upload Posters")
            base_url = '/signin/'  # 1 /signin/
            query_string = urlencode({'next': '/posters/'})  # 2 /posters/
            url = '{}?{}'.format(base_url, query_string)  # 3 /signin/?next=/posters/
            return redirect(url)  # 4
        else:
            form = PosterForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.uploader = user
                # now we can save
                photo.image_id = random.randint(0, 100000)
                photo.save()
            return redirect(f"../posters/")
    posters = reversed(poster.objects.all())
    return render(request, "../templates/posters.html", {
        "posters": posters,
        "currentPage": currentPage
    })


@login_required(login_url='/signin/')
def delete_poster(request, image_id):
    # Poster ID
    if image_id:
        poster.objects.filter(image_id=image_id, uploader=request.user).delete()
    return redirect("/posters/")


@login_required(login_url='/signin/')
def buy(request, movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    title = data.json()["title"]
    user = request.user
    form1 = OrderForm()
    form = form1.save(commit=False)
    form.movie_id = movie_id
    form.user = request.user
    form.movie_title = title
    if form.movie_title is not None:
        # now we can save
        form.save()
        return render(request, "../templates/buy.html", {"title": title, })
    else:
        return render(request, "../templates/buy.html")


@login_required(login_url='/signin/')
def profile(request, path):
    user = request.user
    user_id = User.objects.get(username__exact=user).id
    if path == 'orders_history':
        orders = reversed(order.objects.filter(user=user_id))
        return render(request, "../templates/profile.html", {"orders": orders, 'page': 1, })
    elif path == 'posted_comments':
        comments = reversed(comment.objects.filter(user=user_id))
        return render(request, "../templates/profile.html", {"comments": comments, 'page': 2, })
    elif path == 'uploaded_movies':
        movies = reversed(poster.objects.filter(uploader=user_id))
        return render(request, "../templates/profile.html", {"movies": movies, 'page': 3, })


def forgot(request):
    if request.method == "POST":
        filled_form = ForgotPasswordForm(request.POST)
        if filled_form.is_valid():
            name = filled_form.cleaned_data['name']
            record = User.objects.get(username__exact=name)
            email = record.email
            # change field
            pwd = User.objects.make_random_password()
            record.set_password(pwd)  # replace with your real password
            record.save()
            res = send_mail('Password reset for CiNeWorld ', 'New password is ' + pwd, None, [email])
            return redirect("../passwordsent/")
        else:
            return render(request, "../templates/forgotpassword.html")
    else:
        return render(request, "../templates/forgotpassword.html")


@login_required(login_url='/signin/')
def change(request):
    if request.method == "POST":
        filled_form = ChangePasswordForm(request.POST)
        if filled_form.is_valid():
            pssword = filled_form.cleaned_data['password']
            user = request.user
            record = User.objects.get(username__exact=user)
            record.set_password(pssword)  # replace with entered password
            record.save()
            return redirect("../../passwordchanged/")
        else:
            return render(request, "../templates/changepassword.html")
    else:
        return render(request, "../templates/changepassword.html")


class Pwdsentconfirm(View):
    message1 = "Your Password is sent to your registered mail."
    message2 = "Sign In Again with the sent password."

    def get(self, request):
        return render(request, "../templates/pwd_change_signin_again.html",
                      {"message1": self.message1, "message2": self.message2})


class Pwdchangeconfirm(Pwdsentconfirm):
    message1 = "Your Password is changed successfully."
    message2 = "Sign In Again with new password"


def recently_browsed(request):
    currentPage = "recently_browsed"
    res = []
    msg = ''
    if 'recently_browsed' in request.session:
        for id in request.session['recently_browsed']:
            res.append(requests.get(
                f"https://api.themoviedb.org/3/movie/{id}?api_key={TMDB_API_KEY}&language=en-US").json())
    if len(res) == 0:
        msg = 'No Browsing History captured yet'
    return render(request, '../templates/recently_browsed.html', {
        "items": res, "msg": msg,
        "currentPage": currentPage
    })
