from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

def extract_video_id(link):
    """Extract the video ID from a YouTube video link."""
    parsed_url = urlparse(link)
    if parsed_url.netloc == "www.youtube.com" or parsed_url.netloc == "youtube.com":
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    elif parsed_url.netloc == "youtu.be":
        return parsed_url.path.lstrip("/")
    return None

def get_subtitles(video_id):
    """Retrieve subtitles for the given video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        return str(e)

@app.route('/get_subtitles', methods=['GET'])
def get_subtitles_endpoint():
    """Endpoint to get subtitles for a YouTube video."""
    link = request.args.get('link')
    if not link:
        return jsonify({"error": "No link provided"}), 400

    video_id = extract_video_id(link)
    if not video_id:
        return jsonify({"error": "Invalid YouTube link"}), 400

    subtitles = get_subtitles(video_id)
    return jsonify({"subtitles": subtitles})

if __name__ == '__main__':
    app.run(debug=True)