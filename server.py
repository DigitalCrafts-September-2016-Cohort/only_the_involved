from flask import Flask, render_template, request, redirect, session, flash
import pg
import datetime
# import time

app = Flask('if_you_care')
db = pg.DB(dbname='volunteer_db')
app.secret_key = 'give_a_little'

@app.route('/')
def home_page():
    count = session.get('count', 0)
    session['count'] = count + 1

    return render_template(
        'homepage.html',
        title='If You Care'
    )

@app.route('/registration')
def register_user():
    return render_template(
        'register_user.html'
    )

@app.route('/login')
def login_user():
    return render_template(
        'login.html'
    )

@app.route('/vol_login_handler', methods=['POST'])
def vol_login():
    email = request.form.get('email')
    password = request.form.get('password')
    query = db.query('select * from volunteer where email = $1', email)
    results_list = query.namedresult()
    if len(results_list[0]) > 0:
        if results_list[0].password == password:
            session['email'] = email
    else:
        pass
    return redirect('/')

@app.route('/org_login')
def org_login():
    return render_template(
        'org_login.html'
    )

@app.route('/org_login_handler', methods=['POST'])
def org_login_handler():
    email = request.form.get('email')
    password = request.form.get('password')
    query = db.query('select * from organization where email = $1', email)
    results_list = query.namedresult()
    if len(results_list[0]) > 0:
        if results_list[0].password == password:
            session['email'] = email
    else:
        pass
    return redirect('/')

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

@app.route('/logout')
def logout_handler():
    if session['email']:
        del session['email']
    return redirect('/')

@app.route('/submit_new_vol', methods=['POST'])
def submit_new_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    db.insert(
        'volunteer', {
            'name': name,
            'password': password,
            'email': email
        }
    )
    session['email'] = email
    return redirect('/')

@app.route('/submit_new_org', methods=['POST'])
def submit_new_org():
    name = request.form.get('name')
    description = request.form.get('description')
    email = request.form.get('email')
    password = request.form.get('password')

    db.insert(
        'organization', {
            'name': name,
            'description': description,
            'email': email,
            'password': password
        }
    )
    session['email'] = email
    return redirect('/')

@app.route('/org_profile')
def view_org_profile():
    query = db.query('select * from organization where email = $1', session['email'])
    org_info = query.namedresult()[0]

    return render_template(
        'org_profile.html',
        org_info = org_info
    )

@app.route('/create_new_event')
def create_new_event():

    return render_template(
        'create_new_event.html'
    )

@app.route('/submit_new_event', methods=['POST'])
def submit_new_event():
    query = db.query('select * from organization where email = $1', session['email']).namedresult()[0]
    org_id = query.id
    org_name = query.name

    name = request.form.get('name')
    start_date = request.form.get('date')
    description = request.form.get('description')
    db.insert(
        'project', {
            'name': name,
            'project_description': description,
            'start_time': "",
            'organization_id': org_id,
            'start_date': start_date
        }
    )
    return redirect('/projects')

@app.route('/projects')
def view_projects():
    query = db.query('select organization.name as Organization, project.name as Project, project.project_description as Description, project.start_date as Time from project, organization where project.organization_id = organization.id')
    results_list = query.namedresult()

    return render_template(
        'projects.html',
        title='If You Care',
        entry_list= results_list
    )

@app.route('/search', methods=['POST'])
def search_bar():
    date = request.form.get('date')
    query = db.query('select organization.name as Organization, project.name as Project, project.project_description as Description, project.start_date as Time from project, organization where project.organization_id = organization.id and start_date = $1', date)
    results_list = query.namedresult()

    print "DATE: %r" % date
    return render_template(
        'projects.html',
        entry_list = results_list
    )


@app.route('/register_project')
def register():

    return render_template(
        'register_project.html',
        title='My Projects'
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
