import base64
from io import BytesIO
from flask import Flask, render_template, request, send_from_directory
from calc import np, Figure, strand, linToRadi
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,"uploads")
np.set_printoptions(suppress=True,precision=3)

value = {
    "L":None,
    "cam_r":None,
    "offset":0,
    "profiles":[
    {
        'type':'outStroke',
        'deg':None,
        'motion':None,
        "pnt":50
    },
    {
        'type':'dwell',
        'deg':None,
        'pnt':10,
        'max':True
    },
    {
        'type':'returnStroke',
        'deg':None,
        'motion':None,
        "pnt":50
    },
    {
        'type':'dwell',
        'deg':None,
        'pnt':10,
        'max':False
    }
    ]
}


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        out = np.deg2rad(int(request.form['outStroke']))
        dw = np.deg2rad(int(request.form['dwell']))
        rtn = np.deg2rad(int(request.form['rtnStroke']))
        value["profiles"][3]['deg'] = 2*np.pi - (out+dw+rtn)
        value["profiles"][2]['deg'] = rtn
        value["profiles"][1]['deg'] = dw
        value["profiles"][0]['deg'] = out
        value["cam_r"] = int(request.form['brad'])
        value["L"] = float(request.form['flw'])
        value['profiles'][0]['motion'] = request.form.get('otype')
        value['profiles'][2]['motion'] = request.form.get('rtype')
        
        lcord = strand(value)
        rcord = linToRadi(value,strand(value))
        fig = Figure()
        ax = fig.subplots()
        ax.set_title("Cam profile")
        ax.set_aspect('equal', adjustable='box')
        #ax.plot([0,np.radians(value["profiles"][0]['deg'])],[0,value["cam_r"]+value["L"]],color='teal',ls='--')
        # ax.plot([0,np.radians(value["profiles"][1]['deg']+value["profiles"][0]['deg'])],[0,value["cam_r"]+value["L"]],color='teal',ls='--')
        # ax.plot([0,np.radians(value["profiles"][0]['deg']+value["profiles"][1]['deg']+value["profiles"][2]['deg'])],[0,value["cam_r"]+value["L"]],color='blue')
        # ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*value['cam_r'], color='r', linestyle='--')
        ax.plot(rcord[0],rcord[1],color='#ff7f0e')
        fig2 = Figure()
        ax2 = fig2.subplots()
        ax2.set_title('Follower Displacement')
        ax2.set_xlabel('angle in degree')
        ax2.set_ylabel('Displacement')
        # ax2.axvline(x=value["profiles"][0]['deg'],ymin=0,ymax=value["L"],color='teal',ls='--')
        # ax2.axvline(x=value["profiles"][0]['deg']+value["profiles"][1]['deg'],ymin=0,ymax=value["L"],color='teal',ls='--')
        ax2.plot(lcord[0],lcord[1],color='#ff7f0e')
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

@app.route('/instruction')
def inst():
    return render_template('instruction.html')

@app.route('/download')
def download():
    result = np.transpose(linToRadi(value,strand(value)))
    uploads = app.config['UPLOAD_FOLDER']
    np.savetxt("./uploads/radial.csv",result,delimiter=',',fmt='%.3f')
    return send_from_directory(path="radial.csv",directory=uploads,as_attachment=True)
    

if __name__ == '__main__':
    app.run(debug=True)
