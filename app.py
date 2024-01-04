from flask import Flask, render_template, jsonify
import os
from datetime import datetime, timedelta
from flask import send_file
from dotenv import dotenv_values

app = Flask(__name__)

aqara_env = dotenv_values(".env")
VIDEO_PATH = aqara_env.get("VIDEO_PATH")


@app.route("/")
def index():
    video_metadata = get_video_metadata()
    return render_template("index.html", video_metadata=video_metadata)


def get_video_metadata():
    metadata = []

    for date_folder in os.listdir(VIDEO_PATH):
        date_path = os.path.join(VIDEO_PATH, date_folder)

        if os.path.isdir(date_path):
            date = datetime.strptime(date_folder, "%Y%m%d").date()

            for video_file in os.listdir(date_path):
                if video_file.endswith(".mp4"):
                    video_path = os.path.join(date_path, video_file)

                    # Extract start time from the filename
                    start_time_str = video_file.split(".")[0]
                    start_time = datetime.combine(
                        date, datetime.strptime(start_time_str, "%H%M%S").time()
                    )
                    start_time += timedelta(hours=8)  # timezone difference
                    # Calculate end time (start time + 6 seconds) default footage is 6 sec, todo read duration from mp4 and determine from there
                    end_time = start_time + timedelta(seconds=6)

                    metadata.append(
                        {
                            "video_path": video_path,
                            "start_time": start_time,
                            "end_time": end_time,
                        }
                    )
    # print(metadata)
    return metadata


def extract_start_end_time(file_name):
    start_time = file_name[:6]
    end_time = file_name[:6]
    return start_time, end_time


@app.route("/play/<path:video_path>")
def play(video_path):
    print(video_path)
    return send_file(f"/{video_path}")


if __name__ == "__main__":
    app.run(debug=True, port=7456, host="0.0.0.0")
