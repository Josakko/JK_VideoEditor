import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import moviepy.editor as mp
from moviepy.video.compositing.concatenate import concatenate_videoclips
import cv2
from PIL import Image, ImageTk

class JK_VideoEditor:
    def __init__(self):
        self.window = tk.Tk()
        
        window_width = 400
        window_hight = 500
        
        monitor_width = self.window.winfo_screenwidth()
        monitor_hight = self.window.winfo_screenheight()
        
        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        self.window.geometry(f'{window_width}x{window_hight}+{int(x)}+{int(y)}')
        self.window.title("JK VideoEditor")
        self.window.iconbitmap("JK.ico")
        self.window.config(bg="#dbdbdb")
        self.window.resizable(False, False)
        
        self.font = ("Arial", 12)# font=self.font
                
        self.output_lbl = tk.Label(self.window, text="", font=self.font, bg="#dbdbdb")
        self.output_lbl.pack(pady=10)

        self.output_button = tk.Button(text="Select Output File", font=self.font, width=20, command=self.select_output_file)
        self.output_button.pack(pady=6)
                
        self.input_button = tk.Button(text="Select Input File", font=self.font, width=20, command=self.select_input_file)
        self.input_button.pack(pady=15)
        
        self.separator_lbl = tk.Label(self.window, font=("Arial", 10), bg="#dbdbdb")
        self.separator_lbl.pack()
    
        self.start_time_label = tk.Label(text="Start Time (in seconds):",  font=self.font, bg="#dbdbdb")
        self.start_time_label.pack(pady=5)
        
        self.start_time = tk.Spinbox(from_=0, to=1, font=self.font, width=20, state="disabled")
        self.start_time.pack()

        self.separator_lbl1 = tk.Label(self.window, font=("Arial", 3), bg="#dbdbdb")
        self.separator_lbl1.pack()

        self.end_time_label = tk.Label(text="End Time (in seconds):", font=self.font, bg="#dbdbdb")
        self.end_time_label.pack(pady=5)

        self.end_time = tk.Spinbox(from_=0, to=1, font=self.font, width=20, state="disabled")
        self.end_time.pack()

        self.separator_lbl2 = tk.Label(self.window, font=("Arial", 10), bg="#dbdbdb")
        self.separator_lbl2.pack()

        self.status_lbl = tk.Label(text="No video selected", font=self.font, bg="#dbdbdb") #self.status_lbl.config(text="")
        self.status_lbl.pack(pady=10)
        
        self.edit_button = tk.Button(text="Render Video", font=self.font, width=20, command=self.render_video)
        self.edit_button.pack()


        self.window.mainloop()
        
             
        self.input_file = ""
        self.output_file = ""
    
    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(defaultextension=".mp4", filetypes=[("Video Files", "*.mp4")])
        try:
            self.video = mp.VideoFileClip(self.input_file)
        except:
            return
        
        if self.input_file:
            self.status_lbl.config(text="Selected Video: " + self.input_file)
            
            self.start_time.configure(state="normal", from_=0, to=self.video.duration)
            self.end_time.configure(state="normal", from_=0, to=self.video.duration)


    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
        
        if self.output_file:
            self.output_lbl.configure(text="Output: " + self.output_file)

    def render_video(self):
        try:
            if self.input_file == "":
                messagebox.showerror("Error", "Please select an input file before trying again")
                self.status_lbl.configure(text="Please select an input file before trying again")
                return
            else:
                pass
        except:
            messagebox.showerror("Error", "Please select an input file before trying again")
            self.status_lbl.configure(text="Please select an input file before trying again")
            return
        
        try:
            if self.output_file == "":
                messagebox.showerror("Error", "Please select an output file before trying again")
                self.status_lbl.configure(text="Please select an output file before trying again")
                return
        except:
            messagebox.showerror("Error", "Please select an output file before trying again")
            self.status_lbl.configure(text="Please select an output file before trying again")
            return
        
        try:
            start_time = float(self.start_time.get())
            end_time = float(self.end_time.get())

            if start_time < 0 or end_time < 0:
                messagebox.showerror("Error", "Start and end times must be non-negative!")
                self.status_lbl.configure(text="Start and end times must be non-negative!")
                return

            if end_time <= start_time:
                messagebox.showerror("Error", "End time must be greater than start time!")
                self.status_lbl.configure(text="End time must be greater than start time!")
                return

            if start_time > self.video.duration or end_time > self.video.duration:
                messagebox.showerror("Error", "Start and end times must be within the video duration!")
                self.status_lbl.configure(text="Start and end times must be within the video duration!")
                return

        except ValueError:
            messagebox.showerror("Error", "Start and end times must be numbers!")
            self.status_lbl.configure(text="Start and end times must be numbers!")
            return
        
        
        messagebox.showwarning("Warning", "This process could take several minutes, please do not close the window until rendering is completed.")
        self.window.title("Rendering - JK VideoEditor")
        self.status_lbl.configure(text="Rendering the video...")
        
        try:
            original_duration = self.video.duration

            clip_kept_start = self.video.subclip(0, start_time)
            clip_kept_end = self.video.subclip(end_time, original_duration)

            final_clip = concatenate_videoclips([clip_kept_start, clip_kept_end], method="compose")
            final_clip.write_videofile(self.output_file)

            self.window.title = ("Success - JK VideoEditor")
            msg = f"Video exported to {self.output_file}"
            messagebox.showinfo("Success", msg)
        except:
            self.window.title("Error - JK VideoEditor")
            messagebox.showerror("Error", "Some thing went wrong, please try again!")
            self.status_lbl.configure(text="Some thing went wrong, please try again!")


app = JK_VideoEditor()
