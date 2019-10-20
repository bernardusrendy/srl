import os, random, uuid, pathlib
from flask import Blueprint, Flask, flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import User, Data
from . import UPLOAD_FOLDER,db

operation = Blueprint('operation', __name__)

class sessiondata():
    ext = None
    session_id = None

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','mp4','wav'}
sesdata = sessiondata()

def cekNomor(nama, ext):
    nomor = 1
    path = pathlib.Path(os.path.join(
        UPLOAD_FOLDER, nama, str(nomor) + '.' + ext))
    while path.exists():
        nomor = nomor + 1
        path = pathlib.Path(os.path.join(
            UPLOAD_FOLDER, nama, str(nomor) + '.' + ext))
    return nomor


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@operation.route('/analyze', methods=['POST','GET'])
@login_required
def analyze():
    sesdata.session_id = str(uuid.uuid4())
    print(sesdata.session_id)

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        sesdata.ext = file.filename.rsplit('.', 1)[1].lower()
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("temp" + sesdata.session_id + "." + sesdata.ext)
            file.save(os.path.join(
                UPLOAD_FOLDER, filename))
            return redirect(url_for('operation.newprofile')) #redirect to process page
        else:
            flash('Incorrect File Extension')
            return redirect(url_for('operation.analyze')) #reload the page

    return render_template('analyze.html')

@operation.route('/analyze', methods=['POST', 'GET'])
@login_required
def process():
    return render_template('analyze.html')

@operation.route('/train', methods=['POST','GET'])
@login_required
def traindata():
    sesdata.session_id = str(uuid.uuid4())
    print(sesdata.session_id)

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        sesdata.ext = file.filename.rsplit('.', 1)[1].lower()
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("temp" + sesdata.session_id + "." + sesdata.ext)
            file.save(os.path.join(
                UPLOAD_FOLDER, filename))
            return redirect(url_for('operation.newprofile')) #redirect to process page
        else:
            flash('Ekstensi File Tidak Cocok')
            return redirect(url_for('operation.traindata')) #reload the page

    return render_template('train.html')

@operation.route('/newprofile',  methods=['GET', 'POST'])
@login_required
def newprofile():
    if request.method == 'POST':
        global nama, gender, usia, asal
        if request.form['action'] == 'Submit':
            try:
                nama = request.form['1.nama']
                gender = request.form['2.gender']
                usia = request.form['3.usia']
                asal = request.form['4.daerah']
            except:
                pass
            pathnama = pathlib.Path(os.path.join(UPLOAD_FOLDER, nama))

            # # Check if name exists
            nama_pernah = Data.query.filter_by(nama=nama).first() # if this returns a user, then the email already exists in database

            # Check Missing Items
            if nama == "" or not nama_pernah:
                req = request.form
                missing = list()

                for k, v in req.items():
                    print(k, v)
                    if v == "":
                        missing.append(k)

                if missing:
                    flash(f"Missing fields for {', '.join(missing)}")
                    return redirect(request.url)

            nomor = str(cekNomor(nama, sesdata.ext))

            if not pathnama.exists():
                new_profile = Data(nama=nama, gender=gender, usia=usia, asal=asal)

                db.session.add(new_profile)
                db.session.commit()
                os.makedirs(pathnama)

                print('data inserted')

            os.rename(os.path.join(UPLOAD_FOLDER, "temp" + sesdata.session_id + "." + sesdata.ext), os.path.join(UPLOAD_FOLDER, nama, nomor + '.' + sesdata.ext))

            flash("Data Inserted")
            return redirect(url_for('main.profilelist'))

        elif request.form['action'] == 'Cancel':
            flash("Data Is Not Inserted")
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, "temp" + sesdata.session_id + "." + sesdata.ext))
                return redirect(url_for('main.index'))
            except:
                return redirect(url_for('main.index'))

    return render_template('newprofile.html')
