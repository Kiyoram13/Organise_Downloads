import os
import shutil
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image  # Importar PIL para cargar imágenes

# Configuración de la apariencia
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema azul

# Archivo de configuración para almacenar las extensiones personalizadas
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "file_types": {
            "Imágenes": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
            "Documentos": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt"],
            "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv"],
            "Música": [".mp3", ".wav", ".aac", ".flac"],
            "Instaladores": [".exe", ".msi"],
            "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Otros": []
        }
    }

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
downloads_folder = ""

def select_folder():
    global downloads_folder
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        downloads_folder = folder_selected
        lbl_folder.configure(text=f"📁 Carpeta: {downloads_folder}")

def organize_files():
    if not downloads_folder:
        messagebox.showerror("Error", "¡Selecciona una carpeta primero!")
        return

    selected_types = [key for key, var in check_vars.items() if var.get()]
    
    if not selected_types:
        messagebox.showerror("Error", "¡Selecciona al menos un tipo de archivo!")
        return

    for folder in selected_types:
        folder_path = os.path.join(downloads_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    for file in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, file)
        if os.path.isdir(file_path):
            continue

        file_ext = os.path.splitext(file)[1].lower()
        
        for folder in selected_types:
            if file_ext in config["file_types"][folder]:
                shutil.move(file_path, os.path.join(downloads_folder, folder, file))
                break
        else:
            if "Otros" in selected_types:
                shutil.move(file_path, os.path.join(downloads_folder, "Otros", file))

    messagebox.showinfo("Éxito", "✅ Archivos organizados correctamente.")

def add_extension():
    new_ext = entry_extension.get().strip().lower()
    selected_folder = dropdown_var.get()
    if not new_ext.startswith("."):
        messagebox.showerror("Error", "Las extensiones deben empezar con un punto (Ejemplo: .csv)")
        return
    if not selected_folder:
        messagebox.showerror("Error", "Selecciona una carpeta válida.")
        return
    if new_ext in sum(config["file_types"].values(), []):
        messagebox.showwarning("Aviso", "Esta extensión ya está registrada.")
        return
    config["file_types"][selected_folder].append(new_ext)
    save_config()
    entry_extension.delete(0, 'end')
    messagebox.showinfo("Éxito", f"✅ La extensión {new_ext} se ha agregado a '{selected_folder}'.")

root = ctk.CTk()
root.title("Organizador de Descargas")
root.geometry("500x650")

# Cargar el icono personalizado
icon_path = os.path.join(os.path.dirname(__file__), "resources/dw.png")
icono = ctk.CTkImage(light_image=Image.open(icon_path), size=(32, 32))


font_title = ("Arial", 18, "bold")
font_text = ("Arial", 14)

lbl_title = ctk.CTkLabel(root, text="📂 Organizador de Descargas", font=font_title)
lbl_title.pack(pady=10)

btn_select_folder = ctk.CTkButton(root, text="Seleccionar Carpeta 📁", command=select_folder)
btn_select_folder.pack(pady=10)

lbl_folder = ctk.CTkLabel(root, text="📁 Carpeta: No seleccionada", wraplength=450, font=font_text)
lbl_folder.pack(pady=5)

lbl_options = ctk.CTkLabel(root, text="📌 Selecciona los tipos de archivos a organizar:", font=font_text)
lbl_options.pack(pady=5)

check_vars = {key: ctk.BooleanVar() for key in config["file_types"].keys()}
frame_checks = ctk.CTkFrame(root)
frame_checks.pack(pady=5)

for key, var in check_vars.items():
    chk = ctk.CTkCheckBox(frame_checks, text=key, variable=var)
    chk.pack(anchor="w", padx=20, pady=2)

lbl_add_extension = ctk.CTkLabel(root, text="➕ Agregar nueva extensión:", font=font_text)
lbl_add_extension.pack(pady=5)

frame_add_ext = ctk.CTkFrame(root)
frame_add_ext.pack(pady=5)

entry_extension = ctk.CTkEntry(frame_add_ext, width=150, placeholder_text="Ejemplo: .csv")
entry_extension.pack(side="left", padx=5)

dropdown_var = ctk.StringVar(value="Seleccionar carpeta")
dropdown_folder = ctk.CTkComboBox(frame_add_ext, values=list(config["file_types"].keys()), variable=dropdown_var)
dropdown_folder.pack(side="left", padx=5)

btn_add_extension = ctk.CTkButton(root, text="Agregar", command=add_extension, fg_color="blue")
btn_add_extension.pack(pady=10)

btn_organize = ctk.CTkButton(root, text="🚀 Organizar", command=organize_files, fg_color="green", hover_color="darkgreen")
btn_organize.pack(pady=20)

root.mainloop()