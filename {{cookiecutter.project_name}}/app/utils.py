import functools
import random
import requests
import string
import urllib.parse

from flask import redirect, request, session, url_for

## Utility functions

def random_string(n=32):
    return "".join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

def require_login(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if "username" in session:
            return f(*args, **kwargs)
        return redirect(url_for("skel.login", _next=request.path))
    return wrapped

## CSRF

def set_csrf():
    if "csrf" not in session:
        session["csrf"] = random_string()

def require_csrf(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if request.method == "POST" and session["csrf"] != request.form.get("csrf", ""):
            return 403, "Bad CSRF token!"
        return f(*args, **kwargs)
    return wrapped
