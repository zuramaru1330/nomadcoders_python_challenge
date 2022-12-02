from flask import Flask, render_template, request, redirect, send_file
from extractors.remoteok import extract_remote_ok_jobs
from extractors.we_work_remotely import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")

cache_db = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in cache_db:
        jobs = cache_db[keyword]
    else:
        remoteOk = extract_remote_ok_jobs(keyword)
        weWorkRemotely = extract_wwr_jobs(keyword)
        jobs = remoteOk + weWorkRemotely
        cache_db[keyword] = jobs

    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
     return redirect("/")
    if keyword not in cache_db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, cache_db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")