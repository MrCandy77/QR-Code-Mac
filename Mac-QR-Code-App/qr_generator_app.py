import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.parse import urlparse

import qrcode
from PIL import Image, ImageTk


APP_TITLE = "QR Code Generator"
DEFAULT_SIZE = 300
PREVIEW_SIZE = 280
MIN_SIZE = 100
MAX_SIZE = 2000
WINDOW_BG = "#f4f7fb"


class QRGeneratorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.resizable(False, False)
        self.root.configure(padx=18, pady=18, bg=WINDOW_BG)

        self.url_var = tk.StringVar()
        self.width_var = tk.StringVar(value=str(DEFAULT_SIZE))
        self.height_var = tk.StringVar(value=str(DEFAULT_SIZE))
        self.status_var = tk.StringVar(value="Enter a URL, then generate a QR code.")

        self.generated_image: Image.Image | None = None
        self.preview_image: ImageTk.PhotoImage | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        ttk.Label(main, text="Paste URL").grid(row=0, column=0, sticky="w")
        url_entry = ttk.Entry(main, textvariable=self.url_var, width=46)
        url_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(4, 12))
        url_entry.focus()

        ttk.Label(main, text="Width (px)").grid(row=2, column=0, sticky="w")
        ttk.Label(main, text="Height (px)").grid(row=2, column=1, sticky="w", padx=(12, 0))

        width_spin = ttk.Spinbox(
            main,
            from_=MIN_SIZE,
            to=MAX_SIZE,
            increment=10,
            textvariable=self.width_var,
            width=10,
        )
        width_spin.grid(row=3, column=0, sticky="w", pady=(4, 12))

        height_spin = ttk.Spinbox(
            main,
            from_=MIN_SIZE,
            to=MAX_SIZE,
            increment=10,
            textvariable=self.height_var,
            width=10,
        )
        height_spin.grid(row=3, column=1, sticky="w", padx=(12, 0), pady=(4, 12))

        button_frame = ttk.Frame(main)
        button_frame.grid(row=4, column=0, columnspan=3, sticky="w")

        ttk.Button(button_frame, text="Generate QR Code", command=self.generate_qr).grid(
            row=0, column=0, padx=(0, 8)
        )
        self.download_button = ttk.Button(
            button_frame,
            text="Download PNG",
            command=self.save_png,
            state="disabled",
        )
        self.download_button.grid(row=0, column=1)

        preview_frame = ttk.LabelFrame(main, text="Preview")
        preview_frame.grid(row=5, column=0, columnspan=3, pady=(16, 10), sticky="ew")

        self.preview_label = ttk.Label(
            preview_frame,
            text="Your QR code will appear here.",
            anchor="center",
            width=40,
            padding=12,
        )
        self.preview_label.grid(row=0, column=0)

        status_label = ttk.Label(
            main,
            textvariable=self.status_var,
            wraplength=360,
            justify="left",
            foreground="#1f4e79",
        )
        status_label.grid(row=6, column=0, columnspan=3, sticky="w")

        self.root.bind("<Return>", lambda _event: self.generate_qr())

    def _validate_url(self, raw_url: str) -> str:
        url = raw_url.strip()
        if not url:
            raise ValueError("Please paste a URL first.")

        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"https://{url}"
            parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Enter a valid website URL such as https://example.com")

        return url

    def _read_dimension(self, value: str, label: str) -> int:
        try:
            size = int(value)
        except ValueError as exc:
            raise ValueError(f"{label} must be a whole number.") from exc

        if size < MIN_SIZE or size > MAX_SIZE:
            raise ValueError(f"{label} must be between {MIN_SIZE} and {MAX_SIZE} pixels.")

        return size

    def _default_file_name(self, url: str) -> str:
        host = urlparse(url).netloc.replace("www.", "").strip()
        safe_host = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in host)
        safe_host = safe_host.strip("-") or "qr-code"
        return f"{safe_host}-qr.png"

    def generate_qr(self) -> None:
        try:
            url = self._validate_url(self.url_var.get())
            width = self._read_dimension(self.width_var.get(), "Width")
            height = self._read_dimension(self.height_var.get(), "Height")
        except ValueError as error:
            messagebox.showerror(APP_TITLE, str(error))
            self.status_var.set(str(error))
            return

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        resized = image.resize((width, height), Image.Resampling.NEAREST)
        self.generated_image = resized

        preview = resized.copy()
        preview.thumbnail((PREVIEW_SIZE, PREVIEW_SIZE), Image.Resampling.NEAREST)
        self.preview_image = ImageTk.PhotoImage(preview)
        self.preview_label.configure(image=self.preview_image, text="")
        self.download_button.configure(state="normal")
        self.status_var.set(f"QR code ready for {width} x {height}px PNG download.")

    def save_png(self) -> None:
        if self.generated_image is None:
            messagebox.showinfo(APP_TITLE, "Generate a QR code before downloading it.")
            return

        try:
            url = self._validate_url(self.url_var.get())
        except ValueError:
            default_name = "qr-code.png"
        else:
            default_name = self._default_file_name(url)

        destination = filedialog.asksaveasfilename(
            title="Save QR Code",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[("PNG image", "*.png")],
        )

        if not destination:
            return

        output_path = Path(destination)
        try:
            self.generated_image.save(output_path, format="PNG")
        except OSError as error:
            messagebox.showerror(APP_TITLE, f"Could not save the PNG.\n\n{error}")
            self.status_var.set("Save failed. Choose a different folder and try again.")
            return

        self.status_var.set(f"Saved PNG to {output_path}")
        messagebox.showinfo(APP_TITLE, f"QR code saved to:\n{output_path}")


def main() -> None:
    root = tk.Tk()
    app = QRGeneratorApp(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
