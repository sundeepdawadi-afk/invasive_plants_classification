# 🌿 Invasive Plants Classification (नेपालमा बाह्य मिचाहा वनस्पति पहिचान)

Deep learning classification models and interactive web interface for identifying invasive alien plant species across Nepal, accompanied by curated botanical knowledge graphs, species distributions, and field notes.

Developed as a semester project under the guidance of **[Sandesh Shrestha Sir](https://ku.edu.np/contact-detail/474)** at Kathmandu University (KU).

---

## 👥 Team Members

- **Shivram Saud** — [Google Scholar](https://scholar.google.com/citations?user=RJcXNNIAAAAJ&hl=en)
- **Darwin Acharya** — [Google Scholar](https://scholar.google.com/citations?user=eadu1YYAAAAJ&hl=en)
- **Sundeep Dawadi** — [Google Scholar](https://scholar.google.com/citations?user=WZlKvaoAAAAJ&hl=en)

---

## 🚀 Interactive Web Application: कृषि चश्मा (Krishi Chashma)

An interactive Flask web app powered by a fine-tuned YOLOv11 classifier (`best.pt`) that identifies invasive plant species in real-time.

### ✨ Features
- **Live Identification:** Real-time webcam capture and instant image file upload/drag-and-drop.
- **Top-5 Predictions:** Ranked confidence probabilities with botanical names and official Nepali names.
- **Active Data Labeling:** Confirm predictions and contribute verified photos to class dataset folders.
- **Interactive Species Gallery:** Visual catalog displaying high-resolution sample photos and botanical background for 20+ species.
- **Theme Switcher:** Seamless Dark / Light mode toggle.

### 💻 Running the App Locally

1. **Navigate to the demo directory:**
   ```bash
   cd appdemo
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Start the application:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to: **[http://127.0.0.1:5001](http://127.0.0.1:5001)**

---

## 🧠 Model Architectures & Notebooks

1. **YOLOv11 Classifier:**
   - Notebook: [`colabnote_yolo_n_invasive_final.ipynb`](colabnote_yolo_n_invasive_final.ipynb)
   - Pretrained weights: `appdemo/best.pt`
   - High-speed real-time edge inference on 224×224 images.

2. **DenseNet Deep Feature Classifier:**
   - Notebook: [`local_densenet.ipynb`](local_densenet.ipynb)
   - Evaluates transfer learning accuracy and convergence curves across invasive species classes.

---

## 📦 Dataset

The training and validation dataset of invasive plant species in Nepal is hosted on Hugging Face:
- **Hugging Face Dataset:** [sundeepdawadi-afk/invasive_species_classification_images](https://huggingface.co/datasets/sundeepdawadi-afk/invasive_species_classification_images)

*Disclaimer: Image datasets were collected and compiled from academic and open sources for non-commercial educational and research purposes.*

---

## 📚 Botanical Knowledge Base & Notes

Curated botanical documentation, ecological impacts, and distribution statistics across Nepal's 70+ districts:

- **[Notes Index & Table of Contents](notes/README.md)**
- **[पृष्ठभूमी (Background)](notes/पृष्ठभूमी.md)** — Ecological overview and threats to indigenous flora.
- **[नेपालमा फैलिएका बाह्य मिचाहा वनस्पतिहरू (Full Book Reference)](notes/नेपालमा%20फैलिएका%20बाह्य%20मिचाहा%20वनस्पतिहरू.md)**
- **[Statistics & District Distribution](notes/others/Statistics.md)** — Diversity tables and 210-year invasion history.
- **[Nepali Species Data](notes/Nepali%20Species%20Data.md)** — Comprehensive multilingual dictionary of crops and invasive weeds.
- **[26 Priority Invasive Alien Species](notes/26%20species/)** — Individual species sheets with field screenshots and family classifications.
- **[Citations & Source Documents](notes/others/Citations.md)** — Research publications and Department of Plant Resources (DPR) references.

---

## 📄 License & Attribution
Prepared for Kathmandu University academic project. When citing this repository or using the dataset, please reference the repository authors and source publications listed in [Citations](notes/others/Citations.md).
