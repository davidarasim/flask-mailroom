import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import db, Donor, Donation 

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create_donation():
    # If the user is attempting to create a donation (method is POST)
    #    Find donor from database that matches the donor provided in form
    #    If you find donor and the donation amount entered is an integer:
    #        Create the new donation record for the donor
    #        Redirect the user to the list of all donations
    #    Else:
    #        Render the create.jinja2 template and include an error message 
    # Else the user is just trying to view the create form
    #    so render the create.jinja2 template

    if request.method == 'POST':
        try:
            this_donor = Donor.select().where(Donor.name == request.form['name']).get()
        except:
            return render_template('create.jinja2', error='Incorrect donor name.')

        if this_donor:
            try:
                this_value = int(request.form['donation'])
            except ValueError:
                return render_template('create.jinja2', error='Incorrect donation amount (expecting integer).')

            Donation(donor=this_donor, value=this_value).save()
            return redirect(url_for('all'))

        return render_template('create.jinja2', error='Incorrect donor name.')

    else:
        return render_template('create.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

