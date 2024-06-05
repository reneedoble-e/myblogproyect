from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(80), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    texto = db.Column(db.Text, nullable=False)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('blog'))
    return render_template('login.html')


@app.route('/blog')
def blog():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('blog.html', username=session['username'])


@app.route('/posteos/<usuario>', methods=['GET', 'POST'])
def handle_post(usuario):
    if request.method == 'GET':
        posts = Post.query.filter_by(usuario=usuario).order_by(Post.id.desc()).limit(3).all()
        datos = [{"titulo": post.titulo, "texto": post.texto} for post in posts]
        return jsonify(datos)
    elif request.method == 'POST':
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        new_post = Post(usuario=usuario, titulo=titulo, texto=texto)
        db.session.add(new_post)
        db.session.commit()
        return '', 201
        
 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Base de datos generada")
    app.run(host="127.0.0.1", port=5000)
