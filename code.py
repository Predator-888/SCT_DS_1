import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, OptionMenu, StringVar, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Sample dataset for 2000-2025 ---
data = {
    "Year": list(range(2000, 2026)),
    "0-29 Years": [500 + i * 3 for i in range(26)],
    "30-59 Years": [450 + i * 4 for i in range(26)],
    "60+ Years": [100 + i * 2 for i in range(26)],
    "Male": [520 + i * 4 for i in range(26)],
    "Female": [530 + i * 3 for i in range(26)],
}
df = pd.DataFrame(data)


# --- Plot Function ---
def plot_population(*args):
    year = int(selected_year.get())
    chart_age = selected_age_chart.get()
    chart_gender = selected_gender_chart.get()

    row = df[df["Year"] == year]
    if row.empty:
        return

    # Age groups and values
    age_groups = ["0-29 Years", "30-59 Years", "60+ Years"]
    population = [row.iloc[0][col] for col in age_groups]

    # Gender values
    male = row.iloc[0]["Male"]
    female = row.iloc[0]["Female"]

    # --- Create subplots ---
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    plt.tight_layout(pad=4)

    # --- Chart 1: Age Group ---
    if chart_age == "Bar":
        ax[0].bar(age_groups, population, color=["#FFD54F", "#64B5F6", "#BA68C8"], edgecolor="black")
    elif chart_age == "Pie":
        ax[0].pie(population, labels=age_groups, autopct="%1.1f%%",
                  colors=["#FFD54F", "#64B5F6", "#BA68C8"], startangle=90)
    elif chart_age == "Histogram":
        age_data = [15] * population[0] + [45] * population[1] + [70] * population[2]
        ax[0].hist(age_data, bins=[0, 30, 60, 90], color="#4DB6AC", edgecolor="black", rwidth=0.85)

    ax[0].set_title(f"Age Group Distribution ({year})", fontsize=12, fontweight="bold")

    # --- Chart 2: Gender ---
    if chart_gender == "Bar":
        ax[1].bar(["Male", "Female"], [male, female], color=["#81C784", "#E57373"], edgecolor="black")
    elif chart_gender == "Pie":
        ax[1].pie([male, female], labels=["Male", "Female"], autopct="%1.1f%%",
                  colors=["#81C784", "#E57373"], startangle=90)
    elif chart_gender == "Histogram":
        gender_data = ["Male"] * male + ["Female"] * female
        ax[1].hist(gender_data, bins=2, color="#81C784", edgecolor="black", rwidth=0.85)

    ax[1].set_title(f"Gender Distribution ({year})", fontsize=12, fontweight="bold")

    # --- Show plots in Tkinter ---
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# --- Tkinter GUI ---
root = Tk()
root.title("📊 Population Distribution Viewer (2000-2025)")
root.geometry("1000x750")
root.configure(bg="#f4f6f7")

# --- Title ---
Label(
    root,
    text="Population Distribution Dashboard",
    font=("Segoe UI", 16, "bold"),
    bg="#f4f6f7",
    fg="#2c3e50",
    pady=10
).pack()

# --- Year Selector ---
Label(root, text="Select Year:", font=("Segoe UI", 12), bg="#f4f6f7", fg="#34495e").pack(pady=5)
selected_year = StringVar(value=df["Year"].iloc[0])
year_menu = OptionMenu(root, selected_year, *df["Year"], command=plot_population)
year_menu.config(font=("Segoe UI", 11), bg="#ecf0f1", fg="#2c3e50", width=10)
year_menu.pack(pady=5)

# --- Chart Type Selectors ---
Label(root, text="Select Age Group Chart:", font=("Segoe UI", 12), bg="#f4f6f7", fg="#34495e").pack(pady=5)
selected_age_chart = StringVar(value="Bar")
age_menu = OptionMenu(root, selected_age_chart, "Bar", "Pie", "Histogram", command=plot_population)
age_menu.config(font=("Segoe UI", 11), bg="#ecf0f1", fg="#2c3e50", width=12)
age_menu.pack(pady=5)

Label(root, text="Select Gender Chart:", font=("Segoe UI", 12), bg="#f4f6f7", fg="#34495e").pack(pady=5)
selected_gender_chart = StringVar(value="Bar")
gender_menu = OptionMenu(root, selected_gender_chart, "Bar", "Pie", "Histogram", command=plot_population)
gender_menu.config(font=("Segoe UI", 11), bg="#ecf0f1", fg="#2c3e50", width=12)
gender_menu.pack(pady=5)

# --- Frame for plots ---
frame = Frame(root, bg="#f4f6f7")
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Initial plot
plot_population()

root.mainloop()
