from django.shortcuts import render
from django.http import HttpResponse
from .models import ParentOrder
from .forms import TradeForm

# Create your views here.

def index(request):
	if request.method == 'POST':
		form = TradeForm(request.POST)
		if form.is_valid():
			q = form.cleaned_data['qty']
			q = int(q)
			o = ParentOrder(quantity = q, stock_type = "ACME ETF", is_sell = True)
			o.save()
		return HttpResponse('Successful Trade')
	else:
		form = TradeForm()
	return render(request, 'stocks.html', {'form': form})