from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from stocks.models import ParentOrder, ChildOrder
# from forms import UserForm

@login_required(login_url="login/")
def index(request):
    order_list = ParentOrder.objects.all().order_by('-time_executed')
    for order in order_list:
    	if order.success == False:
    		child_sold = ChildOrder.objects.filter(parent_order=order.id).aggregate(Sum('quantity'))['quantity__sum']
    		if order.quantity == 0:
    			order.progress = 100
    		else:
    			order.progress = (child_sold/order.quantity) * 100
    	else:
    		order.progress = 100
    context_dict = {'orders': order_list}

    return render(request, "index.html", context_dict)

# def register(request):
#     # Like before, get the request's context.
#     context = RequestContext(request)

#     # A boolean value for telling the template whether the registration was successful.
#     # Set to False initially. Code changes value to True when registration succeeds.
#     registered = False

#     # if post, process form data
#     if request.method == 'POST':
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserProfileForm.
#         user_form = UserForm(data=request.POST)

#         # If the two forms are valid...
#         if user_form.is_valid():
#             # Save the user's form data to the database.
#             user = user_form.save()

#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()

#             registered = True

#         # invalid form
#         else:
#             print user_form.errors

#     # Not a HTTP POST, so we render our form using two ModelForm instances.
#     # These forms will be blank, ready for user input.
#     else:
#         user_form = UserForm()

#     # Render the template depending on the context.

#     return render(request, "register.html", {'user_form': user_form, 'registered': registered})