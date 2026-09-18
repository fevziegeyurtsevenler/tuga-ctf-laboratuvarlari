import os
from flask import Flask, render_template, send_from_directory, abort

app = Flask(__name__)

# Primary portal: Spotifly Music Leak Interface
@app.route("/")
def index():
    track_meta = {
        "title": "Kusursuz Plan (Unreleased Leak)",
        "artist": "JANTİ",
        "album": "Single Release 2026",
        "audio_file": "audio/janti_leak_demo.wav"
    }
    return render_template("index.html", track=track_meta)

# Secondary portal discovered via spectrogram: Backstage Gossip Feed
@app.route("/backstage-feed")
def backstage_feed():
    blog_posts = [
        {
            "id": 1,
            "title": "JANTİ's Leaked Audio: Master Recording Breach?",
            "author": "DeepVibe_Insider",
            "date": "2026-09-01",
            "snippet": "The leak originated from an internal mixing session. Check the comment signatures and metadata trails left behind by the sound engineer."
        }
    ]
    return render_template("blog.html", posts=blog_posts)

# Download route for forensic audio analysis
@app.route("/download/audio")
def download_audio():
    audio_dir = os.path.join(app.root_path, "static", "audio")
    filename = "janti_leak_demo.wav"
    if not os.path.exists(os.path.join(audio_dir, filename)):
        abort(404)
    return send_from_directory(audio_dir, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)