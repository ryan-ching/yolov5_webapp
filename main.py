from __future__ import print_function
from fileinput import filename
import os
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import parameters
import os.path as osp
import glob
import numpy as np
import torch

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/upload_image/<int:detect_type>', methods=['POST'])
def upload_image(detect_type=0):  # Change Detect Type to input
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        weight = parameters.weight_ccz
        # --Loading model
        if (detect_type == 0):  # If color chips/zoomed in cuts (CHANGE INTEGER LATER)
            weight = parameters.weight_wli
        model = torch.hub.load('ultralytics/yolov5',
                               'custom', path=weight)
        model.conf = parameters.thresh
        model.cpu()  # CPU
        # model.cuda()  # GPU

        prediction = model(filename, size=parameters.imsize)
        prediction.save()
        flash("YOLOv5 Detections Completed")
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)
