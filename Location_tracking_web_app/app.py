from flask import Flask, render_template, request, session, url_for, redirect
import pymysql
from werkzeug.utils import secure_filename
import pathlib
import os
import geocoder
import requests
import pandas as pd
app = Flask(__name__)
app.secret_key = 'any random string'

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyDwaXa3JZsFqv71812tm1k5FokRzLrX0RM'


def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="track&go")
    return connection


def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        
                       
con = dbConnection()
cursor = con.cursor()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index')
def index():
    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location
    # user = session["user"]
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM feedback")
        result1 = cursor.fetchall()
        return render_template('index.html',result1=result1, latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
       username = request.form.get("name")
       emailaddress = request.form.get("email")
       subject = request.form.get("subject")
       message = request.form.get("message")
       
       print(username,emailaddress,subject,message)
       con = dbConnection()
       cursor = con.cursor()
       sql2 = "INSERT INTO contact(username,email,subject,message) VALUES (%s, %s, %s, %s)"
       val2 = (str(username), str(emailaddress), str(subject), str(message))
       cursor.execute(sql2, val2)
       con.commit()
       return render_template('contact.html')  
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
       username = request.form.get("Username")
       emailaddress = request.form.get("Email")
       phoneno = request.form.get("Contact")
       password = request.form.get("Password")
       
       con = dbConnection()
       cursor = con.cursor()
       sql2 = "INSERT INTO register(Username,Email,Contact,Password) VALUES (%s, %s, %s, %s)"
       val2 = (str(username), str(emailaddress), str(phoneno), str(password))
       cursor.execute(sql2, val2)
       con.commit()
       return render_template('login.html')
    
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
           username = request.form.get("Username")
           print("username", username)
           password = request.form.get("Password")
           con = dbConnection()
           cursor = con.cursor()
           cursor.execute('SELECT * FROM register WHERE Username = %s AND Password = %s', (username, password))
           result = cursor.fetchone()
           print("result", result)
           if result:
               session['user'] = result[1]
               session['email'] = result[2]
               session['contact'] = result[3]
               return redirect(url_for('index'))

           else:
               msg = 'Incorrect username/password!'
               return msg
               return render_template('login.html')
    return render_template('login.html')


@app.route('/services')
def services():
    # Read CSV data
     data = pd.read_csv('static/wap.csv')
     print(data)
   # Get longitude and latitude values
     longitude = data['long'].tolist()
     print(longitude)
     latitude = data['lat'].tolist()
    
     
     return render_template('services.html', longitude=longitude, latitude=latitude,api_key=GOOGLE_MAPS_API_KEY)
  



@app.route('/servicedetails', methods=['POST', 'GET'])
def servicedetails():
    user=session['user']
    email1=session['email']
    contact=session['contact']
    
    
    
    if request.method == "POST":
       name = request.form.get("name")
       Contact = request.form.get("Contact")
       subject = request.form.get("subject")
       
       print(name,Contact,subject)
       con = dbConnection()
       cursor = con.cursor()
       sql2 = "INSERT INTO feedback(name,email,Contact,subject) VALUES (%s, %s, %s, %s)"
       val2 = (str(name), str(email1),str(Contact), str(subject))
       cursor.execute(sql2, val2)
       con.commit()
       message = "feedback successfully added"
       return render_template('service-details.html',message=message)  
    return render_template('service-details.html',user=user,email1=email1,contact=contact)


def get_nearby_places(latitude, longitude, keyword):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&keyword={keyword}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('results', [])

    
    
@app.route('/sampleinnerpage')
def sampleinnerpage():
    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location

        hospitals = get_nearby_places(latitude, longitude, 'hospital')
        hotels = get_nearby_places(latitude, longitude, 'hotel')
        
        return render_template('sample-inner-page.html', api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals, hotels=hotels)


@app.route('/pricing')
def pricing():
    # Read CSV data
    data = pd.read_csv('static/bad_wap.csv')

    # Extract data
    longitude = data['long'].tolist()
    latitude = data['lat'].tolist()
    wap = data['wap'].tolist()
    count = data['count'].tolist()

    return render_template('pricing.html', longitude=longitude, latitude=latitude, api_key=GOOGLE_MAPS_API_KEY, wap=wap, count=count)

@app.route('/getaquote')
def getaquote():
    return render_template('get-a-quote.html')

def get_current_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng
    else:
        return None

def get_nearby_hospitals(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=2000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    # print(data)

    if data.get("status") == "REQUEST_DENIED":
        return None

    return data.get("results", [])

# def get_nearby_hostel(latitude, longitude):
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=2000&type=restaurant&key={GOOGLE_MAPS_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     print(data)

#     if data.get("status") == "REQUEST_DENIED":
#         return None

#     return data.get("results", [])

def get_nearby_restaurant(latitude, longitude,radius1,min_rating1):
    # Set up the API request URL
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius1}&type=restaurant&key={GOOGLE_MAPS_API_KEY}"

    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Check if the request was denied
    if data.get("status") == "REQUEST_DENIED":
        return None

    # Filter by minimum rating (if provided)
    if min_rating1 is not None:
        filtered_results = [result for result in data.get("results", []) if result.get("rating", 0) >= min_rating1]
        print(filtered_results)

    else:
        filtered_results = data.get("results", [])
        
    return filtered_results



# def get_nearby_hospitals1(latitude, longitude,hospitals1):
#     google_maps_api_key = "AIzaSyDwaXa3JZsFqv71812tm1k5FokRzLrX0RM"  # Replace with your actual API key
#     radius = 2000  # 2km radius

#     nearby_hospitals = []
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=hospital&key={google_maps_api_key}"
#     response = requests.get(url)
#     data = response.json()

#     if data.get("status") == "REQUEST_DENIED":
#         return None

#     nearby_hospitals.extend(data.get("results", []))

#     return nearby_hospitals

def get_nearby_hospitals1(latitude, longitude,hospitals1):
    google_maps_api_key = "AIzaSyDwaXa3JZsFqv71812tm1k5FokRzLrX0RM"  # Replace with your actual API key
    radius = 2000  # 2km radius

    nearby_hospitals = []
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=hospital&key={google_maps_api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") == "REQUEST_DENIED":
        return None

    hospitals = data.get("results", [])
    for hospitals1 in hospitals:
        if "government" in hospitals1.get("name", "").lower() or "government" in hospitals1.get("vicinity", "").lower():
            nearby_hospitals.append(hospitals1)
        elif "private" in hospitals1.get("name", "").lower() or "private" in hospitals1.get("vicinity", "").lower():
            nearby_hospitals.append(hospitals1)
        elif "cancer" in hospitals1.get("name", "").lower() or "cancer" in hospitals1.get("vicinity", "").lower():
            nearby_hospitals.append(hospitals1)
        elif "hospital" in hospitals1.get("name", "").lower() or "hospital" in hospitals1.get("vicinity", "").lower():
            nearby_hospitals.append(hospitals1)    


    return nearby_hospitals

@app.route('/hospitals', methods=['POST', 'GET'])
def hospitals():
    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location
        if request.method == "POST":
           hospitals1 = request.form.get("hospitals")
           print("hospitals")
           hospitals = get_nearby_hospitals1(latitude, longitude,hospitals1)
           return render_template('hospitals.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals)
        hospitals = get_nearby_hospitals(latitude, longitude)
        print("hospitals1")
        return render_template('hospitals.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals)
    else:
        return "Could not determine current location."

@app.route('/hostel', methods=['POST', 'GET'])
def hostel():
    current_location = get_current_location()
    print(current_location)
    if current_location:
        latitude, longitude = current_location
        if request.method == "POST":
           radius = request.form.get("distance")
           min_rating = request.form.get("rate")
           radius1=int(radius)
           min_rating1=float(min_rating)
           print(type(min_rating1))
           
           hostel = get_nearby_restaurant(latitude, longitude,radius1,min_rating1)
           return render_template('hostel.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY,hostel=hostel)
        radius1=2000
        min_rating1=3.5
        print(type(min_rating1))
        hostel = get_nearby_restaurant(latitude, longitude,radius1,min_rating1)
        return render_template('hostel.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY,hostel=hostel)
    else:
        return "Could not determine current location."
    
    

################################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0')