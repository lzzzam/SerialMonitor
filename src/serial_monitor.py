from cgitb import text
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import serial.tools.list_ports
import comm
from comm import ser, serialPlotter, transmitt, lock_serial, lock_thread, lock_window

window = Tk()
window.title("Serial Monitor")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)
window.grid_rowconfigure(1, weight=1)

def clearOutput():
    monitor.config(state=NORMAL)
    monitor.delete('1.0', END)
    monitor.config(state=DISABLED)
            
def updatePort():
    ports = serial.tools.list_ports.comports()
    list = []
    for port in ports:
        list.append(port.device)
    port_sel["values"] = list

def selectPort(self):
    lock_serial.acquire()
    if(ser.is_open == True):
        ser.close()
        
    port=port_sel.get()
    ser.port = port
    try:
        ser.open()
    except serial.SerialException as e:
        print(f"{e}")
        monitor.config(state=NORMAL)
        monitor.insert(END, str(e) +"\n" )
        if autoscroll_state.get() == True:
            monitor.see("end")
        monitor.config(state=DISABLED)
    lock_serial.release()
        

def closeSerialMonitor():
    lock_window.acquire()  
    comm.stop_serial_thread = True
    lock_window.release()
    lock_thread.acquire()
    window.destroy()

input = Entry(window)
input.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=EW)

Send = Button(text = "Send", width=10, command = lambda: transmitt(input))
Send.grid(row=0, column=4,  padx=1, pady=1, sticky=EW)

Clear = Button(text = "Clear Output", command = clearOutput)
Clear.grid(row=2, column=4, sticky=EW)

autoscroll_state = BooleanVar()
autoscroll_state.set(True)
autoscroll_chk = Checkbutton(window, width= 15, text='Autoscroll', var=autoscroll_state)
autoscroll_chk.grid(row=2, column=0, sticky = W)

port_sel = Combobox(window, text="Port", width = 20, postcommand = updatePort)
port_sel.bind("<<ComboboxSelected>>", selectPort)
port_sel.grid(row=2, column=3, sticky=E)

monitor = scrolledtext.ScrolledText(window,state=DISABLED, wrap=WORD)
monitor.grid(row=1, column=0, columnspan=5, sticky=NSEW)

Serial = serialPlotter("Serial Thread", monitor, autoscroll_state)
Serial.start()

window.wm_protocol("WM_DELETE_WINDOW", closeSerialMonitor)

window.update()

sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
rw = window.winfo_width()
rh = window.winfo_height()
window.minsize(rw, 233)
window.geometry(f'{rw}x{rh}+{int((sw-rw)/2)}+{int((sh-rh)/2)-30}')

window.mainloop()