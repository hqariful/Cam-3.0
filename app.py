import base64
from io import BytesIO
from flask import Flask, render_template, request
from matplotlib.figure import Figure
import radial, fdisp

app = Flask(__name__)

value = {
    "L":None,
    "cam_r":None,
    "pnt":360,
    "offset":0,
    "profiles":[
    {
        'type':'outStroke',
        'deg':None,
        'motion':None
    },
    {
        'type':'dwell',
        'deg':None
    },
    {
        'type':'returnStroke',
        'deg':None,
        'motion':None
    }
    ]
}

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        value["profiles"][0]['deg'] = int(request.form['outStroke'])
        value["profiles"][1]['deg'] = int(request.form['dwell'])
        value["profiles"][2]['deg'] = int(request.form['rtnStroke'])
        value["cam_r"] = int(request.form['brad'])
        value["L"] = float(request.form['flw'])
        value['profiles'][0]['motion'] = request.form.get('otype')
        value['profiles'][2]['motion'] = request.form.get('rtype')
        print(value)
        xr, yr = radial.run(value)
        x, y = fdisp.run(value)
        fig = Figure()
        ax = fig.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(xr,yr)
        fig2 = Figure()
        ax2 = fig2.subplots()
        ax2.plot(x,y)
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

@app.route('/about')
def about():
    return render_template('about.html')

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