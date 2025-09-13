# Appetite Recommendation through Facial Expressions
This study offers a unique approach for predicting food choices based on user mood by using machine learning algorithms. The system uses a K-means clustering technique to predict meal choices based on specified mood categories like happy, sad, stressed, etc.
The system was trained using a big dataset of food preferences and related mood descriptors.  Giving the user a choice of predefined mood categories from which to select their present mood is the first step. After selecting the user's mood, the system provides food choices. 
The front end of the program makes use of Bootstrap, and the backend makes use of Python and the Flask framework. Using the K-means clustering technique, related food selections are clustered together based on the established mood categories. To improve food predictions depending on user mood, the system utilizes face expression recognition technology. The system is expected to gain an accuracy rate of 70% due to innovative facial emotion recognition.  

Methodology Overview:  
In our project user interface for the mood-based food prediction system is designed to be simple and easy to use. Firstly, giving choice to users to select their current mood either by a manually process or by selecting web camera option. Upon manual option it will be redirected to another end point where we will recommend to users the restaurants in a particular city. The restaurants are aggregated based on the rating. If you select any of the 9 moods, then the model will process it and display the food that most people eat in that mood. And it will show you the restaurants that have the best rating for those types of foods.

Working: We will classify the restaurants based on reviews, locations, and cuisines using K-Means Clustering. For each mood option, K-Means Clustering is crucial in grouping similar establishments. For our study, we used the "Zomato.csv" file from Kaggle, which contains data on food reviews. The restaurants are grouped together based on their reviews using the K-Means Clustering method and the Zomato Dataset. In order to determine the best foods to advise in light of the input mood, the predict food choices algorithm employs sentiment analysis. It makes use of a database of hundreds of review files for meals. We are making use of a different dataset, the mood "food choices" dataset.

Using sentiment analysis and NlTK, this database is utilized to train a model that uses mood to predict food decisions. After processing the input mood that the user picked, we will finally forecast the food. Then, based on the cuisine that our model suggests, we will display the restaurant in that city.

Working: If a user chooses the web camera option to show their feelings about their meal selections. It involves a database called "facial expression" that uses a convolution neural network (CNN) and large samples to determine our face expression. In our study, CNN is primarily employed for image recognition based on face expression. It makes the most precise predictions regarding food choices after analyzing the image.

RESULTS  The primary objective of our project is to provide users with user-friendly interaction that makes them helpful while decision-making. Anticipating a 70 plus accuracy rate, this innovation demonstrates the system's commitment to leveraging advanced technologies for mood-based recommendation precision.  

Website Home Page:

![image](https://github.com/Varshith-0809/Appetite-Recommendation-through-Facial-Expressions/assets/114985735/d54770b0-474d-4d17-9b35-f707f4eeecd9)

Manual Mood Selection:

![image](https://github.com/Varshith-0809/Appetite-Recommendation-through-Facial-Expressions/assets/114985735/08aef22d-529d-4c2a-bd75-1440ef1228e2)

Recommendation

![image](https://github.com/Varshith-0809/Appetite-Recommendation-through-Facial-Expressions/assets/114985735/3ea597be-4bb3-47e0-a54b-b6a3c867435a)

