import tkinter as tk
from tkinter import messagebox
import requests
import folium
import webbrowser
from geopy.distance import geodesic

# Colors & Styling
theme_bg = "#2C3E50"
theme_fg = "#ECF0F1"
button_bg = "#3498DB"
button_fg = "white"
font_style = ("Arial", 12, "bold")

def get_weather():
    API_KEY = "YOUR_OPENWEATHER_API_KEY"
    CITY = "Toronto"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = f"Temperature: {data['main']['temp']}°C\nHumidity: {data['main']['humidity']}%\nWeather: {data['weather'][0]['description']}"
        messagebox.showinfo("Weather Update", weather_info)
    else:
        messagebox.showerror("Error", "Failed to fetch weather data.")

def show_emergency_contacts():
    contacts = "🔥 Emergency Contacts:\n\n📞 Fire Department: 911\n🚑 Ambulance: 911\n🚓 Police: 911\n🌲 Forest Fire Hotline: 1-800-667-1940"
    messagebox.showinfo("Emergency Contacts", contacts)

def open_fire_alerts():
    webbrowser.open("https://www.ontario.ca/page/forest-fires")

def open_map():
    # Create a map centered near Toronto
    wildfire_map = folium.Map(location=[43.7, -79.4], zoom_start=8)
    
    # Example wildfire locations near Toronto
    wildfire_locations = [
        (43.8, -79.5),
        (43.9, -79.3),
        (43.65, -79.38),
        (43.72, -79.5),
        (44.0, -79.2)
    ]
    
    # Safe evacuation location (Pickering)
    safe_location = (43.84, -79.03)
    
    # Alternate evacuation route east of Pickering
    alternate_safe_location = (43.87, -78.8) 
    
    # Add fire markers
    for lat, lon in wildfire_locations:
        folium.Marker(
            [lat, lon],
            tooltip="Wildfire",
            icon=folium.Icon(color='red', icon='glyphicon-fire')
        ).add_to(wildfire_map)
    
    # Add safe evacuation markers
    folium.Marker(
        safe_location,
        tooltip="Safe Evacuation Zone - Pickering",
        icon=folium.Icon(color='green', icon='glyphicon-ok')
    ).add_to(wildfire_map)
    
    folium.Marker(
        alternate_safe_location,
        tooltip="Alternative Safe Evacuation Zone - East of Pickering",
        icon=folium.Icon(color='blue', icon='glyphicon-ok')
    ).add_to(wildfire_map)
    
    # Draw escape routes
    for lat, lon in wildfire_locations:
        folium.PolyLine([(lat, lon), safe_location], color="red", weight=3, opacity=1, tooltip="Danger Zone🔥", dash_array="5,5").add_to(wildfire_map)
        folium.PolyLine([(safe_location), alternate_safe_location], color="green", weight=3, opacity=1, tooltip="Safe Route ✅", arrow_head=True).add_to(wildfire_map)
    
    # Save the map as an HTML file
    map_filename = "wildfire_map.html"
    wildfire_map.save(map_filename)
    
    # Open the map in the default web browser
    webbrowser.open(map_filename)
    
def escape_map(user_location=None, safe_direction=None):
    wildfire_map = folium.Map(location=[43.7, -79.4], zoom_start=8)
    wildfire_locations = [(43.8, -79.5), (43.9, -79.3), (43.65, -79.38), (43.72, -79.5), (44.0, -79.2)]
    safe_location = (43.84, -79.03)
    alternate_safe_location = (43.87, -78.8)
    
    for lat, lon in wildfire_locations:
        folium.Marker([lat, lon], tooltip="Wildfire", icon=folium.Icon(color='red', icon='glyphicon-fire')).add_to(wildfire_map)
    
    folium.Marker(safe_location, tooltip="Safe Zone - Pickering", icon=folium.Icon(color='green', icon='glyphicon-ok')).add_to(wildfire_map)
    folium.Marker(alternate_safe_location, tooltip="Alternative Safe Zone", icon=folium.Icon(color='blue', icon='glyphicon-ok')).add_to(wildfire_map)
    
    for lat, lon in wildfire_locations:
        folium.PolyLine([(lat, lon), safe_location], color="red", weight=3, opacity=1, tooltip="Danger Zone🔥", dash_array="5,5").add_to(wildfire_map)
        folium.Marker([(lat + safe_location[0]) / 2, (lon + safe_location[1]) / 2], icon=folium.DivIcon(html="➡️"), tooltip="Danger Path").add_to(wildfire_map)
        folium.PolyLine([safe_location, alternate_safe_location], color="green", weight=3, opacity=1, tooltip="Safe Route ✅").add_to(wildfire_map)
        folium.Marker([(safe_location[0] + alternate_safe_location[0]) / 2, (safe_location[1] + alternate_safe_location[1]) / 2], icon=folium.DivIcon(html="➡️"), tooltip="Safe Path").add_to(wildfire_map)
    
    if user_location and safe_direction:
        folium.Marker(user_location, tooltip="Your Location", icon=folium.Icon(color='purple', icon='glyphicon-user')).add_to(wildfire_map)
        folium.Marker(safe_direction, tooltip="Recommended Evacuation Direction", icon=folium.Icon(color='orange', icon='glyphicon-road')).add_to(wildfire_map)
        folium.PolyLine([user_location, safe_direction], color="orange", weight=3, opacity=1, tooltip="Evacuation Route 🏃").add_to(wildfire_map)
    
    wildfire_map.save("wildfire_map.html")
    webbrowser.open("wildfire_map.html")

def estimate_evacuation_time():
    def calculate_time():
        try:
            user_lat = float(entry_lat.get())
            user_lon = float(entry_lon.get())
            wind_speed = float(entry_wind.get())
            wind_direction = entry_wind_dir.get().lower()
            fire_spread_rate = float(entry_fire_spread.get())
            
            wildfire_locations = [(43.8, -79.5), (43.9, -79.3), (43.65, -79.38), (43.72, -79.5), (44.0, -79.2)]
            nearest_fire = min(wildfire_locations, key=lambda loc: geodesic((user_lat, user_lon), loc).km)
            distance_km = geodesic((user_lat, user_lon), nearest_fire).km
            evacuation_time_hours = distance_km / fire_spread_rate
            
            if wind_direction in ['north', 'northeast', 'east']:
                safe_direction = (user_lat - 0.2, user_lon + 0.2)
            else:
                safe_direction = (user_lat + 0.2, user_lon - 0.2)
            
            messagebox.showinfo("Evacuation Estimation", f"Estimated Evacuation Time: {evacuation_time_hours:.2f} hours\nRecommended Direction: {wind_direction.capitalize()}")
            tk.Button(evac_window, text="Show on Map", command=lambda: escape_map((user_lat, user_lon), safe_direction)).pack(pady=5)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")
    
    evac_window = tk.Toplevel(root)
    evac_window.title("Evacuation Estimation")
    evac_window.geometry("300x350")
    
    tk.Label(evac_window, text="Enter Your Location:").pack()
    tk.Label(evac_window, text="Latitude:").pack()
    entry_lat = tk.Entry(evac_window)
    entry_lat.pack()
    
    tk.Label(evac_window, text="Longitude:").pack()
    entry_lon = tk.Entry(evac_window)
    entry_lon.pack()
    
    tk.Label(evac_window, text="Wind Speed (km/h):").pack()
    entry_wind = tk.Entry(evac_window)
    entry_wind.pack()
    
    tk.Label(evac_window, text="Wind Direction (N, NE, E, etc.):").pack()
    entry_wind_dir = tk.Entry(evac_window)
    entry_wind_dir.pack()
    
    tk.Label(evac_window, text="Fire Spread Rate (km/h):").pack()
    entry_fire_spread = tk.Entry(evac_window)
    entry_fire_spread.pack()
    
    tk.Button(evac_window, text="Calculate", command=calculate_time).pack(pady=10)
    
# GUI Setup
root = tk.Tk()
root.title("Wildfire Safety App")
root.geometry("400x500")
root.configure(bg=theme_bg)

tk.Label(root, text="Wildfire Safety App", font=("Arial", 16, "bold"), fg=theme_fg, bg=theme_bg).pack(pady=10)

button_options = {
    "width": 30,
    "height": 2,
    "bg": button_bg,
    "fg": button_fg,
    "font": font_style,
    "bd": 2,
    "relief": "raised"
}

btn1 = tk.Button(root, text="Emergency Contacts", command=show_emergency_contacts, **button_options)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Wildfire Alerts", command=open_fire_alerts, **button_options)
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Weather Updates", command=get_weather, **button_options)
btn3.pack(pady=5)

btn4 = tk.Button(root, text="Interactive Map", command=open_map, **button_options)
btn4.pack(pady=5)

btn5 = tk.Button(root, text="Evacuation Estimation", command=estimate_evacuation_time, width=30, height=2, bg=button_bg, fg=button_fg, font=font_style, bd=2, relief="raised")
btn5.pack(pady=5)

root.mainloop()
