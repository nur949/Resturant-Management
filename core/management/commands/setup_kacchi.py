from django.core.management.base import BaseCommand
from core.models import Category, MenuItem, Table, Order, OrderItem, Ingredient, Expense, Reservation, Customer, RestaurantSetting

class Command(BaseCommand):
    help = 'Cleans the database and populates it with Kacchi Bhai menu data.'

    def handle(self, *args, **options):
        self.stdout.write("--- Cleaning Database ---")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        MenuItem.objects.all().delete()
        Category.objects.all().delete()
        Table.objects.all().delete()
        Ingredient.objects.all().delete()
        Expense.objects.all().delete()
        Reservation.objects.all().delete()
        Customer.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Operational data cleared."))

        self.stdout.write("--- Populating Kacchi Bhai Menu ---")
        
        # 1. Categories
        categories = {
            "Kacchi Biryani": "Signature long-grain bashmati kacchi with succulent mutton and flavorful potato.",
            "Morog Polao": "Authentic chicken polao with roasted chicken and aromatic rice.",
            "Sides & Add-ons": "Delicious extras to complement your main meal.",
            "Beverages": "Refreshing drinks and traditional appetisers.",
            "Desserts": "Sweet endings for a perfect meal."
        }
        
        cat_objs = {}
        for name, desc in categories.items():
            obj = Category.objects.create(name=name, description=desc)
            cat_objs[name] = obj
            self.stdout.write(f"Category Created: {name}")

        # 2. Menu Items
        menu_items = [
            {"cat": "Kacchi Biryani", "name": "Bashmati Mutton Kacchi (Regular)", "price": 250.00, "desc": "1 Piece Mutton, 1 Potato, Bashmati Rice."},
            {"cat": "Kacchi Biryani", "name": "Bashmati Mutton Kacchi (Large)", "price": 450.00, "desc": "2 Pieces Mutton, 1 Potato, Extra Rice."},
            {"cat": "Kacchi Biryani", "name": "Special Kacchi Platter", "price": 360.00, "desc": "Kacchi with Roast, Kabab and Borhani."},
            {"cat": "Morog Polao", "name": "Classic Morog Polao", "price": 220.00, "desc": "Aromatic Chinigura rice with 1 pc Chicken Roast."},
            {"cat": "Sides & Add-ons", "name": "Chicken Roast", "price": 130.00, "desc": "Standard sized Bangladeshi chicken roast."},
            {"cat": "Sides & Add-ons", "name": "Beef Rezala", "price": 160.00, "desc": "Classic slow-cooked beef curry."},
            {"cat": "Sides & Add-ons", "name": "Shami Kabab", "price": 40.00, "desc": "Fried beef lentil kabab."},
            {"cat": "Beverages", "name": "Borhani (Glass)", "price": 50.00, "desc": "Traditional spicy yogurt drink."},
            {"cat": "Beverages", "name": "Badam Shorbot", "price": 90.00, "desc": "Milk-based mixed nut refreshing drink."},
            {"cat": "Desserts", "name": "Shahre Jorda", "price": 60.00, "desc": "Traditional sweet orange rice."},
            {"cat": "Desserts", "name": "Special Firni", "price": 50.00, "desc": "Rich and creamy rice pudding."}
        ]
        
        for item in menu_items:
            MenuItem.objects.create(
                category=cat_objs[item["cat"]],
                name=item["name"],
                price=item["price"],
                description=item["desc"]
            )
            self.stdout.write(f"Item Created: {item['name']}")

        self.stdout.write("Creating Tables...")
        for i in range(1, 13):
            Table.objects.create(number=i, capacity=4 if i < 9 else 6)
        
        self.stdout.write("Updating Restaurant Identity...")
        settings = RestaurantSetting.load()
        settings.name = "Kacchi Bhai"
        settings.tagline = "The Ultimate Taste of Kacchi"
        settings.currency_symbol = "TK"
        settings.save()

        self.stdout.write(self.style.SUCCESS("--- Successfully Migrated to Kacchi Bhai Menu ---"))
