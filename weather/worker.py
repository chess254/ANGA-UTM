import requests
import  psycopg2
import psycopg2.extras
from datetime import datetime
import  logging


def fetch_data():

    api_token = '146b384d03128d96'
    url = 'http://api.wunderground.com/api/' +api_token +'/conditions/q/KE/Nairobi.json'

    r = requests.get(url).json()
    data = r['current_observation']

    location = data['observation_location']['city'] #city, state
    weather = data['weather']
    wind_str =data['wind_string']
    temp = data['temp_c']
    humidity = data['relative_humidity']
    precip = data['precip_today_string']
    icon_url =data['icon_url']
    observation_time = data['observation_time']

    try:
        conn = psycopg2.connect (dbname='astral_utm', user='postgres',host='localhost', password='19Scazorla')
        print('opened db successfully')
    except:
        print(datetime.now(),'Unable to connect to db')
        logging.exception('Unable to open db')
        return
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        #write data to db

        cur.execute("""INSERT INTO weather_reading(location,weather,wind_str,temp,humidity,precip,icon_url,observation_time)

                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s)""", (location,weather,wind_str,temp,humidity,precip,icon_url,
                                                               observation_time) )

        conn.commit()
        cur.close()
        conn.close()

        print('data saved on ', datetime.now())

fetch_data()