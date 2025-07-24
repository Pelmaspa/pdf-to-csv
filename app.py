from flask import Flask, request, render_template, send_file
import os
from pdf_to_structured_csv_full_con_descr2 import estrai_righe_con_descrizione, genera_csv_strutturato

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
OUTPUT_FOLDER = os.path.join(app.root_path, 'outputs')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["pdf_file"]
        if file and file.filename.endswith(".pdf"):
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(pdf_path)

            csv_filename = file.filename.replace(".pdf", ".csv")
            csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)

            righe = estrai_righe_con_descrizione(pdf_path)
            genera_csv_strutturato(righe, csv_path)

            return send_file(csv_path, as_attachment=True)

    return render_template("index.html")
