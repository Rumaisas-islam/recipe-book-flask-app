from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'rumaisa_secret_key'

recipes = []

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q')
    if query:
        filtered = [r for r in recipes if query.lower() in r['title'].lower()]
    else:
        filtered = recipes
    return render_template('index.html', recipes=filtered, query=query, username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        flash(f"Welcome, {username}!", "success")
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        recipes.append({'id': len(recipes) + 1, 'title': title, 'ingredients': ingredients, 'steps': steps})
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit(recipe_id):
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if not recipe:
        return redirect(url_for('index'))
    if request.method == 'POST':
        recipe['title'] = request.form['title']
        recipe['ingredients'] = request.form['ingredients']
        recipe['steps'] = request.form['steps']
        return redirect(url_for('index'))
    return render_template('edit.html', recipe=recipe)

@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    global recipes
    recipes = [r for r in recipes if r['id'] != recipe_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
