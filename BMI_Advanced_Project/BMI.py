import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_database()
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_database(self):
        try:
            self.conn = sqlite3.connect("bmi_data.db")
            self.cursor = self.conn.cursor()
            
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")
            self.root.destroy()
    
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#4CAF50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🏥 Advanced BMI Calculator",
            font=("Arial", 20, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack(expand=True)
        
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        input_frame = tk.LabelFrame(
            main_frame,
            text="Enter Your Details",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(input_frame, text="Name:", font=("Arial", 10), bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.entry_name = tk.Entry(input_frame, font=("Arial", 11), width=30)
        self.entry_name.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Weight (kg):", font=("Arial", 10), bg="#f0f0f0").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.entry_weight = tk.Entry(input_frame, font=("Arial", 11), width=30)
        self.entry_weight.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Height (m):", font=("Arial", 10), bg="#f0f0f0").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.entry_height = tk.Entry(input_frame, font=("Arial", 11), width=30)
        self.entry_height.grid(row=2, column=1, pady=5, padx=10)
        
        self.btn_calculate = tk.Button(
            input_frame,
            text="Calculate BMI",
            command=self.calculate_bmi,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        self.btn_calculate.grid(row=3, column=0, columnspan=2, pady=15)
        
        self.result_frame = tk.LabelFrame(
            main_frame,
            text="Result",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=15,
            pady=15
        )
        self.result_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.label_result = tk.Label(
            self.result_frame,
            text="Enter your details and click Calculate",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="#555",
            justify=tk.CENTER
        )
        self.label_result.pack()
        
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X)
        
        tk.Button(
            button_frame,
            text="📊 View History",
            command=self.view_history,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="📈 Show Graph",
            command=self.show_graph,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🗑️ Clear History",
            command=self.clear_history,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        self.root.bind('<Return>', lambda e: self.calculate_bmi())
    
    def calculate_bmi(self):
        try:
            name = self.entry_name.get().strip()
            weight_str = self.entry_weight.get().strip()
            height_str = self.entry_height.get().strip()
            
            if not name:
                messagebox.showwarning("Missing Information", "Please enter your name")
                self.entry_name.focus()
                return
            
            if not weight_str:
                messagebox.showwarning("Missing Information", "Please enter your weight")
                self.entry_weight.focus()
                return
            
            if not height_str:
                messagebox.showwarning("Missing Information", "Please enter your height")
                self.entry_height.focus()
                return
            
            weight = float(weight_str)
            height = float(height_str)
            
            if weight <= 0:
                messagebox.showerror("Invalid Input", "Weight must be greater than 0")
                self.entry_weight.focus()
                return
            
            if height <= 0:
                messagebox.showerror("Invalid Input", "Height must be greater than 0")
                self.entry_height.focus()
                return
            
            if height > 3:
                messagebox.showwarning("Check Input", "Height seems too large. Please enter height in meters (e.g., 1.75)")
                self.entry_height.focus()
                return
            
            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            
            if bmi < 18.5:
                category = "Underweight"
                color = "#2196F3"
                advice = "Consider consulting a nutritionist for a healthy weight gain plan."
            elif bmi < 25:
                category = "Normal"
                color = "#4CAF50"
                advice = "Great! Maintain your healthy lifestyle."
            elif bmi < 30:
                category = "Overweight"
                color = "#FF9800"
                advice = "Consider a balanced diet and regular exercise."
            else:
                category = "Obese"
                color = "#f44336"
                advice = "Please consult a healthcare professional for guidance."
            
            self.label_result.config(
                text=f"BMI: {bmi}\nCategory: {category}\n\n{advice}",
                fg=color,
                font=("Arial", 12, "bold")
            )
            
            self.cursor.execute(
                "INSERT INTO bmi_records VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                (name, weight, height, bmi, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            self.conn.commit()
            
            messagebox.showinfo("Success", f"BMI calculated and saved successfully!\n\nBMI: {bmi}\nCategory: {category}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for weight and height")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save data: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def view_history(self):
        try:
            self.cursor.execute(
                "SELECT id, name, bmi, category, date FROM bmi_records ORDER BY date DESC"
            )
            records = self.cursor.fetchall()
            
            if not records:
                messagebox.showinfo("No Data", "No history found in the system")
                return
            
            history_window = tk.Toplevel(self.root)
            history_window.title("BMI History - All Users")
            history_window.geometry("700x400")
            history_window.configure(bg="#f0f0f0")
            
            tk.Label(
                history_window,
                text="BMI History for All Users",
                font=("Arial", 14, "bold"),
                bg="#f0f0f0"
            ).pack(pady=10)
            
            tree_frame = tk.Frame(history_window)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            tree = ttk.Treeview(
                tree_frame,
                columns=("Name", "Date", "BMI", "Category"),
                show="headings",
                yscrollcommand=scrollbar.set
            )
            tree.pack(fill=tk.BOTH, expand=True)
            
            scrollbar.config(command=tree.yview)
            
            tree.heading("Name", text="Name")
            tree.heading("Date", text="Date & Time")
            tree.heading("BMI", text="BMI")
            tree.heading("Category", text="Category")
            
            tree.column("Name", width=150)
            tree.column("Date", width=200)
            tree.column("BMI", width=100)
            tree.column("Category", width=150)
            
            for record in records:
                tree.insert("", tk.END, values=(record[1], record[4], record[2], record[3]))
            
            def delete_selected():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select a record to delete")
                    return
                
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected record(s)?"):
                    for item in selected:
                        values = tree.item(item)['values']
                        self.cursor.execute(
                            "DELETE FROM bmi_records WHERE name=? AND date=? AND bmi=?",
                            (values[0], values[1], values[2])
                        )
                        tree.delete(item)
                    self.conn.commit()
                    messagebox.showinfo("Success", "Record(s) deleted successfully")
            
            tk.Button(
                history_window,
                text="Delete Selected",
                command=delete_selected,
                bg="#f44336",
                fg="white",
                font=("Arial", 10, "bold")
            ).pack(pady=10)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve history: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def show_graph(self):
        name = self.entry_name.get().strip()
        
        if not name:
            messagebox.showwarning("Missing Information", "Please enter a name to view their BMI trend")
            self.entry_name.focus()
            return
        
        try:
            self.cursor.execute(
                "SELECT bmi, date FROM bmi_records WHERE name=? ORDER BY date",
                (name,)
            )
            records = self.cursor.fetchall()
            
            if not records:
                messagebox.showinfo("No Data", f"No data to plot for {name}")
                return
            
            if len(records) < 2:
                messagebox.showinfo("Insufficient Data", f"{name} needs at least 2 records to plot a trend graph")
                return
            
            bmis = [r[0] for r in records]
            dates = [datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S") for r in records]
            
            graph_window = tk.Toplevel(self.root)
            graph_window.title(f"BMI Trend - {name}")
            graph_window.geometry("800x600")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(dates, bmis, marker='o', linestyle='-', linewidth=2, markersize=8, color="#4CAF50")
            
            ax.axhline(y=18.5, color='#2196F3', linestyle='--', alpha=0.7, label='Underweight')
            ax.axhline(y=25, color='#4CAF50', linestyle='--', alpha=0.7, label='Normal')
            ax.axhline(y=30, color='#FF9800', linestyle='--', alpha=0.7, label='Overweight')
            
            ax.set_xlabel("Date", fontsize=12, fontweight='bold')
            ax.set_ylabel("BMI", fontsize=12, fontweight='bold')
            ax.set_title(f"BMI Trend for {name}", fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate()
            
            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve data: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def clear_history(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM bmi_records")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                messagebox.showinfo("No Data", "No history found in the system")
                return
            
            if messagebox.askyesno(
                "Confirm Clear All History",
                f"Are you sure you want to delete ALL {count} record(s) from the system?\nThis will remove data for all users and cannot be undone."
            ):
                self.cursor.execute("DELETE FROM bmi_records")
                self.conn.commit()
                messagebox.showinfo("Success", "All records have been deleted from the system")
                self.label_result.config(text="Enter your details and click Calculate", fg="#555")
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to clear history: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def on_closing(self):
        try:
            self.conn.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()