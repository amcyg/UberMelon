from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():

    melon_ids = session.get("cart_key")

    melon_qty = {}
    for melon_id in melon_ids:
        if melon_qty.get(melon_id):
            melon_qty[melon_id] += 1
        else:
            melon_qty[melon_id] = 1
    print melon_qty


    melon_dict = {}
    for melon_id, qty in melon_qty.items():
        melon = model.get_melon_by_id(melon_id)
        melon_dict[melon] = qty
    print melon_dict

    grand_total = 0
    for melon, qty in melon_dict.items():
        grand_total += (melon.price * qty)

    return render_template("cart.html",
                            melons = melon_dict,
                            total = grand_total)


    if 'cart_key' in session:
        print "YAY THERE IS A CART!"
        print session["cart_key"]
        for id in session["cart_key"]:
            melon_dict = model.get_melons_by_id(id)

            melon_name = melon_dict[id][0]
            melon_price = melon_dict[id][1]

   
    return render_template("cart.html", melon_name = melon_name,
                                        melon_price = melon_price)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if not session.get('cart_key'):
        session['cart_key'] = []
    session['cart_key'].append(id)

    print session
    flash("A melon has been added to your cart!")      

    return redirect("/cart")



@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    f = request.form

    user_email = f.get('email')
    print(model.get_customer_by_email(user_email))
    customer = model.get_customer_by_email(user_email)

    if customer == None:
        print "You're not in the database!"
        flash("You're not in the database!")
    else:
        session['name'] = customer.firstname
        flash("You've successfully logged on! Yay!")


    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
