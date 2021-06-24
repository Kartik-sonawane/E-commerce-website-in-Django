from django.shortcuts import render, redirect
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# home
class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category ='TW')
  bottomwears = Product.objects.filter(category ='BW')
  mobiles = Product.objects.filter(category ='M')
  laptops = Product.objects.filter(category ='L')
  return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, })


#  product_detail
class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_in_cart= False
  if request.user.is_authenticated:
   item_in_cart= Cart.objects.filter(Q(product = product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html', {'product':product, 'item_in_cart':item_in_cart})


# Add to Cart
@login_required
def add_to_cart(request):
 user = request.user
 product_id =request.GET.get('prod_id')
 product = Product.objects.get(id = product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

# Show Cart
@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 100.0
  totleamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]

  if cart_product:
   for p in cart_product:
    temp_amount =(p.quantity * p.product.discounted_price)
    amount += temp_amount
    totleamount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts':cart, 'totleamount' :totleamount, 'amount':amount})
  else:
   return render(request, 'app/emptycart.html')


# plus or increase quantity
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 100.0
  totleamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
   totleamount = amount + shipping_amount

  data = {
   'quantity' : c.quantity,
   'amount' : amount,
   'totleamount' : totleamount
  }
  return JsonResponse(data)

# minus or increase quantity
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_amount = 100.0
  totleamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
   totleamount = amount + shipping_amount

  data = {
   'quantity' : c.quantity,
   'amount' : amount,
   'totleamount' : totleamount
  }
  return JsonResponse(data)

# remove_cart
def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 100.0
  totleamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
   totleamount = amount + shipping_amount

  data = {
   'amount' : amount,
   'totleamount' : totleamount
  }
  return JsonResponse(data)


# Checkout
@login_required
def checkout(request):
 user = request.user
 addr = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 temp_amount=0.0
 amount = 0.0
 shipping_amount = 100.0
 totleamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
  totleamount = amount + shipping_amount
 return render(request, 'app/checkout.html', {'addr':addr, 'totleamount':totleamount, 'cart_items':cart_items, 'temp_amount':temp_amount})


# Payment Done
@login_required
def paymentdone(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id = custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect('/orders')


# Order
@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})

# Buy Now
@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


# profile
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   nm = form.cleaned_data['name']
   loc = form.cleaned_data['locality']
   ct = form.cleaned_data['city']
   st = form.cleaned_data['state']
   zc = form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=nm, locality=loc, city=ct, state=st, zipcode=zc,)
   reg.save()
   form = CustomerProfileForm()
   messages.success(request, 'Congratulations... Profile Updated Successfully !!')
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


# Address
@login_required
def address(request):
 addr = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'addr':addr, 'active':'btn-primary'})


# mobile Section
def mobile(request, data=None):
 global mobiles
 if data == None:
  mobiles = Product.objects.filter(category = 'M')
 elif data == 'Redmi':
  mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'Realme':
  mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'Oppo':
  mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'Apple':
  mobiles = Product.objects.filter(category='M').filter(brand = data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt = 30000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt = 30000)
 return render(request, 'app/mobile.html', {'mobiles':mobiles})

# laptop section
def laptop(request, data=None):
 global laptops
 if data == None:
  laptops = Product.objects.filter(category ='L')
 elif data == 'Apple':
  laptops = Product.objects.filter(category='L').filter(brand = data)
 elif data == 'Dell':
  laptops = Product.objects.filter(category='L').filter(brand = data)
 elif data == 'Asus':
  laptops = Product.objects.filter(category='L').filter(brand = data)
 elif data == 'hp':
  laptops = Product.objects.filter(category='L').filter(brand = data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt = 50000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt = 50000)
 return render(request, 'app/laptop.html', {'laptops':laptops})

# top wears
def topwear(request, data=None):
 global topwears
 if data == None:
  topwears = Product.objects.filter(category ='TW')
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt = 1000)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt = 1000)
 return render(request, 'app/topwear.html', {'topwears':topwears})

# bottom wears
def bottomwear(request, data=None):
 global bottomwears
 if data == None:
  bottomwears = Product.objects.filter(category ='BW')
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt = 1000)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt = 1000)
 return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})


# registration
class CustomerRegistrationView(View):
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, "Congratulation..! Your Registration is Successful.")
   form.save()
   form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form': form})
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})

