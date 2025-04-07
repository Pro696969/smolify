from flask import Flask, render_template, request
import pyshorteners
import os
from redis import Sentinel
import redis.exceptions
import time

master = None

def redis_command(command, *args):
    max_retries = 3
    count = 0
    backoffseconds = 3
    while True:
        try:
            return command(*args)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            count += 1
            if count > max_retries:
                raise e
            print(f"Redis connection error: {e}. Retrying in {backoffseconds} seconds...")
            time.sleep(backoffseconds)

def redis_setup():
    global master
    redis_sentinels = os.environ.get("REDIS_SENTINELS")
    redis_master = os.environ.get("REDIS_MASTER")
    redis_pass = os.environ.get("REDIS_PASSWORD")
    
    sentinels = []
    for s in redis_sentinels.split(","):
        sentinels.append((s.split(":")[0], int(s.split(":")[1])))

    sentinel = Sentinel(sentinels, socket_timeout=0.1, port=5000)
    master = sentinel.master_for(redis_master, password=redis_pass, socket_timeout=0.1)   # writing
    # slave = sentinel.slave_for('mymaster',password = "admin", socket_timeout=0.1)       # reading

app=Flask(__name__)
redis_setup()

@app.route("/",methods=['POST','GET'])
def home():
    if request.method=="POST":
        url_received=request.form["url"]
        short_url=pyshorteners.Shortener().tinyurl.short(url_received)
        # master.set(short_url, url_received)
        redis_command(master.set, short_url, url_received)
        print(f"URL: {url_received} has been shortened to {short_url}") # debug print DONT REMOVE
        return render_template("form.html",new_url=short_url,old_url=url_received)
    else:
        return render_template("form.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=5000) # keep host as 0.0.0.0 so that anyone can access the server (docker)