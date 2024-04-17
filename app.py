# Importações necessárias
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os

# Criação da aplicação Flask
app = Flask(__name__)

# Diretório e nome do banco de dados
DB_DIR = 'database'
DB_FILE = 'blog.db'
DB_PATH = os.path.join(DB_DIR, DB_FILE)

# Função para conectar ao banco de dados
def connect_db():
    return sqlite3.connect(DB_PATH)

# Função para criar a tabela posts, se não existir
def create_posts_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                          id INTEGER PRIMARY KEY,
                          title TEXT NOT NULL,
                          content TEXT NOT NULL,
                          author TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Verifica se o diretório do banco de dados existe, se não, cria-o
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Verifica se o arquivo do banco de dados existe, se não, cria-o e cria a tabela posts
if not os.path.exists(DB_PATH):
    create_posts_table()

# Rota para exibir a página inicial do blog
@app.route('/')
def index():
    return render_template('index.html')

# Rota para listar todas as postagens do blog e exibir na página 'post.html'
@app.route('/posts', methods=['GET', 'POST'])
def show_posts():
    if request.method == 'POST':
        data = request.form
        title = data.get('title')
        content = data.get('content')
        author = data.get('author')

        if not title or not content or not author:
            return jsonify({'error': 'Dados incompletos'}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content, author) VALUES (?, ?, ?)", (title, content, author))
        conn.commit()
        conn.close()

        # Após criar a postagem, redirecionar para a rota de exibição de postagens
        return redirect(url_for('show_posts'))

    elif request.method == 'GET':
        posts = get_posts_from_db()
        return render_template('post.html', posts=posts)
    
# Rota para deletar uma postagem
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('show_posts'))

# Função para obter todas as postagens do banco de dados
def get_posts_from_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.close()
    return posts

# Execução da aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
