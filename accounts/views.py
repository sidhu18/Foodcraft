from django.shortcuts import render,HttpResponse
import pyrebase
from django.contrib import auth
import time
from datetime import datetime, timezone
import pytz

config = {

    'apiKey': "AIzaSyBYJI0IHnJIVFk247THmD7MyDh6cOpMtpk",
    'authDomain': "foodcraft-9ff58.firebaseapp.com",
    'databaseURL': "https://foodcraft-9ff58.firebaseio.com",
    'projectId': "foodcraft-9ff58",
    'storageBucket': "foodcraft-9ff58.appspot.com",
    'messagingSenderId': "237384934762",
    # "serviceAccount": "/root/Desktop/cpanel-5e873-firebase-adminsdk-n6xb1-7a29d600a3.json"
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()
global userID
global admin_prev
global uid


def signIn(request):
    return render(request, "accounts/signIn.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
        uid = user['localId']
        name = database.child('users').child(uid).child('details').child('name').get().val()
        print(name)
        print(user['idToken'])
        session_id = user['idToken']
        global userID
        userID = str(session_id)
        global admin_prev
        admin_prev = name
        return render(request, "accounts/welcome.html", {"e": name})
    except Exception as e:
        message = "invalid credentials"
        return render(request, "accounts/signIn.html", {"messg": e})


def logout(request):
    global userID
    global admin_prev
    userID = ""
    admin_prev = ""
    return render(request, 'accounts/signIn.html')


def signUp(request):
    return render(request, "accounts/signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "Unable to create account try again"
        return render(request, "accounts/signup.html", {"messg": message})
    uid = user['localId']

    data = {"name": name, "status": "1"}

    database.child("users").child(uid).child("details").set(data)
    return render(request, "accounts/signIn.html")


def add_category(request):
    return render(request,'accounts/add_category.html')

def post_add_category(request):
    category = request.POST.get('category')
    url = request.POST.get('url')
    category_try = request.POST.get('sample')
    total=database.child('total_cat').get().val()
    total=int(total)
    total = total+1
    database.child('total_cat').set(total)

    data={

        "name": category,
        "url": url
    }
    database.child('categories').child(total).set(data)
    return render(request,'accounts/add_category.html')


def create(request):
    Ids = database.child('categories').shallow().get().val()
    cat_Ids=[]
    for i in Ids:
        cat_Ids.append(i)
    cat_Ids.sort()
    cat_name=[]
    for i in cat_Ids:
        cat = database.child('categories').child(i).child('name').get().val()
        cat_name.append(cat)
    cat_list = zip(cat_Ids, cat_name)

    return render(request, 'accounts/create.html',{'cat_list':cat_list})


def post_create(request):

    product_name = request.POST.get('name')
    amounttype = request.POST.get('amounttype')
    category = request.POST.get('category')
    description = request.POST.get('description')
    price = request.POST.get('price')
    url = request.POST.get('url')

    data = {
        "MenuId": category,
        "description": description,
        'image': url,
        "name": product_name,
        "price": int(price),
        "type": amounttype

    }
    product_ID = database.child('total_pro').get().val()
    product_ID=int(product_ID)
    product_ID = product_ID+1
    database.child('total_pro').set(product_ID)
    database.child('products').child(product_ID).set(data)
    return render(request, 'accounts/welcome.html', {'e': 'successfully added product'})


def check_categories(request):
    global userID
    idtoken = userID
    cat_Ids = database.child('categories').shallow().get().val()
    if cat_Ids is None:
        return render(request, 'accounts/check.html', {'e': 'no products found'})

    lis_cat_Ids = []

    for i in cat_Ids:
        lis_cat_Ids.append(i)
    lis_cat_Ids.sort()

    lis_cat_name = []

    for i in lis_cat_Ids:
        cat_name = database.child('categories').child(i).child('name').get().val()
        lis_cat_name.append(cat_name)
    print(lis_cat_Ids)
    print(lis_cat_name)

    comb_lis = zip(cat_Ids, lis_cat_name)

    return render(request, 'accounts/check.html', {'comb_lis': comb_lis })


def post_check(request):

    cat_Id = request.GET.get('z')
    global userID
    product_list = database.child('products').order_by_child('MenuId').equal_to(cat_Id).get().val()


    product_ids = product_list.keys()
    product_features = product_list.values()
    list_des=[]
    list_name=[]
    list_image= []
    list_price=[]
    list_menuId=[]
    list_type=[]

    for i in product_features:
        list_des.append(i['description'])
        list_name.append(i['name'])
        list_image.append(i['image'])
        list_price.append(i['price'])
        list_menuId.append(i['MenuId'])
        list_type.append(i['type'])


    comb_lis = zip(product_ids, list_name, list_des, list_price, list_image, list_type)

    return render(request, 'accounts/product_list.html', {'comb_lis': comb_lis})

def post_remove(request):
    product_ID = request.GET.get('z')
    global userID
    idtoken = userID

    try:
        database.child('products').child(product_ID).remove(userID)
    except Exception as e:
        return render(request, 'accounts/welcome.html', {'e': 'Couldnot remove item'})
    return check_categories(request)


def post_pre_update(request):
    product_ID = request.GET.get('z')
    global userID
    idtoken = userID
    cat_Ids = database.child('categories').shallow().get().val()
    if cat_Ids is None:
        return render(request, 'accounts/welcome.html', {'e': 'no products found'})

    lis_cat_Ids = []
    for i in cat_Ids:
        lis_cat_Ids.append(i)
    lis_cat_Ids.sort()

    lis_cat_name = []

    for i in lis_cat_Ids:
        cat_name = database.child('categories').child(i).child('name').get().val()
        lis_cat_name.append(cat_name)
    print(lis_cat_Ids)
    print(lis_cat_name)

    comb_lis = zip(cat_Ids, lis_cat_name)
    return render(request, 'accounts/post_update.html', {'product_ID':product_ID, 'comb_lis':comb_lis})

def post_update(request):

    product_id = request.POST.get('product_id')
    product_name = request.POST.get('name')
    category = request.POST.get('category')
    amounttype = request.POST.get('amounttype')
    description = request.POST.get('description')
    price = request.POST.get('price')
    url = request.POST.get('url')

    data = {
        "MenuId": category,
        "description": description,
        'image': url,
        "name": product_name,
        "price": int(price),
        "type": amounttype
    }
    database.child('products').child(product_id).set(data)
    return render(request, 'accounts/welcome.html', {'e': 'Item edited Successfully'})


'''The below function is used for viewing the new orders placed by the users'''


def view_new_orders(request):

    global userID
    global admin_prev

    orders = database.child('orders').child(admin_prev).order_by_key().limit_to_last(11).get().val()
    print(orders)
    orders.pop('stable', None)
    return render(request, 'accounts/new_orders_list.html', {'orders': orders})



def order_taken(request):
    global admin_prev
    global userID

    order_id = request.GET.get('z')
    selected = database.child('orders').child(admin_prev).child(order_id).get().val()
    uid = database.child('orders').child(admin_prev).child(order_id).child('user_ID').get().val()
    if admin_prev == 'admin1':
        try:
            database.child('orders').child('admin2').child(order_id).set(selected)
            database.child('Users').child(uid).child('orders_made').child(order_id).child('status').set(1)
            database.child('orders').child(admin_prev).child(order_id).remove(userID)
            return view_new_orders(request)
        except Exception as e:
            return render(request, 'accounts/welcome.html', {'e': e})

    if admin_prev == 'admin2':
        try:
            database.child('orders').child('admin3').child(order_id).set(selected)
            database.child('Users').child(uid).child('orders_made').child(order_id).child('status').set(2)
            database.child('orders').child(admin_prev).child(order_id).remove(userID)
            return view_new_orders(request)
        except Exception as e:
            return render(request, 'accounts/welcome.html', {'e': e})

    if admin_prev == 'admin3':
        try:
            database.child('orders').child('delivered').child(order_id).set(selected)
            database.child('Users').child(uid).child('orders_made').child(order_id).child('status').set(3)
            database.child('orders').child(admin_prev).child(order_id).remove(userID)
            return view_new_orders(request)
        except Exception as e:
            return render(request, 'accounts/welcome.html', {'e': e})


def view_completed_orders(request):
    global userID
    global admin_prev

    orders = database.child('orders').child('delivered').order_by_key().limit_to_last(11).get().val()
    orders.pop('stable', None)
    print(orders)


    return render(request, 'accounts/view_completed_orders.html', {'orders': orders})












