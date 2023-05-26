from flask import Blueprint, render_template, request, jsonify
from flask_mail import Message
from ..models.api_key import ApiKey
from ..main import app, db, mail
from datetime import datetime, timedelta

api_key_bp = Blueprint('api_key', __name__)

@api_key_bp.route('/request', methods=['POST'])
def request_handler():
    # request details
    request_email = request.form.get('email')
    request_reason = request.form.get('access_reason')

    # user details
    ip_address = request.remote_addr

    # generate key
    try:
        key = ApiKey.generate_key()
        new_key = ApiKey(
            key=key,
            created_by=,
            level=0,
            ignore_limits=0,
            name='',
            description=,
            ip_addresses=ip_address,
            status='active',
            permission='',
            date_expiration=None,
            date_created=datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
            date_activation=(datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %I:%M:%S %p')
        )

        db.session.add(new_key)
        db.session.commit()
    except Exception as e:
        return False

    return True

@api_key_bp.route('/server/send_email', methods=['POST'])
def server_send_email():
    # email details
    recipient = app.DEFAULT_ADMIN_EMAIL
    body = render_template('bunny_email.html',
        title=f'labs.tewi.club - Your access has been approved!',
        header_text=f'Your&nbsp;<a href="https://labs.tewi.club/steam/workshop" style="color: white;" target="_blank">SteamWorkshop</a>&nbsp;access&nbsp;has&nbsp;been&nbsp;approved!',
        body_message=f'Please click the button below to access your API key. The link will expire in 7 days so keep a backup of your API key somewhere private and safe!'
    )

    msg = Message(
        subject="Test send",
        sender='no-reply@tewi.club',
        recipients=[recipient],
        html=body
    )

    mail.send(msg)

    return True