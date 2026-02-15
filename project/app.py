from flask import Flask, request, render_template, jsonify
import os
import subprocess

app = Flask(__name__)

# Absolute paths to avoid location confusion
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")

os.makedirs(PDF_FOLDER, exist_ok=True)

print("Using PDF folder:", PDF_FOLDER)


@app.route("/")
def index():
    return render_template("index.html")


# ===== FILE UPLOAD =====
@app.route("/upload", methods=["POST"])
def upload():

    if "pdfs" not in request.files:
        return jsonify({"message": "No files received"})

    files = request.files.getlist("pdfs")

    count = 0

    for file in files:
        if file.filename.strip() == "":
            continue

        save_path = os.path.join(PDF_FOLDER, file.filename)

        file.save(save_path)
        count += 1

        print("Saved:", save_path)

    return jsonify({
        "message": f"{count} PDFs saved in {PDF_FOLDER}"
    })


# ===== ASK QUESTION =====
@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    question = data.get("question", "")

    # Run your original RAG script as external program
    process = subprocess.Popen(
        ["python", "rag_script.py"],
        cwd=BASE_DIR,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, error = process.communicate(input=question)

    # Clean terminal text
    clean = output.replace("Ask your viva question:", "")
    clean = clean.replace("--- ASSISTANT RESPONSE ---", "")
    clean = clean.strip()

    if error:
        clean += "\n\n[ERROR]\n" + error

    return jsonify({"answer": clean})


if __name__ == "__main__":
    app.run(debug=True)
