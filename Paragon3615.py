from flask import Flask, json, request, send_file, after_this_request
import subprocess
import uuid
import os

app = Flask(__name__)


@app.route("/espeak")
def espeak():
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


@app.route("/espeak-ng")
def espeak_ng():
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
        "espeak-ng",
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


@app.route("/espeak-json")
def espeak_voices():
    try:
        result = subprocess.run(["espeak", "--voices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Skip header
        voices = []

        for line in lines:
            parts = line.strip().split(None, 4)
            if len(parts) >= 5:
                _, lang, _, voice_name, _ = parts
                voices.append({
                    "lang": lang,
                    "voice": voice_name
                })

        return json.dumps(voices), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}
    return send_file(out_file, mimetype="audio/wav")


@app.route("/espeak-ng-json")
def espeak_ng_voices():
    try:
        result = subprocess.run(["espeak-ng", "--voices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Skip header
        voices = []

        for line in lines:
            parts = line.strip().split(None, 4)
            if len(parts) >= 5:
                _, lang, _, voice_name, _ = parts
                voices.append({
                    "lang": lang,
                    "voice": voice_name
                })

        return json.dumps(voices), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3615)
