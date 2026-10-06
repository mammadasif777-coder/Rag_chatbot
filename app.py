import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from rag import add_document, answer, reset_collection

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files or request.files["pdf"].filename == "":
        return jsonify({"message": "Please choose a PDF first."}), 400
    file = request.files["pdf"]
    name = secure_filename(file.filename)
    path = os.path.join("uploads", name)
    file.save(path)
    reset_collection()
    n = add_document(path, name)
    return jsonify({"message": f"Indexed {n} chunks"})

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json["question"]
    return jsonify({"answer": answer(question)})

if __name__ == "__main__":
    app.run(debug=True)