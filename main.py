import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualizer:
    def __init__(self):
        plt.xlabel("Years")
        plt.ylabel("Investment Value")
        plt.title("Compound Interest Over Time")

        self.gui_root = tk.Tk()
        self.gui_root.title("Compound Interest Visualizer")

        self.plots: [SubPlot] = []

    def add_sub_plot(self, sub_plot: "SubPlot"):
        self.plots.append(sub_plot)
        self.redraw()

    def remove_sub_plot(self, sub_plot: "SubPlot"):
        self.plots.remove(sub_plot)
        self.redraw()

    def redraw(self):
        plt.clf()

        plt.xlabel("Years")
        plt.ylabel("Investment Value")
        plt.title("Compound Interest Over Time")

        for plot in self.plots:
            plot.draw_plot()

        mplcursors.cursor(hover=False)  # Click on plot points to show values
        plt.legend()
        plt.draw()

    def main(self):
        frame = ttk.Frame(self.gui_root)
        frame.pack(padx=10, pady=10)
        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame)
        canvas.get_tk_widget().pack()

        # Button to add input section
        style = ttk.Style()
        style.configure("Add.TButton", background="green")
        button_frame = ttk.Frame(self.gui_root)
        button_frame.pack(side='right', padx=10, pady=10)
        button1 = ttk.Button(button_frame, text='Add plot input section', style="Add.TButton",
                             command=lambda: SubPlot(self).tkinter_input_section())
        button1.pack(side='right')

        # Add one standard plot
        SubPlot(self).tkinter_input_section()

        self.gui_root.mainloop()


class SubPlot:
    def __init__(self,
                 visualizer: Visualizer,
                 initial_investment: int = 5000,
                 yearly_investment: int = 0,
                 annual_return: float = 0.08,
                 age_started: int = 22,
                 max_age: int = 67):
        assert 0 < annual_return < 1
        assert age_started < max_age
        assert initial_investment >= 0
        assert yearly_investment >= 0

        self.visualizer = visualizer
        self.initial_investment = initial_investment
        self.annual_return = annual_return
        self.yearly_investment = yearly_investment
        self.age_started = age_started
        self.max_age = max_age

        self.visualizer.add_sub_plot(self)

    def draw_plot(self):
        x_values = [age for age in range(self.age_started, self.max_age)]

        y_values = [
            (self.initial_investment * (1 + self.annual_return) ** (age - self.age_started)) +
            (self.yearly_investment * (((1 + self.annual_return) ** (age - self.age_started) - 1) / self.annual_return))
            for age in x_values
        ]

        plt.plot(x_values, y_values,
                 label=f"Init: {self.initial_investment}, Recurrent: {self.yearly_investment}, " +
                       f"Return: {self.annual_return}, Age started: {self.age_started}")

    def tkinter_input_section(self):
        input_frame = ttk.Frame(self.visualizer.gui_root)
        input_frame.pack(padx=10, pady=10)

        ttk.Label(input_frame, text="Initial:").grid(row=0, column=0)
        self.initial_investment_entry = ttk.Entry(input_frame)
        self.initial_investment_entry.grid(row=0, column=1)
        self.initial_investment_entry.insert(0, str(self.initial_investment))

        ttk.Label(input_frame, text="Yearly:").grid(row=0, column=2)
        self.yearly_investment_entry = ttk.Entry(input_frame)
        self.yearly_investment_entry.grid(row=0, column=3)
        self.yearly_investment_entry.insert(0, str(self.yearly_investment))

        ttk.Label(input_frame, text="Annual %:").grid(row=0, column=4)
        self.annual_return_entry = ttk.Entry(input_frame)
        self.annual_return_entry.grid(row=0, column=5)
        self.annual_return_entry.insert(0, str(self.annual_return))

        ttk.Label(input_frame, text="Age Started:").grid(row=0, column=6)
        self.age_started_entry = ttk.Entry(input_frame)
        self.age_started_entry.grid(row=0, column=7)
        self.age_started_entry.insert(0, str(self.age_started))

        ttk.Label(input_frame, text="Max Age:").grid(row=0, column=8)
        self.max_age_entry = ttk.Entry(input_frame)
        self.max_age_entry.grid(row=0, column=9)
        self.max_age_entry.insert(0, str(self.max_age))

        # Remove button
        style = ttk.Style()
        style.configure("RM.TButton", background="red")
        remove_button = ttk.Button(input_frame, text="rm", style="RM.TButton",
                                   command=lambda: self.visualizer.remove_sub_plot(self) or input_frame.destroy())
        remove_button.grid(row=0, column=10)

        # Update button
        update_button = ttk.Button(input_frame, text="Update", command=self.update_values)
        update_button.grid(row=0, column=11)

    def update_values(self):
        self.initial_investment = float(self.initial_investment_entry.get())
        self.yearly_investment = int(self.yearly_investment_entry.get())
        self.annual_return = float(self.annual_return_entry.get())
        self.age_started = int(self.age_started_entry.get())
        self.max_age = int(self.max_age_entry.get())
        self.visualizer.redraw()


if __name__ == "__main__":
    viz = Visualizer()
    viz.main()
