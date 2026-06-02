from django.urls import path
from .. import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Menu CRUD
    path('menu/', views.MenuItemListView.as_view(), name='menu_list'),
    path('menu/add/', views.MenuItemCreateView.as_view(), name='menu_add'),
    path('menu/<int:pk>/edit/', views.MenuItemUpdateView.as_view(), name='menu_edit'),
    path('menu/<int:pk>/delete/', views.MenuItemDeleteView.as_view(), name='menu_delete'),
    
    # Category CRUD
    path('category/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Tables CRUD
    path('tables/', views.TableListView.as_view(), name='table_list'),
    path('tables/add/', views.TableCreateView.as_view(), name='table_add'),
    path('tables/<int:pk>/edit/', views.TableUpdateView.as_view(), name='table_edit'),
    path('tables/<int:pk>/delete/', views.TableDeleteView.as_view(), name='table_delete'),
    
    # Orders
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('order/<int:pk>/print/', views.ReceiptDetailView.as_view(), name='order_print'),
    path('create-order/<int:table_id>/', views.create_order, name='create_order'),
    
    # Kitchen
    path('kitchen/', views.KitchenDashboardView.as_view(), name='kitchen_dashboard'),
    
    # Inventory CRUD
    path('inventory/', views.IngredientListView.as_view(), name='ingredient_list'),
    path('inventory/add/', views.IngredientCreateView.as_view(), name='ingredient_add'),
    path('inventory/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient_detail'),
    path('inventory/<int:pk>/edit/', views.IngredientUpdateView.as_view(), name='ingredient_edit'),
    path('inventory/<int:pk>/delete/', views.IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('inventory/update-stock/<int:pk>/', views.update_stock, name='update_stock'),
    
    # Expense CRUD
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense_add'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
    
    # Reports
    path('reports/', views.ReportsDashboardView.as_view(), name='reports'),
    path('reports/export/csv/', views.export_sales_csv, name='export_sales_csv'),
    
    # Reservations CRUD
    path('reservations/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservations/add/', views.ReservationCreateView.as_view(), name='reservation_add'),
    path('reservations/<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='reservation_edit'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    
    # Customers CRUD
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),

    # Audit Logs
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit_log_list'),

    # Settings & User Management
    path('settings/', views.SettingsView.as_view(), name='settings_home'),
    path('settings/profile/', views.PersonalProfileView.as_view(), name='personal_profile'),
    path('settings/update/', views.RestaurantSettingUpdateView.as_view(), name='settings_update'),
    path('settings/users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('settings/users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('settings/users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # AJAX paths
    path('ajax/add-order-item/', views.add_order_item, name='add_order_item'),
    path('ajax/update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('ajax/get-cart-details/<int:order_id>/', views.get_cart_details, name='get_cart_details'),
    path('ajax/update-order-status/', views.update_order_status, name='update_order_status'),
    path('ajax/update-item-status/', views.update_item_status, name='update_item_status'),
    path('ajax/get-active-orders/', views.get_active_orders_json, name='get_active_orders'),
    path('ajax/toggle-user-status/', views.toggle_user_status, name='toggle_user_status'),
    path('ajax/reset-user-password/', views.reset_user_password, name='reset_user_password'),
    
    # Notifications
    path('ajax/notifications/', views.get_notifications, name='get_notifications'),
    path('ajax/notifications/<int:pk>/read/', views.mark_as_read, name='mark_notification_read'),
]
