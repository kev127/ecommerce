from django.contrib import admin
from .models import Service,RecentWork,Customer,Order,Product

admin.site.register(Service)
admin.site.register(RecentWork)
admin.site.register(Product,AdminProduct)
admin.site.register(Customer)
admin.site.register(Order)
