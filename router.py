from flask import Blueprint
from flask import render_template as renderTemplate
from flask import redirect
from flask import request
from flask import session
from cryptography.fernet import Fernet
from uuid import uuid4

from controllers.email import resetPasswordEmail

router = Blueprint("router", __name__)

OUTSTANDINGSECRETS = []
KEY = b'jIQ2n_UnV_YJCyUZoVhwFALM-SgkLzdnj4nCXZcw-6k='
CIPHER_SUITE = Fernet(KEY)

@router.route('/puppy')
def puppy():
	return "puppies"

@router.route('/')
def index():
	return renderTemplate(
		'login.html',
		title='Root Access'
	)

@router.route('/logout')
def logout():
	session.clear()
	print('Session destroyed')
	return redirect('/')

@router.route('/home')
def renderHome():
	if session['authorized']:
		return renderTemplate(
		'home.html'
	)
	else:
		redirect('/')

@router.route('/auth', methods=['POST'])
def authUser():
	global CIPHER_SUITE
	email = request.form.get('email')
	password = request.form.get('pass')
	encryptedPass = CIPHER_SUITE.encrypt(bytes(password, encoding='utf-8'))
	authorized = True
	if authorized:
		session['authorized'] = True
		return redirect('/home')
	return redirect('/')

@router.route('/plantParameters', methods=["GET"])
def getPlantParameters():
	if(session['authorized']):
		return renderTemplate(
			'plantParameters.html'
		)
	return redirect('/')

@router.route('/plantParameters', methods=["POST"])
def postPlantParameters():
	if(session['authorized']):
		moistureMin = request.form.get('moistureMin')
		moistureMax = request.form.get('moistureMax')
		lightMin = request.form.get('lightMin')
		return redirect('/home')
	return redirect('/')

@router.route('/resetPassword', methods=['GET'])
def getResetPassword():
	return renderTemplate(
		'resetPassword.html'
	)

@router.route('/resetPassword', methods=['POST'])
def postResetPassword():
	global OUTSTANDINGSECRETS
	email = request.form.get('email').strip()
	if(email != ''):
		secret = uuid4()
		for element in OUTSTANDINGSECRETS:
			if email in element:
				OUTSTANDINGSECRETS.remove(element)
				break
		myDict = {email: secret}
		OUTSTANDINGSECRETS.append(myDict)
		resetPasswordEmail(email, secret)
		return redirect('/')
	return redirect('/resetPassword')

@router.route('/changePassword', methods=["GET"])
def getChangePassword():
	global OUTSTANDINGSECRETS
	email = request.args.get('email')
	secret = request.args.get('ref')
	myDict = {email: secret}
	if myDict in OUTSTANDINGSECRETS:
		session['email'] = email
		return renderTemplate('changePassword.html')

@router.route('/changePassword', methods=["POST"])
def postResetPassword():
	global OUTSTANDINGSECRETS, CIPHER_SUITE
	newPassword = request.form.get('pass')
	encryptedPass = CIPHER_SUITE.encrypt(bytes(newPassword, encoding='utf-8'))
	# Do database stuff
	return redirect('/')