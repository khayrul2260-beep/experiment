"""
Assignment 9: Python GUI Application
Mandala Studio - a symmetry drawing app built with tkinter.
Draw with the mouse and your strokes are repeated around the centre
to make mandalas and kaleidoscope patterns.
Run:  python mandala_studio.py
"""
import colorsys
import math
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox

CANVAS_SIZE = 560
BG_COLOR = "#101820"


def symmetric_points(x, y, cx, cy, folds, mirror):
    """Return every point made by rotating (x, y) around (cx, cy).
    If mirror is True each rotated point also gets a mirror image."""
    dx, dy = x - cx, y - cy
    points = []
    for k in range(folds):
        a = 2 * math.pi * k / folds
        rx = dx * math.cos(a) - dy * math.sin(a)
        ry = dx * math.sin(a) + dy * math.cos(a)
        points.append((cx + rx, cy + ry))
        if mirror:
            points.append((cx - rx, cy + ry))
    return points


def rainbow_color(step):
    """Colour that slowly cycles through the rainbow."""
    r, g, b = colorsys.hsv_to_rgb((step % 360) / 360, 0.85, 1.0)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


class MandalaStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mandala Studio")
        self.configure(bg="#1b2733")
        self.resizable(False, False)

        self.color = "#ffd166"
        self.folds = tk.IntVar(value=8)
        self.brush = tk.IntVar(value=3)
        self.mirror = tk.BooleanVar(value=True)
        self.rainbow = tk.BooleanVar(value=False)
        self.guides = tk.BooleanVar(value=True)

        self.stroke_id = 0
        self.hue = 0
        self.last = None
        self.stroke_tags = []

        self.build_widgets()
        self.draw_guides()

    def build_widgets(self):
        tk.Label(self, text="Mandala Studio", font=("Segoe UI", 18, "bold"),
                 bg="#1b2733", fg="#ffd166").pack(pady=(10, 0))
        tk.Label(self, text="Draw anywhere - your stroke repeats around the centre",
                 font=("Segoe UI", 10), bg="#1b2733", fg="#9fb3c8").pack()

        self.canvas = tk.Canvas(self, width=CANVAS_SIZE, height=CANVAS_SIZE,
                                bg=BG_COLOR, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(padx=12, pady=10)
        self.canvas.bind("<ButtonPress-1>", self.start_stroke)
        self.canvas.bind("<B1-Motion>", self.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

        panel = tk.Frame(self, bg="#1b2733")
        panel.pack(padx=12, pady=(0, 4), fill="x")

        tk.Label(panel, text="Symmetry", bg="#1b2733", fg="white").grid(row=0, column=0, sticky="w")
        tk.Scale(panel, from_=2, to=24, orient="horizontal", variable=self.folds,
                 length=170, bg="#1b2733", fg="white", highlightthickness=0,
                 command=lambda v: self.draw_guides()).grid(row=0, column=1, padx=6)
        tk.Label(panel, text="Brush", bg="#1b2733", fg="white").grid(row=0, column=2, sticky="w")
        tk.Scale(panel, from_=1, to=12, orient="horizontal", variable=self.brush,
                 length=130, bg="#1b2733", fg="white", highlightthickness=0).grid(row=0, column=3, padx=6)

        checks = tk.Frame(self, bg="#1b2733")
        checks.pack(pady=2)
        for text, var, cmd in (("Mirror", self.mirror, None),
                               ("Rainbow", self.rainbow, None),
                               ("Guides", self.guides, self.draw_guides)):
            tk.Checkbutton(checks, text=text, variable=var, command=cmd,
                           bg="#1b2733", fg="white", selectcolor="#1b2733",
                           activebackground="#1b2733", activeforeground="white").pack(side="left", padx=8)

        btns = tk.Frame(self, bg="#1b2733")
        btns.pack(pady=(4, 12))
        self.color_btn = tk.Button(btns, text="Pick colour", bg=self.color, command=self.pick_color)
        self.color_btn.grid(row=0, column=0, padx=4)
        tk.Button(btns, text="Undo", command=self.undo).grid(row=0, column=1, padx=4)
        tk.Button(btns, text="Clear", command=self.clear).grid(row=0, column=2, padx=4)
        tk.Button(btns, text="Save drawing", command=self.save).grid(row=0, column=3, padx=4)

    # ----- drawing -----
    def centre(self):
        return CANVAS_SIZE / 2, CANVAS_SIZE / 2

    def draw_guides(self):
        self.canvas.delete("guide")
        if not self.guides.get():