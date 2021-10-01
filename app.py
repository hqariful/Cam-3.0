import base64
from io import BytesIO
from flask import Flask, render_template, request, send_from_directory
from matplotlib.figure import Figure
import numpy as np
import os
import radial, fdisp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,"uploads")
np.set_printoptions(suppress=True,precision=3)

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
        rcord = radial.run(value)
        cord = fdisp.run(value)
        fig = Figure()
        ax = fig.subplots(subplot_kw={'projection': 'polar'})
        ax.set_title("Cam profile")
        ax.plot([0,0],[0,value["cam_r"]+value["L"]],color='teal',ls='--')
        ax.plot([0,np.radians(value["profiles"][0]['deg'])],[0,value["cam_r"]+value["L"]],color='teal',ls='--')
        ax.plot([0,np.radians(value["profiles"][1]['deg']+value["profiles"][0]['deg'])],[0,value["cam_r"]+value["L"]],color='teal',ls='--')
        #ax.plot([0,np.radians(value["profiles"][0]['deg']+value["profiles"][1]['deg']+value["profiles"][2]['deg'])],[0,value["cam_r"]+value["L"]],color='blue')
        ax.plot(np.linspace(0, 2*np.pi, 100), np.ones(100)*value['cam_r'], color='r', linestyle='--')
        ax.plot(rcord[0],rcord[1],color='#ff7f0e')
        fig2 = Figure()
        ax2 = fig2.subplots()
        ax2.set_title('Follower Displacement')
        ax2.set_xlabel('angle in degree')
        ax2.set_ylabel('Displacement')
        ax2.axvline(x=value["profiles"][0]['deg'],ymin=0,ymax=value["L"],color='teal',ls='--')
        ax2.axvline(x=value["profiles"][0]['deg']+value["profiles"][1]['deg'],ymin=0,ymax=value["L"],color='teal',ls='--')
        ax2.plot(cord[0],cord[1],color='#ff7f0e')
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
    rcord = np.transpose(radial.run(value))
    cord = np.transpose(fdisp.run(value))
    zero = np.zeros((360,1),dtype=int)
    result = np.append(cord,zero,axis=1)
    uploads = app.config['UPLOAD_FOLDER']
    np.savetxt("./uploads/cam_displacement.csv",result,delimiter=',',fmt='%.3f')
    np.savetxt("./uploads/radial.csv",rcord,delimiter=',',fmt='%.3f')
    return send_from_directory(path="cam_displacement.csv",directory=uploads,as_attachment=True)
    

if __name__ == '__main__':
    app.run(debug=True)
