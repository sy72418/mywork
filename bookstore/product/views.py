from django.shortcuts import render

# Create your views here.

from .models import goods

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def product(request):
    
    book = ''
    
    if 'p' in request.GET:
        book = request.GET['p']
        if len(book)>0:
            allgoods = goods.objects.filter(title__icontains=book)

        else:
            allgoods = goods.objects.all()
    else:
        allgoods = goods.objects.all()
        
    paginator = Paginator(allgoods,20)
    page = request.GET.get('page')
    try:
        allgoods = paginator.page(page)
    except PageNotAnInteger:
        allgoods = paginator.page(1)
    except EmptyPage:
        allgoods = paginator.page(paginator.num_pages)
        
        
    
    return render(request,'product.html',locals())