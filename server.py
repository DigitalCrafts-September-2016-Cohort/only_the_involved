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

@app.route('/login_handler')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    query = db.query('select * from volunteer where email = $1', email)
    results_list = namedresult()
    if len(results_list[0]) > 0:
        if results_list[0].password == password:
            session['email']
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
def submit_new_org():
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
