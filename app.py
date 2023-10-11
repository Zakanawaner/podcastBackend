from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os, json, base64

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route('/')
def getGeneral():
    return jsonify({'message': "Tremendo cumbiote papi"})
    

@app.route('/podcast-text/<nb>')
def getPodcastText(nb):
    with open('./static/strings.json', 'r') as archivo:
        datos = json.load(archivo)
        return jsonify({'message': datos['podcast'+ nb]})


@app.route('/episodes-text')
def getEpisodesText():
    with open('./static/strings.json', 'r') as archivo:
        datos = json.load(archivo)
        return jsonify({'message': datos['episodes']})


@app.route('/tales-text')
def getTalesText():
    with open('./static/strings.json', 'r') as archivo:
        datos = json.load(archivo)
        return jsonify({'message': datos['tales']})


@app.route('/pdf/<filename>', methods=['GET'])
def download_document(filename):
    filepath = './static/tales/' + filename
    return send_file(filepath, as_attachment=True)


@app.route('/get-tales', methods=['GET'])
def get_tales():
    pdf_directory = './static/tales'
    img_directory = './static/images/'
    with open('./static/strings.json', 'r') as archivo:
        datos = json.load(archivo)
    available_documents = []
    documentList = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    documentList.sort(key=lambda x: float(x.split(' ')[0]))
    for filename in documentList:
        with open(img_directory + filename.replace('.pdf', '.jpeg'), 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        available_documents.append({
            'title': filename,
            'image': image_base64,
            'uri': datos['uri'][filename.split(" - ")[0]]
        })

    return jsonify({'message': available_documents})


@app.route('/about-text/<nb>')
def getAboutText(nb):
    with open('./static/strings.json', 'r') as archivo:
        datos = json.load(archivo)
        return jsonify({'message': datos['about' + nb]})


if __name__ == '__main__':
    app.run()