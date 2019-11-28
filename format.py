import logging
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def default_route():
    app.logger.debug("this is a DEBUG message")
    app.logger.info("this is an INFO message")
    app.logger.warning("this is a WARNING message")
    app.logger.error("this is an ERROR message")
    app.logger.critical("this is a CRITICAL message")
    return jsonify("hello world")

if __name__ == "__main__":
   app.logger.setLevel(logging.INFO)
   app.run(host="0.0.0.0", port=8000, debug=True)