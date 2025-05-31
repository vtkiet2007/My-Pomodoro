import customtkinter as ctk
import threading
import time
import os
import sys
from tkinter import messagebox
import pygame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class PomodoroTimer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro Timer")
        self.attributes("-fullscreen", True)

        pygame.mixer.init()
        self.break_sound = pygame.mixer.Sound(os.path.join(BASE_PATH, "sounds", "notification.mp3"))

        self.pomodoro_history = []
        self.is_running = False
        self.remaining_time = 0
        self.default_duration = 25 * 60
        self.break_message = ["Duỗi vai", "Thả lỏng cánh tay", "Những mắt 30s", "Uống nước"]

        self.timer_thread = None

        self.time_label = ctk.CTkLabel(self, text="25:00", font=("Arial", 72))
        self.time_label.pack(pady=40)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.toggle_timer)
        self.start_button.pack(pady=10)

        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.reset_timer)
        self.reset_button.pack(pady=10)

        self.duration_slider = ctk.CTkSlider(self, from_=5, to=60, number_of_steps=11, command=self.update_duration)
        self.duration_slider.set(25)
        self.duration_slider.pack(pady=10)

        self.duration_label = ctk.CTkLabel(self, text="Thời gian: 25 phút")
        self.duration_label.pack(pady=5)

        self.history_label = ctk.CTkLabel(self, text="\nLịch sử Pomodoro", anchor="w", justify="left")
        self.history_label.pack(pady=10, fill="both", expand=True)

        self.remaining_time = self.default_duration
        self.update_time_label()

    def update_duration(self, value):
        minutes = int(float(value))
        self.default_duration = minutes * 60
        self.remaining_time = self.default_duration
        self.duration_label.configure(text=f"Thời gian: {minutes} phút")
        self.update_time_label()

    def update_time_label(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.configure(text=f"{minutes:02}:{seconds:02}")

    def toggle_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.configure(text="Pause")
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()
        else:
            self.is_running = False
            self.start_button.configure(text="Start")

    def run_timer(self):
        while self.is_running and self.remaining_time > 0:
            time.sleep(1)
            self.remaining_time -= 1
            self.update_time_label()
        if self.remaining_time <= 0:
            self.break_sound.play()
            self.is_running = False
            self.start_button.configure(text="Start")
            self.pomodoro_history.append(time.strftime("Hoàn thành lúc %H:%M:%S"))
            self.update_history()
            messagebox.showinfo("Hết giờ!", f"Đã đến lúc nghỉ! {self.get_break_tip()}")
            self.remaining_time = self.default_duration
            self.update_time_label()

    def reset_timer(self):
        self.is_running = False
        self.start_button.configure(text="Start")
        self.remaining_time = self.default_duration
        self.update_time_label()

    def update_history(self):
        history_text = "\n".join(self.pomodoro_history[-5:])
        self.history_label.configure(text=f"\nLịch sử Pomodoro:\n{history_text}")

    def get_break_tip(self):
        return self.break_message[len(self.pomodoro_history) % len(self.break_message)]

if __name__ == "__main__":
    app = PomodoroTimer()
    app.mainloop()
