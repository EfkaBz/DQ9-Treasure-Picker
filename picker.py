import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Drag & Drop
from tkinterdnd2 import TkinterDnD, DND_FILES

# =====================
# BASE DIR (FIX PYINSTALLER)
# =====================
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)   # dossier du .exe
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MAPS_DIR = os.path.join(BASE_DIR, "maps")
LOC_DIR = os.path.join(MAPS_DIR, "localisation_treasure")
REG_DIR = os.path.join(MAPS_DIR, "regions")

IMG_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

# =====================
# UI CONSTANTS
# =====================
THUMB_SIZE = (190, 120)
DETAIL_LOC_SIZE = (560, 350)
DETAIL_REG_SIZE = (560, 560)
QUERY_PREVIEW_SIZE = (420, 420)

# Palette
BG = "#0f1115"
PANEL = "#151923"
CARD = "#1b2130"
TEXT = "#e7eaf0"
MUTED = "#9aa4b2"
ACCENT = "#e11d48"   # rouge
BORDER = "#2a3242"
INPUT = "#101521"


def apply_dark_theme(root: tk.Tk):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg=BG)

    style.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 10))

    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=PANEL)
    style.configure("Card.TFrame", background=CARD)

    style.configure("TLabel", background=BG, foreground=TEXT)
    style.configure("Muted.TLabel", background=BG, foreground=MUTED)
    style.configure("Panel.TLabel", background=PANEL, foreground=TEXT)
    style.configure("PanelMuted.TLabel", background=PANEL, foreground=MUTED)

    style.configure(
        "TButton",
        background=CARD,
        foreground=TEXT,
        padding=(10, 6),
        relief="flat",
        bordercolor=BORDER
    )
    style.map(
        "TButton",
        background=[("active", "#222a3b"), ("pressed", "#252f45")],
    )

    style.configure(
        "Accent.TButton",
        background=ACCENT,
        foreground="#ffffff",
        padding=(12, 7),
        relief="flat",
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#f43f5e"), ("pressed", "#be123c")],
    )

    style.configure(
        "TEntry",
        fieldbackground=INPUT,
        background=INPUT,
        foreground=TEXT,
        insertcolor=TEXT,
        padding=(8, 6),
        relief="flat"
    )

    style.configure(
        "Vertical.TScrollbar",
        background=BG,
        troughcolor=PANEL,
        bordercolor=BG,
        arrowcolor=MUTED
    )


# =====================
# HELPERS
# =====================

def list_images(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(f for f in os.listdir(folder) if f.lower().endswith(IMG_EXTS))

def stem(filename):
    return os.path.splitext(filename)[0]

def parse_direction_and_base(key: str):
    """
    key ex: 'pontaudy_sud_est_x2'
    - directions: nord/sud/est/ouest
    - si finit par _x2 => double la DERNIERE direction (juste avant)
    """
    parts = key.split("_")
    has_x2 = parts and parts[-1] == "x2"
    if has_x2:
        parts = parts[:-1]

    dirs = []
    while parts and parts[-1] in ("nord", "sud", "est", "ouest"):
        dirs.append(parts[-1])
        parts = parts[:-1]
    dirs.reverse()

    base_name = "_".join(parts) if parts else key
    double_last = has_x2 and len(dirs) >= 1

    def fmt(d, doubled=False):
        if d == "nord":
            return "⬆️⬆️ Nord x2" if doubled else "⬆️ Nord"
        if d == "sud":
            return "⬇️⬇️ Sud x2" if doubled else "⬇️ Sud"
        if d == "est":
            return "➡️➡️ Est x2" if doubled else "➡️ Est"
        if d == "ouest":
            return "⬅️⬅️ Ouest x2" if doubled else "⬅️ Ouest"
        return d

    arrows = []
    for i, d in enumerate(dirs):
        arrows.append(fmt(d, doubled=(double_last and i == len(dirs) - 1)))

    return base_name, " + ".join(arrows)

def build_exact_pairs():
    """
    Paires exactes:
      regions/<name>.<ext> <-> localisation_treasure/loc_<name>.<ext>
    """
    reg_files = list_images(REG_DIR)
    loc_files = list_images(LOC_DIR)

    pairs = []
    for reg in reg_files:
        key = stem(reg)
        matches = [lf for lf in loc_files if stem(lf) == f"loc_{key}"]
        if len(matches) == 1:
            pairs.append((reg, matches[0], key))
    return pairs, reg_files, loc_files

def is_image_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in IMG_EXTS


# =====================
# DETAIL WINDOW
# =====================

class DetailWindow(tk.Toplevel):
    def __init__(self, parent, key, reg_file, loc_file):
        super().__init__(parent)
        self.title("DQ9 Treasure Picker — Détails")
        self.geometry("1250x740")
        self.configure(bg=BG)
        self.thumbs = []

        base_name, arrows_text = parse_direction_and_base(key)

        top = ttk.Frame(self, style="Panel.TFrame")
        top.pack(fill="x", padx=12, pady=12)

        ttk.Label(top, text=f"Région: {base_name}", style="Panel.TLabel", font=("Segoe UI", 12, "bold")).pack(side="left")
        if arrows_text:
            ttk.Label(top, text=arrows_text, style="PanelMuted.TLabel", font=("Segoe UI", 10)).pack(side="left", padx=12)

        btns = ttk.Frame(top, style="Panel.TFrame")
        btns.pack(side="right")

        ttk.Button(
            btns,
            text="Ouvrir région",
            command=lambda: os.startfile(os.path.abspath(os.path.join(REG_DIR, reg_file)))
        ).pack(side="left", padx=6)

        ttk.Button(
            btns,
            text="Ouvrir loc",
            command=lambda: os.startfile(os.path.abspath(os.path.join(LOC_DIR, loc_file)))
        ).pack(side="left", padx=6)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        left = ttk.Frame(body, style="Panel.TFrame")
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Image région", style="PanelMuted.TLabel").pack(anchor="w", padx=10, pady=(10, 6))

        reg_path = os.path.join(REG_DIR, reg_file)
        reg_img = Image.open(reg_path).convert("RGBA")
        reg_img.thumbnail(DETAIL_REG_SIZE)
        reg_tk = ImageTk.PhotoImage(reg_img)
        self.thumbs.append(reg_tk)
        ttk.Label(left, image=reg_tk, style="Panel.TLabel").pack(padx=10, pady=10)

        right = ttk.Frame(body, style="Panel.TFrame")
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        ttk.Label(right, text="Localisation (loc_*)", style="PanelMuted.TLabel").pack(anchor="w", padx=10, pady=(10, 4))
        ttk.Label(right, text=loc_file, style="Panel.TLabel").pack(anchor="w", padx=10, pady=(0, 10))

        loc_path = os.path.join(LOC_DIR, loc_file)
        loc_img = Image.open(loc_path).convert("RGBA")
        loc_img.thumbnail(DETAIL_LOC_SIZE)
        loc_tk = ImageTk.PhotoImage(loc_img)
        self.thumbs.append(loc_tk)
        ttk.Label(right, image=loc_tk, style="Panel.TLabel").pack(anchor="w", padx=10, pady=(0, 10))


# =====================
# MAIN APP (TkinterDnD)
# =====================

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        apply_dark_theme(self)

        self.title("DQ9 Treasure Picker")
        self.geometry("1500x900")

        self.thumbs = []
        self.current_image_tk = None

        self.pairs, self.reg_files, self.loc_files = build_exact_pairs()

        self.build_ui()

    # -------------- mouse wheel support --------------

    def _on_mousewheel(self, event):
        delta = getattr(event, "delta", 0)
        if delta == 0:
            return
        step = -1 if delta > 0 else 1
        self.canvas.yview_scroll(step * 3, "units")

    def _on_mousewheel_linux_up(self, event):
        self.canvas.yview_scroll(-3, "units")

    def _on_mousewheel_linux_down(self, event):
        self.canvas.yview_scroll(3, "units")

    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    # -------------- UI --------------

    def build_ui(self):
        top = ttk.Frame(self, style="Panel.TFrame")
        top.pack(fill="x", padx=12, pady=12)

        ttk.Button(top, text="📂 Importer une image", style="Accent.TButton", command=self.open_image).pack(side="left")
        ttk.Label(top, text="Glisser-déposer une image dans le panneau à gauche", style="PanelMuted.TLabel").pack(side="left", padx=12)

        ttk.Label(top, text="Recherche:", style="PanelMuted.TLabel").pack(side="left", padx=(30, 6))
        self.search_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.search_var, width=40)
        entry.pack(side="left")
        entry.bind("<KeyRelease>", lambda e: self.render())

        self.info = ttk.Label(
            top,
            text=f"Regions: {len(self.reg_files)} | Loc: {len(self.loc_files)} | Paires: {len(self.pairs)}",
            style="PanelMuted.TLabel"
        )
        self.info.pack(side="right")

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # LEFT (drop zone)
        left = ttk.Frame(body, style="Panel.TFrame")
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Image chargée", style="Panel.TLabel", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 6))

        self.image_label = ttk.Label(
            left,
            text="Dépose une image ici\n(ou utilise Importer)",
            style="PanelMuted.TLabel",
            justify="center"
        )
        self.image_label.pack(padx=10, pady=(0, 10))

        # Drag & Drop target
        self.image_label.drop_target_register(DND_FILES)
        self.image_label.dnd_bind("<<Drop>>", self.on_drop_file)

        # RIGHT (scroll)
        right = ttk.Frame(body, style="Panel.TFrame")
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self.canvas = tk.Canvas(right, bg=PANEL, highlightthickness=0)
        self.scroll = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side="right", fill="y", pady=10)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

        self.inner = ttk.Frame(self.canvas, style="Panel.TFrame")
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.render()

    # -------------- Drag & Drop --------------

    def on_drop_file(self, event):
        try:
            # event.data peut contenir un ou plusieurs chemins, parfois entourés de {}
            paths = self.tk.splitlist(event.data)
            if not paths:
                return
            path = paths[0]
            path = path.strip("{}")

            if not os.path.exists(path):
                messagebox.showerror("Drag & Drop", "Chemin invalide.")
                return

            if not is_image_file(path):
                messagebox.showerror("Drag & Drop", "Fichier non supporté. (png/jpg/webp/bmp)")
                return

            self.load_image(Image.open(path))

        except Exception as e:
            messagebox.showerror("Drag & Drop", str(e))

    # -------------- image input --------------

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if path:
            try:
                self.load_image(Image.open(path))
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def load_image(self, img):
        preview = img.copy()
        preview.thumbnail(QUERY_PREVIEW_SIZE)
        self.current_image_tk = ImageTk.PhotoImage(preview)
        self.image_label.config(image=self.current_image_tk, text="")
        self.image_label.image = self.current_image_tk

    # -------------- detail --------------

    def open_detail(self, key, reg_file, loc_file):
        base_name, arrows_text = parse_direction_and_base(key)
        txt = base_name if not arrows_text else f"{base_name} | {arrows_text}"
        self.info.config(text=txt)
        DetailWindow(self, key, reg_file, loc_file)

    # -------------- render --------------

    def render(self):
        for w in self.inner.winfo_children():
            w.destroy()
        self.thumbs.clear()

        q = self.search_var.get().strip().lower()
        pairs = sorted(self.pairs, key=lambda x: x[2])
        if q:
            pairs = [p for p in pairs if q in p[2].lower() or q in p[0].lower() or q in p[1].lower()]

        cols = 6
        for idx, (reg_file, loc_file, key) in enumerate(pairs):
            loc_path = os.path.join(LOC_DIR, loc_file)

            img = Image.open(loc_path).convert("RGBA")
            img.thumbnail(THUMB_SIZE)
            tk_img = ImageTk.PhotoImage(img)
            self.thumbs.append(tk_img)

            card = ttk.Frame(self.inner, style="Card.TFrame")
            card.grid(row=idx // cols, column=idx % cols, padx=10, pady=10, sticky="n")

            btn = ttk.Button(
                card,
                image=tk_img,
                command=lambda k=key, r=reg_file, l=loc_file: self.open_detail(k, r, l)
            )
            btn.pack(padx=10, pady=(10, 8))

            base_name, arrows_text = parse_direction_and_base(key)

            ttk.Label(
                card,
                text=base_name,
                background=CARD,
                foreground=TEXT,
                font=("Segoe UI", 10, "bold"),
                justify="center"
            ).pack(padx=10)

            ttk.Label(
                card,
                text=arrows_text if arrows_text else "",
                background=CARD,
                foreground=MUTED,
                font=("Segoe UI", 9),
                justify="center"
            ).pack(padx=10, pady=(2, 10))


if __name__ == "__main__":
    App().mainloop()
