import os
import django

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')
django.setup()

from core.models import Category, MenuItem, Table, Order, OrderItem, Ingredient, Expense, Reservation, Customer, RestaurantSetting

def clean_database():
    print("--- Cleaning Database ---")
    # Delete operational data (Order items first because of FK)
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    MenuItem.objects.all().delete()
    Category.objects.all().delete()
    Table.objects.all().delete()
    Ingredient.objects.all().delete()
    Expense.objects.all().delete()
    Reservation.objects.all().delete()
    Customer.objects.all().delete()
    print("Operational data cleared.")

def populate_kacchi_bhai():
    print("--- Populating Kacchi Bhai Menu ---")
    
    # 1. Categories
    categories = {
        "Kacchi Biryani": "Our signature long-grain bashmati kacchi with succulent mutton and flavorful potato.",
        "Morog Polao": "Authentic Bangladeshi style chicken polao with roasted chicken and aromatic rice.",
        "Sides & Add-ons": "Delicious extras to complement your main meal.",
        "Beverages": "Refreshing drinks and traditional appetisers.",
        "Desserts": "Sweet endings for a perfect meal."
    }
    
    cat_objs = {}
    for name, desc in categories.items():
        obj = Category.objects.create(name=name, description=desc)
        cat_objs[name] = obj
        print(f"Category Created: {name}")

    # 2. Menu Items
    menu_items = [
        # Kacchi
        {"cat": "Kacchi Biryani", "name": "Bashmati Kacchi (Regular)", "price": 250.00, "desc": "1 Piece Mutton, 1 Potato, Bashmati Rice."},
        {"cat": "Kacchi Biryani", "name": "Bashmati Kacchi (Large)", "price": 450.00, "desc": "2 Pieces Mutton, 1 Potato, Extra Rice."},
        {"cat": "Kacchi Biryani", "name": "Special Kacchi Platter", "price": 360.00, "desc": "Kacchi with Roast, Kabab and Borhani."},
        
        # Morog Polao
        {"cat": "Morog Polao", "name": "Classic Morog Polao", "price": 220.00, "desc": "Aromatic Chinigura rice with 1 pc Chicken Roast."},
        {"cat": "Morog Polao", "name": "Morog Polao Special", "price": 280.00, "desc": "Classic polao with extra rezala gravy."},
        
        # Sides
        {"cat": "Sides & Add-ons", "name": "Chicken Roast", "price": 130.00, "desc": "Standard sized Bangladeshi chicken roast."},
        {"cat": "Sides & Add-ons", "name": "Beef Rezala", "price": 160.00, "desc": "Classic slow-cooked beef curry."},
        {"cat": "Sides & Add-ons", "name": "Shami Kabab", "price": 40.00, "desc": "Fried beef lentil kabab."},
        {"cat": "Sides & Add-ons", "name": "Mutton Piece (Extra)", "price": 180.00, "desc": "Extra piece of mutton for kacchi lovers."},
        
        # Beverages
        {"cat": "Beverages", "name": "Borhani (Glass)", "price": 50.00, "desc": "Traditional spicy yogurt drink."},
        {"cat": "Beverages", "name": "Badam Shorbot", "price": 90.00, "desc": "Milk-based mixed nut refreshing drink."},
        {"cat": "Beverages", "name": "Mineral Water (500ml)", "price": 20.00, "desc": "Fresh drinking water."},
        
        # Desserts
        {"cat": "Desserts", "name": "Shahre Jorda", "price": 60.00, "desc": "Traditional sweet orange rice with baby sweets."},
        {"cat": "Desserts", "name": "Special Firni", "price": 50.00, "desc": "Rich and creamy rice pudding."}
    ]
    
    for item in menu_items:
        MenuItem.objects.create(
            category=cat_objs[item["cat"]],
            name=item["name"],
            price=item["price"],
            description=item["desc"]
        )
        print(f"Item Created: {item['name']}")

    # 3. Tables
    print("Creating Tables...")
    for i in range(1, 13):
        Table.objects.create(number=i, capacity=4 if i < 9 else 6)
    
    # 4. Update Restaurant Settings
    print("Updating Restaurant Identity...")
    settings = RestaurantSetting.load()
    settings.name = "Kacchi Bhai"
    settings.tagline = "The Ultimate Taste of Kacchi"
    settings.currency_symbol = "TK"
    settings.save()

if __name__ == "__main__":
    clean_database()
    populate_kacchi_bhai()
    print("--- Successfully Migrated to Kacchi Bhai Menu ---")
