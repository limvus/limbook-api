from flask import Blueprint, render_template

from limbook_api.auth import requires_auth

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return render_template('home.html')


@main.route("/secure-route")
@requires_auth('read:secure_route')
def secure():
    return 'Secure location accessed'
