from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, render_template, request, redirect, session, flash
import pg
import datetime
import os
# import time

db = pg.DB(
    dbname=os.environ.get('PG_DBNAME_VOLUNTEER_DB'),
    host=os.environ.get('PG_HOST'),
    user=os.environ.get('PG_USERNAME'),
    passwd=os.environ.get('PG_PASSWORD')
)

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask('if_you_care', template_folder=tmp_dir)

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

@app.route('/new_login')
def new_login():
    if session['vol_email']:
        del session['vol_email']
    elif session['org_email']:
        del session['org_email']
    return redirect('/login')

@app.route('/vol_login_handler', methods=['POST'])
def vol_login():
    email = request.form.get('email')
    password = request.form.get('password')
    query = db.query('select * from volunteer where email = $1', email)
    results_list = query.namedresult()
    if results_list != []:
        if results_list[0].password == password:
            session['vol_email'] = email
            return redirect('/vol_profile')
    else:
        pass
    return redirect('/login')

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
    if results_list != []:
        if results_list[0].password == password:
            session['org_email'] = email
            return redirect('/org_profile')
    else:
        return redirect('/org_login')

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

@app.route('/vol_logout')
def vol_logout_handler():
    if session['vol_email']:
        del session['vol_email']
    return redirect('/')

@app.route('/org_logout')
def org_logout_handler():
    if session['org_email']:
        del session['org_email']
    return redirect('/')

@app.route('/submit_new_vol', methods=['POST'])
def submit_new_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    query = db.query('select * from volunteer where email =$1', email)
    vol_info = query.namedresult()

    if vol_info == []:
        db.insert(
            'volunteer', {
                'name': name,
                'password': password,
                'email': email,
                'age': age
            }
        )
        session['vol_email'] = email
        return redirect('/vol_profile')
    else:
        return redirect('/login')


@app.route('/submit_new_org', methods=['POST'])
def submit_new_org():
    name = request.form.get('name')
    description = request.form.get('description')
    email = request.form.get('email')
    password = request.form.get('password')
    query = db.query('select * from organization where email =$1', email)
    org_info = query.namedresult()

    if org_info == []:
        db.insert(
            'organization', {
                'name': name,
                'description': description,
                'password': password,
                'email': email
            }
        )
        session['org_email'] = email
        return redirect('/org_profile')
    else:
        return redirect('/org_login')


@app.route('/org_profile')
def view_org_profile():
    query = db.query('select organization.name as Organization, project.id as project_id, organization.id as org_id, project.name as Project, project.project_description as Description, project.start_date as Date, project.start_time as Time, project.vol_needed, project.vol_total from project, organization where project.organization_id = organization.id and organization.email = $1 order by date asc', session['org_email'])
    query_name = db.query('select * from organization where email = $1', session['org_email'])
    org_info = query.namedresult()
    org_name = query_name.namedresult()[0].name

    return render_template(
        'org_profile.html',
        org_info = org_info,
        org_name = org_name
    )

@app.route('/vol_profile')
def view_vol_profile():
    query = db.query('select * from volunteer where email = $1', session['vol_email'])
    vol_info = query.namedresult()[0]

    query2 = db.query('select volunteer.name as vol_name, volunteer.age, project.name as project_name, project.project_description, project.start_time, project.start_date from volunteer, participation, project where volunteer.id = participation.volunteer_id and participation.project_id = project.id and volunteer.email = $1', session['vol_email'])
    project_info = query2.namedresult()

    return render_template(
        'vol_profile.html',
        project_info = project_info,
        vol_info = vol_info
    )

@app.route('/create_new_event')
def create_new_event():

    return render_template(
        'create_new_event.html'
    )

@app.route('/submit_new_event', methods=['POST'])
def submit_new_event():
    query = db.query('select * from organization where email = $1', session['org_email']).namedresult()[0]
    org_id = query.id
    org_name = query.name

    name = request.form.get('name')
    start_date = request.form.get('date')
    start_time = request.form.get('start_time')
    description = request.form.get('description')
    vol_count = request.form.get('vol_count')
    hour = request.form.get('hour')
    minutes = request.form.get('minutes')
    time_period = request.form.get('time_period')
    print "TIME: %s:%s:%s" % (hour, minutes, time_period)

    if time_period == "pm":
        hour = int(hour)
        hour += 12

    time = "%s:%s" % (hour, minutes)
    print "SECOND TIME: %s" % time

    print hour
    db.insert(
        'project', {
            'name': name,
            'project_description': description,
            'start_time': time,
            'organization_id': org_id,
            'start_date': start_date,
            'vol_needed': vol_count,
            'vol_total': vol_count
        }
    )
    return redirect('/org_profile')

@app.route('/projects', methods=['POST'])
def search_bar():
    date = request.form.get('date')
    query = db.query('select organization.name as Organization, project.name as Project, project.project_description as Description, project.start_date as Time, project.vol_needed, project.vol_total from project, organization where project.organization_id = organization.id and start_date = $1', date)
    search_results_list = query.namedresult()

    # print "DATE: %r" % date
    # return redirect('projects', searches = {'search_results_list' : 'search_results_list'})
    return render_template(
        'projects.html',
        entry_list = search_results_list
    )

@app.route('/projects')
def view_projects():
    # if 'searches['search_results_list']' in locals() or 'searches.search_results_list' in globals():
    #     entry_list = search_results_list
    # else:
    query = db.query('select organization.name as Organization, project.id as project_id, organization.id as org_id, project.name as Project, project.project_description as Description, project.start_date as Date, project.start_time as Time, project.vol_needed, project.vol_total from project, organization where project.organization_id = organization.id order by date desc')
    entry_list = query.namedresult()

    return render_template(
        'projects.html',
        title='If You Care',
        entry_list= entry_list
    )

        # start_time_list = []
        # for result in results_list:
        #     start_time_list.append(result.time)

        # print "START TIME LIST: %s" % start_time_list

        # start_time = str(entry_list[0].time)
        # print "Start TIME: %s" % start_time
        # print "TYPE OF START TIME: %r" % type(start_time)
        # hour = ""
        # minutes = ""
        # counter = 0

        # for char in start_time:
        #     while counter < 5:
        #         if counter < 2:
        #             hour += char
        #         elif counter != 2:
        #             minutes += char
        #         counter += 1
        #         break
        #
        # print "HOUR NOW: %s" % hour
        # print "MINUTES NOW %s" % minutes
        #
        # time_period = ""
        # hour = int(hour)
        # if hour > 12:
        #     hour -= 12
        #     time_period = "pm"
        # else:
        #     time_period = "am"
        # hour = str(hour)
        # minutes = str(minutes)
        # start_time = "%s:%s %s" % (hour, minutes, time_period)
        # print start_time
        # print "START TIME YAYAY!!! %s" % start_time

        # print "Hour %s" % hour
        # print "Minutes %s" % minutes
        #
        # print "TIME: %s" % hour
        # print "TYPE OF TIME: %r" % type(hour)
        # print "MINUTES: %s" %(minutes)
        # print "TYPE OF MINUTES: %r" % type(minutes)



    # return render_template(
    #     'projects.html',
    #     entry_list = results_list
    # )


@app.route('/register_project/<project_id>')
def register(project_id):
    query = db.query('select organization.name as organization, project.name as project, project.project_description as description, organization.id as org_id, project.start_time as time, project.start_date as date, project.vol_needed from project, organization where project.organization_id = organization.id and project.id = $1', project_id)
    org_info = query.namedresult()[0]
    return render_template(
        'register_project.html',
        org_info = org_info,
        project_id = project_id
    )
@app.route('/register_project/<project_id>/confirm')
def confirm(project_id):

    # make a query to grab info from the volunteer and participation tables in db
    query = db.query('select participation.project_id as project_id, volunteer.id as vol_id from volunteer, participation where volunteer.id = participation.volunteer_id and email = $1', session['vol_email'])
    project_info = query.namedresult()
    # set this value to be used to check if user has already registered for the project
    is_found = False
    # check if the above query grabbed any info or is empty
    if project_info != []:
        # if not empty, check to see if volunteer has already signed up for the project
        # by seeing if the project id is linked to volunteer_id in the participation table in db
        for project in project_info:
            project_id = int(project_id)
            if project.project_id == project_id:
                is_found = True
                # implement Flash later to alert user has already signed up for the event
                # until then, redirect to homepage until better solution
                return redirect('/')
            else:
                pass

    if is_found == False:
        # make a connection and insert volunteer's participation in the project
        query5 = db.query('select id from volunteer where email = $1', session['vol_email'])
        vol_id = query5.namedresult()[0].id
        db.insert(
            'participation', {
                'project_id': project_id,
                'volunteer_id': vol_id
            }
        )
        query2 = db.query('select * from project where project.id = $1', project_id)
        vol_count = query2.namedresult()[0].vol_needed
        vol_count = int(vol_count) - 1

        db.update(
            'project', {
                'id': project_id,
                'vol_needed': vol_count
            }
        )
        return redirect('/vol_profile')

@app.route('/project_vols/<project_id>')
def view_project_vols(project_id):
    query = db.query('select volunteer.name as vol_name, volunteer.email as vol_email from volunteer, participation, project where volunteer.id = participation.volunteer_id and project.id = participation.project_id and project.id = $1', project_id)
    vols_info = query.namedresult()

    return render_template(
        'view_project_vols.html',
        vols_info = vols_info
    )
@app.route('/org_list')
def orglist():
    query = db.query('select * from organization')
    org_list = query.namedresult()
    return render_template(
        'org_list.html',
        org_list = org_list
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
