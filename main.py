import os
import time
import base64
import logging
import requests
from flask import Flask, request, render_template, session, redirect, abort, flash, jsonify

app = Flask(__name__)   # create our flask app
app.secret_key = os.environ.get('SECRET_KEY')

def twitter_connect():
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print("Twitter Response: ", auth_resp.status_code)

    auth_resp.json().keys()
    print("Response Keys: ", auth_resp.json().keys())

    access_token = auth_resp.json()['access_token']
    print("Access Token: ", access_token)

    # post request

    myobj = {'somekey': 'somevalue'}

    upload_resource_url = 'https://upload.twitter.com/1.1/media/upload.json'

    x = requests.post(upload_resource_url, data = myobj)

    print(x.text)

    return access_token

def search_request(access_token, base_url):
    # search request

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }

    search_params = {
        'q': 'General Election',
        'result_type': 'recent',
        'count': 2
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)

    search_resp.status_code

    tweet_data = search_resp.json()

    for x in tweet_data['statuses']:
        print(x['text'] + '\n')


# def twitter_query():



@app.route("/")
def home():
    return render_template("home.html")
    
if __name__ == "__main__":
    
    base_url = 'https://api.twitter.com/'

    access_token = twitter_connect()
    search_request(access_token, base_url)
    app.run(debug=True)


# from instagram.client import InstagramAPI

# # configure Instagram API
# instaConfig = {
# 	'client_id':os.environ.get(''),
# 	'client_secret':os.environ.get('CLIENT_SECRET'),
# 	'redirect_uri' : os.environ.get('REDIRECT_URI')
# }
# api = InstagramAPI(**instaConfig)

# @app.route('/')
# def user_photos():

# 	# if instagram info is in session variables, then display user photos
# 	if 'instagram_access_token' in session and 'instagram_user' in session:
# 		userAPI = InstagramAPI(access_token=session['instagram_access_token'])
# 		recent_media, next = userAPI.user_recent_media(user_id=session['instagram_user'].get('id'),count=25)

# 		templateData = {
# 			'size' : request.args.get('size','thumb'),
# 			'media' : recent_media
# 		}

# 		return render_template('display.html', **templateData)
		

# 	else:

# 		return redirect('/connect')

# # Redirect users to Instagram for login
# @app.route('/connect')
# def main():

# 	url = api.get_authorize_url(scope=["likes","comments"])
# 	return redirect(url)

# # Instagram will redirect users back to this route after successfully logging in
# @app.route('/instagram_callback')
# def instagram_callback():
    
#     app.getLogger()

#     code = request.args.get('code')

#     if code:

# 		access_token, user = api.exchange_code_for_access_token(code)
# 		if not access_token:
# 			return 'Could not get access token'

# 		app.logger.debug('got an access token')
# 		app.logger.debug(access_token)

# 		# Sessions are used to keep this data 
# 		session['instagram_access_token'] = access_token
# 		session['instagram_user'] = user

# 		return redirect('/') # redirect back to main page
		
# 	else:
# 		return "Uhoh no code provided"
	
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

# # This is a jinja custom filter
# @app.template_filter('strftime')
# def _jinja2_filter_datetime(date, fmt=None):
#     pyDate = time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y') # convert instagram date string into python date/time
#     return time.strftime('%Y-%m-%d %h:%M:%S', pyDate) # return the formatted date.