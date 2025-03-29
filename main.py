from flask import Flask, render_template, request
import pyshorteners
import redis

# redis server
REDIS_HOST = "localhost" 
REDIS_PORT = 6969   
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=="POST":
        url_received=request.form["url"]
        short_url=pyshorteners.Shortener().tinyurl.short(url_received)
        r.set(short_url, url_received)
        print(f"URL: {url_received} has been shortened to {short_url}") # debug print
        return render_template("form.html",new_url=short_url,old_url=url_received)
    else:
        return render_template("form.html")

if __name__=="__main__":
    app.run(debug=True, port=5000)