import psutil
import tkinter as tk
from tkinter import scrolledtext
import threading
import time


# متغير للتحكم في تشغيل/إيقاف المراقبة
monitoring = False

def start_monitoring():
    """بدء مراقبة الشبكة"""
  
    global monitoring
    monitoring = True
    monitor_thread = threading.Thread(target=monitor_network, daemon=True)
    monitor_thread.start()

def stop_monitoring():
    
    """إيقاف مراقبة الشبكة"""
    global monitoring
    monitoring = False

def monitor_network():
    """مراقبة البيانات الخاصة بالشبكة وتحديث الواجهة"""
    time.sleep(2)
    while monitoring:
        text_box.delete(1.0, tk.END)  # مسح النص القديم
        for interface, data in psutil.net_io_counters(pernic=True).items():
            text_box.insert(tk.END, f"\n[+]Network Interface: {interface}\n", "bold")
            text_box.insert(tk.END, f"    Bytes Sent   : {data.bytes_sent} Bytes\n", "normal")
            text_box.insert(tk.END, f"    Bytes Received: {data.bytes_recv} Bytes\n", "normal")
            text_box.insert(tk.END, f"    Packets Sent  : {data.packets_sent}\n", "normal")
            text_box.insert(tk.END, f"    Packets Received: {data.packets_recv}\n", "normal")
            text_box.insert(tk.END, f"    Errors In    : {data.errin}\n", "error")
            text_box.insert(tk.END, f"    Errors Out   : {data.errout}\n", "error")
            text_box.insert(tk.END, "-" * 50 + "\n", "separator")
            time.sleep(3)
        text_box.yview(tk.END)  # التمرير تلقائياً إلى الأسفل
        

# إنشاء نافذة Tkinter
root = tk.Tk()
root.title("Network Monitor")
root.geometry("600x400")
root.configure(bg="#1c2833")
root.resizable(False,False)
#icone
root.iconphoto(False,tk.PhotoImage(file="images/router.png"))
# صندوق نصي قابل للتمرير لعرض البيانات
text_box = scrolledtext.ScrolledText(root, width=80, height=20,fg="#52be80",bg="black", font=("Courier", 10))
text_box.pack(pady=10)

# إضافة أنماط نصوص
text_box.tag_configure("bold",foreground="#f1c40f", font=("Courier", 10, "bold"))
text_box.tag_configure("error", foreground="red")
text_box.tag_configure("separator", foreground="gray")
text_box.tag_configure("normal", foreground="#52be80")

# أزرار التحكم
frame = tk.Frame(root,bg="#1c2833")
frame.pack(pady=5)

start_button = tk.Button(frame, text="Start Monitoring", command=start_monitoring, bg="green", fg="white",border=2)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(frame, text="Stop Monitoring", command=stop_monitoring, bg="red", fg="white",border=2)
stop_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(frame, text="Exit", command=root.quit, bg="gray", fg="white")
exit_button.grid(row=0, column=2, padx=10)

# تشغيل النافذة
root.mainloop()