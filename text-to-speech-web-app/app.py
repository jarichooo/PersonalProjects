from flask import Flask, render_template, request, send_file, jsonify, url_for
import os
from werkzeug.utils import secure_filename
from main import extract_text  

app = Flask(__name__)

# define paths
UPLOAD_FOLDER = os.path.join("static", "uploads")
MP3_FOLDER = os.path.join("static", "mp3s")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MP3_FOLDER, exist_ok=True)

# flask config for consistency
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MP3_FOLDER'] = MP3_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        start = int(request.form.get("start", 0))
        end = int(request.form.get("end", 1))

        if uploaded_file and uploaded_file.filename.endswith(".pdf"):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            mp3_filename = os.path.splitext(filename)[0] + "_output.mp3"
            extract_text(filepath, start=start, end=end, fileName=mp3_filename)

            mp3_path = os.path.join(app.config['MP3_FOLDER'], mp3_filename)

            if os.path.exists(mp3_path):
                # render a page with audio player
                return send_file(mp3_path, as_attachment=True)
            else:
                return "MP3 file was not generated", 500

    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')
    start = int(request.form.get('start', 0))
    end = int(request.form.get('end', 1))

    if not uploaded_file or not uploaded_file.filename.endswith('.pdf'):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(uploaded_file.filename)
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(pdf_path)

    mp3_filename = os.path.splitext(filename)[0] + '_output.mp3'
    mp3_path = os.path.join(app.config['MP3_FOLDER'], mp3_filename)

    extract_text(pdf_path, start, end, fileName=mp3_filename)

    if not os.path.exists(mp3_path):
        return jsonify({"error": "MP3 file not generated"}), 500

    return jsonify({"mp3_url": url_for('static', filename=f'mp3s/{mp3_filename}')})

if __name__ == "__main__":
    app.run(debug=True)