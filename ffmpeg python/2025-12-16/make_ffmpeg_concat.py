import sys
import os
import ctypes
from ctypes import wintypes

def copy_to_clipboard_windows(text):
    CF_UNICODETEXT = 13
    GMEM_MOVEABLE = 0x0002

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    # Function signatures
    user32.OpenClipboard.argtypes = [wintypes.HWND]
    user32.OpenClipboard.restype = wintypes.BOOL

    user32.EmptyClipboard.argtypes = []
    user32.EmptyClipboard.restype = wintypes.BOOL

    user32.SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
    user32.SetClipboardData.restype = wintypes.HANDLE

    user32.CloseClipboard.argtypes = []
    user32.CloseClipboard.restype = wintypes.BOOL

    kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
    kernel32.GlobalAlloc.restype = wintypes.HGLOBAL

    kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalLock.restype = wintypes.LPVOID

    kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    kernel32.GlobalUnlock.restype = wintypes.BOOL

    if not user32.OpenClipboard(None):
        raise RuntimeError("Failed to open clipboard")

    user32.EmptyClipboard()

    data = (text + "\0").encode("utf-16-le")
    h_global = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
    if not h_global:
        user32.CloseClipboard()
        raise MemoryError("GlobalAlloc failed")

    lp_global = kernel32.GlobalLock(h_global)
    if not lp_global:
        kernel32.GlobalFree(h_global)
        user32.CloseClipboard()
        raise MemoryError("GlobalLock failed")

    ctypes.memmove(lp_global, data, len(data))
    kernel32.GlobalUnlock(h_global)

    user32.SetClipboardData(CF_UNICODETEXT, h_global)
    user32.CloseClipboard()

def main():
    if len(sys.argv) < 2:
        print("Drag and drop MP4 files onto this script.")
        return

    mp4s = []
    for f in sys.argv[1:]:
        f = os.path.abspath(f)
        if f.lower().endswith(".mp4") and os.path.isfile(f):
            mp4s.append(f)

    if not mp4s:
        print("No MP4 files found.")
        return

    first_name = os.path.splitext(os.path.basename(mp4s[0]))[0]
    output_name = f"{first_name} - concat.mp4"

    with open("filelist.txt", "w", encoding="utf-8") as out:
        for f in mp4s:
            out.write(f"file '{f.replace('\\', '/')}'\n")

    command = f'ffmpeg -f concat -safe 0 -i filelist.txt -c copy "{output_name}"'

    print("\nFFmpeg command:\n")
    print(command)
    print()

    answer = input("Copy command to clipboard? (y/n): ").strip().lower()
    if answer == "y" and sys.platform.startswith("win"):
        copy_to_clipboard_windows(command)
        print("Command copied to clipboard (Unicode safe).")



if __name__ == "__main__":
    main()
