from flask import Flask, request, send_file, after_this_request
import subprocess
import uuid
import os

app = Flask(__name__)


@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    out_file = f"/tmp/{uuid.uuid4()}.wav"

    # Appel espeak pour générer le fichier
    subprocess.run(["espeak", text, "-w", out_file])

    # Planifie suppression du fichier après envoi
    @after_this_request
    def cleanup(response):
        try:
            os.remove(out_file)
        except Exception as e:
            print(f"[WARN] Impossible de supprimer {out_file}: {e}")
        return response

    return send_file(out_file, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3615)
