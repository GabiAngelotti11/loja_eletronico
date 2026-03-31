"""
App Flask (projeto de loja eletrônica).

Observações:
- Este projeto usa dados simulados em listas (não conecta em banco).
- As "rotas protegidas" são apenas simuladas: não há autenticação real.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session

# Instância da aplicação Flask
app = Flask(__name__)

# Chave secreta necessária para o Flask conseguir assinar as sessões/flash messages
app.secret_key = 'chave_secreta_super_segura_para_o_trabalho'

# --------------------------------------------------------------------
# DADOS SIMULADOS
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
    """
    Renderiza a página inicial pública do sistema.

    - **Método**: GET
    - **Saída**: HTML (`templates/index.html`)
    """
    # Página inicial vitrine.
    # Usa `templates/index.html`, que herda `base_publica.html`.
    return render_template('index.html')

# Login (GET para exibir formulário, POST para processar envio)
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Exibe e processa o login (simulado).

    - **GET**: mostra o formulário de login.
    - **POST**: valida se `email` e `senha` foram preenchidos e, se sim,
      marca o usuário como logado via `session['logado']` e redireciona.
    """
    if request.method == 'POST':
        # Simula a verificação de login (sem autenticação real).
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if email and senha:
            # Se os campos foram preenchidos, simula "login" e redireciona.
            session['logado'] = True
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
    """
    Exibe e processa o cadastro de usuário (simulado, sem persistência).

    - **GET**: mostra o formulário de cadastro.
    - **POST**: valida campos obrigatórios e se as senhas conferem.
      Em caso de sucesso, redireciona para o login.
    """
    if request.method == 'POST':
        # Simula o processamento do cadastro (sem persistir dados).
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirma_senha = request.form.get('confirma_senha')
        
        # Validação simples dos campos obrigatórios.
        if not nome or not email or not senha or not confirma_senha:
            flash('Erro ao cadastrar. Verifique os dados.', 'danger')
            return render_template('cadastro.html')

        if senha != confirma_senha:
            flash('As senhas não conferem. Tente novamente.', 'warning')
            return render_template('cadastro.html')

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
    """
    Encerra a sessão do usuário (simulado).

    Limpa todos os dados em `session` e redireciona para a tela de login.
    """
    # Simula encerramento de sessão e redireciona para login.
    session.clear()
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
    """
    Lista usuários disponíveis no sistema (dados fixos + dados em sessão).

    - Exige `session['logado']` (proteção simulada).
    - Combina `usuarios_db` (memória) com `session['usuarios']` (cadastros via formulário).
    - Renderiza `templates/usuarios/listar_usuarios.html`.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    # Lista usuários simulados + usuários gravados na sessão.
    usuarios_session = session.get('usuarios', [])
    usuarios = usuarios_db + usuarios_session
    return render_template('usuarios/listar_usuarios.html', usuarios=usuarios)

@app.route('/usuarios/excluir/<int:usuario_id>', methods=['POST'])
def excluir_usuario(usuario_id: int):
    """
    Exclui um usuário pelo `usuario_id` (simulado).

    - Remove tanto do `usuarios_db` (lista em memória) quanto de `session['usuarios']`
      (lista criada via formulário).
    - Mostra feedback via `flash` e redireciona para a listagem.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))

    removido = False

    # Remove da lista "fixa" em memória (enquanto o servidor estiver rodando).
    global usuarios_db
    antes = len(usuarios_db)
    usuarios_db = [u for u in usuarios_db if int(u.get('id', 0)) != usuario_id]
    if len(usuarios_db) != antes:
        removido = True

    # Remove da sessão (onde ficam os usuários criados via formulário).
    usuarios_session = session.get('usuarios', [])
    antes_sessao = len(usuarios_session)
    usuarios_session = [u for u in usuarios_session if int(u.get('id', 0)) != usuario_id]
    if len(usuarios_session) != antes_sessao:
        session['usuarios'] = usuarios_session
        session.modified = True
        removido = True

    if removido:
        flash('Usuário excluído com sucesso!', 'success')
    else:
        flash('Usuário não encontrado.', 'warning')

    return redirect(url_for('listar_usuarios'))

@app.route('/usuarios/inserir', methods=['GET', 'POST'])
def inserir_usuario():
    """
    Exibe e processa o formulário de cadastro de usuário (proteção simulada).

    - **GET**: mostra o formulário.
    - **POST**: valida campos obrigatórios e salva o novo usuário em `session['usuarios']`
      com um `id` incremental baseado no maior id existente.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Processa envio do formulário (POST).
        # Validação simples (campos obrigatórios).
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        perfil = request.form.get('perfil') or 'Cliente'

        if not nome or not email or not senha:
            # Se algum campo obrigatório estiver vazio, avisa e mantém no formulário.
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('usuarios/inserir_usuario.html')
            
        # Gravar na sessão (mesmo esquema do seu exemplo).
        if 'usuarios' not in session:
            session['usuarios'] = []

        existentes = usuarios_db + session.get('usuarios', [])
        proximo_id = (max([u.get('id', 0) for u in existentes]) + 1) if existentes else 1

        novo_usuario = {
            'id': proximo_id,
            'nome': nome,
            'email': email,
            'perfil': perfil
        }

        session['usuarios'].append(novo_usuario)
        session.modified = True

        flash('Usuário salvo com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
        
    # Se GET, apenas mostra o formulário.
    return render_template('usuarios/inserir_usuario.html')

# --------------------------------------------------------------------
# PRODUTOS
# --------------------------------------------------------------------

@app.route('/produtos/listar')
def listar_produtos():
    """
    Lista produtos disponíveis no sistema (dados fixos + dados em sessão).

    - Exige `session['logado']` (proteção simulada).
    - Combina `produtos_db` (memória) com `session['produtos']` (cadastros via formulário).
    - Renderiza `templates/produtos/listar_produtos.html`.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    # Lista produtos simulados + produtos gravados na sessão.
    produtos_session = session.get('produtos', [])
    produtos = produtos_db + produtos_session
    return render_template('produtos/listar_produtos.html', produtos=produtos)

@app.route('/produtos/excluir/<int:produto_id>', methods=['POST'])
def excluir_produto(produto_id: int):
    """
    Exclui um produto pelo `produto_id` (simulado).

    - Remove tanto de `produtos_db` (lista em memória) quanto de `session['produtos']`
      (lista criada via formulário).
    - Mostra feedback via `flash` e redireciona para a listagem.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))

    removido = False

    # Remove da lista "fixa" em memória (enquanto o servidor estiver rodando).
    global produtos_db
    antes = len(produtos_db)
    produtos_db = [p for p in produtos_db if int(p.get('id', 0)) != produto_id]
    if len(produtos_db) != antes:
        removido = True

    # Remove da sessão (onde ficam os produtos criados via formulário).
    produtos_session = session.get('produtos', [])
    antes_sessao = len(produtos_session)
    produtos_session = [p for p in produtos_session if int(p.get('id', 0)) != produto_id]
    if len(produtos_session) != antes_sessao:
        session['produtos'] = produtos_session
        session.modified = True
        removido = True

    if removido:
        flash('Produto excluído com sucesso!', 'success')
    else:
        flash('Produto não encontrado.', 'warning')

    return redirect(url_for('listar_produtos'))

@app.route('/produtos/inserir', methods=['GET', 'POST'])
def inserir_produto():
    """
    Exibe e processa o formulário de cadastro de produto (proteção simulada).

    - **GET**: mostra o formulário.
    - **POST**: valida campos mínimos, converte `preco` para float e `estoque` para int,
      gera `id` incremental e salva em `session['produtos']`.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Processa envio do formulário de produto.
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        estoque = request.form.get('estoque')

        if not nome or preco is None or preco == '':
            # Validação mínima do que é obrigatório no formulário.
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('produtos/inserir_produtos.html')
            
        if 'produtos' not in session:
            session['produtos'] = []

        try:
            preco_float = float(preco)
        except (TypeError, ValueError):
            flash('Preço inválido.', 'danger')
            return render_template('produtos/inserir_produtos.html')

        try:
            estoque_int = int(estoque) if estoque not in (None, '') else 0
        except (TypeError, ValueError):
            estoque_int = 0

        existentes = produtos_db + session.get('produtos', [])
        proximo_id = (max([p.get('id', 0) for p in existentes]) + 1) if existentes else 1

        novo_produto = {
            'id': proximo_id,
            'nome': nome,
            'preco': round(preco_float, 2),
            'estoque': estoque_int
        }

        session['produtos'].append(novo_produto)
        session.modified = True

        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))
        
    # Se GET, exibe o formulário.
    return render_template('produtos/inserir_produtos.html')

# --------------------------------------------------------------------
# CATEGORIAS
# --------------------------------------------------------------------

@app.route('/categorias/listar')
def listar_categorias():
    """
    Lista categorias disponíveis no sistema (dados fixos + dados em sessão).

    - Exige `session['logado']` (proteção simulada).
    - Combina `categorias_db` (memória) com `session['categorias']` (cadastros via formulário).
    - Renderiza `templates/categorias/listar_categorias.html`.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    # Lista categorias simuladas + categorias gravadas na sessão.
    categorias_session = session.get('categorias', [])
    categorias = categorias_db + categorias_session
    return render_template('categorias/listar_categorias.html', categorias=categorias)

@app.route('/categorias/excluir/<int:categoria_id>', methods=['POST'])
def excluir_categoria(categoria_id: int):
    """
    Exclui uma categoria pelo `categoria_id` (simulado).

    - Remove tanto de `categorias_db` (lista em memória) quanto de `session['categorias']`
      (lista criada via formulário).
    - Mostra feedback via `flash` e redireciona para a listagem.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))

    removido = False

    # Remove da lista "fixa" em memória (enquanto o servidor estiver rodando).
    global categorias_db
    antes = len(categorias_db)
    categorias_db = [c for c in categorias_db if int(c.get('id', 0)) != categoria_id]
    if len(categorias_db) != antes:
        removido = True

    # Remove da sessão (onde ficam as categorias criadas via formulário).
    categorias_session = session.get('categorias', [])
    antes_sessao = len(categorias_session)
    categorias_session = [c for c in categorias_session if int(c.get('id', 0)) != categoria_id]
    if len(categorias_session) != antes_sessao:
        session['categorias'] = categorias_session
        session.modified = True
        removido = True

    if removido:
        flash('Categoria excluída com sucesso!', 'success')
    else:
        flash('Categoria não encontrada.', 'warning')

    return redirect(url_for('listar_categorias'))

@app.route('/categorias/inserir', methods=['GET', 'POST'])
def inserir_categoria():
    """
    Exibe e processa o formulário de cadastro de categoria (proteção simulada).

    - **GET**: mostra o formulário.
    - **POST**: valida `nome`, gera `id` incremental e salva em `session['categorias']`.
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Processa envio do formulário de categoria.
        nome = request.form.get('nome')
        descricao = request.form.get('descricao') or ''

        if not nome:
            # Validação mínima: nome é obrigatório.
            flash('O nome da categoria é obrigatório.', 'warning')
            return render_template('categorias/inserir_categorias.html')

        if 'categorias' not in session:
            session['categorias'] = []

        existentes = categorias_db + session.get('categorias', [])
        proximo_id = (max([c.get('id', 0) for c in existentes]) + 1) if existentes else 1

        nova_categoria = {
            'id': proximo_id,
            'nome': nome,
            'descricao': descricao
        }

        session['categorias'].append(nova_categoria)
        session.modified = True

        flash('Categoria criada!', 'success')
        return redirect(url_for('listar_categorias'))
        
    # Se GET, exibe o formulário.
    return render_template('categorias/inserir_categorias.html')

# --------------------------------------------------------------------
# EQUIPE (layout próprio, sem herança de base)
# --------------------------------------------------------------------

@app.route('/equipe')
def equipe():
    """
    Renderiza a página "Sobre a equipe" (protegida, simulada).

    - Exige `session['logado']`.
    - Retorna `templates/sobre_equipe.html` (sem herdar base, conforme regra do projeto).
    """
    if not session.get('logado'):
        flash('Faça login para acessar o sistema.', 'warning')
        return redirect(url_for('login'))
    # Não usa herança de template conforme regra
    return render_template('sobre_equipe.html')

if __name__ == '__main__':
    # debug=True facilita durante o desenvolvimento (auto-recarrega).
    app.run(debug=True)