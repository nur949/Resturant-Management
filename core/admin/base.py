from django.contrib import admin
from ..models import Category, MenuItem, Table, Order, OrderItem, Expense, Ingredient, RecipeItem, Customer, Reservation, RestaurantSetting, UserProfile

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Expense)
admin.site.register(Ingredient)
admin.site.register(RecipeItem)
admin.site.register(Customer)
admin.site.register(Reservation)
admin.site.register(RestaurantSetting)
admin.site.register(UserProfile)
