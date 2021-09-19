from flask import Flask, render_template, url_for, make_response, redirect, request
import requests, json, validators, datetime

app = Flask(
    __name__,
    root_path=None,
    template_folder= 'html/',
    static_folder= '/'
)

# GLOBALS
TITLE = "URLs"

######################################## none/404
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('home'))

######################################## HOME
@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        data = f"""
            <form>
              <input type="text" name="URL" placeholder="http://example.com">
              <input type="submit" name="check" value="CHECK">
            </form>
            <section for="result"></section>
            <a href="historyBook">History</a>
        """
        return render_template("index.html", **globals(), **locals())

    elif request.method == "POST":

        # REQUEST VALIDATING
        if request.get_json()["for"] != "URLcheck":
            return make_response(json.dumps({"PythonResponse": "BAD_REQUEST"}), 400)

        # URL VALIDATING
        if not validators.url(request.get_json()["URL"]):
            return make_response(json.dumps({"PythonResponse": "OK", "HTTPErrorResponse": "Invalid URL"}), 200)

        # GETTING HEADERS
        data = None
        try:
            getHeaders = requests.head(request.get_json()["URL"])
        except requests.exceptions.HTTPError:
            data = {"PythonResponse": "OK", "HTTPErrorResponse": "HTTP Error"}
        except requests.exceptions.ConnectionError:
            data = {"PythonResponse": "OK", "HTTPErrorResponse": "Connection Error. This site can’t be reached"}
        else:
            data = {
                            "PythonResponse": "OK",
                            "data": {
                                "url": getHeaders.url,
                                "status": getHeaders.status_code,
                                "statusDescription": requests.status_codes._codes[getHeaders.status_code][0].replace("_", " "),
                                "responseTime": getHeaders.elapsed.total_seconds()
                            }
                        }

            # HISTORY WRITING
            with open("history/history.txt", "a") as f:
                f.write(f'{getHeaders.status_code}|{requests.status_codes._codes[getHeaders.status_code][0].replace("_", " ")}|{getHeaders.url}|{getHeaders.elapsed.total_seconds()}|{datetime.datetime.now()}\n')

        return make_response(json.dumps(data), 200)

@app.route("/historyBook", methods=["GET"])
def historyBook():
    history = ""
    with open("history/history.txt") as f:
        for line in f:
            line = line.split("|")
            history += f"""
                <tr>
                  <td>{line[0]}</td>
                  <td>{line[1]}</td>
                  <td>{line[2]}</td>
                  <td>{line[3]}</td>
                  <td>{line[4]}</td>
                </tr>
            """
    data = f"""
            <a href="home">Home</a>
            <section>
              <h1>History</h1>
              <table>
                <tr>
                  <th>STATUS</th>
                  <th>STATUS DESCRIPTION</th>
                  <th>URL</th>
                  <th>RESPONSE TIME</th>
                  <th>DATE</th>
                </tr>
                {history}
              </table>
            </section>
    """
    return render_template("index.html", **globals(), **locals())

# Flask Run
if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True, threaded=True)
