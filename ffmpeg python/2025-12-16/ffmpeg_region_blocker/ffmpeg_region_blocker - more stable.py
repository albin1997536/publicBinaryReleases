import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

rectangles = []
start_x = start_y = None
current_rect = None
video_path = None

STATUS_CLEAR_MS = 2000

def open_video():
    global img_tk, video_path
    path = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.mkv *.avi")]
    )
    if not path:
        return

    video_path = path

    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Could not read video")
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(img)

    canvas.delete("all")
    rectangles.clear()

    canvas.config(width=img.width, height=img.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    base, ext = os.path.splitext(os.path.basename(path))
    output_name_var.set(f"{base}-no-duplicateframes{ext}")

    set_status("Video loaded")

def on_mouse_down(event):
    global start_x, start_y, current_rect
    start_x, start_y = event.x, event.y
    current_rect = canvas.create_rectangle(
        start_x, start_y, start_x, start_y,
        outline="red", width=2
    )

def on_mouse_drag(event):
    canvas.coords(current_rect, start_x, start_y, event.x, event.y)

def on_mouse_up(event):
    global current_rect
    x1, y1, x2, y2 = canvas.coords(current_rect)
    x = int(min(x1, x2))
    y = int(min(y1, y2))
    w = int(abs(x2 - x1))
    h = int(abs(y2 - y1))

    if w > 5 and h > 5:
        rectangles.append({
            "id": current_rect,
            "x": x, "y": y, "w": w, "h": h
        })
    else:
        canvas.delete(current_rect)

    current_rect = None

def on_right_click(event):
    to_remove = None
    for rect in rectangles:
        if (
            rect["x"] <= event.x <= rect["x"] + rect["w"] and
            rect["y"] <= event.y <= rect["y"] + rect["h"]
        ):
            to_remove = rect
            break

    if to_remove:
        canvas.delete(to_remove["id"])
        rectangles.remove(to_remove)
        set_status("Region deleted")

def build_ffmpeg_command():
    if not video_path or not rectangles:
        return None

    drawboxes = [
        f"drawbox=x={r['x']}:y={r['y']}:w={r['w']}:h={r['h']}:color=black@1:t=fill"
        for r in rectangles
    ]

    filter_chain = ",".join(drawboxes + ["mpdecimate", "setpts=N/FRAME_RATE/TB"])

    output_name = output_name_var.get().strip()
    if not output_name:
        return None

    return (
        f'ffmpeg -i "{video_path}" '
        f'-vf "{filter_chain}" '
        f'-an "{output_name}"'
    )

def generate_ffmpeg():
    cmd = build_ffmpeg_command()
    if not cmd:
        set_status("Load video and draw at least one region")
        return

    output.delete("1.0", tk.END)
    output.insert(tk.END, cmd)
    set_status("Command generated")

def copy_command():
    cmd = output.get("1.0", tk.END).strip()
    if not cmd:
        set_status("Nothing to copy")
        return

    root.clipboard_clear()
    root.clipboard_append(cmd)
    root.update()
    set_status("Copied to clipboard")

def set_status(text):
    status_label.config(text=text)
    root.after_cancel(getattr(set_status, "after_id", None))
    set_status.after_id = root.after(STATUS_CLEAR_MS, lambda: status_label.config(text=""))

# GUI setup
root = tk.Tk()
root.title("FFmpeg mpdecimate Region Blocker")

# Instructions
tk.Label(
    root,
    text="Draw regions to ignore (Left-drag = add, Right-click = remove)",
    font=("Segoe UI", 10, "bold")
).pack(pady=(5, 2))

canvas = tk.Canvas(root, bg="black")
canvas.pack()

canvas.bind("<ButtonPress-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
canvas.bind("<Button-3>", on_right_click)
canvas.bind("<Control-Button-1>", on_right_click)

controls = tk.Frame(root)
controls.pack(pady=6)

tk.Label(controls, text="Step 1:").grid(row=0, column=0, sticky="e")
tk.Button(controls, text="Open Video", command=open_video).grid(row=0, column=1, padx=5)

tk.Label(controls, text="Step 2:").grid(row=0, column=2, sticky="e")
tk.Button(controls, text="Generate Command", command=generate_ffmpeg).grid(row=0, column=3, padx=5)

tk.Label(controls, text="Step 3:").grid(row=0, column=4, sticky="e")
tk.Button(controls, text="Copy Command", command=copy_command).grid(row=0, column=5, padx=5)

tk.Label(root, text="Output filename:").pack()
output_name_var = tk.StringVar()
tk.Entry(root, textvariable=output_name_var, width=60).pack(pady=2)

output = tk.Text(root, height=4, width=120)
output.pack(pady=5)

status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=(0, 5))

root.mainloop()
