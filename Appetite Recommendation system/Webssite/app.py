import os

from flask import Flask, Response, render_template, request, redirect, url_for
from utils.camera import FileUpload, VideoCamera
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',''])
from nltk.stem import WordNetLemmatizer

food_data = pd.read_csv('C:\\Users\\varsh\\OneDrive\\Desktop\\Vs Code\\Minor project\FRTE\\food_choices.csv')
res_data = pd.read_csv('C:\\Users\\varsh\\OneDrive\\Desktop\\Vs Code\\Minor project\\FRTE\\zomato.csv', encoding='latin-1')
# Filtering rows where 'Country Code' is 1 (India) and 'City' is 'New Delhi'
res_data = res_data.loc[(res_data['Country Code'] == 1) & (res_data['City'] == 'New Delhi'), :]
res_data = res_data.loc[res_data['Longitude'] != 0, :] # Filtering out rows where 'Longitude' is 0
res_data = res_data.loc[res_data['Latitude'] != 0, :]
res_data = res_data.loc[res_data['Latitude'] < 29] # clearing out invalid outlier
res_data = res_data.loc[res_data['Rating text'] != 'Not rated']
res_data['Cuisines'] = res_data['Cuisines'].astype(str) # Adding a new column 'fusion_num' representing the number of cuisines in each row

REDIRECT_SIGNAL = 'redirect'

# Define a function to search for comfort foods based on mood
def search_comfort(mood):
    lemmatizer = WordNetLemmatizer()
    foodcount = {}
    for i in range(124):
        # Process and tokenize the comfort_food_reasons column
        temp = [temps.strip().replace('.','').replace(',','').lower() for temps in str(food_data["comfort_food_reasons"][i]).split(' ') if temps.strip() not in stop ]
        # Check if the mood is in the tokenized comfort_food_reasons
        if mood in temp:
            # Process and tokenize the comfort_food column
            foodtemp = [lemmatizer.lemmatize(temps.strip().replace('.','').replace(',','').lower()) for temps in str(food_data["comfort_food"][i]).split(',') if temps.strip() not in stop ]
            # Count occurrences of each comfort food
            for a in foodtemp:
                if a not in foodcount.keys():
                    foodcount[a] = 1 
                else:
                    foodcount[a] += 1
    # Sort the comfort foods based on their occurrences
    sorted_food = []
    sorted_food = sorted(foodcount, key=foodcount.get, reverse=True)
    return sorted_food

def find_my_comfort_food(mood):
  topn = []
  topn = search_comfort(mood) #function create dictionary only for particular mood
  return topn[:3]

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/find', methods=['GET'])
def find_restaurant():
    mood = request.args.get('mood')
    result = find_my_comfort_food(mood)
    result_str = 'You should eat {}, {}, or {}.'.format(result[0], result[1], result[2])
    food_to_cuisine_map = {
        "pizza": "pizza",
        "ice cream": "ice cream",
        "chicken wings": "mughlai",
        "chinese": "chinese",
        "chip": "bakery",
        "chocolate": "bakery",
        "candy": "bakery",
        "mcdonalds": "burger",
        "burger": "burger",
        "cooky": "bakery",
        "mac and cheese": "american",
        "pasta": "italian",
        "soup": "chinese",
        "dark chocolate": "bakery",
        "terra chips" : "bakery",
        "reese's cups(dark chocolate)": "bakery"
    }
    restaurants_list = []
    for item in result:
        # Filter restaurants based on the cuisine associated with each comfort food
        restaurants = res_data[res_data.Cuisines.str.contains(food_to_cuisine_map[item], case=False)].sort_values(by='Aggregate rating', ascending=False).head(3)
        #as an example
        restaurants_list.append(restaurants.iloc[0])
        restaurants_list.append(restaurants.iloc[1])
        restaurants_list.append(restaurants.iloc[2])
        # Render a template with the result, mood, and restaurant data
    return render_template('result.html', result = result_str, mood = mood, restaurants1 = restaurants_list[:3], restaurants2 = restaurants_list[3:6], restaurants3 = restaurants_list[6:])


def gen(camera):
        while True:
            frame, emotion = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            if emotion:
                 yield f"redirect {emotion}"

@app.route('/video_feed')
def video_feed():
    camera = VideoCamera()
    for frames in gen(camera):
         if frames.split()[0] == REDIRECT_SIGNAL:
              return redirect(url_for('emotion_detected', emotion=frames.split()[1]))
    return Response(gen(VideoCamera()), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion_detected/<emotion>')
def emotion_detected(emotion):
    return redirect(url_for('find_restaurant', mood=emotion))
    # return render_template('result.html', mood=emotion)

@app.route('/image_upload', methods=['GET', 'POST'])
def image_upload():
    image = request.files['image']
    image.save('static/created_images/image.jpg')
    f = FileUpload()
    pred = f.get_roi()
    return render_template('image_upload.html', data=pred)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port, debug = True)
