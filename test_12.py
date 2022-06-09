from cmath import sin
import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import random
from striprtf.striprtf import rtf_to_text
import csv
from datetime import datetime
import Clint


### IP Extraction ###
with open('/Users/yarden.yalinevich/PycharmProjects/pythonProject/Values.rtf') as infile:
    content = infile.read()
    text = rtf_to_text(content)
    split_text = text.split()
    IP_index = split_text.index('IP')
    IP = split_text[IP_index+2]
    PORT_index = split_text.index('PORT')
    PORT = split_text[PORT_index+2]

print(IP,PORT)

### CSV creation ###
csv_file_name = '/Volumes/GoogleDrive/My Drive/CyberRIdge/Python_projects/python_test3/CSV/'+str(datetime.today().strftime('%d-%m-%Y %H;%M;%S.%f')[:-3])
fieldnames = ['temp', 'Index']
with open(f"{csv_file_name}.csv",'w',newline='') as f:
    thewriter = csv.DictWriter(f,fieldnames=fieldnames)
    thewriter.writeheader()

ret = Clint.ip_send(1,'GetOnChipTemp')

### Figure shape creation ### 
fig,ax = plt.subplot_mosaic([['upper left', 'right'],
                            ['lower left', 'right']])
### Give space at the bottom of the window for the buttons ### 
plt.subplots_adjust(bottom=0.2)

index = count()
x_vals = []
y_vals = []
x_vals2 = []
y_vals2 = []
### Animate function ### 
def animate(i):
    ind = next(index)
    temp_message = str(Clint.ip_send(1,'GetOnChipTemp'))[:-3]
    temp_val = temp_message.split(',')[2]
    with open(f"{csv_file_name}.csv",'a',newline='') as f:
        thewriter = csv.DictWriter(f,fieldnames=fieldnames)
        thewriter.writerow({fieldnames[0]: temp_val,fieldnames[1]: ind})
    x_vals.append(ind)
    y_vals.append(random.randint(0,5))

    ax['upper left'].cla()
    ax['upper left'].plot(x_vals,y_vals)

ani = FuncAnimation(fig,animate, interval = 1000)

index2 = count()
def animate2(i):
    with open(f"{csv_file_name}.csv",'r') as f:
        reader = csv.DictReader(f)#,fieldnames=fieldnames)
        index_vec = []
        temp_vec = []
        for line in reader:
             index_vec.append(float(line['Index']))
             temp_vec.append(float(line['temp']))
    ax['right'].cla()
    ax['right'].plot(index_vec,temp_vec)

ani2 = FuncAnimation(fig,animate2, interval = 1000)

index3 = count()
def animate3(i):
    with open(f"{csv_file_name}.csv",'r') as f:
        reader = csv.DictReader(f)#,fieldnames=fieldnames)
        index_vec = []
        temp_vec = []
        for line in reader:
             index_vec.append(float(line['Index']))
             temp_vec.append(float(line['temp']))
    ax['lower left'].cla()
    ax['lower left'].plot(index_vec[-10:-1],temp_vec[-10:-1])
ani3 = FuncAnimation(fig,animate3, interval = 1000)

### Buttons class ###
class buttons:
    def zero(self, event):
        print(0)
    def one(self, event):
        print(1)
    def retrive_vertion_send(self, event):
        ax['lower left'].cla()
        ax['lower left'].plot([1,2,3,4],[10,49,3,100])

### Buttons instance creation ###
buttons_class = buttons()
### Order of button creation:
#  1)placement
#  2)button definition and button text
#  3)function attaching on click  ###
plot_zero = plt.axes([0.7, 0.05, 0.1, 0.075])
bzero = Button(plot_zero, '0')
bzero.on_clicked(buttons_class.zero)
plot_one = plt.axes([0.81, 0.05, 0.1, 0.075])
bone = Button(plot_one, '1')
bone.on_clicked(buttons_class.one)
call_function = plt.axes([0.49,0.05,0.2,0.075])
b_call_function = Button(call_function,'Retrive vertion')
b_call_function.on_clicked(buttons_class.retrive_vertion_send)
plt.show()
