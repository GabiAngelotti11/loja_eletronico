"""
App Flask (projeto de loja eletrônica).

Observações:
- Este projeto usa dados simulados em listas (não conecta em banco).
- As "rotas protegidas" são apenas simuladas: não há autenticação real.
"""

from flask import Flask, render_template, request, redirect, url_for, flash

# Instância da aplicação Flask
app = Flask(__name__)

# Chave secreta necessária para o Flask conseguir assinar as sessões/flash messages
app.secret_key = 'chave_secreta_super_segura_para_o_trabalho'

# --------------------------------------------------------------------
# DADOS SIMULADOS (listas em memória)
# --------------------------------------------------------------------

# "Tabela" 1: Usuários (mínimo 5 registros)
usuarios_db = [
    {'id': 1, 'nome': 'Admin Silva', 'email': 'admin@loja.com', 'perfil': 'Administrador'},
    {'id': 2, 'nome': 'João Cliente', 'email': 'joao@email.com', 'perfil': 'Cliente'},
    {'id': 3, 'nome': 'Maria Vendedora', 'email': 'maria@loja.com', 'perfil': 'Vendedor'},
    {'id': 4, 'nome': 'Carlos Suporte', 'email': 'carlos@loja.com', 'perfil': 'Suporte'},
    {'id': 5, 'nome': 'Ana Gerente', 'email': 'ana@loja.com', 'perfil': 'Gerente'}
]

# "Tabela" 2: Produtos
produtos_db = [
    {'id': 1, 'nome': 'Notebook Acer Aspire 5 (USB-C)', 'preco': 3500.00, 'estoque': 12},
    {'id': 2, 'nome': 'Smartphone Galaxy S23', 'preco': 4200.00, 'estoque': 8},
    {'id': 3, 'nome': 'Monitor Dell 27"', 'preco': 1500.00, 'estoque': 15},
    {'id': 4, 'nome': 'Teclado Mecânico Redragon', 'preco': 250.00, 'estoque': 30},
    {'id': 5, 'nome': 'Mouse Sem Fio Logitech', 'preco': 120.00, 'estoque': 45}
]

# "Tabela" 3: Categorias
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

# Rota da página inicial (/)
@app.route('/', endpoint='index')
def pagina_inicial():
    # Página inicial vitrine.
    # Usa `templates/index.html`, que herda `base_publica.html`.
    return render_template('index.html')

# Login (GET para exibir formulário, POST para processar envio)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simula a verificação de login (sem autenticação real).
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if email and senha:
            # Se os campos foram preenchidos, simula "login" e redireciona.
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))
        else:
            # Se campos faltarem, mostra feedback via flash.
            flash('Preencha todos os campos.', 'danger')
            
    # Se GET (ou POST inválido), renderiza o formulário.
    return render_template('login.html')

# Cadastro de novo usuário (GET para exibir, POST para processar envio)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Simula o processamento do cadastro (sem persistir dados).
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validação simples dos campos obrigatórios.
        if nome and email and senha:
            # Se ok, exibe mensagem e manda para login.
            flash('Cadastro realizado! Faça login para continuar.', 'success')
            return redirect(url_for('login'))
        else:
            # Se campos faltarem, avisa via flash.
            flash('Erro ao cadastrar. Verifique os dados.', 'danger')
            
    # Se GET (ou POST inválido), renderiza o formulário de cadastro.
    return render_template('cadastro.html')

# Logout (simulado)
@app.route('/logout')
def logout():
    # Simula encerramento de sessão e redireciona para login.
    flash('Sessão encerrada.', 'info')
    return redirect(url_for('login'))


# ==========================================
# ROTAS "PROTEGIDAS" (Simuladas - após login)
# ==========================================

# --------------------------------------------------------------------
# USUÁRIOS
# --------------------------------------------------------------------

@app.route('/usuarios/listar')
def listar_usuarios():
    # Lista usuários simulados.
    return render_template('usuarios/listar_usuario.html', usuarios=usuarios_db)

@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    if request.method == 'POST':
        # Processa envio do formulário (POST).
        # Validação simples (campos obrigatórios).
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            # Se algum campo obrigatório estiver vazio, avisa e mantém no formulário.
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('usuarios/inserir_usuario.html')
            
        # Como é projeto simulado, não salvamos de fato, só exibimos sucesso.
        flash('Usuário salvo com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
        
    # Se GET, apenas mostra o formulário.
    return render_template('usuarios/inserir_usuario.html')

# --------------------------------------------------------------------
# PRODUTOS
# --------------------------------------------------------------------

@app.route('/produtos/listar')
def listar_produtos():
    # Lista produtos simulados.
    return render_template('produtos2/listar_produtos2.html', produtos=produtos_db)

@app.route('/produtos/inserir', methods=['GET', 'POST'])
def inserir_produto():
    if request.method == 'POST':
        # Processa envio do formulário de produto.
        nome = request.form.get('nome')
        preco = request.form.get('preco')

        if not nome or preco is None or preco == '':
            # Validação mínima do que é obrigatório no formulário.
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('produtos2/inserir_produtos2.html')
            
        # Como é projeto simulado, não persistimos os dados.
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
        
    # Se GET, exibe o formulário.
    return render_template('produtos2/inserir_produtos2.html')

# --------------------------------------------------------------------
# CATEGORIAS
# --------------------------------------------------------------------

@app.route('/categorias/listar')
def listar_categorias():
    # Lista categorias simuladas.
    return render_template('categoria3/listar_categoria3.html', categorias=categorias_db)

@app.route('/categorias/inserir', methods=['GET', 'POST'])
def inserir_categoria():
    if request.method == 'POST':
        # Processa envio do formulário de categoria.
        if not request.form.get('nome'):
            # Validação mínima: nome é obrigatório.
            flash('O nome da categoria é obrigatório.', 'warning')
            return render_template('categoria3/inserir_categoria3.html')
            
        # Como é projeto simulado, não persistimos no array.
        flash('Categoria criada!', 'success')
        return redirect(url_for('listar_categorias'))
        
    # Se GET, exibe o formulário.
    return render_template('categoria3/inserir_categoria3.html')

# --------------------------------------------------------------------
# EQUIPE (layout próprio, sem herança de base)
# --------------------------------------------------------------------

@app.route('/equipe')
def equipe():
    # Não usa herança de template conforme regra
    return render_template('sobre.html')

if __name__ == '__main__':
    # debug=True facilita durante o desenvolvimento (auto-recarrega).
    app.run(debug=True)