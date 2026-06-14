import os
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import traffic_light_detector as detector


MODEL_PATH = "models/traffic_sign_model.h5"
PREVIEW_PX = 160


def _bar_color(conf):
    if conf >= 0.80:
        return "#2ecc71"
    if conf >= 0.50:
        return "#f39c12"
    return "#e74c3c"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traffic Sign Recognition")
        self.configure(bg="#1a1a2e")
        self.resizable(False, False)
        self._model    = None
        self._img_tk   = None
        self._img_path = None
        self._build_ui()
        self._load_model_async()

    def _build_ui(self):
        hdr = tk.Frame(self, bg="#16213e", pady=6)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Traffic Sign Recognition",
                 font=("Helvetica", 12, "bold"),
                 fg="#e0e0e0", bg="#16213e").pack()
        tk.Label(hdr, text="GTSRB  43 classes  CNN",
                 font=("Helvetica", 8), fg="#7f8c8d", bg="#16213e").pack()

        body = tk.Frame(self, bg="#1a1a2e")
        body.pack(padx=10, pady=8)

        left = tk.Frame(body, bg="#1a1a2e")
        left.pack(side="left", padx=(0, 10))

        self._canvas = tk.Canvas(left, width=PREVIEW_PX, height=PREVIEW_PX,
                                 bg="#0f3460", highlightthickness=0)
        self._canvas.pack()

        btn_col = tk.Frame(left, bg="#1a1a2e")
        btn_col.pack(pady=(6, 0))

        tk.Button(btn_col, text="Open Image",
                  command=self._open_image,
                  font=("Helvetica", 9, "bold"),
                  bg="#e94560", fg="white",
                  activebackground="#c0392b", activeforeground="white",
                  relief="flat", padx=8, pady=4,
                  cursor="hand2", width=11).pack(pady=(0, 3))

        self._pred_btn = tk.Button(btn_col, text="Classify",
                                   command=self._classify,
                                   font=("Helvetica", 9, "bold"),
                                   bg="#0f3460", fg="white",
                                   activebackground="#1a5276", activeforeground="white",
                                   relief="flat", padx=8, pady=4,
                                   cursor="hand2", state="disabled", width=11)
        self._pred_btn.pack()

        right = tk.Frame(body, bg="#16213e", padx=8, pady=8)
        right.pack(side="left", fill="both")

        tk.Label(right, text="Prediction",
                 font=("Helvetica", 8, "bold"),
                 fg="#7f8c8d", bg="#16213e").pack(anchor="w")

        self._result_label = tk.Label(right, text="",
                                      font=("Helvetica", 10, "bold"),
                                      fg="#e0e0e0", bg="#16213e",
                                      wraplength=240, justify="left")
        self._result_label.pack(anchor="w", pady=(2, 6))

        self._bar_widgets = []
        for _ in range(5):
            row = tk.Frame(right, bg="#16213e")
            row.pack(fill="x", pady=1)

            lbl = tk.Label(row, text="", font=("Helvetica", 7),
                           fg="#bdc3c7", bg="#16213e", width=20, anchor="w")
            lbl.pack(side="left")

            bg = tk.Frame(row, bg="#2c3e50", height=8, width=110)
            bg.pack(side="left", padx=3)
            bg.pack_propagate(False)

            bar = tk.Frame(bg, bg="#2ecc71", height=8, width=0)
            bar.place(x=0, y=0, relheight=1)

            pct = tk.Label(row, text="", font=("Helvetica", 7),
                           fg="#bdc3c7", bg="#16213e", width=5, anchor="w")
            pct.pack(side="left")

            self._bar_widgets.append((lbl, bg, bar, pct))

        self._status = tk.StringVar(value="Loading model...")
        self._status_lbl = tk.Label(self, textvariable=self._status,
                                    font=("Helvetica", 7), fg="#7f8c8d",
                                    bg="#1a1a2e")
        self._status_lbl.pack(pady=(0, 4))

    def _set_status(self, msg, color="#7f8c8d"):
        self.after(0, lambda: self._status.set(msg))
        self.after(0, lambda: self._status_lbl.configure(fg=color))

    def _load_model_async(self):
        def _load():
            try:
                self._model = detector.load_model(MODEL_PATH)
                self._set_status("Model ready", color="#2ecc71")
            except Exception as e:
                self._set_status(str(e), color="#e74c3c")
        threading.Thread(target=_load, daemon=True).start()

    def _open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.ppm"),
                       ("All files", "*.*")]
        )
        if not path:
            return
        self._img_path = path
        img = Image.open(path).convert("RGB")
        img.thumbnail((PREVIEW_PX, PREVIEW_PX))
        self._img_tk = ImageTk.PhotoImage(img)
        self._canvas.delete("all")
        self._canvas.create_image(PREVIEW_PX // 2, PREVIEW_PX // 2,
                                  anchor="center", image=self._img_tk)
        self._result_label.configure(text="")
        for lbl, _, bar, pct in self._bar_widgets:
            lbl.configure(text="")
            bar.place(width=0)
            pct.configure(text="")
        self._pred_btn.configure(state="normal")
        self._set_status(os.path.basename(path))

    def _classify(self):
        if self._model is None:
            return
        self._pred_btn.configure(state="disabled")
        self._set_status("Classifying...")

        def _run():
            try:
                results = detector.predict(self._model, self._img_path)
                self.after(0, lambda: self._update_ui(results))
            except Exception as e:
                self._set_status(str(e), color="#e74c3c")
                self.after(0, lambda: self._pred_btn.configure(state="normal"))

        threading.Thread(target=_run, daemon=True).start()

    def _update_ui(self, results):
        name, conf = results[0]
        self._result_label.configure(text=f"{name}  ({conf*100:.1f}%)")

        for i, (lbl, _, bar, pct) in enumerate(self._bar_widgets):
            if i >= len(results):
                lbl.configure(text="")
                bar.place(width=0)
                pct.configure(text="")
                continue
            n, c = results[i]
            lbl.configure(text=n[:20])
            bar.configure(bg=_bar_color(c))
            bar.place(width=max(int(c * 110), 1))
            pct.configure(text=f"{c*100:.1f}%")

        self._set_status("Done", color="#2ecc71")
        self._pred_btn.configure(state="normal")


if __name__ == "__main__":
    App().mainloop()