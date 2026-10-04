import uuid
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CheckoutForm, RegisterForm, ReviewForm
from .models import Product, Order, OrderItem, Review, Brand, Colour, Category

def home(request):
    products = Product.objects.filter(active=True).prefetch_related("colours","sizes")
    q = request.GET.get("q","").strip()
    category = request.GET.get("category","")
    brand = request.GET.get("brand","")
    colour = request.GET.get("colour","")
    discount = request.GET.get("discount","")
    if q: products = products.filter(name__icontains=q)
    if category: products = products.filter(category__name__iexact=category)
    if brand: products = products.filter(brand__name__iexact=brand)
    if colour: products = products.filter(colours__name__iexact=colour)
    if discount == "12": products = products.filter(discount_percent__lte=12)
    elif discount == "40": products = products.filter(discount_percent__lte=40)
    elif discount == "80": products = products.filter(discount_percent__lte=80)
    return render(request, "home.html", {
        "products": products.distinct(), "brands": Brand.objects.all(),
        "colours": Colour.objects.all(), "categories": Category.objects.all(),
        "selected": request.GET
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    reviews = product.reviews.select_related("user").order_by("-created_at")
    can_review = request.user.is_authenticated and OrderItem.objects.filter(
        order__user=request.user, product=product, order__status="DELIVERED").exists()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        if not can_review:
            messages.error(request, "You can review this product after purchasing and receiving it.")
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product, review.user = product, request.user
                review.save()
                messages.success(request, "Review added.")
                return redirect("product_detail", pk=pk)
    else:
        form = ReviewForm()
    return render(request, "product_detail.html", {"product":product,"reviews":reviews,"form":form,"can_review":can_review})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    if request.method != "POST":
        return redirect("product_detail", pk=pk)
    colour = request.POST.get("colour","")
    size = request.POST.get("size","")
    quantity = max(1, int(request.POST.get("quantity",1)))
    cart = request.session.get("cart", {})
    key = f"{pk}:{colour}:{size}"
    current = cart.get(key, {"product_id":pk,"colour":colour,"size":size,"quantity":0})
    current["quantity"] = min(current["quantity"] + quantity, product.stock or 1)
    cart[key] = current
    request.session["cart"] = cart
    messages.success(request, "Product added to bag.")
    return redirect("cart")

def cart_items(request):
    result=[]
    cart=request.session.get("cart",{})
    for key,item in cart.items():
        try:
            p=Product.objects.get(pk=item["product_id"],active=True)
            result.append((key,item,p))
        except Product.DoesNotExist:
            pass
    return result

def cart(request):
    items=cart_items(request)
    subtotal=sum((p.selling_price*item["quantity"] for _,item,p in items), Decimal("0"))
    return render(request,"cart.html",{"items":items,"subtotal":subtotal})

def update_cart(request, pk):
    if request.method=="POST":
        key=request.POST.get("key")
        qty=max(1,int(request.POST.get("quantity",1)))
        cart=request.session.get("cart",{})
        if key in cart:
            cart[key]["quantity"]=qty
            request.session["cart"]=cart
    return redirect("cart")

def remove_from_cart(request, pk):
    key=request.POST.get("key") if request.method=="POST" else None
    cart=request.session.get("cart",{})
    if key in cart:
        del cart[key]
        request.session["cart"]=cart
    return redirect("cart")

@login_required
def checkout(request):
    items=cart_items(request)
    if not items:
        messages.info(request,"Your bag is empty.")
        return redirect("home")
    subtotal=sum((p.selling_price*item["quantity"] for _,item,p in items), Decimal("0"))
    delivery=Decimal("0") if subtotal >= Decimal("999") else Decimal("50")
    total=subtotal+delivery
    if request.method=="POST":
        form=CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order=Order.objects.create(
                    user=request.user, order_id="ORD"+uuid.uuid4().hex[:12].upper(),
                    full_name=form.cleaned_data["full_name"], email=form.cleaned_data["email"],
                    mobile=form.cleaned_data["mobile"], address=form.cleaned_data["address"],
                    city=form.cleaned_data["city"], state=form.cleaned_data["state"],
                    pincode=form.cleaned_data["pincode"], subtotal=subtotal,
                    delivery_charge=delivery, total_amount=total,
                    payment_method=form.cleaned_data["payment_method"],
                    payment_status="PENDING" if form.cleaned_data["payment_method"]!="COD" else "PENDING")
                for _,item,p in items:
                    OrderItem.objects.create(order=order,product=p,colour=item["colour"],
                                             size=item["size"],quantity=item["quantity"],price=p.selling_price)
            request.session["cart"]={}
            return redirect("order_detail", order_id=order.order_id)
    else:
        form=CheckoutForm(initial={"full_name":request.user.get_full_name(),"email":request.user.email})
    return render(request,"checkout.html",{"form":form,"items":items,"subtotal":subtotal,"delivery":delivery,"total":total})

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("home")
    else: form=RegisterForm()
    return render(request,"auth/register.html",{"form":form})

def user_login(request):
    if request.method=="POST":
        user=authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user:
            login(request,user); return redirect("home")
        messages.error(request,"Invalid username or password.")
    return render(request,"auth/login.html")

def user_logout(request):
    logout(request); return redirect("home")

@login_required
def profile(request):
    orders=request.user.orders.order_by("-created_at")
    return render(request,"profile.html",{"orders":orders})

@login_required
def order_detail(request,order_id):
    order=get_object_or_404(Order,order_id=order_id,user=request.user)
    return render(request,"order_detail.html",{"order":order})
