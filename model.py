import sqlite3

class Melon(object):
    """A wrapper object that corresponds to rows in the melons table."""
    def __init__(self, id, melon_type, common_name, price, imgurl, flesh_color, rind_color, seedless):
        self.id = id
        self.melon_type = melon_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        return "$%.2f"%self.price

    def __repr__(self):
        return "<Melon: %s, %s, %s>"%(self.id, self.common_name, self.price_str())

class Customer(object):
    def __init__(self, firstname, surname, user_email, user_password):
      self.firstname = firstname
      self.surname = surname
      self.email = user_email
      self.password = user_password

def connect():
    conn = sqlite3.connect("melons.db")
    cursor = conn.cursor()
    return cursor

def get_melons():
    """Query the database for the first 30 melons, wrap each row in a Melon object"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE imgurl <> ''
               LIMIT 30;"""

    cursor.execute(query)
    melon_rows = cursor.fetchall()

    melons = []

    for row in melon_rows:
        melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                      row[6], row[7])

        melons.append(melon)

    print melons

    return melons

def get_customer_by_email(email):
    print "email is %s" % email
    cursor = connect()
    query = """SELECT givenname, surname, password
                FROM customers
                WHERE email = ?;"""

    cursor.execute(query, (email, ))
    customer_row = cursor.fetchone()

    if not customer_row == None:
      customer_firstname = customer_row[0]
      customer_surname = customer_row[1]
      customer_password = customer_row[2]
      customer_email = email
      customer = Customer(customer_firstname, customer_surname, customer_email, customer_password)

    else:
      customer = None

    return customer


def get_melon_by_id(id):
    """Query for a specific melon in the database by the primary key"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE id = ?;"""

    cursor.execute(query, (id,))

    row = cursor.fetchone()
    
    if not row:
        return None

    melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7])
    
    return melon

# def get_melons_by_id(id):
#     """Query for a specific melon in the database by the primary key"""
#     cursor = connect()
#     query = """SELECT id, melon_type, common_name,
#                       price, imgurl,
#                       flesh_color, rind_color, seedless
#                FROM melons
#                WHERE id = ?;"""

#     cursor.execute(query, (id,))

#     melon_rows = cursor.fetchall()

#     melons_dict = {}

#     for row in melon_rows:
#         melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
#                       row[6], row[7])
        
#         melon_id = melon.id
#         melon_name = melon.common_name
#         melon_price = melon.price

#         melons_dict[melon_id] = (melon_name, melon_price)


#     return melons_dict

