from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import pie, user
from flask import flash


@app.route('/process/pie', methods=['POST'])
def process_recipe():
    if not pie.Pie.validate_pie(request.form):
        session['pie_name'] = request.form['name']
        session['pie_filling'] = request.form['filling']
        session['pie_crust'] = request.form['crust']
        return redirect('/dashboard')
    data={
        'user_id': session['user_id'],
        'name': request.form['name'],
        'filling': request.form['filling'],
        'crust': request.form['crust'],
    }
    pie.Pie.create_recipe(data)
    session['pie_name'] = ""
    session['pie_filling'] = ""
    session['pie_crust'] = ""
    return redirect('/dashboard')

@app.route('/edit/pie/<int:pie_id>')
def edit_pie(pie_id):
    if not session['user_id']:
        return redirect('/')
    data={'id': pie_id}
    return render_template('edit_pie.html', pie=pie.Pie.get_one_pie(data))

@app.route('/edit/process/<int:pie_id>', methods=['POST'])
def process_edit(pie_id):
    if not pie.Pie.validate_pie(request.form):
        return redirect(f'/edit/pie/{pie_id}')
    data={
        'id': pie_id,
        'name': request.form['name'],
        'filling': request.form['filling'],
        'crust': request.form['crust'],
    }
    pie.Pie.edit_pie(data)
    return redirect('/dashboard')

@app.route('/delete/pie/<int:pie_id>')
def process_delete(pie_id):
    data={'id': pie_id}
    pie.Pie.delete_pie(data)
    return redirect('/dashboard')

@app.route('/pies')
def all_pies_with_votes():
    if not session['user_id']:
        return redirect('/')
    return render_template('/all_pies.html', all_pies=pie.Pie.get_all_pies_with_votes())

@app.route('/show/<int:pie_id>')
def show_one_pie(pie_id):
    data={
        'user_id': session['user_id'],
        'pie_id' : pie_id
        }
    return render_template('show_one_pie.html', pie=pie.Pie.get_one_pie(data), user_is_voter=user.User.is_user_voter(data))

@app.route('/vote/plus_one/<int:pie_id>', methods=['POST'])
def plus_one_vote(pie_id):
    data={
        'user_id': session['user_id'],
        'pie_id': pie_id
    }
    pie.Pie.add_vote(data)
    return redirect(f'/show/{pie_id}')

@app.route('/vote/minus_one/<int:pie_id>', methods=['POST'])
def minus_one_vote(pie_id):
    data={
        'user_id': session['user_id'],
        'pie_id': pie_id
    }
    pie.Pie.subtract_vote(data)
    return redirect(f'/show/{pie_id}')

