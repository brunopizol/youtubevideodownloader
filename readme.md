# YouTube Downloader App

This is a Python-based YouTube downloader application with a graphical user interface (GUI) built using **Tkinter**. The app allows users to download YouTube videos in various formats including video, audio (MP3), and GIF. 

### Features
- Download YouTube videos in the best quality.
- Download audio as MP3 files.
- Convert YouTube videos to GIFs with customizable start and end times.
- Simple and easy-to-use interface.
  
## Requirements

To run this application, you need to have Python installed on your machine along with the necessary dependencies. The dependencies for this project are:

- Python 3.x
- yt-dlp: A tool to download videos from YouTube and other sites.
- moviepy: A Python library for video editing.

## Installation

### 1. Clone the repository or download the script.

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

### 2. Install dependencies.

To install the required Python packages, run the following command:

```bash
pip install -r requirements.txt
```

### 3. Requirements file (`requirements.txt`)

Create a `requirements.txt` file with the following content:

```
yt-dlp
moviepy
tkinter
```

## Running the Application

To run the application, simply execute the following command:

```bash
python main.py
```

This will launch the YouTube Downloader GUI, where you can enter a YouTube URL, choose the download format, and select an output folder.

## Building the Executable

To build a standalone `.exe` file for Windows, you can use **PyInstaller**. Here’s how you can do it:

### 1. Install PyInstaller

If you don’t have PyInstaller installed, you can install it via pip:

```bash
pip install pyinstaller
```

### 2. Build the executable

To package the application into a single executable, run the following command:

```bash
pyinstaller --onefile --windowed --icon=komainu.png your_script_name.py
```

This will generate the `.exe` file in the `dist` folder.

### 3. Locate the Executable

The `.exe` file will be located in the `dist` folder. You can now run the application on any Windows machine without needing Python installed.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
