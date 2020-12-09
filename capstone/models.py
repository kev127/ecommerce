from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class RecentWork(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.title

class Product(models.Model):
	name = models.CharField(max_length=220)
	price = models.IntegerField(default=0)
	category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
	description = models.TextField()
	image = models.ImageField(upload_to='upload/products')
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

class Category(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


	@staticmethod
	def getAllCategory():
		return Category.objects.all()