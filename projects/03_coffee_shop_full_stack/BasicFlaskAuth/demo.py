from flask import Flask, request, abort


app = Flask(__name__)


@app.route("/header")
def headers():
    if "Authorization" not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    header_part = auth_header.split(" ")

    if len(header_part) != 2 :
        abort(401)
    
    elif header_part[0].lower() != "bearer":
        abort(401)

    print(header_part)
    return "not today !"


if __name__ == "__main__":
    app.run(debug=True)