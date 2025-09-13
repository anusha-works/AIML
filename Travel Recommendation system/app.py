from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import requests
from custom_functions import citybased, city_places
from chat import chatbot

app = Flask(__name__)
app.config["SECRET_KEY"] = "AnirudhKowluri"

# Database Employees
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

def is_admin():
    if current_user.is_admin == 0:
        return False
    else:
        return True

SEARCH_BOX_SESSION_TOKEN = '01f91271-8638-4551-88b4-b4f5bc70dc93&access_token=pk.eyJ1Ijoia293bHVyaWFuaXJ1ZGgiLCJhIjoiY2xubXdrOWpjMDBndTJycWkxMmVjOGU0dyJ9.qxA13Khvq4jd-o-kNv2ShQ'
SEAERCH_BOX_ACCESS_TOKEN = 'pk.eyJ1Ijoia293bHVyaWFuaXJ1ZGgiLCJhIjoiY2xubXdrOWpjMDBndTJycWkxMmVjOGU0dyJ9.qxA13Khvq4jd-o-kNv2ShQ'

UNSPLASH_CLIENT_ID = 'o9Gb9l_n5RMPD-wM-F1ge92Gra4HKsZ6F9CFCt0GKQ8'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template('index.html', logged_in=current_user.is_authenticated)

@app.route('/contact')
def contact():
    return render_template('contact.html', logged_in=current_user.is_authenticated)

@app.route('/about')
def about():
    return render_template('about.html', logged_in=current_user.is_authenticated)

# ?q=restaurants+in+hyderabad&language=en&types=place&session_token=

@app.route('/locations')
def locations():
    return render_template('locations.html', logged_in=current_user.is_authenticated)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        city = request.form.get('city')
        departure = request.form.get('departureDate')
        return_date = request.form.get('returnDate')
        quantity = request.form.get('quantity')
        budget = request.form.get('budget')

        # restaurants = url_for('get_restaurants', city=city)
        restaurants = citybased(city.title())
        output = []
        if restaurants:
            response = requests.get(url='http://127.0.0.1:5000/get-photos', params={'query': 'restaurant'})
            photos = response.json()['images']
            # print(photos)
            # photos = photos.get('images')
            while len(photos)<=len(restaurants):
                for i in range(len(photos)):
                    photos.append(photos[i])

            
            for i in range(len(restaurants)):
                output.append({'restaurant': restaurants[i], 'image': photos[i]})

        places = city_places(city.title())
        places_output = []
        for place in places:
            if place != '':
                response = requests.get(url='http://127.0.0.1:5000/get-photos', params={'query': place})
                photo = response.json()['images'][0]
                places_output.append({'place': place, 'image': photo})
        return render_template('output.html', logged_in=current_user.is_authenticated, restaurants=output, places=places_output)

    return render_template('register.html', logged_in=current_user.is_authenticated)

@app.route('/output')
def output():
    return render_template('output.html', logged_in=current_user.is_authenticated)

@app.route('/get-restaurants')
def get_restaurants():
    city = request.args.get('city')
    url = 'https://api.mapbox.com/search/searchbox/v1/suggest'
    params = {
        'q': f'Restaurants in {city}',
        'session_token': SEARCH_BOX_SESSION_TOKEN,
        'access_token': SEAERCH_BOX_ACCESS_TOKEN
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    restaurants = data.get('suggestions')[1:]
    output = []
    for restaurant in restaurants:
        lst = {'name':restaurant['name'], 'address': restaurant['full_address']}
        output.append(lst)
    return jsonify({'restaurants': output})

@app.route('/get-photos')
def get_photos():
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': request.args.get('query'),
        'client_id': UNSPLASH_CLIENT_ID,
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    results = data.get('results')
    urls = []
    for i in results:
        urls.append(i['urls']['full'])
    return jsonify({'images': urls})

@app.route('/get-reply')
def get_reply():
    msge = request.args.get('message')
    reply = chatbot(msge)
    print(reply)
    return jsonify({'message':reply})

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            flash("User not exists")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html', logged_in=current_user.is_authenticated)

@app.route('/signup', methods=["POST"])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(name=name).first()
    if user:
        flash("User name already exists")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email already exists")
        return redirect(url_for('login'))
    new_user = User(
        name=name,
        email=email,
        password=password,
    )
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        flash("Invalid credentials")
        return redirect(url_for('login'))
    
    login_user(new_user)
    return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)