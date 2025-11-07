# #!/usr/bin/python3
# import numpy as np
# import os
# import sys
# from PIL import Image
# from feature_extractor import FeatureExtractor
# from datetime import datetime
# from flask import Flask, request, render_template, abort
# from pathlib import Path

# app = Flask(__name__)
# path = os.path.realpath(os.path.dirname(sys.argv[0]))
# # Read image features
# fe = FeatureExtractor()
# features = []
# img_paths = []
# file_name=[]

# # Define allowed image formats
# ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

# for feature_path in Path("./static/feature").glob("*.npy"):
#     features.append(np.load(feature_path))
#     img_paths.append(Path("./static/Images") / (feature_path.stem + ".jpg"))
#     file_name.append(Path(feature_path.stem))
#     # # Look for corresponding images with the same stem (base name) in the allowed formats
#     # base_name = feature_path.stem  # This gets the base name of the feature file (without extension)
    
#     # # Check for matching image file extensions
#     # for ext in ALLOWED_EXTENSIONS:
#     #     img_path = Path("./static/Images") / (base_name + "." + ext)
#     #     if img_path.exists():  # If the image file exists, add it to the img_paths list
#     #         img_paths.append(img_path)
#     #         file_name.append(Path(base_name))  # You can still store the base name for reference
#     #         break  # Stop after finding the first match (since we expect one image per feature file)

# features = np.array(features)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         file = request.files['query_img']

#         # Save query image
#         img = Image.open(file.stream)  # PIL image
#         uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
#         img.save(uploaded_img_path)

#         # Run search
#         query = fe.extract(img)
#         dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
#         ids = np.argsort(dists)[:100]  # Top 30 results
#         scores = [(dists[id], img_paths[id],file_name[id]) for id in ids]

#         return render_template('index.html',
#                                query_path=uploaded_img_path,
#                                scores=scores)
#     else:
#         return render_template('index.html')


# @app.before_request
# def limit_remote_addr():
#     allowed_ip = "192.168.11.126"
#     if request.remote_addr != allowed_ip:
#         abort(403)  # Forbidden

# @app.before_request
# def limit_remote_addr():
#     allowed_ip = "192.168.11.126"
#     if request.remote_addr != allowed_ip:
#         abort(403)  # Forbidden


# if __name__=="__main__":
#     app.run(host="192.168.11.78", port=5001, debug=True)

#!/usr/bin/python3
import os
import sys
import numpy as np
from PIL import Image
from datetime import datetime
from pathlib import Path
from flask import Flask, request, render_template, abort
from feature_extractor import FeatureExtractor

# -------------------- Flask Setup --------------------
app = Flask(__name__)
path = os.path.realpath(os.path.dirname(sys.argv[0]))

# -------------------- Initialization --------------------
fe = FeatureExtractor()
features = []
img_paths = []
file_names = []

# Allowed image extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

# -------------------- Load Precomputed Features --------------------
print("🔍 Loading precomputed features...")

feature_dir = Path("./static/feature")
image_dir = Path("./static/Images")

for feature_path in feature_dir.glob("*.npy"):
    base_name = feature_path.stem  # e.g. image123

    # Find corresponding image with supported extension
    image_path = None
    for ext in ALLOWED_EXTENSIONS:
        candidate = image_dir / f"{base_name}.{ext}"
        if candidate.exists():
            image_path = candidate
            break

    if image_path:
        features.append(np.load(feature_path))
        img_paths.append(image_path)
        file_names.append(base_name)
    else:
        print(f"⚠️ No image found for feature: {base_name}")

features = np.array(features)
print(f"✅ Loaded {len(features)} features successfully.")

# -------------------- IP Restriction --------------------
@app.before_request
def restrict_ip_access():
    # allowed_ip = "192.168.11.126"
    remote_ip = request.remote_addr

    # if remote_ip != allowed_ip:
    #     print(f"🚫 Access denied for IP: {remote_ip}")
    #     abort(403)  # Forbidden
    allowed_ips = {"192.168.11.126", "192.168.11.78"}
    if remote_ip not in allowed_ips:
        abort(403)


# -------------------- Routes --------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('query_img')
        if not file:
            return render_template('index.html', error="No file uploaded")

        # Save uploaded image
        img = Image.open(file.stream)
        timestamp = datetime.now().isoformat().replace(":", ".")
        uploaded_img_path = f"static/uploaded/{timestamp}_{file.filename}"
        img.save(uploaded_img_path)

        # Run feature extraction & search
        query_vector = fe.extract(img)
        dists = np.linalg.norm(features - query_vector, axis=1)
        ids = np.argsort(dists)[:100]  # Top 100 matches

        results = [
            (float(dists[i]), str(img_paths[i]), file_names[i]) for i in ids
        ]

        return render_template('index.html', query_path=uploaded_img_path, scores=results)

    # GET method
    return render_template('index.html')

# -------------------- Run App --------------------
if __name__ == "__main__":
    print("🚀 Flask server running on http://192.168.11.78:5001")
    app.run(host="192.168.11.78", port=5001, debug=True)
