from django.shortcuts import render,redirect
from django.views import View
from .models import Service, RecentWork, Product, Customer, Order
from django.http  import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

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

@login_required(login_url='/accounts/login/')
class shop(View):

	def get(self,request):
		cart = request.session.get('cart')
		products = Product.getAllProduct().order_by('-id')

		if request.GET.get('id'):
			filterProductById = Product.objects.get(id=int(request.GET.get('id')))
			return render(request, 'all-capstone/products.html',{"product":filterProductById})

		if not cart:
			request.session['cart'] = {}

		if request.GET.get('category_id'):
			filterProduct = Product.getProductByFilter(request.GET['category_id'])
			return render(request, 'all-capstone/shop.html',{"products":filterProduct,})

		return render(request, 'all-capstone/shop.html',{"products":products})

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
        
         
class OrderView(View):
	def get(self,request):
		customer_id = request.session.get('customer')
		orders = Order.objects.filter(customer=customer_id).order_by("-date").order_by("-id")
		print(orders)
		return render(request,'all-capstone/order.html',{"orders":orders})

class Cart(View):
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

class login(View):
	return_url = None

	def get(self,request):
		Login.return_url = request.GET.get('return_url')
		return render(request,'registration/login.html')

	def post(self,request):
		userData = request.POST
		customerEmail = Customer.emailExits(userData["email"])
		if customerEmail:
			if check_password(userData["password"],customerEmail.password):
				request.session["customer"] = customerEmail.id
				if Login.return_url:
					return HttpResponseRedirect(Login.return_url)
				else:
					Login.return_url = None
					return redirect('home')
			else:
				return render(request,'registration/login.html',{"userData":userData,"error":"Email or password doesn't match"})
		else:
			return render(request,'registration/login.html',{"userData":userData,"error":"Email or password doesn't match"})


def logout(request):
	request.session.clear()
	return redirect('home')