from products import *
from shops import *
from orders import *


@app.route('/')
def index():
    return render_template("main_page.html")


if __name__ == "__main__":
    app.run(debug=True)
