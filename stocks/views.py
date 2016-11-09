from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.db.models import Sum, F

from forms import ParentOrderForm
from models import ParentOrder, ChildOrder
from threading import Thread

@login_required(login_url="/")
def index(request):
	if request.method == 'POST':
		form = ParentOrderForm(request.POST)

		if form.is_valid():
			order = ParentOrder(
				quantity = form.cleaned_data['quantity'], 
				stock_type = "ACME ETF", 
				is_sell = True,
				user = request.user)
			if order.is_valid():
				order.save()
			else:
				return HttpResponse("Invalid Order! Order quantity must be an integer greater than zero.")

			t1 = Thread(target=order.trade)  # automatically try to execute trade upon submission
			t1.daemon = True
			t1.start()
			return redirect('index')

		else:
			print form.errors

	else:
		form = ParentOrderForm()

	return render(request, 'place_order.html', {'form': form})

@login_required(login_url="/")
def order_detail(request, id):
	try:
		children = ChildOrder.objects.filter(parent_order__id=id).order_by('-time_executed')
	except ChildOrder.DoesNotExist:
		raise Http404('No Child Orders')

	parent = get_object_or_404(ParentOrder, id=id)
	
	total_price = children.filter(is_successful=True).aggregate(total=Sum(F('price') * F('quantity')))
	total_sold = children.filter(is_successful=True).aggregate(Sum('quantity'))

	if total_sold['quantity__sum'] == None:
		progress = 0.0
	else:
		progress = (float(total_sold['quantity__sum'])/float(parent.quantity)) * 100

	return render(request, 'order_detail.html', 
		{
		'child_orders': children, 
		'parent_order': parent, 
		'average_price': '{:,.2f}'.format(total_price['total']/total_sold['quantity__sum']),
		'total_price': '{:,.2f}'.format(total_price['total']),
		'total_sold': '{:,d}'.format(total_sold['quantity__sum']),
		'progress': progress
		})