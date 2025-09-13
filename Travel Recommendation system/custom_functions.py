import pandas as pd


res = pd.read_csv('swiggy.csv')
places = pd.read_csv('Places.csv').to_dict(orient='records')

def citybased(city):
    res['City']=res['City'].str.lower()
    citybase=res[res['City']==city.lower()]
    citybase=citybase.sort_values(by='Avg ratings',ascending=False)
    if(citybase.empty==0):
        rname=citybase[['Restaurant','Avg ratings','Address','Price']]
        return rname.head().to_dict(orient='records')
    else:
        # print('No restuarants Available')
        return None

def city_places(city):
    for place in places:
        if place['City'] == city:
            req = place['Famous_Places'].replace("\xa0", ' ').split(',')
            return req
            
# print(city_places('Hyderabad'))
# print("Top 5 restuarants")
# print(citybased('Hyderabad'))