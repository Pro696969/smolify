from flask import Flask, render_template, request
import pyshorteners
import redis
from redis import Sentinel

# redis server
# REDIS_HOST = "172.18.0.2" 
# REDIS_PORT = 6379
# r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

sentinel = Sentinel([('172.18.0.5', 5000), ('172.18.0.6', 5000), ('172.18.0.7', 5000)], socket_timeout=0.1)

master = sentinel.master_for('mymaster',password = "admin", socket_timeout=0.1) # writing
slave = sentinel.slave_for('mymaster',password = "admin", socket_timeout=0.1)   # reading

app=Flask(__name__)

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=="POST":
        url_received=request.form["url"]
        short_url=pyshorteners.Shortener().tinyurl.short(url_received)
        master.set(short_url, url_received)
        print(f"URL: {url_received} has been shortened to {short_url}") # debug print
        return render_template("form.html",new_url=short_url,old_url=url_received)
    else:
        return render_template("form.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=5000) # keep host as 0.0.0.0 so that anyone can access the server (docker)