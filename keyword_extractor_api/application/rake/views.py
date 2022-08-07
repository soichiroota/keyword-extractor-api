import nltk
from flask import Blueprint, jsonify, request
from rake_ja import JapaneseRake, Tokenizer
from rake_nltk import Rake

nltk.download("stopwords")
nltk.download("punkt")
rake_blueprint = Blueprint("rake", __name__)


@rake_blueprint.route("/rake", methods=["post"])
def post():
    json_data = request.get_json()

    if json_data.get("lang") == "ja":
        tok = Tokenizer()
        ja_rake = JapaneseRake()
        tokens = tok.tokenize(json_data["text"])
        ja_rake.extract_keywords_from_text(tokens)
        data = ja_rake.get_ranked_phrases_with_scores()
    else:
        # Uses stopwords for english from NLTK, and all puntuation characters by
        # default
        r = Rake()

        # Extraction given the text.
        r.extract_keywords_from_text(json_data["text"])

        # To get keyword phrases ranked highest to lowest.
        r.get_ranked_phrases()

        # To get keyword phrases ranked highest to lowest with scores.
        data = r.get_ranked_phrases_with_scores()

    response = dict(data=data)
    return jsonify(response)
