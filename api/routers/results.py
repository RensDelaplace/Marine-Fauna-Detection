#Import
import asyncio
import os
from pathlib import Path
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import  StreamingResponse

router = APIRouter()

# Endpoint for result videos
@router.get("/results/{video:path}")
def resultVideo(video: str, range: str = Header()):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(script_dir))
    video_path = Path(os.path.join(project_dir, "results", video))
    file_byte_size = video_path.stat().st_size
    range_parts = range.replace('bytes=', '').split('-')
    start = int(range_parts[0])
    end = int(range_parts[1]) if len(range_parts) > 1 and range_parts[1] else file_byte_size - 1

    if start >= file_byte_size:
        raise HTTPException(status_code=416, detail="Requested Range Not Satisfiable")

    end = min(end, file_byte_size - 1)
    content_length = end - start + 1

    chunk_size = 1024 * 1024  # 1 MB chunks

    async def stream_file(start, end):
        with open(video_path, mode="rb") as file_bytes:
            file_bytes.seek(start)
            while start <= end:
                read_size = min(chunk_size, end - start + 1)
                data = file_bytes.read(read_size)
                if not data:
                    break
                yield data
                start += read_size

    try:
        return StreamingResponse(
            stream_file(start, end),
            status_code=206,
            media_type="video/mp4",
            headers={
                'Accept-Ranges': 'bytes',
                'Content-Range': f'bytes {start}-{end}/{file_byte_size}',
                'Content-Length': str(content_length),
            }
        )
    except asyncio.CancelledError:
        print("Request was cancelled")
        raise HTTPException(status_code=499, detail="Client Closed Request")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
