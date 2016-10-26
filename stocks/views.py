from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from forms import ParentOrderForm
from models import ParentOrder

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
			return redirect('index')

		else:
			print form.errors

	else:
		form = ParentOrderForm()

	return render(request, 'stocks.html', {'form': form})