from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

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
		children = ChildOrder.objects.filter(parent_order__id=id)
	except ChildOrder.DoesNotExist:
		raise Http404('No Child Orders')
	context_dict = {'child_orders': children}


	return render(request, 'order_detail.html', context_dict)