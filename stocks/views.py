from django.shortcuts import render
from django.http import HttpResponse
from forms import ParentOrderForm

# Create your views here.

def index(request):
	if request.method == 'POST':
		form = ParentOrderForm(request.POST)

		if form.is_valid():
			order = order_form.save()
			order.save()
			return HttpResponse('Successful Trade')

		else:
			print form.errors

	else:
		form = ParentOrderForm()
	return render(request, 'stocks.html', {'form': form})

