import fitz  # PyMuPDF
import pyttsx3
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import tempfile
import threading

# ----------------- PDF Text Extraction ----------------- #
def extract_text(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
        doc.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF: {e}")
    return text

# ----------------- Text to Speech (pyttsx3 offline) ----------------- #
def speak_text_offline(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.say(text)
    engine.runAndWait()

# ----------------- Text to MP3 (gTTS online) ----------------- #
def save_text_to_mp3(text, output_path):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        messagebox.showinfo("Success", f"Audio saved at {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save MP3: {e}")

# ----------------- GUI Functions ----------------- #
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        entry_pdf_path.delete(0, tk.END)
        entry_pdf_path.insert(0, file_path)

def browse_save_path():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                             filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        entry_save_path.delete(0, tk.END)
        entry_save_path.insert(0, file_path)

def convert_pdf_to_audio():
    pdf_path = entry_pdf_path.get()
    if not pdf_path or not os.path.exists(pdf_path):
        messagebox.showwarning("Warning", "Please select a valid PDF file.")
        return

    text = extract_text(pdf_path)
    if not text.strip():
        messagebox.showwarning("Warning", "PDF contains no readable text.")
        return

    # Check user's choice: play audio or save as MP3
    choice = var_option.get()
    if choice == "Play":
        threading.Thread(target=speak_text_offline, args=(text,), daemon=True).start()
    elif choice == "Save MP3":
        save_path = entry_save_path.get()
        if not save_path:
            messagebox.showwarning("Warning", "Please select a save location for MP3.")
            return
        threading.Thread(target=save_text_to_mp3, args=(text, save_path), daemon=True).start()

# ----------------- GUI Layout ----------------- #
root = tk.Tk()
root.title("PDF to Audiobook Converter")
root.geometry("600x250")

# PDF file selection
tk.Label(root, text="Select PDF File:").pack(pady=(10, 0))
frame_pdf = tk.Frame(root)
frame_pdf.pack(pady=5, fill=tk.X, padx=10)
entry_pdf_path = tk.Entry(frame_pdf, width=50)
entry_pdf_path.pack(side=tk.LEFT, padx=(0,5))
tk.Button(frame_pdf, text="Browse", command=browse_file).pack(side=tk.LEFT)

# Save MP3 path (optional)
tk.Label(root, text="Save MP3 As:").pack(pady=(10,0))
frame_save = tk.Frame(root)
frame_save.pack(pady=5, fill=tk.X, padx=10)
entry_save_path = tk.Entry(frame_save, width=50)
entry_save_path.pack(side=tk.LEFT, padx=(0,5))
tk.Button(frame_save, text="Browse", command=browse_save_path).pack(side=tk.LEFT)

# Options: Play or Save MP3
var_option = tk.StringVar(value="Play")
frame_option = tk.Frame(root)
frame_option.pack(pady=10)
tk.Radiobutton(frame_option, text="Play Audio", variable=var_option, value="Play").pack(side=tk.LEFT, padx=20)
tk.Radiobutton(frame_option, text="Save as MP3", variable=var_option, value="Save MP3").pack(side=tk.LEFT, padx=20)

# Convert Button
tk.Button(root, text="Convert", font=("Arial", 14), bg="green", fg="white",
          command=convert_pdf_to_audio).pack(pady=10)

root.mainloop()
