import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from yt_dlp import YoutubeDL
import threading
import os
import shutil

progreso_label = None
progreso_barra = None

def obtener_ruta_ffmpeg():
    ruta_local = os.path.join(os.getcwd(), 'ffmpeg', 'bin', 'ffmpeg.exe')
    if os.path.exists(ruta_local):
        return os.path.dirname(ruta_local)
    ruta_sistema = shutil.which("ffmpeg")
    if ruta_sistema:
        return os.path.dirname(ruta_sistema)
    messagebox.showerror(
        "Error",
        "No se encontró FFmpeg.\n\nDescárgalo desde https://ffmpeg.org/download.html"
    )
    return None

def descargar_video():
    url = url_entry.get()
    calidad = calidad_var.get()

    if not url:
        messagebox.showwarning("Advertencia", "Por favor ingresa una URL válida.")
        return

    carpeta = filedialog.askdirectory()
    if not carpeta:
        return

    ruta_ffmpeg = obtener_ruta_ffmpeg()
    if not ruta_ffmpeg:
        return

    resoluciones = {
        "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    }
    formato = resoluciones.get(calidad, "best")

    ydl_opts = {
        'format': formato,
        'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
        'progress_hooks': [hook_progreso],
        'quiet': True,
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'ffmpeg_location': ruta_ffmpeg,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    def ejecutar_descarga():
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            progreso_label.config(text="¡Descarga completa!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar el video.\n\n{e}")
            progreso_label.config(text="Error en la descarga.")
        progreso_barra['value'] = 0

    threading.Thread(target=ejecutar_descarga).start()

def hook_progreso(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        porcentaje = int(downloaded_bytes * 100 / total_bytes) if total_bytes else 0
        progreso_label.config(text=f"Descargando: {porcentaje}%")
        progreso_barra['value'] = porcentaje
        progreso_label.update()
        progreso_barra.update()

root = tk.Tk()
root.title("Descargador YouTube con yt-dlp + Progreso")
root.geometry("450x300")
root.resizable(False, False)

tk.Label(root, text="URL del video de YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=55)
url_entry.pack(pady=5)

tk.Label(root, text="Selecciona la calidad:").pack(pady=5)
calidad_var = tk.StringVar(value="720p")
for res in ["480p", "720p", "1080p"]:
    tk.Radiobutton(root, text=res, variable=calidad_var, value=res).pack()

tk.Button(root, text="Descargar", command=descargar_video).pack(pady=10)

progreso_label = tk.Label(root, text="Progreso: 0%")
progreso_label.pack(pady=5)
progreso_barra = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progreso_barra.pack(pady=5)

root.mainloop()
