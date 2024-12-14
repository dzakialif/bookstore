from .cart import Cart

# create context processor
def cart(request):
    # return the default data from our cart
    return {'cart': Cart(request)}