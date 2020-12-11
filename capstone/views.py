from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import View
from .models import Service, RecentWork, Product, Customer, Order, Category
from django.http  import HttpResponse,Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    return render(request, 'all-capstone/home.html')

def about(request):
    return render(request, 'all-capstone/about.html')

def service(request):
    return render(request, 'all-capstone/service.html')

def recent(request):
    return render(request, 'all-capstone/recent-works.html')

def contacts(request):
    return render(request, 'all-capstone/contacts.html')

class Shop(View):

	def get(self,request):
		cart = request.session.get('cart')
		categories = Category.getAllCategory()
		products = Product.getAllProduct().order_by()

		if request.GET.get('id'):
			filterProductById = Product.objects.get(id=int(request.GET.get('id')))
			return render(request, 'all-capstone/products.html',{"product":filterProductById,"categories":categories})

		if not cart:
			request.session['cart'] = {}

		if request.GET.get('category_id'):
			filterProduct = Product.getProductByFilter(request.GET['category_id'])
			return render(request, 'all-capstone/shop.html',{"products":filterProduct,"categories":categories})

		return render(request, 'all-capstone/shop.html',{"products":products,"categories":categories})

	def post(self,request):
		product = request.POST.get('product')

		cart = request.session.get('cart')
		if cart:
			quantity = cart.get(product)
			if quantity:
				cart[product] = quantity+1
			else:
				cart[product] = 1
		else:
			cart = {}
			cart[product] = 1

		print(cart)
		request.session['cart'] = cart
		return redirect('cart')
        
class Order(View):
	def get(self,request):
		customer_id = request.session.get('customer')
		return render(request,'all-capstone/order.html')

class cart(View):
	def get(self,request):
		productList = list(request.session.get('cart').keys())
		if request.GET.get('increase'):
			pId = request.GET.get('increase')
			products = request.session.get('cart')
			products[pId] += 1
			request.session['cart'] = products

		if request.GET.get('decrease'):
			pId = request.GET.get('decrease')
			products = request.session.get('cart')
			print(products[pId])
			if products[pId] > 1:
				products[pId] -= 1
				request.session['cart'] = products
				productList = list(request.session.get('cart').keys())
			else :
				del products[pId]
				request.session['cart'] = products
				productList = list(request.session.get('cart').keys())
				

		allProduct = Product.getProductById(productList)
		return render(request,'all-capstone/cart.html',{"allProduct":allProduct})

class Checkout(View):
	def get(self,request):
		return redirect('cart')
	
	def post(self,request):
		address = request.POST.get('address')
		phone = request.POST.get('phone')
		cart = request.session.get('cart')
		products = Product.getProductById(list(cart.keys()))
		customer = request.session.get('customer')
		print(address,phone,cart,products,customer)

		for product in products:
			newOrder = Order(
					product=product,
					customer=Customer(id=customer),
					quantity=cart[str(product.id)],
					price=product.price,
					address=address,
					phone=phone,
				)
			newOrder.save()

		request.session['cart'] = {}
		return redirect('order')

class signup(View):

	def get(self,request):
		return render(request,'registration/registration_form.html')
			
	def post(self,request):
		userData = request.POST
		# validate
		error = self.validateData(userData)
		if error :
			return render(request,'registration/registration_form.html',{"error":error,"userData":userData})
		else:
			if Customer.emailExits(userData['email']):
				error["emailExits_error"] = "Email Already Exits"
				return render(request,'registration/registration_form.html',{"error":error,"userData":userData})
			else:
				customer = Customer(
					name=userData['name'],
					email=userData['email'],
					phone=userData['phone'],
					password=make_password(userData['password']),
				)
				customer.save()
				return redirect('home')

	# Validate form method
	def validateData(self,userData):
		error = {}
		if not userData['name'] or not userData['email']  or not userData['phone']  or not userData['password'] or not userData['confirm_password']:
			error["field_error"] = "All field must be required"
		elif len(userData['password'])<8 and len(userData['confirm_password'])<8 :
			error['minPass_error'] = "Password must be 8 char"
		elif len(userData['name']) > 25 or len(userData['name']) < 3 :
			error["name_error"] = "Name must be 3-25 charecter"
		elif len(userData['phone']) != 11:
			error["phoneNumber_error"] = "Phone number must be 11 charecter."
		elif userData['password'] != userData['confirm_password']:
			error["notMatch_error"] = "Password doesn't match"	

		return error


class login(View):
	return_url = None

	def get(self,request):
		login.return_url = request.GET.get('return_url')
		return render(request,'registration/login.html')

	def post(self,request):
		userData = request.POST
		customerEmail = Customer.emailExits(userData["email"])
		if customerEmail:
			if check_password(userData["password"],customerEmail.password):
				request.session["customer"] = customerEmail.id
				if login.return_url:
					return HttpResponseRedirect(login.return_url)
				else:
					login.return_url = None
					return redirect('home')
			else:
				return render(request,'registration/login.html',{"userData":userData,"error":"Email or password doesn't match"})
		else:
			return render(request,'registration/login.html',{"userData":userData,"error":"Email or password doesn't match"})

def logout(request):
	request.session.clear()