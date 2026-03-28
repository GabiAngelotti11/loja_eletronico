from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, static_folder='statics')
# Chave secreta necessária para usar o flash messages (mensagens de alerta)
app.secret_key = 'chave_secreta_super_segura_para_o_trabalho'

# ---(Listas Python)

# Tabela 1: Usuários (Obrigatório)
usuarios_db = [
    {'id': 1, 'nome': 'Admin Silva', 'email': 'admin@loja.com', 'perfil': 'Administrador'},
    {'id': 2, 'nome': 'João Cliente', 'email': 'joao@email.com', 'perfil': 'Cliente'},
    {'id': 3, 'nome': 'Maria Vendedora', 'email': 'maria@loja.com', 'perfil': 'Vendedor'},
    {'id': 4, 'nome': 'Carlos Suporte', 'email': 'carlos@loja.com', 'perfil': 'Suporte'},
    {'id': 5, 'nome': 'Ana Gerente', 'email': 'ana@loja.com', 'perfil': 'Gerente'}
]

# Tabela 2: Produtos
produtos_db = [
    {'id': 1, 'nome': 'Notebook Acer Aspire 5 (USB-C)', 'preco': 3500.00, 'estoque': 12},
    {'id': 2, 'nome': 'Smartphone Galaxy S23', 'preco': 4200.00, 'estoque': 8},
    {'id': 3, 'nome': 'Monitor Dell 27"', 'preco': 1500.00, 'estoque': 15},
    {'id': 4, 'nome': 'Teclado Mecânico Redragon', 'preco': 250.00, 'estoque': 30},
    {'id': 5, 'nome': 'Mouse Sem Fio Logitech', 'preco': 120.00, 'estoque': 45}
]

# Tabela 3: Categorias
categorias_db = [
    {'id': 1, 'nome': 'Informática', 'descricao': 'Computadores e periféricos'},
    {'id': 2, 'nome': 'Smartphones', 'descricao': 'Celulares e acessórios'},
    {'id': 3, 'nome': 'Áudio', 'descricao': 'Fones, caixas de som e microfones'},
    {'id': 4, 'nome': 'Games', 'descricao': 'Consoles, jogos e acessórios gamers'},
    {'id': 5, 'nome': 'Casa Inteligente', 'descricao': 'Assistentes virtuais e automação'}
]


# ==========================================
# ROTAS PÚBLICAS (Sem login)
# ==========================================

@app.route('/', endpoint='index')
def pagina_inicial():
    # Página inicial vitrine (Usa base_publica)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simula a verificação de login
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if email and senha:
            # Se preencheu, "loga" e manda pra lista de usuários
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))
        else:
            flash('Preencha todos os campos.', 'danger')
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Simula o processamento do cadastro
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validação simples no back-end
        if nome and email and senha:
            flash('Cadastro realizado! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Erro ao cadastrar. Verifique os dados.', 'danger')
            
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    # Simula encerramento de sessão
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('login'))


# ==========================================
# ROTAS PROTEGIDAS (Simuladas - Após login)
# ==========================================

# --- USUÁRIOS ---
@app.route('/usuarios/listar')
def listar_usuarios():
    return render_template('usuarios/listar_usuario.html', usuarios=usuarios_db)

@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    if request.method == 'POST':
        # Validação simples
        if not request.form.get('nome') or not request.form.get('email'):
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('usuarios/inserir_usuario.html')
            
        flash('Usuário salvo com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
        
    return render_template('usuarios/inserir_usuario.html')

# --- PRODUTOS ---
@app.route('/produtos/listar')
def listar_produtos():
    return render_template('produtos2/listar_produtos2.html', produtos=produtos_db)

@app.route('/produtos/inserir', methods=['GET', 'POST'])
def inserir_produto():
    if request.method == 'POST':
        if not request.form.get('nome'):
            flash('O nome do produto é obrigatório.', 'danger')
            return render_template('produtos2/inserir_produtos2.html')
            
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
        
    return render_template('produtos2/inserir_produtos2.html')

# --- CATEGORIAS ---
@app.route('/categorias/listar')
def listar_categorias():
    return render_template('categoria3/listar_categoria3.html', categorias=categorias_db)

@app.route('/categorias/inserir', methods=['GET', 'POST'])
def inserir_categoria():
    if request.method == 'POST':
        if not request.form.get('nome'):
            flash('O nome da categoria é obrigatório.', 'warning')
            return render_template('categoria3/inserir_categoria3.html')
            
        flash('Categoria criada!', 'success')
        return redirect(url_for('listar_categorias'))
        
    return render_template('categoria3/inserir_categoria3.html')

# --- EQUIPE ---
@app.route('/equipe')
def equipe():
    # Não usa herança de template conforme regra
    return render_template('sobre.html')

if __name__ == '__main__':
    # debug=True facilita a vida durante o desenvolvimento, recarregando o servidor
    app.run(debug=True)