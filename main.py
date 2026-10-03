import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class WeatherApp(App):
    def build(self):
        self.title = "AH : Irfan Weather App"
        
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        self.header = Label(
            text="AH : Irfan Weather", 
            font_size='26sp', 
            bold=True,
            color=(0.4, 0.8, 1, 1),
            size_hint=(1, 0.15)
        )
        layout.add_widget(self.header)
        
        self.auto_btn = Button(
            text="[ Auto Detect My Location ]", 
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(0.2, 0.7, 0.9, 1),
            size_hint=(1, 0.12)
        )
        self.auto_btn.bind(on_press=self.auto_detect_location)
        layout.add_widget(self.auto_btn)
        
        self.city_input = TextInput(
            hint_text="Or enter city name (e.g. Dhaka)", 
            multiline=False,
            font_size='18sp',
            size_hint=(1, 0.12),
            padding=[15, 12]
        )
        layout.add_widget(self.city_input)
        
        self.search_btn = Button(
            text="Search City", 
            font_size='18sp',
            background_normal='',
            background_color=(0.0, 0.5, 0.8, 1),
            size_hint=(1, 0.12)
        )
        self.search_btn.bind(on_press=self.get_weather_by_input)
        layout.add_widget(self.search_btn)
        
        self.result_label = Label(
            text="Click 'Auto Detect' or search a city!", 
            font_size='18sp',
            halign='center',
            valign='middle',
            color=(0.85, 0.95, 1, 1),
            size_hint=(1, 0.49)
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        layout.add_widget(self.result_label)
        
        return layout

    def auto_detect_location(self, instance):
        self.result_label.text = "Detecting your location..."
        try:
            res = requests.get("http://ip-api.com/json/").json()
            if res.get("status") == "success":
                lat = res.get("lat")
                lon = res.get("lon")
                city = res.get("city", "")
                country = res.get("country", "")
                self.fetch_weather_data(lat, lon, city, country)
            else:
                self.result_label.text = "Could not detect location automatically."
        except Exception as e:
            self.result_label.text = "Error detecting location! Check internet."

    def get_weather_by_input(self, instance):
        city = self.city_input.text.strip()
        if not city:
            self.result_label.text = "Please enter a city name!"
            return

        self.result_label.text = "Searching weather..."
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url).json()

            if "results" in geo_res:
                lat = geo_res["results"][0]["latitude"]
                lon = geo_res["results"][0]["longitude"]
                city_name = geo_res["results"][0]["name"]
                country = geo_res["results"][0].get("country", "")
                self.fetch_weather_data(lat, lon, city_name, country)
            else:
                self.result_label.text = "City not found! Check spelling."
        except Exception as e:
            self.result_label.text = "Error fetching weather data!"

    def fetch_weather_data(self, lat, lon, city_name, country):
        try:
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            w_res = requests.get(weather_url).json()

            current = w_res["current_weather"]
            temp = current["temperature"]
            wind = current["windspeed"]

            self.result_label.text = (
                f"Location: {city_name}, {country}\n\n"
                f"Temperature: {temp} °C\n\n"
                f"Wind Speed: {wind} km/h"
            )
        except Exception as e:
            self.result_label.text = "Failed to load weather data."

if __name__ == "__main__":
    WeatherApp().run()
