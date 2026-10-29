from flask import Flask, render_template, request, jsonify, send_from_directory
from ultralytics import YOLO
from PIL import Image
import io
import numpy as np
from flask_cors import CORS
import os
import random
from datetime import datetime

# Setup directories relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
INVASIVE_DIR = os.path.join(STATIC_DIR, 'invasive_data')

from species_mapping import species_data

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
CORS(app)

# Load YOLOv11 model (classification)
MODEL_PATH = os.path.join(BASE_DIR, 'best.pt')
model = YOLO(MODEL_PATH)

def get_species_folder(scientific_name):
    """Finds the actual folder on disk matching scientific_name (case-insensitive fallback)."""
    if not os.path.isdir(INVASIVE_DIR):
        return None
    # Exact match
    direct = os.path.join(INVASIVE_DIR, scientific_name)
    if os.path.isdir(direct):
        return scientific_name
    # Case-insensitive match
    for name in os.listdir(INVASIVE_DIR):
        if name.lower() == scientific_name.lower():
            return name
    return None

def get_random_icon(scientific_name):
    folder_name = get_species_folder(scientific_name)
    if not folder_name:
        return None
    folder = os.path.join(INVASIVE_DIR, folder_name)
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not files:
        return None
    return f'/static/invasive_data/{folder_name}/{random.choice(files)}'

@app.route('/')
def index():
    # List all scientific names and nepali names from species_data, with a random icon
    species_list = []
    for s in species_data:
        icon = get_random_icon(s['scientific_name'])
        species_list.append({
            'scientific_name': s['scientific_name'],
            'nepali_name': s['nepali_name'],
            'icon': icon
        })
    return render_template('index.html', species_list=species_list, active_page='gallery')

@app.route('/identify')
def identify():
    return render_template('identify.html', active_page='identify')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    img = img.resize((224, 224))
    # Run inference
    results = model(img)
    # Get top-5 predictions
    top5 = results[0].probs.top5
    probs = results[0].probs.data
    names = results[0].names
    predictions = []
    for idx in top5:
        sci_name = names[idx]
        conf = float(probs[idx])
        # Case-insensitive match against species_data
        matched = next((s for s in species_data if s['scientific_name'].lower() == sci_name.lower()), None)
        nepali_name = matched['nepali_name'] if matched else 'Unknown'
        # Canonical scientific name if matched
        display_sci = matched['scientific_name'] if matched else sci_name
        predictions.append({'class': display_sci, 'raw_class': sci_name, 'confidence': conf, 'nepali_name': nepali_name})
    return jsonify({'predictions': predictions})

@app.route('/species/images/<scientific_name>')
def species_images(scientific_name):
    # Path to images for this species
    folder_name = get_species_folder(scientific_name)
    if not folder_name:
        return jsonify({'images': []})
    folder = os.path.join(INVASIVE_DIR, folder_name)
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    urls = [f'/static/invasive_data/{folder_name}/{f}' for f in files]
    return jsonify({'images': urls})

@app.route('/species/<scientific_name>')
def species_page(scientific_name):
    # Find species info case-insensitively
    species = next((s for s in species_data if s['scientific_name'].lower() == scientific_name.lower()), None)
    if not species:
        canonical_name = scientific_name
        nepali_name = 'Unknown'
        short_description = ''
        long_description = ''
    else:
        canonical_name = species['scientific_name']
        nepali_name = species['nepali_name']
        short_description = species.get('short_description', '')
        long_description = species.get('long_description', '')
    return render_template('species.html', scientific_name=canonical_name, nepali_name=nepali_name, short_description=short_description, long_description=long_description, active_page='gallery')

@app.route('/save-labeled', methods=['POST'])
def save_labeled():
    if 'image' not in request.files or 'class' not in request.form:
        return jsonify({'success': False, 'error': 'Missing image or class'}), 400
    file = request.files['image']
    class_name = request.form['class']
    folder_name = get_species_folder(class_name) or class_name
    folder = os.path.join(INVASIVE_DIR, folder_name)
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f'user_{timestamp}.jpg'
    path = os.path.join(folder, filename)
    file.save(path)
    return jsonify({'success': True, 'filename': filename})

@app.route('/api/sample-images')
def sample_images():
    """Returns a list of sample images from diverse classes for quick testing."""
    samples = []
    if os.path.isdir(INVASIVE_DIR):
        folders = [d for d in os.listdir(INVASIVE_DIR) if os.path.isdir(os.path.join(INVASIVE_DIR, d))]
        for d in folders:
            folder_path = os.path.join(INVASIVE_DIR, d)
            files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                samples.append({
                    'species': d,
                    'url': f'/static/invasive_data/{d}/{files[0]}'
                })
    return jsonify({'samples': samples[:8]})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting कृषि चश्मा demo on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)