from flask import Blueprint, session, current_app, send_file, render_template, request, send_from_directory
from database import db
from app.models.user import User
import os

bp = Blueprint('idcard', __name__, url_prefix='/idcard')


@bp.route('/showidcard')
def showidcard():
    session_id = str(session['id'])

    #cursor = db.connection.cursor()
    #cursor.execute("SELECT filename FROM accounts WHERE ID = " + session_id)
    #filename = (cursor.fetchone()[0])

    filename = User.query.filter_by(id=session_id).first().filename

    return render_template('idcard.html', filename=filename)


@bp.route('/document')
def getidcard():
    filename = request.args.get('filename')
    return send_file(os.path.join(os.getcwd() + '/' + current_app.config['UPLOAD_FOLDER'], filename))
    #return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
