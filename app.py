from flask import Flask, send_file, request, jsonify
from excel_final_formation import final_formation
from recog import face_recog
from add_data import upload_data
from model import glove_detection

app = Flask(__name__)


def create_excel_file():
    filename = final_formation()
    return filename


def process_face_data(icu):
    
    name,desg = face_recog()
    upload_data(desg,name,icu)
    return name


def process_gloves_data():
    
    predicted = glove_detection()
    
    if predicted:
        gl = "Gloves Predicted"
    else:
        gl = "Gloves not Predicted"
        
    
    return gl


@app.route("/", methods=["GET"])
def download_excel():
    excel_file_path = create_excel_file()
    return send_file(excel_file_path, as_attachment=True)


@app.route("/face", methods=["POST"])
def handle_face():
    input_string = request.json.get("input_string")
    if not input_string:
        return jsonify({"error": "Invalid input"}), 400
    result = process_face_data(input_string)
    return jsonify({"result": result})


@app.route("/gloves", methods=["GET"])
def handle_gloves():
    result = process_gloves_data()
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
