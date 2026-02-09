from flask import Flask, request, render_template, jsonify
import os
import subprocess

app = Flask(__name__)

PDF_FOLDER = "pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- MULTIPLE PDF UPLOAD ----------
@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist("pdfs")

    for f in files:
        path = os.path.join(PDF_FOLDER, f.filename)
        f.save(path)

    return jsonify({
        "message": f"{len(files)} PDFs uploaded successfully"
    })


# ---------- ASK QUESTION ----------
@app.route("/ask", methods=["POST"])
def ask():

    q = request.json["question"]

    # Run YOUR ORIGINAL SCRIPT
    process = subprocess.Popen(
        ["python", "rag_core.ipynb"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    output = process.communicate(input=q)[0]

    return jsonify({
        "answer": output
    })


if __name__ == "__main__":
    app.run(debug=True)
