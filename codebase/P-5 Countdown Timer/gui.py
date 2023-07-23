import sys
import pygame
import tkinter as tk
from tkinter import ttk

sys.path.insert(0, ".")

from count_down_timer import Time, CountDownTimer
from utils import is_int, value_exceeds_max

pygame.mixer.init()


class TimerControls(ttk.Frame):
    def __init__(self, root: tk.Tk | ttk.Frame = None):
        super().__init__(root)
        self._container = ttk.Frame(self)

        self._toggle_pause_button_text = tk.StringVar()
        self._toggle_pause_button_text.set("Pause")
        self.toggle_pause_button = ttk.Button(self._container, textvariable=self._toggle_pause_button_text)

        self.reset_button = ttk.Button(self._container, text="Reset")

    def render(self) -> None:
        self.toggle_pause_button.pack(side=tk.LEFT, padx=10)
        self.reset_button.pack(side=tk.LEFT)
        self._container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def set_toggle_pause_button_text(self, value: str) -> None:
        self._toggle_pause_button_text.set(value)


class TimeRemainingDisplay(ttk.Frame):
    def __init__(self, root: tk.Tk | ttk.Frame = None):
        self._styles = {
            "TRD.TFrame": {
                "background": "#EB455F",
            },
            "TRD.TLabel": {
                "background": "#EB455F",
                "foreground": "white"
            }
        }
        self._configure_styles()
        super().__init__(root, style="TRD.TFrame")

        self._time_remaining = tk.StringVar()
        self._time_remaining_label = ttk.Label(self, font=("Ubuntu", 40, "bold"),
                                               style="TRD.TLabel", textvariable=self._time_remaining)

    def set_time_remaining(self, value):
        self._time_remaining.set(value)

    def _configure_styles(self):
        style = ttk.Style()
        for style_name, style_settings in self._styles.items():
            style.configure(style_name, **style_settings)

    def render(self):
        self._time_remaining_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class TimerDurationForm(ttk.Frame):
    def __init__(self, root: tk.Tk | ttk.Frame = None):
        self._styles = {
            "TDF_TITLE_CONTAINER.TFrame": {
                "background": "#EB455F",
                "foreground": "white"
            },
            "TDF_SUBMIT_BTN.TButton": {
                "background": "#EB455F",
                "foreground": "white"
            },
            "ERROR.TLabel": {
                "foreground": "red",
                "font": ("Ubuntu", 7)
            }
        }
        self.configure_styles()
        super().__init__(root)

        self.large_bold_font = ("Ubuntu", 15, "bold")
        self.small_regular_font = ("Ubuntu", 9)

        self._title_container = ttk.Frame(self, style="TDF_TITLE_CONTAINER.TFrame")
        self._title = ttk.Label(self._title_container, text="ASSESS YOUR TIME", font=self.large_bold_font)

        self._form_container = ttk.Frame(self)

        self._minutes_error_tracker = tk.StringVar()
        self._valid_minutes = False
        self._minutes_error_message = ttk.Label(self._form_container, textvariable=self._minutes_error_tracker,
                                                style="ERROR.TLabel")

        self._seconds_error_tracker = tk.StringVar()
        self._valid_seconds = False
        self._seconds_error_message = ttk.Label(self._form_container, textvariable=self._seconds_error_tracker,
                                                style="ERROR.TLabel")

        self._minutes_entry_label = ttk.Label(self._form_container, text="Minutes", font=self.small_regular_font)
        self._minutes_entry = ttk.Entry(self._form_container, width=40, validate="key",
                                        validatecommand=(root.register(self.validate_minutes), "%P"))

        self._seconds_entry_label = ttk.Label(self._form_container, text="Seconds", font=self.small_regular_font)
        self._seconds_entry = ttk.Entry(self._form_container, width=40, validate="key",
                                        validatecommand=(root.register(self.validate_seconds), "%P"))

        self.submit_button = ttk.Button(self._form_container, text="START", style="TDF_SUBMIT_BTN.TButton",
                                        width=40)

    def configure_styles(self):
        style = ttk.Style()
        for style_name, style_settings in self._styles.items():
            style.configure(style_name, **style_settings)
        style.map("TDF_SUBMIT_BTN.TButton", background=[('active', "#EB455F")])

    def is_valid(self) -> bool:
        return self._valid_minutes and self._valid_seconds

    def validate_minutes(self, minutes) -> bool:
        if is_int(minutes) and not value_exceeds_max(minutes, 59):
            self._minutes_error_tracker.set("")
            self._valid_minutes = True
        else:
            self._minutes_error_tracker.set("Only integers less than 60")
            self._valid_minutes = False
        return self._valid_minutes

    def validate_seconds(self, seconds) -> bool:
        if is_int(seconds) and not value_exceeds_max(seconds, 59):
            self._seconds_error_tracker.set("")
            self._valid_seconds = True
        else:
            self._seconds_error_tracker.set("Only integers less than 60")
            self._valid_seconds = False
        return self._valid_seconds

    def render(self) -> None:
        self._minutes_entry_label.grid(row=0, column=0, sticky=tk.W)
        self._minutes_entry.grid(row=1, column=0, ipady=7)
        self._minutes_error_message.grid(row=2, column=0, pady=5, sticky=tk.W)

        self._seconds_entry_label.grid(row=3, column=0, sticky=tk.W)
        self._seconds_entry.grid(row=4, column=0, ipady=7)
        self._seconds_error_message.grid(row=5, column=0, pady=5, sticky=tk.W)

        self.submit_button.grid(row=6, column=0, sticky=tk.W, pady=10, ipady=7)

        self._title.pack()
        self._title_container.pack(side=tk.TOP, pady=20)

        self._form_container.pack(side=tk.TOP)

        self.pack(side=tk.TOP, fill=tk.X, expand=True)

    @property
    def minutes(self):
        return int(self._minutes_entry.get())

    @property
    def seconds(self):
        return int(self._seconds_entry.get())


class GUICountDownTimer(ttk.Frame):
    def __init__(self, root: tk.Tk = None):
        super().__init__(root)
        self.window_title = "Count Down Timer By Kirabo Ibrahim"
        self.timer_duration = None
        self.timer = None
        self.time_depleted = False
        self.timer_paused = False

        self.root_width, self.root_height = (400, 600)

        root.geometry("{}x{}".format(self.root_height, self.root_width))
        root.title(self.window_title)
        root.iconphoto(False, tk.PhotoImage(file="images/icon.jpg"))

        self.timer_duration_form = TimerDurationForm(self)
        self.time_remaining_display = TimeRemainingDisplay(self)
        self.timer_controls = TimerControls(self)

        self.time_remaining_subscription = None
        self.time_depleted_subscription = None
        self.time_depleted_sound = pygame.mixer.Sound("sounds/door-bell-sound.wav")
        self.timer_duration_form.render()

        self.pack(fill=tk.BOTH, expand=True)
        self.set_up_event_listeners()

    def set_up_event_listeners(self) -> None:
        self.timer_duration_form.submit_button.configure(command=lambda this=self: this.on_duration_form_submit())
        self.timer_controls.toggle_pause_button.configure(command=lambda this=self: this.toggle_pause())
        self.timer_controls.reset_button.configure(command=lambda this=self: this.reset())

    def on_duration_form_submit(self) -> None:
        if self.timer_duration_form.is_valid():
            self.timer_duration = Time(self.timer_duration_form.minutes, self.timer_duration_form.seconds)
            self.timer = CountDownTimer(self.timer_duration)
            self.start()

    def toggle_pause(self) -> None:
        if not self.time_depleted:
            self.resume() if self.timer_paused else self.pause()

    def resume(self) -> None:
        self.timer_controls.set_toggle_pause_button_text("Pause")
        self.timer.resume()
        self.timer_paused = False

    def pause(self):
        self.timer_controls.set_toggle_pause_button_text("Resume")
        self.timer.pause()
        self.timer_paused = True

    def reset(self) -> None:
        self.dispose_subscriptions()
        self.timer = CountDownTimer(self.timer_duration)
        self.timer_paused = False
        self.time_depleted = False
        self.start()

    def dispose_subscriptions(self):
        if self.time_remaining_subscription:
            self.time_remaining_subscription.dispose()
        if self.time_depleted_subscription:
            self.time_depleted_subscription.dispose()

    def start(self) -> None:
        self.timer_duration_form.destroy()
        self.render_timer()
        self.time_remaining_subscription = self.timer.time_remaining.subscribe(lambda time_remaining, this=self: this.time_remaining_display.
                                                                               set_time_remaining(this.format_time(time_remaining)))
        self.time_depleted_subscription = self.timer.depleted.subscribe(lambda time_depleted, this=self:
                                                                        this.on_time_depleted(time_depleted))

    def on_time_depleted(self, time_depleted):
        self.time_depleted = time_depleted
        if self.time_depleted:
            self.time_depleted_sound.play()

    def render_timer(self) -> None:
        self.time_remaining_display.render()
        self.timer_controls.render()

    @staticmethod
    def format_time(time: Time) -> str:
        return "{:02d}:{:02d}".format(time.minutes, time.seconds)


toplevel_window = tk.Tk()
count_down_timer = GUICountDownTimer(root=toplevel_window)
count_down_timer.mainloop()
