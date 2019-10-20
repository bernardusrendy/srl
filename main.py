from flask import Blueprint, send_from_directory, render_template, flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from . import db, APP_ROOT
from .models import User, Data
import os

main = Blueprint('main', __name__)

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try:
        lst = os.listdir(path)
        lst.sort()
    except OSError as e:
        print(e.errno)
        print(e.filename)
        print(e.strerror) #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profilelist():
    global listid, listnama, listuser
    listid = []
    listnama = []
    # try :

    rows = Data.query.all()

    # print(rows)
    for row in rows:
        listid.append(row.id)
        listnama.append(row.nama)

    # except :
    # return redirect('/')
    # print(data)
    return render_template('ProfileList.html', len=len(listid), listid=listid, listnama=listnama)

@main.route('/profile/<userid>')
@login_required
def userprofile(userid):
    global nama, gender, usia, asal
    try:
        res =  Data.query.get(userid)
        nama = res.nama
        gender = res.gender
        usia = res.usia
        asal = res.asal
        tree = make_tree(os.path.join(APP_ROOT,'uploads',nama))
        print(tree)
    except:
        return redirect(url_for('main.profilelist'))  # 404 page
    # print(data)
    return render_template('ProfilePage.html', tree=tree, userid=userid, nama=nama, gender=gender, usia=usia, asal=asal)

@main.route('/static/<userid>/<path:filename>')
@login_required
def profilefiles(userid,filename):
    nama =  Data.query.get(userid).nama
    print(nama)
    return send_from_directory(os.path.join('uploads',nama), filename)
