import tkinter as tk
from tkinter import ttk
import math
import random

class TagWolfGUI:
    def __init__(self, root, api_client):
        self.root = root
        self.api = api_client
        self.animation_id = None
        self.particles = []
        self.glow_angle = 0
        self.setup_window()
        self.create_gradient()
        self.create_ui()
        self.start_animations()
        
    def setup_window(self):
        self.root.title("TagWolf - Aus Kronach")
        self.root.geometry("800x600")
        self.center_window()
        self.root.resizable(True, True)
        self.root.minsize(700, 500)
        
    def center_window(self):
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_gradient(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        start_color = (155, 89, 182)
        end_color = (52, 152, 219)
        
        for i in range(600):
            ratio = i / 600
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, 800, i, fill=color, width=1)
    
    def create_ui(self):
        self.title_text = self.canvas.create_text(
            400, 150,
            text="TagWolf",
            font=("Segoe UI", 64, "bold"),
            fill="white",
            anchor="center"
        )
        
        self.subtitle_text = self.canvas.create_text(
            400, 230,
            text="AUS KRONACH",
            font=("Segoe UI", 40, "bold"),
            fill="white",
            anchor="center"
        )
        
        self.glow_ring = self.canvas.create_oval(
            340, 90, 460, 210,
            outline="white",
            width=2,
            stipple="gray50"
        )
        
        self.status_frame = tk.Frame(self.root, bg='white', bd=2, relief=tk.RAISED)
        self.status_frame.place(x=100, y=300, width=600, height=100)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="API-Status: Wird geprüft...",
            font=("Segoe UI", 11),
            bg='white',
            fg='#2c3e50'
        )
        self.status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(
            self.status_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=5)
        self.progress.start(10)
        
        self.test_btn = tk.Button(
            self.status_frame,
            text="API Testen",
            command=self.test_api_with_animation,
            bg='#3498db',
            fg='white',
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT
        )
        self.test_btn.pack(pady=5)
        
        self.info_frame = tk.Frame(self.root, bg='white', bd=1, relief=tk.SOLID)
        self.info_frame.place(x=100, y=420, width=600, height=80)
        
        self.info_text = tk.Label(
            self.info_frame,
            text="Willkommen bei TagWolf!\nDie offizielle App aus Kronach",
            font=("Segoe UI", 10),
            bg='white',
            fg='#7f8c8d',
            justify=tk.CENTER
        )
        self.info_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.close_btn = tk.Button(
            self.root,
            text="Schließen",
            command=self.close_with_animation,
            bg='#e74c3c',
            fg='white',
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            relief=tk.FLAT
        )
        self.close_btn.place(x=350, y=520, width=100, height=40)
        
        self.create_floating_particles()
    
    def create_floating_particles(self):
        for _ in range(30):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(2, 6)
            speed_x = random.uniform(-0.5, 0.5)
            speed_y = random.uniform(-0.5, 0.5)
            alpha = random.randint(100, 200)
            
            particle = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=f'#{alpha:02x}{alpha:02x}{255:02x}',
                outline="",
                tags="particle"
            )
            
            self.particles.append({
                'id': particle,
                'x': x,
                'y': y,
                'size': size,
                'speed_x': speed_x,
                'speed_y': speed_y,
                'alpha': alpha
            })
    
    def animate_particles(self):
        for particle in self.particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            if particle['x'] < -20:
                particle['x'] = 820
            if particle['x'] > 820:
                particle['x'] = -20
            if particle['y'] < -20:
                particle['y'] = 620
            if particle['y'] > 620:
                particle['y'] = -20
            
            self.canvas.coords(
                particle['id'],
                particle['x'], particle['y'],
                particle['x'] + particle['size'],
                particle['y'] + particle['size']
            )
        
        self.root.after(50, self.animate_particles)
    
    def animate_glow(self):
        self.glow_angle += 0.05
        radius = 60 + math.sin(self.glow_angle) * 10
        
        x1 = 400 - radius
        y1 = 150 - radius
        x2 = 400 + radius
        y2 = 150 + radius
        
        self.canvas.coords(self.glow_ring, x1, y1, x2, y2)
        
        alpha = int(100 + math.sin(self.glow_angle * 2) * 50)
        color = f'#{alpha:02x}{alpha:02x}{255:02x}'
        self.canvas.itemconfig(self.glow_ring, outline=color)
        
        self.root.after(50, self.animate_glow)
    
    def animate_text_pulse(self):
        sizes = [60, 64, 60, 64]
        current = int((self.glow_angle * 10) % len(sizes))
        font_size = sizes[current]
        
        self.canvas.itemconfig(
            self.title_text,
            font=("Segoe UI", font_size, "bold")
        )
        
        self.root.after(200, self.animate_text_pulse)
    
    def test_api_with_animation(self):
        self.animate_button_click(self.test_btn)
        
        def test():
            try:
                result = self.api.get_info()
                self.show_success_animation()
                messagebox.showinfo("API Test", f"API erfolgreich erreicht!\n\n{result}")
            except Exception as e:
                self.show_error_animation()
                messagebox.showerror("API Fehler", f"API nicht erreichbar:\n{str(e)}")
        
        thread = threading.Thread(target=test, daemon=True)
        thread.start()
    
    def animate_button_click(self, button):
        original_bg = button.cget('bg')
        button.config(bg='#ff6b6b')
        self.root.after(150, lambda: button.config(bg=original_bg))
    
    def show_success_animation(self):
        for i in range(10):
            x = random.randint(300, 500)
            y = random.randint(250, 350)
            particle = self.canvas.create_oval(
                x, y, x + 8, y + 8,
                fill='#27ae60',
                outline=''
            )
            self.root.after(i * 50, lambda p=particle: self.canvas.delete(p))
    
    def show_error_animation(self):
        for i in range(10):
            x = random.randint(300, 500)
            y = random.randint(250, 350)
            particle = self.canvas.create_oval(
                x, y, x + 8, y + 8,
                fill='#e74c3c',
                outline=''
            )
            self.root.after(i * 50, lambda p=particle: self.canvas.delete(p))
    
    def close_with_animation(self):
        self.fade_out()
    
    def fade_out(self):
        alpha = 1.0
        
        def fade():
            nonlocal alpha
            alpha -= 0.05
            if alpha <= 0:
                self.root.quit()
            else:
                self.root.attributes('-alpha', alpha)
                self.root.after(30, fade)
        
        fade()
    
    def start_animations(self):
        self.animate_particles()
        self.animate_glow()
        self.animate_text_pulse()
    
    def update_api_status(self, status):
        self.progress.stop()
        self.progress.destroy()
        
        if status.get("status") == "online":
            self.status_label.config(
                text=f"API-Status: ✅ Online - {status.get('message', '')}",
                fg='#27ae60'
            )
            self.status_frame.config(bg='#d5f4e6')
        else:
            self.status_label.config(
                text=f"API-Status: ❌ Offline - {status.get('error', 'Keine Verbindung')}",
                fg='#e74c3c'
            )
            self.status_frame.config(bg='#ffe6e6')
