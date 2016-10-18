from flask import Flask, render_template, request, redirect, session, flash
import pg
import datetime

app = Flask('if_you_care')
db = pg.DB(dbname='volunteer_db')
app.secret_key = 'give_a_little'

@app.route('/')
def home_page():
    return render_template(
        'homepage.html',
        title='If You Care'
    )

@app.route('/org_signup')
def render_org_signup():
    return render_template(
        'org_signup.html',
        title='If You Care'
    )

@app.route('/vol_signup')
def render_vol_signup():
    return render_template(
        'vol_signup.html',
        title='If You Care'
    )

@app.route('/submit_new_vol', methods=['POST'])
def submit_new_user():
    name = request.form.get('name')

    db.insert(
        'volunteer', {
            'name': name
        }
    )
    return redirect('/')

@app.route('/submit_new_org', methods=['POST'])
def submit_new_user():
    name = request.form.get('name')
    description = request.form.get('description')

    db.insert(
        'organization', {
            'name': name,
            'description': description
        }
    )
    return redirect('/')

@app.route('/projects')
def view_projects():
    return render_template(
        'projects.html',
        title='If You Care'
    )

if __name__ == '__main__':
    app.run(debug=True)

#
# Anti script tag function for input areas:
#
# def anti_script(content):
#     edited = content.replace('<script>', '&lt;script&gt;').replace(
#         '</script>', '&lt;/script&gt;')
#     return edited
#
