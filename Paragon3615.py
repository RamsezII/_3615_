from flask import Flask, request, send_file, after_this_request
import subprocess
import uuid
import os

app = Flask(__name__)


@app.route("/tts")
def tts():
    text = request.args.get("text", "").strip()
    if not text:
        return "Missing 'text' parameter", 400

    # Paramètres dynamiques
    lang = request.args.get("lang", "fr")
    speed = request.args.get("speed", "140")
    pitch = request.args.get("pitch", "50")
    volume = request.args.get("volume", "100")

    # Fichier temporaire
    out_file = f"/tmp/{uuid.uuid4()}.wav"

    # Construction de la commande espeak
    command = [
        "espeak",
        "-v", lang,
        "-s", speed,
        "-p", pitch,
        "-a", volume,
        "-w", out_file,
        text
    ]

    try:
        subprocess.run(command, check=True)
    except Exception as e:
        return f"Error in espeak: {e}", 500

    @after_this_request
    def cleanup(response):
        try:
            os.remove(out_file)
        except Exception as e:
            print(f"[WARN] Could not remove temp file: {e}")
        return response

    return send_file(out_file, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3615)
