import os
from flask import Flask, render_template, send_from_directory, url_for, request, redirect
import passcheck
import csv

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/check_password', methods=['POST', 'GET'])
def check_password():
    if request.method == 'POST':
        try:
            password = request.form['password']
            count = passcheck.pwned_api_check(password)
        except:
            return 'something failed'
        if count:
            return f'{password} was found {count} times... You should probably change your password.'
        else:
            return f"{password} was NOT found. OK to proceed."
    else:
        return 'Something did not work'


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'Did not save to database'
    else:
        return 'Something went wrong. Try again.'


def write_to_csv(data):
    with open('./contacts/contacts.csv', newline='', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
