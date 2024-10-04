from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import yt_dlp

app = FastAPI()

allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cur_dir = os.getcwd()

@app.post("/download")
async def download_video(link: str = Form(...)):
    video_filename = "sample.mp4"
    output_path = os.path.join(cur_dir, video_filename)

    youtube_dl_options = {
        "format": "bestvideo+bestaudio/best",  # Use best available formats
        "outtmpl": output_path,
    }

    try:
        # Create a YoutubeDL object
        with yt_dlp.YoutubeDL() as ydl:
            # Extract video information
            info_dict = ydl.extract_info(link, download=False)
            # Get the available formats
            formats = info_dict.get('formats', [])
            
            # Print available formats for debugging
            for format in formats:
                print(f"Format ID: {format['format_id']}, Extension: {format['ext']}, Resolution: {format.get('height', 'N/A')}p")

        # Download the video
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return FileResponse(output_path, media_type='video/mp4', filename=video_filename)
