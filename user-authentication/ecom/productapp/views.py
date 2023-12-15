from django.shortcuts import render
from .models import products
from math import ceil
# Create your views here.
def product(request):
    current_user=request.user
    all_products=[]
    cat_product=products.objects.values('category','id')
    category={item['category'] for item in cat_product}
    for categories in category:
        product=products.objects.filter(category=categories)
        n=len(product)
        number_slide=n//4 + ceil((n/4)-(n//4))
        all_products.append([product,range(1,number_slide),number_slide])
    product_list={
        'all_products':all_products
    }
    return render(request,"product/product-home.html",product_list)

