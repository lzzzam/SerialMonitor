import ctypes
import threading
from tkinter import *
import serial

lock_thread = threading.Lock()
lock_serial = threading.Lock()
lock_window = threading.Lock()

ser = serial.Serial(timeout=1)
stop_serial_thread = False
stop_main_thread = False


class serialPlotter(threading.Thread):
    def __init__(self, name, monitor, autoscroll):
      threading.Thread.__init__(self)
      self.name = name
      self.monitor = monitor
      self.autoscroll = autoscroll
      self.char = ""
      self.plot = False
      
    def receive(self):
        lock_serial.acquire()
        if(ser.is_open == True and ser.in_waiting > 0):
            self.chr = ser.read()
            self.plot = True
        lock_serial.release()
        
    def run(self):
        lock_thread.acquire()
        print ("Starting " + self.name)
        
        while(True):
            self.receive()
            if (stop_serial_thread == True):
                break
            else:
                lock_window.acquire()
                if (self.plot == True):
                    self.monitor.config(state=NORMAL)
                    self.monitor.insert(END,self.chr)
                    if self.autoscroll.get() == True:
                        self.monitor.see("end")
                    self.monitor.config(state=DISABLED)
                    self.plot = False
                lock_window.release()
                
        if (ser.is_open == True):
            ser.flush
            ser.flushInput()
            ser.close()
            
        print("Ending " + self.name)
        lock_thread.release()
        
            
def transmitt(entry=None):
    if(ser.is_open == True):
        str = entry.get()
        if str != "":
            ser.write(str.encode('ascii'))