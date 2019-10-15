from flask import (Flask, render_template)
from flask import request
from flask import jsonify
from flask import send_file
import sentiment as CE
import fancySentiment as FS
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

@app.route('/sentiment/<number>')
def home(number):

    videoId = number
    comments = CE.commentExtract(videoId)
    if comments == "nocomment":
        return "nocomment"
    psent, nsent = CE.sentiment(comments)
    result = FS.fancySentiment(comments, videoId)
    return jsonify(positive = str(psent), negative = str(nsent))

@app.route('/wordcloud/<number>')
def wordclou(number):

    videoId = number
    #comments = CE.commentExtract(videoId)
    #result = FS.fancySentiment(comments)
    #if result == "success":
    #    return send_file("fig.png", mimetype='image/gif')
    name = "/home/faizollah/mysite/wc/"+videoId+".png"
    return send_file(name, mimetype='image/gif')

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)