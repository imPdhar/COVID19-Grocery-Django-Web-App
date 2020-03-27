from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
import pyrebase
config={
    'apiKey': "AIzaSyDjKBhKFMQXgEsY1Mwu1iF5hciYoDWHXlw",
    'authDomain': "covid-grocer.firebaseapp.com",
    'databaseURL': "https://covid-grocer.firebaseio.com",
    'projectId': "covid-grocer",
    'storageBucket': "covid-grocer.appspot.com",
    'messagingSenderId': "392378464185",
    'appId': "1:392378464185:web:347bde56bd9bd3b49ae868",
    'measurementId': "G-5Z5SR79KCH"
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()
def display(request):
    return render(request,"display.html")

def signIn(request):
    return render(request,"signIn.html")
def shoplist(request):
    html="<html><head><title>home page</title></head><body>"
    loc=request.POST.get('loc')
    datab=dict(dict(database.get().val())['users'])

    no_shop_present = True
    for i in datab.keys():
        if datab[i]['details']['location']==loc:
            no_shop_present = False
            html=html+"<table border =\"5\"><tr><td rowspan=\"2\">"+datab[i]['details']["shopname"]+"</td><td>"+datab[i]['details']["description"]+"</td></tr>            <tr><td>"+datab[i]['details']["location"]+"</td></tr>            </table>"


    if no_shop_present:
        html += "<h2>Sorry no shop is registerd for this location on this app</h2>"
    else:
        html+="<br><br><input type=\"button\" value=\"Place Order\" onclick=\"location.href='{% url 'orderdetails' %}'\">"

    html=html+"</body></html>"
    fptr=open("./templates/shoplist.html","w")
    fptr.write(html)
    fptr.close()
    #return HttpResponse(html)
    return render(request,"shoplist.html")

def thankyou(request):
    customer_name = request.POST.get('customername')
    contact = request.POST.get('contact')
    email = request.POST.get('email')
    shop_name = request.POST.get('shopname')
    shop_name = shop_name.replace(" ", "")
    shop_name = shop_name.lower()
    shopping_list = request.POST.get('shoppinglist')

    datab=dict(dict(database.get().val())['users'])

    shop_not_found = True
    for key in datab.keys():
        if datab[key]['details']['shopname'].lower() == shop_name:

            shop_not_found = False
            orderdetails = {"contact": contact, "email": email, "shoppinglist": shopping_list}
            database.child("users").child(key).child("details").child("order_list").child(customer_name).set(orderdetails)

    html="<html><head><title>home page</title></head><body>"
    if shop_not_found:
        html += "<h2>Sorry, Invalid shop name.</h2>"
    else:
        html += "<h2 style=\"text-align: center;\">Thank you for shopping with us. </h2><br><br>"
        html += "<input type=\"button\" style=\"text-align: center;\" value=\"Continue Shopping\" onclick=\"location.href='{% url 'log' %}'\">"
    html=html+"</body></html>"

    fptr=open("./templates/thankyou.html","w")
    fptr.write(html)
    fptr.close()

    return render(request, "thankyou.html")

def orderdetails(request):
    return render(request,"order_details.html")
def postsign(request):
    email=request.POST.get('email')
    passw=request.POST.get("pass")
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid email or password"
        return render(request, "signIn.html",{"message":message})

    html="<html><head><title>home page</title></head><body>"
    html += '<table style="width:100%" border="2"><tr><th>Customer Name</th><th>Items Ordered</th><th>Email-Id</th><th>Phone Number</th><th>Prompts</th></tr>'


    try:
        datab=dict(dict(database.get().val())['users'][user['localId']]['details']['order_list'])
    except KeyError:
        datab = {}
    print("\n******************")
    print(datab)
    print("********************")

    # print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)

    #all the for loop goes here
    for customer in datab.keys():
        name = customer
        orders = datab[customer]['shoppinglist']
        email = datab[customer]['email']
        contact = datab[customer]['contact']
        accep_reject_form = "accept reject form"
        html += '<tr><td>'+name+'</td><td>'+orders+'</td><td>'+email+'</td><td>'+contact+'</td>'

        html += '''
                <td>
                    <form action="/process_order/" method="POST">{% csrf_token %}
                       <input type="radio" name="accept" value="'''+user['localId']+'''">Accept
                       <input type="radio" name="reject" value="'''+user['localId']+'''">Reject<br>
                       <input type="submit" name="submit" value="'''+customer+'''">
                    </form>
                </td>
                '''

    html += '</table><br><br>'
    #adding logout button
    html += '''<div class="container">
                <button type="button" onclick="location.href='{% url 'log' %}'">
                    Logout
                </button>
            </div>'''

    html += '</body></html>'
    fptr=open("./templates/homepage.html","w")
    fptr.write(html)
    fptr.close()
    return render(request, "homepage.html")
    # return render(request,"welcome.html",{"e":email})

def process_order(request):
    from django.core.mail import send_mail
    accept=request.POST.get('accept')
    reject=request.POST.get("reject")
    submit=request.POST.get('submit')

    html="<html><head><title>home page</title></head><body>"
    html += '<table style="width:100%" border="2"><tr><th>Customer Name</th><th>Items Ordered</th><th>Email-Id</th><th>Phone Number</th><th>Prompts</th></tr>'

    uid = None
    if accept != None:
        uid = accept
    else:
        uid = reject


    customer_email = dict(database.get().val())['users'][uid]['details']['order_list'][submit]['email']

    if accept != None:
        send_mail(
        'Your order is confirmed.',
        'Your order is confirmed and will be ready in 30 minutes.',
        'covidgrocer@gmail.com',
        [customer_email],
        fail_silently=False)
        
        print("sending email to ", customer_email)
        #send order conformation mail to above mail id

    else:
        send_mail(
        'Your order is rejected.',
        'Your order is rejected due to unavailability of items. Please try again.',
        'covidgrocer@gmail.com',
        [customer_email],
        fail_silently=False)
        print("sending email to ", customer_email)
        #order rejection mail to above mail id

    datab = {}
    try:
        data=dict(dict(database.get().val())['users'][uid]['details']['order_list'])
        print(data.pop(submit))
        database.child("users").child(uid).child("details").child('order_list').set(data)
        datab=dict(dict(database.get().val())['users'][uid]['details']['order_list'])
    except KeyError:
        datab = {}
    for customer in datab.keys():
        name = customer + "from second page"
        orders = datab[customer]['shoppinglist']
        email = datab[customer]['email']
        contact = datab[customer]['contact']
        accep_reject_form = "accept reject form"
        html += '<tr><td>'+name+'</td><td>'+orders+'</td><td>'+email+'</td><td>'+contact+'</td>'

        html += '''
                <td>
                    <form action="/process_order/" method="POST">{% csrf_token %}
                       <input type="radio" name="accept" value="'''+uid+'''">Accept
                       <input type="radio" name="reject" value="'''+uid+'''">Reject<br>
                       <input type="submit" name="submit" value="'''+customer+'''">
                    </form>
                </td>
                '''

    html += '</table><br><br>'
    #adding logout button
    html += '''<div class="container">
                <button type="button" onclick="location.href='{% url 'log' %}'">
                    Logout
                </button>
            </div>'''

    html += '</body></html>'
    fptr=open("./templates/homepage.html","w")
    fptr.write(html)
    fptr.close()
    return render(request, "homepage.html")


def logout(request):
    auth.logout(request)
    return render(request, "display.html")

def signUp(request):
    return render(request, "signUp.html")
def postsignUp(request):
    name=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('password')
    shopname=request.POST.get('shopname')
    shopname = shopname.replace(" ", "")
    shopname = shopname.lower()
    location=request.POST.get('location')
    description=request.POST.get('description')
    try:
        user=authe.create_user_with_email_and_password(email,password)
    except:
        message=("Please enter correct details.")
        return render(request,"signUp.html",{"message":message})
    uid=user['localId']
    data={"name":name,"shopname":shopname,"location":location,"description":description,"status":"1", "order_list": {}}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")

def acceptmail(request,customer_email):
    from django.core.mail import send_mail

    send_mail(
    'Your order is confirmed.',
    'Your order is confirmed and will be ready in 30 minutes.',
    'covidgrocer@gmail.com',
    [customer_email],
    fail_silently=False)

    return render(request,"display.html")

def rejectmail(request):
    from django.core.mail import send_mail

    send_mail(
    'Your order is rejected.',
    'Your order is rejecteddue to unavailabilty of items. Please try again.',
    'covidgrocer@gmail.com',
    ['mahimap7@gmail.com'],
    fail_silently=False)

    return render(request,"display.html")



# <input type="button" value="Accept" onclick="location.href='{% url 'acceptmail' %}'">
# <input type="submit" value="Reject" onclick="location.href='{% url 'rejectmail' %}'">
