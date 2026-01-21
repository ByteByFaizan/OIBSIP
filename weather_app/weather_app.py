import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import threading

INK_BLACK = "#01161e"
DARK_TEAL = "#124559"
AIR_FORCE_BLUE = "#598392"
ASH_GREY = "#aec3b0"
BEIGE = "#eff6e0"
ACCENT_COLOR = "#2a9d8f"
ERROR_COLOR = "#e63946"
SUCCESS_COLOR = "#06ffa5"

API_KEY = "0cd7974972b640d684b141328261301"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast Dashboard")
        self.root.geometry("900x850")
        self.root.config(bg=INK_BLACK)
        self.root.minsize(900, 850)

        self.unit = "C"
        self.icon_img = None
        self.data = None
        self.loading = False
        self.search_history = []
        self.favorites = []
        self.animation_id = None

        self.create_ui()
        
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        self.city_entry.bind('<KeyRelease>', self.on_search_change)

    def create_ui(self):
        header_frame = tk.Frame(self.root, bg=DARK_TEAL, height=90)
        header_frame.pack(fill=tk.X, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Weather Forecast Dashboard",
            font=("Segoe UI", 28, "bold"),
            bg=DARK_TEAL,
            fg=BEIGE
        )
        title_label.pack(expand=True, pady=10)

        main_container = tk.Frame(self.root, bg=INK_BLACK)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        left_panel = tk.Frame(main_container, bg=INK_BLACK, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 15))

        search_frame = tk.Frame(left_panel, bg=DARK_TEAL, padx=15, pady=15)
        search_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            search_frame,
            text="City Search",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_TEAL,
            fg=BEIGE
        ).pack(anchor="w", pady=(0, 8))

        entry_frame = tk.Frame(search_frame, bg=BEIGE, padx=2, pady=2)
        entry_frame.pack(fill=tk.X)

        self.city_entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 13),
            bg=BEIGE,
            fg=INK_BLACK,
            relief="flat",
            insertbackground=INK_BLACK
        )
        self.city_entry.pack(fill=tk.X, ipady=10, padx=3, pady=3)
        self.city_entry.focus()

        self.search_btn = tk.Button(
            search_frame,
            text="Search Weather",
            bg=ACCENT_COLOR,
            fg=BEIGE,
            font=("Segoe UI", 11, "bold"),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.get_weather,
            activebackground=SUCCESS_COLOR,
            activeforeground=INK_BLACK
        )
        self.search_btn.pack(fill=tk.X, pady=(8, 0))

        controls_frame = tk.Frame(left_panel, bg=DARK_TEAL, padx=15, pady=15)
        controls_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            controls_frame,
            text="Controls",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_TEAL,
            fg=BEIGE
        ).pack(anchor="w", pady=(0, 8))

        self.toggle_btn = tk.Button(
            controls_frame,
            text="Switch to Fahrenheit",
            bg=AIR_FORCE_BLUE,
            fg=BEIGE,
            font=("Segoe UI", 10),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.toggle_unit,
            activebackground=ASH_GREY,
            activeforeground=INK_BLACK
        )
        self.toggle_btn.pack(fill=tk.X, pady=(0, 8))

        self.chart_btn = tk.Button(
            controls_frame,
            text="Show Temperature Chart",
            bg=AIR_FORCE_BLUE,
            fg=BEIGE,
            font=("Segoe UI", 10),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.show_embedded_chart,
            activebackground=ASH_GREY,
            activeforeground=INK_BLACK
        )
        self.chart_btn.pack(fill=tk.X, pady=(0, 8))

        self.refresh_btn = tk.Button(
            controls_frame,
            text="Refresh Data",
            bg=AIR_FORCE_BLUE,
            fg=BEIGE,
            font=("Segoe UI", 10),
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.refresh_weather,
            activebackground=ASH_GREY,
            activeforeground=INK_BLACK
        )
        self.refresh_btn.pack(fill=tk.X)

        info_frame = tk.Frame(left_panel, bg=DARK_TEAL, padx=15, pady=15)
        info_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            info_frame,
            text="Weather Icon",
            font=("Segoe UI", 12, "bold"),
            bg=DARK_TEAL,
            fg=BEIGE
        ).pack(anchor="w", pady=(0, 10))

        icon_container = tk.Frame(info_frame, bg=INK_BLACK, padx=3, pady=3)
        icon_container.pack()
        
        self.icon_label = tk.Label(
            icon_container, 
            bg=INK_BLACK,
            text="No data",
            font=("Segoe UI", 10),
            fg=ASH_GREY
        )
        self.icon_label.pack(padx=20, pady=20)

        self.status_label = tk.Label(
            info_frame,
            text="Ready to search",
            font=("Segoe UI", 9),
            bg=DARK_TEAL,
            fg=ASH_GREY,
            wraplength=250,
            justify="left"
        )
        self.status_label.pack(pady=(15, 0), anchor="w")

        right_panel = tk.Frame(main_container, bg=INK_BLACK)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        output_frame = tk.Frame(right_panel, bg=DARK_TEAL, padx=3, pady=3)
        output_frame.pack(fill=tk.BOTH, expand=True)

        text_container = tk.Frame(output_frame, bg=BEIGE)
        text_container.pack(fill=tk.BOTH, expand=True)

        self.output = tk.Text(
            text_container,
            bg=BEIGE,
            fg=INK_BLACK,
            font=("Consolas", 10),
            relief="flat",
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_container, command=self.output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.config(yscrollcommand=scrollbar.set)

        self.output.tag_config("title", font=("Segoe UI", 32, "bold"), foreground=DARK_TEAL)
        self.output.tag_config("subtitle", font=("Segoe UI", 15, "italic"), foreground=AIR_FORCE_BLUE)
        self.output.tag_config("header", font=("Segoe UI", 13, "bold"), foreground=DARK_TEAL)
        self.output.tag_config("subheader", font=("Segoe UI", 11, "bold"), foreground=AIR_FORCE_BLUE)
        self.output.tag_config("data", font=("Consolas", 10), foreground=INK_BLACK)
        self.output.tag_config("highlight", font=("Consolas", 10, "bold"), foreground=ACCENT_COLOR)

        footer_frame = tk.Frame(self.root, bg=DARK_TEAL, height=35)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False)
        
        self.footer_label = tk.Label(
            footer_frame,
            text="Powered by WeatherAPI.com",
            font=("Segoe UI", 9),
            bg=DARK_TEAL,
            fg=ASH_GREY
        )
        self.footer_label.pack(expand=True)

        self.add_button_hover_effects()
        self.show_welcome_screen()

    def add_button_hover_effects(self):
        buttons = [
            (self.search_btn, ACCENT_COLOR, SUCCESS_COLOR),
            (self.toggle_btn, AIR_FORCE_BLUE, ASH_GREY),
            (self.chart_btn, AIR_FORCE_BLUE, ASH_GREY),
            (self.refresh_btn, AIR_FORCE_BLUE, ASH_GREY)
        ]
        
        for btn, normal, hover in buttons:
            btn.bind("<Enter>", lambda e, h=hover: e.widget.config(bg=h))
            btn.bind("<Leave>", lambda e, n=normal: e.widget.config(bg=n))

    def on_search_change(self, event):
        text = self.city_entry.get().strip()
        if len(text) > 0:
            self.search_btn.config(bg=SUCCESS_COLOR, fg=INK_BLACK)
        else:
            self.search_btn.config(bg=ACCENT_COLOR, fg=BEIGE)
    def show_welcome_screen(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n\n\n")
        self.output.insert(tk.END, "Welcome to Weather Dashboard\n\n", "title")
        self.output.insert(tk.END, "Enter a city name to get started\n\n", "subtitle")
        self.output.insert(tk.END, "Features:\n", "header")
        self.output.insert(tk.END, "  • Real-time weather data\n")
        self.output.insert(tk.END, "  • 5-day forecast\n")
        self.output.insert(tk.END, "  • Hourly predictions\n")
        self.output.insert(tk.END, "  • Air quality index\n")
        self.output.insert(tk.END, "  • Weather alerts\n")
        self.output.insert(tk.END, "  • Temperature charts\n\n")
        self.output.insert(tk.END, "Press Enter or click Search to begin", "subheader")

    def toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"
        self.toggle_btn.config(
            text="Switch to Celsius" if self.unit == "F" else "Switch to Fahrenheit"
        )
        if self.data:
            self.display_weather(self.data)

    def update_status(self, message, color=BEIGE):
        self.status_label.config(text=message, fg=color)

    def show_loading(self):
        self.loading = True
        self.search_btn.config(state=tk.DISABLED, text="Searching...")
        self.toggle_btn.config(state=tk.DISABLED)
        self.chart_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.DISABLED)
        self.animate_loading(0)

    def animate_loading(self, count):
        if not self.loading:
            return
        dots = "." * (count % 4)
        spaces = " " * (3 - count % 4)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"\n\n\n\n")
        self.output.insert(tk.END, f"Fetching weather data{dots}{spaces}\n\n", "title")
        self.output.insert(tk.END, "Please wait while we retrieve the latest information", "subtitle")
        self.update_status("Loading weather data...", ASH_GREY)
        self.animation_id = self.root.after(350, self.animate_loading, count + 1)

    def stop_loading(self):
        self.loading = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        self.search_btn.config(state=tk.NORMAL, text="Search Weather")
        self.toggle_btn.config(state=tk.NORMAL)
        self.chart_btn.config(state=tk.NORMAL)
        self.refresh_btn.config(state=tk.NORMAL)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name")
            return

        thread = threading.Thread(target=self.fetch_weather, args=(city,))
        thread.daemon = True
        thread.start()

    def refresh_weather(self):
        if self.data:
            city = self.data['location']['name']
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
            self.get_weather()
        else:
            messagebox.showinfo("No Data", "Please search for a city first")

    def fetch_weather(self, city):
        self.show_loading()

        try:
            url = (
                f"https://api.weatherapi.com/v1/forecast.json"
                f"?key={API_KEY}&q={city}&days=5&aqi=yes&alerts=yes"
            )
            response = requests.get(url, timeout=10)
            data = response.json()
            
            self.root.after(0, self.stop_loading)

            if "error" in data:
                error_msg = data["error"]["message"]
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                self.root.after(0, lambda: self.update_status(f"Error: {error_msg}", ERROR_COLOR))
                self.root.after(0, self.show_welcome_screen)
                return

            self.data = data
            if city not in self.search_history:
                self.search_history.append(city)
            
            self.root.after(0, lambda: self.display_weather(data))
            self.root.after(0, lambda: self.update_status(
                f"Weather data loaded successfully for {data['location']['name']}", 
                SUCCESS_COLOR
            ))
            
            current_time = datetime.now().strftime("%I:%M %p, %B %d, %Y")
            self.root.after(0, lambda: self.footer_label.config(
                text=f"Last updated: {current_time} | Powered by WeatherAPI.com"
            ))

        except requests.Timeout:
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: messagebox.showerror("Timeout", "Request timed out. Please check your connection and try again."))
            self.root.after(0, lambda: self.update_status("Request timeout", ERROR_COLOR))
        except requests.ConnectionError:
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: messagebox.showerror("Connection Error", "Unable to connect to the weather service. Please check your internet connection."))
            self.root.after(0, lambda: self.update_status("Connection failed", ERROR_COLOR))
        except Exception as e:
            self.root.after(0, self.stop_loading)
            self.root.after(0, lambda: messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}"))
            self.root.after(0, lambda: self.update_status("Unexpected error", ERROR_COLOR))

    def display_weather(self, data):
        self.output.delete("1.0", tk.END)

        current = data["current"]
        location = data["location"]
        forecast = data["forecast"]["forecastday"]

        temp = current["temp_c"] if self.unit == "C" else current["temp_f"]
        feels_like = current["feelslike_c"] if self.unit == "C" else current["feelslike_f"]
        wind = current["wind_kph"] if self.unit == "C" else current["wind_mph"]
        wind_unit = "km/h" if self.unit == "C" else "mph"
        unit = "°C" if self.unit == "C" else "°F"

        self.output.insert(tk.END, f"\n{temp:.1f}{unit}\n", "title")
        self.output.insert(tk.END, f"{current['condition']['text']}\n", "subtitle")
        self.output.insert(tk.END, f"Feels like {feels_like:.1f}{unit}\n\n", "subtitle")
        
        self.output.insert(tk.END, f"{location['name']}, {location['country']}\n", "header")
        self.output.insert(tk.END, f"Local time: {location['localtime']}\n")
        self.output.insert(tk.END, "═" * 70 + "\n\n", "data")

        self.output.insert(tk.END, "Current Conditions\n", "header")
        self.output.insert(tk.END, f"Humidity       : {current['humidity']}%\n", "data")
        self.output.insert(tk.END, f"Wind Speed     : {wind:.1f} {wind_unit} {current['wind_dir']}\n", "data")
        self.output.insert(tk.END, f"Cloud Cover    : {current['cloud']}%\n", "data")
        self.output.insert(tk.END, f"Visibility     : {current['vis_km']} km\n", "data")
        self.output.insert(tk.END, f"Pressure       : {current['pressure_mb']} mb\n", "data")
        self.output.insert(tk.END, f"UV Index       : {current['uv']} ", "data")
        
        uv_level = self.get_uv_level(current['uv'])
        self.output.insert(tk.END, f"({uv_level})\n", "highlight")
        
        if 'air_quality' in current and current['air_quality']:
            aqi = current['air_quality'].get('us-epa-index', 'N/A')
            aqi_desc = self.get_aqi_description(aqi)
            self.output.insert(tk.END, f"Air Quality    : {aqi} ({aqi_desc})\n", "data")
        
        self.output.insert(tk.END, "\n" + "═" * 70 + "\n\n", "data")

        try:
            icon_url = "https:" + current["condition"]["icon"]
            img_response = requests.get(icon_url, timeout=5)
            img = Image.open(BytesIO(img_response.content)).resize((150, 150), Image.Resampling.LANCZOS)
            self.icon_img = ImageTk.PhotoImage(img)
            self.icon_label.config(image=self.icon_img, text="")
        except Exception:
            self.icon_label.config(text="Icon unavailable", image="")

        self.output.insert(tk.END, "Hourly Forecast (Next 12 Hours)\n\n", "header")
        current_hour = datetime.now().hour
        hours_shown = 0
        
        for d in forecast:
            if hours_shown >= 12:
                break
            for h in d["hour"]:
                hour_time = int(h['time'].split()[1].split(':')[0])
                if hour_time >= current_hour and hours_shown < 12:
                    t = h["temp_c"] if self.unit == "C" else h["temp_f"]
                    precip = h.get('chance_of_rain', 0)
                    self.output.insert(
                        tk.END,
                        f"{h['time'][11:16]}  |  {t:5.1f}{unit}  |  {h['condition']['text']:20s}  |  Rain: {precip}%\n",
                        "data"
                    )
                    hours_shown += 1
            current_hour = 0

        self.output.insert(tk.END, "\n" + "═" * 70 + "\n\n", "data")

        self.output.insert(tk.END, "5-Day Forecast\n\n", "header")
        for d in forecast:
            date = datetime.strptime(d['date'], '%Y-%m-%d').strftime('%a, %b %d')
            max_t = d["day"]["maxtemp_c"] if self.unit == "C" else d["day"]["maxtemp_f"]
            min_t = d["day"]["mintemp_c"] if self.unit == "C" else d["day"]["mintemp_f"]
            condition = d["day"]["condition"]["text"]
            rain_chance = d["day"].get("daily_chance_of_rain", 0)
            self.output.insert(
                tk.END,
                f"{date:15}  |  High: {max_t:5.1f}{unit}  Low: {min_t:5.1f}{unit}  |  {condition:20s}  |  Rain: {rain_chance}%\n",
                "data"
            )

        if 'alerts' in data and data['alerts'].get('alert'):
            self.output.insert(tk.END, "\n" + "═" * 70 + "\n\n", "data")
            self.output.insert(tk.END, "Weather Alerts\n\n", "header")
            for alert in data['alerts']['alert']:
                self.output.insert(tk.END, f"ALERT: {alert['headline']}\n", "highlight")
                self.output.insert(tk.END, f"       {alert.get('desc', 'No description')}\n\n", "data")

    def get_uv_level(self, uv):
        if uv <= 2:
            return "Low"
        elif uv <= 5:
            return "Moderate"
        elif uv <= 7:
            return "High"
        elif uv <= 10:
            return "Very High"
        else:
            return "Extreme"

    def get_aqi_description(self, aqi):
        descriptions = {
            1: "Good",
            2: "Moderate",
            3: "Unhealthy for Sensitive",
            4: "Unhealthy",
            5: "Very Unhealthy",
            6: "Hazardous"
        }
        return descriptions.get(aqi, "Unknown")

    def show_embedded_chart(self):
        if not self.data:
            messagebox.showwarning("No Data", "Please fetch weather data first")
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title(f"Temperature Forecast - {self.data['location']['name']}")
        chart_window.geometry("900x600")
        chart_window.config(bg=INK_BLACK)

        dates = []
        max_temps = []
        min_temps = []
        avg_temps = []

        for d in self.data["forecast"]["forecastday"]:
            date_obj = datetime.strptime(d["date"], '%Y-%m-%d')
            dates.append(date_obj.strftime('%m/%d'))
            
            if self.unit == "C":
                max_temps.append(d["day"]["maxtemp_c"])
                min_temps.append(d["day"]["mintemp_c"])
                avg_temps.append(d["day"]["avgtemp_c"])
            else:
                max_temps.append(d["day"]["maxtemp_f"])
                min_temps.append(d["day"]["mintemp_f"])
                avg_temps.append(d["day"]["avgtemp_f"])

        fig, ax = plt.subplots(figsize=(9, 5.5), facecolor=INK_BLACK)
        ax.set_facecolor(BEIGE)
        
        ax.plot(dates, max_temps, marker="o", label="Max Temp", linewidth=3, color=ERROR_COLOR, markersize=8)
        ax.plot(dates, avg_temps, marker="s", label="Avg Temp", linewidth=3, color=ACCENT_COLOR, markersize=8)
        ax.plot(dates, min_temps, marker="^", label="Min Temp", linewidth=3, color=AIR_FORCE_BLUE, markersize=8)
        
        ax.fill_between(dates, min_temps, max_temps, alpha=0.2, color=ASH_GREY)
        
        city_name = self.data['location']['name']
        ax.set_title(f"Temperature Forecast - {city_name}", fontsize=18, fontweight='bold', color=BEIGE, pad=20)
        ax.set_xlabel("Date", fontsize=13, fontweight='bold', color=DARK_TEAL)
        ax.set_ylabel(f"Temperature ({'°C' if self.unit == 'C' else '°F'})", fontsize=13, fontweight='bold', color=DARK_TEAL)
        ax.legend(loc='best', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(colors=DARK_TEAL)
        
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()