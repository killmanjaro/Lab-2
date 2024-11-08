import matplotlib
matplotlib.use('TkAgg') # tell matplotlib to work with Tkinter
import tkinter as tk # normal import of tkinter for GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Canvas widget
import matplotlib.pyplot as plt
import numpy as np
import tkinter.messagebox as tkmb
from rainfall import Rainfall
from tkinter import Tk, Toplevel, Frame, Button

# Alyssa Goldgeisser
# Lab 2
# Module 2

try:
    my_file = 'sf_rainfall.csv'
    r = Rainfall(my_file)
except FileNotFoundError:
    tkmb.showerror(title='Error', message=f'{my_file} not found.')
    raise SystemExit


class MainWindow(tk.Tk):
    def __init__(self):
        ''' constructor for mainwindow class, creates the original window and calls other windows '''
        super().__init__()
        self.title('Rainfall')
        low_year, high_year = r.get_first_last_years()
        high_yr, high_rainfall = r.get_highest_rainfall()
        low_yr, low_rainfall = r.get_lowest_rainfall()
        med_rainfall = r.get_median_rainfall()

        self.header = tk.Label(self, text=f'SF Rainfall {low_year}-{high_year}', fg='purple', font='Helvetica, 12').grid(row=1, column=1)
        self.monthly_avg_btn = tk.Button(self, text='Monthly Average', fg='red', font='Helvetica, 10', command=self.go_plotting_avg).grid(row=5, column=0)
        self.monthly_range_btn = tk.Button(self, text='Monthly Range', fg='green', font='Helvetica, 10', command=self.go_plotting_range).grid(row=5, column=1)
        self.yearly_total_btn = tk.Button(self, text='Yearly Total', fg='blue', font='Helvetica, 10', command=self.go_yearly_total).grid(row=5, column=2)

        self.highest_yrly_rainfall = tk.Label(self, text=f'Highest yearly rainfall: {high_yr}, {high_rainfall:.2f} inches', fg='purple', font='Helvetica, 10').grid(row=10, column=1)
        self.lowest_yrly_rainfall = tk.Label(self, text=f'Lowest yearly rainfall: {low_yr}, {low_rainfall:.2f} inches', fg='purple', font='Helvetica, 10').grid(row=11, column=1)
        self.median_rainfall = tk.Label(self, text=f'Median Rainfall: {med_rainfall:.2f} inches', fg='purple', font='Helvetica, 10').grid(row=12, column=1)

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(0, weight=1)

       
    def go_plotting_avg(self):  
        ''' calls plot window class with plotting average passed as an argument '''
        x = 'plotting average'  
        PlotWindow(x, 0, 0)

    def go_plotting_range(self):
        ''' calls plot window class with plotting range passed as an argument'''
        x = 'plotting range'
        PlotWindow(x, 0, 0)

    def go_yearly_total(self):
        ''' calls dialog window class '''
        DialogWindow(self)
    
class PlotWindow(tk.Toplevel):
    ''' plotting window class for each graph '''
    def __init__(self, my_attribute, arg1, arg2):
        self.my_attribute = my_attribute
        self.arg1 = arg1
        self.arg2 = arg2
        self.plot()

    def plot(self) :
        ''' function that plots for each scenario'''
        display = tk.Toplevel()
        fig = plt.figure(figsize=(5,5))
        if self.my_attribute == 'plotting average' :
            r.plot_average_rainfall()
        elif self.my_attribute == 'plotting range' :
            r.plot_rainfall_distribution()
        else:
            r.plot_yearly_rainfall(self.arg1, self.arg2)

        canvas = FigureCanvasTkAgg(fig, master=display)
        canvas.get_tk_widget().grid()
        canvas.draw()

class DialogWindow(tk.Toplevel):
    def __init__(self, master):
        ''' constructor for DialogWindow class, which pops a window that accepts input and is validated'''
        super().__init__(master)
        self._userVar = tk.StringVar()
        self.prompt = tk.Label(self, text="Enter the range of years")
        self.prompt.grid(row=0)
        self.userinput = tk.Entry(self, textvariable=self._userVar)
        self.userinput.grid(row=0, column=1)
        self.userinput.bind("<Return>", self.getInput)    
        self.grab_set()
        self.focus_set()

    def getInput(self, event) :
        ''' getinput function, validates input '''
        self._userAnswer = self._userVar.get()
        low_yr, high_yr = self._userAnswer.split()
        rainfall_low, rainfall_high = r.get_first_last_years()
        try:
            if len(low_yr) != 4 or len(high_yr) != 4:
                print('Start and end years must be four digits long')
                raise ValueError
            
            low_yr = int(low_yr) 
            high_yr = int(high_yr)

            if low_yr >= rainfall_low and high_yr <= rainfall_high:
                pass
            else:
                raise ValueError
            
            if low_yr < high_yr:
                pass
            else:
                raise ValueError
            
        except (ValueError , TypeError):   
            low_yr = rainfall_low
            high_yr = rainfall_high
            tkmb.showerror(title="Error", message=f'Invalid years, using {rainfall_low} {rainfall_high}', parent=self)

        x = 'plot total'
        PlotWindow(x, low_yr, high_yr)
        self.destroy()     


app = MainWindow()
app.mainloop()
