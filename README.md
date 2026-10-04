# Men's Fashion Django E-Commerce Starter

A responsive Django clothing-store starter with:
- Men/Kids categories
- Brand, colour and discount filters
- Product details, colour-image switching and size selection
- Session cart / shopping bag
- Login, registration and profile
- Checkout and order creation
- Django admin for products, customers and orders
- Reviews restricted to customers who bought the product
- SQLite development database

## Windows setup

```bat
cd mens_fashion_django
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Add products

Use Django Admin to create Categories, Brands, Colours, Sizes and Products.
Upload product images through the admin.

## Payment

The checkout currently records a selected payment method and creates an order. It does **not** process real card/UPI payments. For production, integrate a payment gateway such as Razorpay/Stripe using server-side verification and webhooks; never store card numbers, CVV or UPI PINs.
