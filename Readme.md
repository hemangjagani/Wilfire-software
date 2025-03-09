# Wildfire Safety App

## 📌 Description
A simple Tkinter-based wildfire safety app that provides emergency contacts, wildfire alerts, weather updates, interactive maps, and evacuation time estimation.

## 🚀 Installation & Usage

### **1️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **2️⃣ Run the App**
```sh
python app.py
```

### **3️⃣ Build an Executable (.exe)**
Run the batch file to create an `.exe`:
```sh
build_exe.bat
```
Your executable will be inside the `dist` folder.

Alternatively, you can manually use PyInstaller:
```sh
pyinstaller --onefile --noconsole app.py
```

### **4️⃣ Run in Docker**
```sh
docker build -t wildfire-safety .
docker run -it wildfire-safety
```

## 🔗 Links
- [Wildfire Alerts](https://www.ontario.ca/page/forest-fires)
- [Weather API](https://openweathermap.org/)
