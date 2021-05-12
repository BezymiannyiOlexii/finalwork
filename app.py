from shops import *
from products import *


@app.route('/')
def index():
    try:
        return f'ну че погнали ебана в рот!{request.args["id"]}'
    except:
        return redirect("/?id=nrejnoren")


if __name__ == "__main__":
    app.run(debug=True)
