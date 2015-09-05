from flask import Flask, send_from_directory, current_app

app = Flask(__name__)


@app.route("/")
def main():
    return send_from_directory(current_app.static_folder, "index.html")

if __name__ == "__main__":
    app.run()
