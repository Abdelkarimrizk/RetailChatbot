from flask import Flask, send_from_directory
from agent.general import general_bp
import os

app = Flask(__name__, static_folder="../dist", static_url_path="/")
app.register_blueprint(general_bp)

@app.route("/")
@app.route("/<path:path>")
def serve_react(path="index.html"):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run()
