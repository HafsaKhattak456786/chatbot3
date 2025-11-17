from flask import Flask, request, jsonify, send_file
from gtts import gTTS
from io import BytesIO
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)  # Allow mobile app to call API

# -------------------- Data --------------------

braille_alphabet = {
    "A": {"dots": "dot 1", "pattern": ["●", "○", "○", "○", "○", "○"]},
    "B": {"dots": "dots 1 and 2", "pattern": ["●", "●", "○", "○", "○", "○"]},
    "C": {"dots": "dots 1 and 4", "pattern": ["●", "○", "○", "●", "○", "○"]},
    "D": {"dots": "dots 1, 4 and 5", "pattern": ["●", "○", "○", "●", "●", "○"]},
    "E": {"dots": "dots 1 and 5", "pattern": ["●", "○", "○", "○", "●", "○"]},
    "F": {"dots": "dots 1, 2 and 4", "pattern": ["●", "●", "○", "●", "○", "○"]},
    "G": {"dots": "dots 1, 2, 4 and 5", "pattern": ["●", "●", "○", "●", "●", "○"]},
    "H": {"dots": "dots 1, 2 and 5", "pattern": ["●", "●", "○", "○", "●", "○"]},
    "I": {"dots": "dots 2 and 4", "pattern": ["○", "●", "○", "●", "○", "○"]},
    "J": {"dots": "dots 2, 4 and 5", "pattern": ["○", "●", "○", "●", "●", "○"]},
    "K": {"dots": "dots 1 and 3", "pattern": ["●", "○", "●", "○", "○", "○"]},
    "L": {"dots": "dots 1, 2 and 3", "pattern": ["●", "●", "●", "○", "○", "○"]},
    "M": {"dots": "dots 1, 3 and 4", "pattern": ["●", "○", "●", "●", "○", "○"]},
    "N": {"dots": "dots 1, 3, 4 and 5", "pattern": ["●", "○", "●", "●", "●", "○"]},
    "O": {"dots": "dots 1, 3 and 5", "pattern": ["●", "○", "●", "○", "●", "○"]},
    "P": {"dots": "dots 1, 2, 3 and 4", "pattern": ["●", "●", "●", "●", "○", "○"]},
    "Q": {"dots": "dots 1, 2, 3, 4 and 5", "pattern": ["●", "●", "●", "●", "●", "○"]},
    "R": {"dots": "dots 1, 2, 3 and 5", "pattern": ["●", "●", "●", "○", "●", "○"]},
    "S": {"dots": "dots 2, 3 and 4", "pattern": ["○", "●", "●", "●", "○", "○"]},
    "T": {"dots": "dots 2, 3, 4 and 5", "pattern": ["○", "●", "●", "●", "●", "○"]},
    "U": {"dots": "dots 1, 3 and 6", "pattern": ["●", "○", "●", "○", "○", "●"]},
    "V": {"dots": "dots 1, 2, 3 and 6", "pattern": ["●", "●", "●", "○", "○", "●"]},
    "W": {"dots": "dots 2, 4, 5 and 6", "pattern": ["○", "●", "○", "●", "●", "●"]},
    "X": {"dots": "dots 1, 3, 4 and 6", "pattern": ["●", "○", "●", "●", "○", "●"]},
    "Y": {"dots": "dots 1, 3, 4, 5 and 6", "pattern": ["●", "○", "●", "●", "●", "●"]},
    "Z": {"dots": "dots 1, 3, 5 and 6", "pattern": ["●", "○", "●", "○", "●", "●"]}
}

braille_numbers = {
    "1": {"dots": "same as letter A, dot 1", "pattern": ["●", "○", "○", "○", "○", "○"]},
    "2": {"dots": "same as letter B, dots 1 and 2", "pattern": ["●", "●", "○", "○", "○", "○"]},
    "3": {"dots": "same as letter C, dots 1 and 4", "pattern": ["●", "○", "○", "●", "○", "○"]},
    "4": {"dots": "same as letter D, dots 1, 4 and 5", "pattern": ["●", "○", "○", "●", "●", "○"]},
    "5": {"dots": "same as letter E, dots 1 and 5", "pattern": ["●", "○", "○", "○", "●", "○"]},
    "6": {"dots": "same as letter F, dots 1, 2 and 4", "pattern": ["●", "●", "○", "●", "○", "○"]},
    "7": {"dots": "same as letter G, dots 1, 2, 4 and 5", "pattern": ["●", "●", "○", "●", "●", "○"]},
    "8": {"dots": "same as letter H, dots 1, 2 and 5", "pattern": ["●", "●", "○", "○", "●", "○"]},
    "9": {"dots": "same as letter I, dots 2 and 4", "pattern": ["○", "●", "○", "●", "○", "○"]},
    "0": {"dots": "same as letter J, dots 2, 4 and 5", "pattern": ["○", "●", "○", "●", "●", "○"]}
}

braille_rules = [
    "Rule 1: Each Braille cell has up to 6 dots.",
    "Rule 2: Dots 1, 2, 3 are on the left, and 4, 5, 6 on the right.",
    "Rule 3: Letters and numbers share patterns, but numbers start with a prefix.",
    "Rule 4: Punctuation uses special dot patterns.",
    
]

# -------------------- Endpoints --------------------

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Braille Learning API",
        "endpoints": ["/alphabet/<letter>", "/number/<digit>", "/rules", "/speak"]
    })

@app.route('/alphabet/<letter>')
def get_alphabet(letter):
    letter = letter.upper()
    if letter in braille_alphabet:
        return jsonify({"letter": letter, "dots": braille_alphabet[letter]["dots"]})
    return jsonify({"error": "Letter not found"}), 404

@app.route('/number/<digit>')
def get_number(digit):
    if digit in braille_numbers:
        return jsonify({"number": digit, "dots": braille_numbers[digit]["dots"]})
    return jsonify({"error": "Number not found"}), 404

@app.route('/rules')
def get_rules():
    return jsonify({"rules": braille_rules})

# Optional: server-side voice output
@app.route('/speak', methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Generate speech
    tts = gTTS(text=text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    return send_file(mp3_fp, mimetype="audio/mp3")

# -------------------- Run Server --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
