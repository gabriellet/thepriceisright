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
			try:
				order = ParentOrder(
					quantity = form.cleaned_data['quantity'], 
					stock_type = "ACME ETF", 
					is_sell = True,
					user = request.user)
				if order.is_valid():
					order.save()
				else:
					# TODO
					return HttpResponse("Invalid Order! Order quantity must be an integer greater than zero.")

				t1 = Thread(target=order.trade)  # automatically try to execute trade upon submission
				t1.daemon = True
				t1.start()
				return redirect('index')

			except:
				# TODO
				return HttpResponse("Invalid Order!")

		else:
			# TODO
			return HttpResponse("Form not Valid")

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

	if total_sold['quantity__sum'] is None:
		progress = 0.0
	else:
		progress = (float(total_sold['quantity__sum'])/float(parent.quantity)) * 100

	if total_price['total'] is None:
		avg_price = 0.0
		total_price = 0.0
		total_sold = 0
	else:
		total_price = total_price['total']
		total_sold = total_sold['quantity__sum']
		avg_price = '{:,.2f}'.format(total_price/total_sold)

	return render(request, 'order_detail.html', 
		{
		'child_orders': children, 
		'parent_order': parent, 
		'average_price': avg_price,
		'total_price': '{:,.2f}'.format(total_price),
		'total_sold': '{:,d}'.format(total_sold),
		'progress': progress
		})

def get_progress(request, id):
	parent = get_object_or_404(ParentOrder, id=id)
	current_progress = '{:,.2f}'.format(parent.progress)
	return HttpResponse(current_progress)


def pause_order(request, id):
	parent = get_object_or_404(ParentOrder, id=id)
	parent.status = ParentOrder.PAUSED
	parent.save()

def cancel_order(request, id):
	parent = get_object_or_404(ParentOrder, id=id)
	parent.status = ParentOrder.CANCELLED
	parent.save()
