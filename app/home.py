from flask import session, render_template_string, render_template, redirect, url_for, Blueprint, request
from markupsafe import Markup
from app.models.user import User
from app.models.action import Action
from database import db

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/')
def home(msg=None):
    if 'loggedin' in session:

        session_id = session['id']
        #surname = str(request.args.get('surname')) if request.args.get('surname') is not None else session['surname']

        # cursor = db.connection.cursor()
        #
        # cursor.execute("SELECT * FROM operations WHERE idUser ="+str(session_id))
        # operations_list = cursor.fetchall()
        #
        # cursor.execute(" SELECT amount FROM accounts WHERE id = %s" % str(session_id))
        # data = cursor.fetchone()[0]

        #VULNERABLE
        #template = open('app/templates/home.html').read()
        #resp = template.replace('{{ session.surname }}', surname)
        #return render_template_string(resp, balance=data, operationsList=operations_list, msg=msg)
        #
        # return render_template('home.html', balance=data, msg=msg, operationsList=operations_list)

        #SQL_ALCHEMY
        actions = Action.query.filter_by(id_user=session_id).all()
        user = User.query.filter_by(id=session_id).first()

        return render_template('home.html', balance=user.amount, msg=msg, operationsList=actions)

    return redirect(url_for('auth.login'))


@bp.route('/action', methods=['POST'])
def actions():
    if request.method == 'POST':
        causal = request.form["causal"]
        causal = Markup.escape(causal)

        #cursor = db.connection.cursor()
        session_id = str(session['id'])

        #OLD
        #cursor.execute("SELECT password FROM accounts WHERE id ="+session_id)
        #psw = cursor.fetchone()

        #SLQALCHEMY
        current_user = User.query.filter_by(id=session_id).first()
        psw = current_user.password

        if psw == request.form["password"]:
            actual_balance = current_user.amount
            amount = int(Markup.escape(request.form["amount"]))
            if request.form["action"] == 'Withdraw':
                if (actual_balance - amount) >= 0:
                    new_balance = actual_balance - amount
                    current_user.amount = new_balance
                    new_action = Action(session_id, amount, causal, 'withdraw')
                    Action.add(new_action)
                else:
                    msg = "You don't have enough money"
                    return home(msg=msg)
            else:
                new_balance = actual_balance + amount
                User.query.filter_by(id=session_id).first().amount = new_balance
                new_action = Action(session_id, amount, causal, 'deposit')
                Action.add(new_action)


        # if psw:
        #     if psw[0] == request.form["password"]:
        #         cursor.execute("SELECT amount FROM accounts WHERE id = "+session_id)
        #         actual_balance = cursor.fetchone()
        #         amount = int(Markup.escape(request.form["amount"]))
        #         if request.form["action"] == 'Withdraw':
        #             if (int(actual_balance[0]) - int(amount)) >= 0:
        #                 new_balance = int(actual_balance[0]) - amount
        #                 cursor.execute("UPDATE accounts SET amount = %s WHERE id = %s", (new_balance, session_id))
        #                 cursor.execute("INSERT INTO operations (idUser, amount, causal ,operationType) VALUES "
        #                                "(%s, %s, %s, %s)", (session_id, amount, causal, 'withdraw'))
        #                 db.connection.commit()
        #             else:
        #                 msg = "You don't have enough money!"
        #                 return home(msg=msg)
        #         else:
        #             new_balance = int(actual_balance[0]) + int(amount)
        #
        #             #VULNERABLE
        #             cursor.execute("UPDATE accounts SET amount = %s WHERE id = %s", (new_balance, session_id))
        #             cursor.execute("INSERT INTO operations (idUser, amount, causal ,operationType) VALUES "
        #                            "(%s, %s, %s, %s)", (session_id, amount, causal, 'deposit'))
        #             db.connection.commit()

        return home()


# @bp.route('/operations')
# def operations():
#     cursor = db.connect.cursor()
#     cursor.execute("SELECT * FROM operations")
#     result = cursor.fetchone()
#     date = result[2].date()
#     return 'op'
