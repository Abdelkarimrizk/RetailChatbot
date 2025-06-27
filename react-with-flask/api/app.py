from flask import Flask
from agent.general import general_bp

app = Flask(__name__, static_folder="../dist", static_url_path="/")
app.register_blueprint(general_bp)

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run()