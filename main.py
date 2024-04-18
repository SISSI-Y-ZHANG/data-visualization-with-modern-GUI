# Remaining Update(s):
# - change dropdown menu from weeks to month 
#   e.g. check if mon.month == thu.month
# - use line graph to draw the trend of EVERY SINGLE DAY
# - fix bar size for total average

# Reflection: 
# I could write less code by splitting functions into simpler ones
# since I have written very similar lines in more than one place.

import datetime as dt
from calendar import monthrange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
weekday_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# used to store data for each week
class Week:
    def __init__(self, monday): 
        self.year = monday[0]
        self.month = monday[1]
        self.day = monday[2]
        self.data = []

    def create_week(self, days): # a list of numbers
        self.data = days

    def average(self):
        temp = list(self.data)
        c = 0
        # accounts for missing data
        for i in range(len(temp)):
            if type(temp[i]) == str:
                c += 1
                temp[i] = 0
        if c==7:
            avg = 0
        else:
            avg = sum(temp)/(7-c)
        avg = "{:.2f}".format(avg)
        return float(avg)

    def range(self):
        first = f'{month_name[self.month-1]}. {self.day}, {self.year}'
        x = dt.datetime(self.year, self.month, self.day) + dt.timedelta(days=6)
        last = f'{month_name[x.month-1]}. {x.day}, {x.year}'
        return [first, last]

    def text_form(self):
        return f'{self.year}/{self.month}/{self.day}'


# used to store Weeks
class Week_List:
    def __init__(self):
        self.weeks = []
        self.span = {}
        # span stores all data in years and month (in comparison to weeks)

        '''
        example.span = {
            2023: {'Jul': [...], 'Aug': [...], ...}
            2024: {'Jan': [...], ...}
            ...
            }
        '''

    def insert(self, item):
        self.weeks.append(item)

    # this method converts data stored with respect to weeks to years and months
    def span_update(self):
        for week in self.weeks:
            x = dt.datetime(week.year, week.month, week.day)
            w, v = monthrange(x.year, x.month)
            if x.year not in self.span.keys():
                self.span[x.year] = {}
            if x.year in self.span.keys() and x.month not in self.span[x.year].keys():
                self.span[x.year][x.month] = ['N/A']*v
            
            leap_flag = False

            for i in range(len(week.data)):
                y = x + dt.timedelta(days=i)

                if y.month != x.month and y.year == x.year and not leap_flag:
                    w, v = monthrange(y.year, y.month)
                    self.span[x.year][y.month] = ['N/A']*v
                    leap_flag = True
                elif y.month != x.month and y.year != x.year and not leap_flag:
                    w, v = monthrange(y.year, y.month)
                    self.span[y.year] = {}
                    self.span[y.year][y.month] = ['N/A']*v
                    leap_flag = True

                self.span[y.year][y.month][y.day-1] = week.data[i]

    def range(self):
        first = f'{month_name[self.weeks[0].month-1]}, {self.weeks[0].year}'
        last = f'{month_name[self.weeks[-1].month-1]}, {self.weeks[-1].year}'
        return [first, last]

    def text_form(self):
        txt = []
        for i in self.weeks:
            txt.append(i.text_form())
        return txt


class Bargraph_Window:
    def __init__(self, master, week_list):
        self.master = master # this is the root
        self.master.geometry('750x500')
        self.master.title('Weekly Numerical Data Tracker')

        self.data_list = week_list
        self.current = len(self.data_list.weeks)-1 # current-displaying week

        options = self.data_list.text_form()
        options.insert(0, 'Select Week')

        # left panel
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.frame.grid_rowconfigure(4, weight=1)

        self.label1 = ctk.CTkLabel(self.frame, text='Weekly Bargraph')
        self.label1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.button1 = ctk.CTkButton(self.frame, text='Previous Week', command=self.left_flip)
        self.button1.grid(row=1, column=0, padx=20, pady=10)

        self.button2 = ctk.CTkButton(self.frame, text='Next Week', command=self.right_flip)
        self.button2.grid(row=2, column=0, padx=20, pady=10)

        self.drop_down = ctk.CTkOptionMenu(self.frame, values=options, command=self.update)
        self.drop_down.grid(row=3, column=0, padx=20, pady=(10, 10))

        self.button3 = ctk.CTkButton(self.frame, text='Total Average', command=self.total)
        self.button3.grid(row=4, column=0, padx=20, pady=10)

        # bargraph
        self.fig, self.ax = plt.subplots()
        self.print_bar(self.data_list.weeks[self.current])

        self.button4 = ctk.CTkButton(self.master, text='Quit Program', command=self.quit)
        self.button4.grid(row=5, column=1, padx=20, pady=10)
        
    def print_bar(self, week):
        data = week.data
        week_range = week.range()

        #self.ax.bar(range(len(data)), data, color='steelblue')
        for i, value in enumerate(data):
            if type(value) == str:
                self.ax.bar(i, 1, color='pink')
                self.ax.text(i, 1+0.1, str(value), ha='center', va='bottom')
            else:
                self.ax.bar(i, value, color='steelblue')
                self.ax.text(i, value+0.1, str(value), ha='center', va='bottom')
                
        self.ax.set_xlabel("Weekdays")
        self.ax.set_xticks(range(len(data)), weekday_name)
        self.ax.set_ylabel("Hours")
        self.ax.set_yticks(range(16))

        self.ax.set_title(f"Week from {week_range[0]} to {week_range[1]}")
        self.ax.axhline(y=week.average(), color='sandybrown', linestyle='--', label='Average')
        
        canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

    def left_flip(self):
        if self.current > 0:
            self.current -= 1
            self.ax.clear()
            self.print_bar(self.data_list.weeks[self.current])
            
            self.button3.destroy()
            self.button3 = ctk.CTkButton(self.frame, text='Total Average', command=self.total)
            self.button3.grid(row=4, column=0, padx=20, pady=10)
            #print('left flip')
        else:
            #print('first week!')
            pass

    def right_flip(self):
        if self.current < len(self.data_list.weeks)-1:
            self.current += 1
            self.ax.clear()
            self.print_bar(self.data_list.weeks[self.current])
            
            self.button3.destroy()
            self.button3 = ctk.CTkButton(self.frame, text='Total Average', command=self.total)
            self.button3.grid(row=4, column=0, padx=20, pady=10)
            #print('right flip')
        else:
            #print('last week!')
            pass

    def update(self, new_date: str):
        if new_date == 'Select Week':
            pass
        else:
            for i in range(len(self.data_list.weeks)):
                if self.data_list.weeks[i].text_form() == new_date:
                    self.current = i
                    break
            self.ax.clear()
            self.print_bar(self.data_list.weeks[self.current])
            self.t_return()
            #print('update to', new_date)

    def total(self):
        self.ax.clear()
        month_range = self.data_list.range()

        data_dict = {}
        flags = []
        for year in self.data_list.span:
            for month in self.data_list.span[year]:
                key = f'{month_name[month-1]}'
                temp = list(self.data_list.span[year][month])
                # remove missing data
                c = 0
                for i in range(len(temp)):
                    if type(temp[i]) == str:
                        temp[i] = 0
                        c += 1
                if c == len(temp):
                    data_dict[key] = 0
                else:
                    data_dict[key] = sum(temp)/(len(temp)-c)
                # flags for color change
                if c >= len(temp)/2:
                    flags.append(True)
                else:
                    flags.append(False)

        data = list(data_dict.values())
        for i in range(len(data)):
            data[i] = float("{:.2f}".format(data[i]))
        labels = list(data_dict.keys())
        
        while 0 in data:
            data.remove(0)
        total_avg = sum(data)/len(data)

        #self.ax.bar(range(len(data)), data, color='cadetblue')
        for i, value in enumerate(data):
            if flags[i]:
                self.ax.bar(i, value, color='lightcoral')
                self.ax.text(i, value+0.1, str(value), ha='center', va='bottom')
            else:
                self.ax.bar(i, value, color='cadetblue')
                self.ax.text(i, value+0.1, str(value), ha='center', va='bottom')

        self.ax.set_xlabel("Months")
        self.ax.set_xticks(range(len(labels)), labels)
        self.ax.set_ylabel("Hours")
        self.ax.set_yticks(range(16))

        self.ax.set_title(f"Months from {month_range[0]} to {month_range[1]}")
        self.ax.axhline(y=total_avg, color='sandybrown', linestyle='--', label='Average')

        canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=1, columnspan=6, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.button3.destroy()
        self.button3 = ctk.CTkButton(self.frame, text='Return', command=self.t_return)
        self.button3.grid(row=4, column=0, padx=20, pady=10)
        #print('total')

    def t_return(self):
        self.button3.destroy()
        self.button3 = ctk.CTkButton(self.frame, text='Total Average', command=self.total)
        self.button3.grid(row=4, column=0, padx=20, pady=10)
        self.ax.clear()
        self.print_bar(self.data_list.weeks[self.current])
        #print('return')

    def quit(self):
        self.master.quit()
        #print('quit')


def read_data(file_name, week_list):
    with open(file_name) as in_data:
        line = in_data.readline()
        c = 1

        while line:
            line = line.strip().split('/')
            year, month, date = [eval(i) for i in line]
            weekday = dt.datetime(year, month, date).weekday()
            if weekday == 0:
                monday = [year, month, date]
            else:
                print(f'line {c} is not a monday')
                break

            line = in_data.readline().strip().split()
            c += 1
            if len(line) == 7:
                days = [eval(i) for i in line]
            else:
                print(f'the number of digits is not 7 in line {c}')
                break

            # make a Week
            week = Week(monday)
            week.create_week(days)
            week_list.insert(week)

            # read new lines
            line = in_data.readline()
            c += 1
            while line == '\n':
                line = in_data.readline()
                c += 1


def main():
    week_list = Week_List()
    read_data("sleep data 2023.txt", week_list)
    week_list.span_update()

    root = ctk.CTk()
    window = Bargraph_Window(root, week_list)
    root.mainloop()

if __name__ == '__main__':
    main()
