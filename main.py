import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x700")  # Increased height to accommodate new features
        self.create_widgets()

    def create_widgets(self):
        # Input URL
        tk.Label(self.root, text="YouTube Video URL:").pack(pady=10)
        self.url_entry = tk.Entry(self.root, width=60)
        self.url_entry.pack(pady=5)

        # Choose format
        tk.Label(self.root, text="Download Format:").pack(pady=10)
        self.format_var = tk.StringVar(value="video")
        video_radio = tk.Radiobutton(self.root, text="Video", variable=self.format_var, value="video")
        audio_radio = tk.Radiobutton(self.root, text="Audio (MP3)", variable=self.format_var, value="audio")
        gif_radio = tk.Radiobutton(self.root, text="GIF", variable=self.format_var, value="gif")
        video_radio.pack()
        audio_radio.pack()
        gif_radio.pack()

        # GIF Options (Hidden by default)
        self.gif_options_frame = tk.Frame(self.root)
        tk.Label(self.gif_options_frame, text="GIF Start Time (seconds):").pack(pady=5, anchor="w")
        self.gif_start_entry = tk.Entry(self.gif_options_frame, width=10)
        self.gif_start_entry.pack(pady=5, anchor="w")
        tk.Label(self.gif_options_frame, text="GIF End Time (seconds):").pack(pady=5, anchor="w")
        self.gif_end_entry = tk.Entry(self.gif_options_frame, width=10)
        self.gif_end_entry.pack(pady=5, anchor="w")
        self.gif_options_frame.pack_forget()

        # Output directory selection
        tk.Label(self.root, text="Output Directory:").pack(pady=10)
        self.output_path = tk.StringVar()
        self.output_button = tk.Button(self.root, text="Select Folder", command=self.select_output_folder)
        self.output_button.pack(pady=5)

        # Start Download Button
        self.download_button = tk.Button(self.root, text="Download", command=self.start_download)
        self.download_button.pack(pady=20)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Update GIF options visibility based on selection
        self.format_var.trace("w", self.toggle_gif_options)

    def toggle_gif_options(self, *args):
        if self.format_var.get() == "gif":
            self.gif_options_frame.pack(pady=10)
        else:
            self.gif_options_frame.pack_forget()

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
            messagebox.showinfo("Folder Selected", f"Output folder set to: {folder}")

    def start_download(self):
        url = self.url_entry.get()
        output_path = self.output_path.get()
        format_type = self.format_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        if not output_path:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        self.progress_bar.start(10)
        try:
            if format_type == "video":
                self.download_video(url, output_path)
            elif format_type == "audio":
                self.download_audio(url, output_path)
            elif format_type == "gif":
                self.download_and_convert_to_gif(url, output_path)
            messagebox.showinfo("Success", "Operation completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process: {e}")
        finally:
            self.progress_bar.stop()

    def download_video(self, url, output_path):
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_audio(self, url, output_path):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_and_convert_to_gif(self, url, output_path):
        # Step 1: Download the video
        temp_video_path = os.path.join(output_path, "temp_video.mp4")
        ydl_opts = {
            'format': 'best',
            'outtmpl': temp_video_path,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Step 2: Convert video to GIF
        try:
            start_time = float(self.gif_start_entry.get() or 0)
            end_time = float(self.gif_end_entry.get() or 10)
            gif_output_path = os.path.join(output_path, "output.gif")

            self.video_to_gif(temp_video_path, gif_output_path, start_time, end_time)
        finally:
            # Cleanup temp video
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)

    def video_to_gif(self, input_video_path, output_gif_path, start_time=0, end_time=None, resize_factor=0.5, fps=15):
        try:
            # Load the video file (disable audio if not needed)
            video = VideoFileClip(input_video_path, audio=False)

            # If end_time is not provided, set it to the video's duration
            if end_time is None:
                end_time = video.duration

            # Trim the video to the desired time range
            video_clip = video.subclip(start_time, end_time)

            # Resize the video clip to reduce GIF size (resize_factor controls the reduction percentage)
            video_clip = video_clip.resize(resize_factor)

            # Convert to GIF with a reduced frame rate and optimized size
            video_clip.write_gif(output_gif_path, fps=fps)

            print("GIF successfully created!")

        except Exception as e:
            print(f"Error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
