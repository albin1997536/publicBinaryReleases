`pip install opencv-python pillow`



## How It Works

1. **Video Frame Preview**:  
   The program reads the first frame of the selected video using OpenCV and displays it with Pillow in a Tkinter canvas.

2. **Region Selection**:  
   Users draw rectangles over areas they want to ignore. These are stored as coordinates for later use.

3. **FFmpeg Command Generation**:  
   - The program builds a **filter_complex** chain:
     - Split the video into two streams:  
       - `masked` stream: applies black rectangles on selected regions  
       - `orig` stream: original, unmodified video  
     - Overlay the original over the masked frames so pixels remain intact.  
     - Apply `mpdecimate` on the masked stream to remove duplicate frames based on the masked regions.  
     - Adjust timestamps with `setpts=N/FRAME_RATE/TB`.  
   - Generates a complete FFmpeg command that performs this process on the entire video.

4. **Execution**:  
   Users copy the generated command and run it in a terminal. FFmpeg then outputs a video where duplicates are removed **while ignoring the user-selected regions**.

---

## Technical Notes

- Uses **OpenCV** to read video frames.  
- Uses **Pillow** for Tkinter image rendering.  
- The FFmpeg command uses `split`, `drawbox`, `overlay`, `mpdecimate`, and `setpts`.  
- The program handles multiple regions and maintains the correct aspect ratio of the video.  
- Status messages in the GUI provide real-time feedback (e.g., “Copied to clipboard”, “Region deleted”).
