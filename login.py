# Logs in to CTFd
import requests
import re

def login(username, password, url, session=requests.session()):
    """Logs in at the specified url with the given username and password, returns a valid, logged in session object"""
    nonce_ex = re.compile(r'.*<input type="hidden" name="nonce" value="([^"]*)">.*', flags=re.DOTALL)
    login_form = session.get(url).text
    nonce = nonce_ex.match(login_form).groups(1)[0]
    payload = {
        'name': username,
        'password': password,
        'nonce': nonce
    }
    csrf_ex = re.compile(r'''.*'csrfNonce': "([^"]*)"*''', flags=re.DOTALL)
    csrf = csrf_ex.match(session.post('https://playcodecup.com/login', data=payload).text).groups(1)[0]
    session.headers.update({'CSRF-Token':csrf})
    return session