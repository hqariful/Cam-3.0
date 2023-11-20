import base64
from io import BytesIO
from flask import Flask, render_template, request, send_from_directory
import numpy as np
import main
from calculate import linear_tragectory as LT
from plotter import disp_diag, radial_plot
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path,"uploads")
np.set_printoptions(suppress=True,precision=3)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        max_disp = int(request.form['flw'])
        dwell = (int(request.form['dwell']))
        outStroke_angle = (int(request.form['outStroke']))
        returnStroke_angle = (int(request.form['rtnStroke']))
        rF = int(request.form["offset"]) # Offset Distance
        rB = int(request.form['brad']) # Base Circle

        if request.form.get('otype') == 'const_v':
            outStroke = LT.Constant_Velocity(outStroke_angle,max_disp)
        elif request.form.get('otype') == 'const_a':
            outStroke = LT.Constant_Acceleration(outStroke_angle,max_disp)
        elif request.form.get('otype') == 'shm':
            outStroke = LT.Simple_Harmonic(outStroke_angle,max_disp)
        elif request.form.get('otype') == 'cyc':
            outStroke = LT.Cycloidal(outStroke_angle,max_disp)

        if request.form.get('rtype') == 'const_v':
            returnStroke = LT.Constant_Velocity(returnStroke_angle,max_disp)
        elif request.form.get('rtype') == 'const_a':
            returnStroke = LT.Constant_Acceleration(returnStroke_angle,max_disp)
        elif request.form.get('rtype') == 'shm':
            returnStroke = LT.Simple_Harmonic(returnStroke_angle,max_disp)
        elif request.form.get('rtype') == 'cyc':
            returnStroke = LT.Cycloidal(returnStroke_angle,max_disp)
        
        theta, r = main.main(outStroke,dwell,returnStroke, max_disp)
        fig1 = disp_diag(theta,r)
        fig2 = radial_plot(theta,r,rB,rF)
        
        # Save it to a temporary buffer.
        buf = BytesIO()
        buf2 = BytesIO()
        fig1.savefig(buf, format="png")
        fig2.savefig(buf2, format="png")
        result = (theta,r)
        np.savetxt("./uploads/radial.csv",result,delimiter=',',fmt='%.3f')
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
    uploads = app.config['UPLOAD_FOLDER']
    return send_from_directory(path="radial.csv",directory=uploads,as_attachment=True)
    

if __name__ == '__main__':
    app.run(debug=True)
