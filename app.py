from shops import *
from products import *


@app.route('/')
def index():
    return render_template("main_page.html")


if __name__ == "__main__":
    app.run(debug=True)
