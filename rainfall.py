import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Alyssa Goldgeisser
# Lab 2
# Module 2

def print_return_value(f):
    ''' decorator that returns the size of a container'''
    def wrapper(*args, **kwargs):
        return_val = f(*args, **kwargs)
        print("Number of data points plotted:", return_val)
        return return_val
    return wrapper

class Rainfall:
    def __init__(self, file_name):
        '''
        constructor for rainfall class, reads from file and creats 3 arrays
        one that is all data, another that is only years, and the third
        that is just rainfall.
         
        '''
        self.rain_arr = np.genfromtxt(file_name, delimiter=',', skip_footer=1)
        self.years_arr = self.rain_arr[:,0]
        self._monthly_rainfall_arr = self.rain_arr[:, 1:]
        self.rain_arr_copy = self._monthly_rainfall_arr.copy() #run only once
        self.mean_monthly_rainfall_arr = np.mean(self._monthly_rainfall_arr, axis=0) # same as above

    def get_highest_rainfall(self):
        ''' getter function that returns the highest yearly rainfall and year'''
        max_idx = np.argmax(np.sum(self.rain_arr[:, 1:], axis=1))
        year = int(self.rain_arr[max_idx, 0])
        rainfall = np.sum(self.rain_arr[max_idx, 1:])
        return year, rainfall

    def get_lowest_rainfall(self):
        ''' getter function that returns the lowest yearly rainfall and year'''
        min_idx = np.argmin(np.sum(self.rain_arr[:, 1:], axis=1))
        year = int(self.rain_arr[min_idx, 0])
        rainfall = np.sum(self.rain_arr[min_idx, 1:])
        return year, rainfall

    def get_median_rainfall(self):
        ''' getter function that returns the median rainfall '''
        median_rainfall = np.median(np.sum(self._monthly_rainfall_arr, axis=1))
        return median_rainfall

    @print_return_value
    def plot_rainfall_distribution(self):
        ''' plots the monthly rainfall distribution from 1850 to 2023 '''       
        self.rain_arr_copy.shape = (2088,)
        plt.hist(self.rain_arr_copy, color='green')
        plt.title("Monthly rainfall distribution")
        plt.xlabel("Inches of rain")
        plt.ylabel("Frequency")
        return len(self.rain_arr_copy)

    @print_return_value
    def plot_average_rainfall(self):    
        ''' plots the average rainfall for each month from 1850 to 2023 '''
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.bar(months, self.mean_monthly_rainfall_arr, color='red')
        plt.title("Average rainfall for each months")
        plt.xlabel("Months of the year")
        plt.ylabel("Inches of rainfall for each month")
        return len(self.mean_monthly_rainfall_arr)

    @print_return_value
    def plot_yearly_rainfall(self, start_year, end_year):
        ''' plots the average rainfall for each year on a given range'''
        start_idx = np.where(self.years_arr == start_year)[0][0]
        end_idx = np.where(self.years_arr == end_year)[0][0]
        years_range = self.years_arr[start_idx:end_idx + 1]
        rainfall_range = np.sum(self._monthly_rainfall_arr[start_idx:end_idx + 1], axis=1)
        plt.plot(years_range, rainfall_range, label="Yearly Rainfall")
        avg_yearly_rainfall = np.mean(rainfall_range)
        plt.plot([start_year, end_year], [avg_yearly_rainfall, avg_yearly_rainfall], 'r--', label='Average Rainfall')

        plt.title('Yearly Rainfall Trend')
        plt.xlabel('Year')
        plt.ylabel('Rainfall (inches)')
        plt.legend()
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True)) 
        return len(years_range)
    
    def get_first_last_years(self):
        ''' getter function that gets the low and high years from the csv file'''
        low_year = int(self.years_arr[0])
        high_year = int(self.years_arr[-1])

        return low_year, high_year



