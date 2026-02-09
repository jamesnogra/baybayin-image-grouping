from flask import Flask, render_template, jsonify, request
import os
import shutil

PORT = 8885

app = Flask(__name__)

IMAGE_FOLDER = os.path.join(app.root_path, 'static/temp_images')
ALLOWED_EXT = {'.jpg', '.jpeg', '.png'}
SYLLABLES = [
    'a', 'e_i', 'o_u',
    'ba', 'be_bi', 'bo_bu', 'b',
    'ka', 'ke_ki', 'ko_ku', 'k',
    'da', 'de_di', 'do_du', 'd',
    'ga', 'ge_gi', 'go_gu', 'g',
    'ha', 'he_hi', 'ho_hu', 'h',
    'la', 'le_li', 'lo_lu', 'l',
    'ma', 'me_mi', 'mo_mu', 'm',
    'na', 'ne_ni', 'no_nu', 'n',
    'nga', 'nge_ngi', 'ngo_ngu', 'ng',
    'pa', 'pe_pi', 'po_pu', 'p',
    'sa', 'se_si', 'so_su', 's',
    'ta', 'te_ti', 'to_tu', 't',
    'wa', 'we_wi', 'wo_wu', 'w',
    'ya', 'ye_yi', 'yo_yu', 'y'
]

@app.route("/")
def index():
    images = []
    if os.path.exists(IMAGE_FOLDER):
        for filename in os.listdir(IMAGE_FOLDER):
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_EXT:
                images.append(filename)
    return render_template("index.html", images=images, syllables=SYLLABLES)

@app.route('/move-images', methods=['POST'])
def move_images():
    data = request.get_json()
    selected_items = data.get('selected_images', [])
    destination = data.get('destination', '')

    if not selected_items or not destination:
        return {"status": "error", "message": "Missing data"}, 400

    # Define your base paths
    # Using absolute paths is safer to avoid "file not found" errors
    base_dir = os.path.abspath(os.path.dirname(__file__))
    source_folder = os.path.join(base_dir, 'static', 'temp_images')
    target_folder = os.path.join(base_dir, 'static', 'grouped', destination)

    # 1. Create the target directory if it doesn't exist
    # exist_ok=True prevents an error if the folder already exists
    os.makedirs(target_folder, exist_ok=True)

    moved_count = 0
    for img_name in selected_items:
        source_path = os.path.join(source_folder, img_name)
        target_path = os.path.join(target_folder, img_name)

        # 2. Check if file exists before moving to prevent crashes
        if os.path.exists(source_path):
            shutil.move(source_path, target_path)
            moved_count += 1

    return {
        "status": "success",
        "message": f"Successfully moved {moved_count} images to {destination}",
        "moved_count": moved_count
    }, 200

if __name__ == "__main__":
    app.run(debug=True, port=PORT, host="0.0.0.0")