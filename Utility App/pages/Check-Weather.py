import requests
import streamlit as st

# API key
key = 'f6f5534e3d2b49589b0120145240101'

st.title("Weather App")
city = st.text_input("Enter a City name")

if st.button('Show Weather'):
    if city:
        respons = requests.get(f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}")
        if respons.status_code == 200 and respons.json():
            city_name = respons.json()['location']['name']
            region = respons.json()['location']['region']
            country = respons.json()['location']['country']
            # img = respons.json()['current']['condition']['icon']
            
            st.write(f"\nCity: {city_name},   Region: {region},   Country: {country}")
            st.write(f"\nTemperature in Celcius: {respons.json()['current']['temp_c']}°C, Feels like: {respons.json()['current']['feelslike_c']}°C")
            st.write(f"\nSky Condition: {respons.json()['current']['condition']['text']}, Cloud cover: {respons.json()['current']['cloud']}%")
            # st.image(img, width=300)
            st.write(f"\nHumidity: {respons.json()['current']['humidity']}%, Wind Speed: {respons.json()['current']['wind_kph']}kph")
        else:
            st.error("\nError...! Unable to fetch weather data")
