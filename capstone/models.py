from django.db import models
import datetime

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class RecentWork(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/recent")

    def __str__(self):
        return self.title

class Product(models.Model):
	name = models.CharField(max_length=220)
	price = models.IntegerField(default=0)
	description = models.TextField()
	image = models.ImageField(upload_to='media/products')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

	@staticmethod
	def getAllProduct():
		return Product.objects.all()

	@staticmethod
	def getProductByFilter(category_id):
		if category_id:
			return Product.objects.filter(category = category_id)
		else:
			return Product.getAllProduct()

	@staticmethod
	def getProductById(productList):
		return Product.objects.filter(id__in=productList)

class Customer(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=255)
	phone = models.CharField(max_length=15)
	password = models.CharField(max_length=255)

	def __str__(self):
		return self.name


	@staticmethod
	def emailExits(userEmail):
		try:
			email = Customer.objects.get(email=userEmail)
			return email
		except:
			return False

class Order(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	price = models.IntegerField()
	date = models.DateField(default=datetime.datetime.today)
	address = models.CharField(max_length=255,blank=True)
	phone = models.CharField(max_length=15,blank=True)
	completed = models.BooleanField(default=False)

	
	def __str__(self):
		return self.customer.email

class Category(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


	@staticmethod
	def getAllCategory():
		return Category.objects.all()