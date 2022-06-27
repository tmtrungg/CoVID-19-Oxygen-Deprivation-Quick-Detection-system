import sys
from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)

client = gspread.authorize(creds)

sheet = client.open("Final").sheet1

oxlevel = sheet.cell(2,3).value
bodytemp = sheet.cell(2,4).value
print(oxlevel)
print(bodytemp)

LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11 
LED_ON = 15

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.00005
E_DELAY = 0.00005

GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
GPIO.setwarnings(False)
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable  


now = datetime.now()
d1 = now.strftime("%d/%m/%Y %H:%M :%S")
def proccessingoutput(oxlevel,bodytemp) :
    if ( float(bodytemp) > 38 ) :
        if ( float(oxlevel) > 100 ) :
            return "invalid ox level"
        
        if (( float(oxlevel) >= 60 ) and ( float(oxlevel) <= 100)) :
            return  "Low suspicion level!"
        if (float(oxlevel) < 60 ) :
            return  "High suspicion level!!!"
        
    if (( float(bodytemp) >= 35 ) and ( float(bodytemp) <= 38 )) :
        if ( float(oxlevel) > 100 ) :
            return  "invalid ox level"
        
        if (( float(oxlevel) >= 60 ) and ( float(oxlevel) <= 100)) :
            return  "Normal 😊"
        
        if (float(oxlevel) < 60 ) :
            return  "Low suspicion level!"
        
    if (float(bodytemp) <= 35 ) :
        return  "Other disease"

themess = proccessingoutput(oxlevel,bodytemp)
print(themess)



def lcdplayplay(oxlevel,bodytemp,themess):
    lcd_init()
    
    GPIO.output(LED_ON, True)
    time.sleep(1)
    GPIO.output(LED_ON, False)
    time.sleep(1)
    GPIO.output(LED_ON, True)
    time.sleep(1)
    count = 0

    #Display measurement
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("OXG : " + oxlevel,2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("TEMP : " + bodytemp,2)

    time.sleep(5) # 3 second delay

    #Display Condition
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("Condition: ",1)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string(themess,1)

    time.sleep(5) # 5 second delay

    # Turn off backlight
    GPIO.output(LED_ON, False)

def lcd_init():
    

    # Initialise display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)  
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
    # Send string to display
    # style=1 Left justified
    # style=2 Centred
    # style=3 Right justified

    if style==1:
            message = message.ljust(LCD_WIDTH," ")  
    elif style==2:
            message = message.center(LCD_WIDTH," ")
    elif style==3:
            message = message.rjust(LCD_WIDTH," ")

    for i in range(LCD_WIDTH):
            lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode) # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
            GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
            GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
            GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
            GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, True)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)  
    time.sleep(E_DELAY)      

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
            GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
            GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
            GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
            GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(E_DELAY)    
    GPIO.output(LCD_E, True)  
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)  
    time.sleep(E_DELAY)



lcdplayplay(oxlevel,bodytemp,themess)
def dohistory():
    
    textzz = outputtext.get()
    if ( textzz == "Ben" ) :
        x = open('text1.txt', 'a')
        x.write(str(d1) + ":         Oxygen Level : " + str(oxlevel) + "         " + "Body Temperature : " + str(bodytemp))
        x.write("\n")
        x.close()
        
        y = open('text1.txt', 'r')
        label1 = Label(win, text = y.read()).pack()
        y.close()
        
    elif ( textzz == "Amee" ) :
        x = open('text2.txt', 'a+')
        x.write(str(d1) + ":         Oxygen Level : " + str(oxlevel) + "         " + "Body Temperature : " + str(bodytemp))
        x.write("\n")
        x.close()
        
        y = open('text2.txt', 'r')
        label1 = Label(win, text = y.read()).pack()
        y.close()
        
    elif ( textzz == "John" ) :
        x = open('text3.txt', 'a+')
        x.write(str(d1) + ":         Oxygen Level : " + str(oxlevel) + "         " + "Body Temperature : " + str(bodytemp))
        x.write("\n")
        x.close()
        
        y = open('text3.txt', 'r')
        label1 = Label(win, text = y.read()).pack()
        y.close()
        
    else :
        
        label1 = Label(win, text = textzz + "\n" + str(d1) + ":         Oxygen Level : " + str(oxlevel) + "         " + "Body Temperature : " + str(bodytemp)).pack()

win = Tk()
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

x_cor = (screen_width/2) - 500/2
y_cor = (screen_height/2) - 200/2


win.geometry("%dx%d+%d+%d" % (500,200,x_cor,y_cor))
outputtext = StringVar()
win.title("Measurement History")
myFont = tkinter.font.Font(family = "Helvetica", size = 15, weight = "bold")


label = Label(win, text = "Enter your name ( Ben, John, Amee or other guesses ) :").pack()
entry = Entry(win, textvariable=outputtext).pack()
button1 = Button(win,font = myFont,text = "History", command = dohistory,fg = "black", bg = "white").pack()
