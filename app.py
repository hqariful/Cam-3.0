import base64
from io import BytesIO
from flask import Flask, render_template, request
from matplotlib.figure import Figure
import radial, fdisp, value


app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        value.profiles[0]['deg'] = int(request.form['outStroke'])
        value.profiles[1]['deg'] = int(request.form['dwell'])
        value.profiles[2]['deg'] = int(request.form['rtnStroke'])
        value.L = float(request.form['flw'])
        radial.run()
        fdisp.run()
        fig = Figure()
        ax = fig.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(radial.cord[0,0:],radial.cord[1])
        fig2 = Figure()
        ax2 = fig2.subplots()
        ax2.plot(fdisp.cord[0,0:],fdisp.cord[1])
        # Save it to a temporary buffer.
        buf = BytesIO()
        buf2 = BytesIO()
        fig.savefig(buf, format="png")
        fig2.savefig(buf2, format="png")
        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        data2 = base64.b64encode(buf2.getbuffer()).decode("ascii")
        return render_template('view.html',img=f"data:image/png;base64,{data}",img2=f"data:image/png;base64,{data2}")
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