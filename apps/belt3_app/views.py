from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from models import *
from django.contrib import messages

def index(request):
	context = {
		"users" : User.objects.all()
	}
	return render(request, "belt3_app/index.html", context)

def register(request):
	errors = User.objects.regvalidator(request.POST, "create")
	if len(errors): 
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect("/") 
	else:
		newuser = User.objects.create(name=request.POST["name"], alias=request.POST['alias'], email=request.POST["email"], password=request.POST["password"], dob=request.POST['dob'])
		newuser.save()
		request.session["user_id"] = newuser.id
		messages.success(request, "Successfully registered!")
		return redirect("/quotes")

def quotes(request):
	if 'user_id' not in request.session:
		return redirect('/')
	user = User.objects.get(id=request.session["user_id"])	
	context = {
		"users" : user,
		'favorite': Quote.objects.filter(userfavorite= user),
		'quote': Quote.objects.exclude(userfavorite= user)
	}
	return render(request, "belt3_app/quotes.html", context)

def log(request):
	errors = User.objects.logvalidator(request.POST, "log")
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error, extra_tags="log")
		return redirect("/")
	else:
		request.session["user_id"] = User.objects.get(email=request.POST["email"]).id
		request.session["status"] = "logged in"
		return redirect("/quotes")

def logout(request):

	del request.session['user_id']
	return redirect('/')
def posts(request):
	errors = Quote.objects.quotevalidator(request.POST, 'quote')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect("/quotes")
	newquote=  Quote.objects.create(quoteby=request.POST['quoted'], message= request.POST['message'],user= User.objects.get(id=request.session['user_id']))
	return redirect('/users/'+str(request.session["user_id"]))

def show(request, id):
	context = {
		"user" : User.objects.get(id=request.session["user_id"]),
		'content': Quote.objects.filter(user=int(id) ),
		'count': Quote.objects.count()
	}
	return render(request, "belt3_app/user.html", context)

def favorite(request, id):
	user = User.objects.get(id = request.POST['user_id'])
	print request.POST['user_id']
	quote = Quote.objects.get(id = request.POST['quote_id'])
	print request.POST['quote_id']
	quote.userfavorite.add(user)
	print quote.userfavorite.add(user)
	quote.save()
	return redirect('/quotes')

def removefav(request, id):
	user = User.objects.get(id = request.POST['user_id'])
	print request.POST['user_id']
	quote = Quote.objects.get(id = request.POST['quote_id'])
	print request.POST['quote_id']
	quote.userfavorite.remove(user)
	print quote.userfavorite.remove(user)
	quote.save()
	return redirect('/quotes')

# def post(request):
# 	newpost = Review.objects.create(review = request.POST['review'], rating = request.POST['rating'], reviewer = User.objects.get(id=request.session["user_id"]), book = Book.objects.get()
# 	return redirect('/belt3_app/thewall')


# def posts(request):
# 	errors = User.objects.quotevalidator(request.POST, "create")
# 	if len(errors): 
# 		for error in errors.itervalues():
# 			messages.error(request, error)
# 		return redirect("/") 
# 	else:
# 		newquote=  Quote.objects.create(quoted=request.POST['quoted'], message= request.POST['message'],user= User.objects.get(id=request.session['user_id']))
# 	return redirect('/users/'+id)