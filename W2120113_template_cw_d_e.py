import csv
import tkinter as tk
from collections import defaultdict

# Task D: Histogram Display
class HistogramApp:
    def __init__(self, date, traffic_data):
        self.date = date
        self.traffic_data = traffic_data
        self.root = tk.Tk()
        self.canvas = None

    def setup_window(self):
        self.root.title(f"Traffic Histogram - {self.date}")
        self.canvas = tk.Canvas(self.root, width=900, height=550, bg="white")
        self.canvas.pack()
        self.canvas.create_text(50, 25, text=f"Histogram of Vehicle Frequency per Hour ({self.date})",
                                font=("Arial", 15, "bold"), fill="#60625F", anchor="w")
        self.canvas.create_rectangle(50, 45, 75, 70, fill="#9FF697", outline="#60625F", width=2)
        self.canvas.create_text(80, 57.5, text="Elm Avenue/Rabbit Road", font=("Arial", 10), fill="#60625F", anchor="w")
        self.canvas.create_rectangle(50, 75, 75, 100, fill="#F99794", outline="#60625F", width=2)
        self.canvas.create_text(80, 87.5, text="Hanley Highway/Westway", font=("Arial", 10), fill="#60625F", anchor="w")

    def draw_histogram(self):
        chart_base = 400
        max_height = 300
        bar_width = 15
        gap = 15
        max_frequency = max(max(self.traffic_data["Elm"]), max(self.traffic_data["Hanley"]))

        if max_frequency == 0:
            self.canvas.create_text(450, 250, text="No data to display.", font=("Arial", 15, "bold"), fill="red", anchor="center")
            return

        bar_x_start = 100

        for i, count in enumerate(self.traffic_data["Elm"]):
            bar_height = (count / max_frequency) * max_height
            self.canvas.create_rectangle(bar_x_start, chart_base - bar_height, bar_x_start + bar_width, chart_base,
                                          fill="#9FF697", outline="#60625F")
            self.canvas.create_text(bar_x_start + bar_width / 2, chart_base - bar_height - 10, text=f"{count}",
                                     font=("Arial", 9), fill="#50AE56", anchor="center")
            bar_x_start += bar_width + gap

        bar_x_start = 100 + bar_width

        for i, count in enumerate(self.traffic_data["Hanley"]):
            bar_height = (count / max_frequency) * max_height
            self.canvas.create_rectangle(bar_x_start, chart_base - bar_height, bar_x_start + bar_width, chart_base,
                                          fill="#F99794", outline="#60625F")
            self.canvas.create_text(bar_x_start + bar_width / 2, chart_base - bar_height - 10, text=f"{count}",
                                     font=("Arial", 9), fill="#DD7663", anchor="center")
            bar_x_start += bar_width + gap

        self.canvas.create_line(80, chart_base, 820, chart_base, fill="#5E5E5C", width=2)

        for i in range(24):
            hour_label_x = 100 + i * (bar_width + gap)
            self.canvas.create_text(hour_label_x, chart_base + 20, text=f"{i:02d}", font=("Arial", 10), fill="#60625F", anchor="center")

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.root.mainloop()

# Task E: Handling Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        self.traffic_data = None

    def validate_date_input(self):
        while True:
            try:
                year = int(input("Please enter the year of the survey in the format YYYY:"))
                if 2000 <= year <= 2024:
                    leap_year_checking = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
                else:
                    print("Out of Range - values must be in the range from 2000 to 2024.")
                    continue
            except ValueError:
                print("Integer required.")
                continue
            break

        while True:
            try:
                month = int(input("Please enter the month of the survey in the format MM:"))
                if 1 <= month <= 12:
                    break
                else:
                    print("Out of Range - values must be in the range 1 to 12.")
            except ValueError:
                print("Integer required.")

        while True:
            try:
                day = int(input("Please enter the day of the survey in the format dd:"))
                if month in [1, 3, 5, 7, 8, 10, 12] and 1 <= day <= 31:
                    break
                elif month in [4, 6, 9, 11] and 1 <= day <= 30:
                    break
                elif month == 2:
                    if leap_year_checking and 1 <= day <= 29:
                        break
                    elif not leap_year_checking and 1 <= day <= 28:
                        break
                    else:
                        print("Invalid day for February.")
                else:
                    print("Invalid day for the selected month.")
            except ValueError:
                print("Integer required.")

        file_name = f"traffic_data{day:02d}{month:02d}{year}.csv"
        return file_name

    def load_csv_file(self, file_path):
        traffic_data = {"Elm": [0] * 24, "Hanley": [0] * 24}
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    hour = int(row['timeOfDay'].split(':')[0])
                    junction_name = row['JunctionName']

                    if "Elm Avenue" in junction_name:
                        traffic_data["Elm"][hour] += 1
                    elif "Hanley Highway" in junction_name:
                        traffic_data["Hanley"][hour] += 1
            print("Data successfully loaded.")
            self.traffic_data = traffic_data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            self.traffic_data = None
        except KeyError:
            print("Error: Missing required columns in the CSV file.")
            self.traffic_data = None

    def handle_user_interaction(self):
        while True:
            file_name = self.validate_date_input()
            self.load_csv_file(file_name)

            if self.traffic_data:
                app = HistogramApp(file_name, self.traffic_data)
                app.run()
            else:
                print("Skipping histogram generation due to data loading error.")

            user_input = input("Do you want to load another dataset? (Y/N): ").strip().upper()
            if user_input == 'N':
                print("End of run.")
                break
            elif user_input != 'Y':
                print("Invalid input, please enter 'Y' or 'N'.")

if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.handle_user_interaction()
