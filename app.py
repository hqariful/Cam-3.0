import base64
from io import BytesIO
from flask import Flask, render_template, request
from matplotlib.figure import Figure
import calculate

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        calculate.profiles[0]['deg'] = int(request.form['outStroke'])
        calculate.profiles[1]['deg'] = int(request.form['dwell'])
        calculate.profiles[2]['deg'] = int(request.form['rtnStroke'])
        calculate.L = float(request.form['flw'])
        calculate.run()
        fig = Figure()
        ax = fig.subplots()
        ax.plot(calculate.cord[0,0:],calculate.cord[1])
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<a href='/'>HOME</a><img src='data:image/png;base64,{data}'/>"
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

"""import base64
from io import BytesIO

from flask import Flask
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route("/")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"""