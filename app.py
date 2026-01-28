from flask import Flask, request, jsonify, redirect
from shortener import URLShortener

app = Flask(__name__)
shortener = URLShortener()


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL missing"}), 400

    original_url = data["url"]
    short_code = shortener.shorten(original_url)

    return jsonify({
        "short_url": f"http://127.0.0.1:8000/{short_code}"
    }), 201


@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    original_url = shortener.expand(short_code)

    if not original_url:
        return jsonify({"error": "Short URL not found"}), 404

    return redirect(original_url, code=302)


@app.route("/stats/<short_code>", methods=["GET"])
def stats(short_code):
    data = shortener.get_stats(short_code)

    if not data:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
