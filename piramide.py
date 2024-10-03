from wsgiref.simple_server import make_server  # Importa a função para criar o servidor WSGI
from pyramid.config import Configurator  # Importa o Configurator para configurar a aplicação Pyramid
from pyramid.response import Response  # Importa a classe Response para criar respostas HTTP
from pyramid.request import Request  # Importa a classe Request para manipular requisições
from pyramid.view import view_config  # Importa o decorador para configurar views

# View para exibir o formulário de login
@view_config(route_name='login', request_method='GET')
def login_form(request: Request):
    # Retorna um HTML com o formulário de login
    return Response('''
        <html>
            <body>
                <h2>Login</h2>
                <form action="/" method="post">  <!-- Formulário que envia dados para o método POST -->
                    <label for="username">Username:</label><br>
                    <input type="text" id="username" name="username"><br>  <!-- Campo para nome de usuário -->
                    <label for="password">Password:</label><br>
                    <input type="password" id="password" name="password"><br><br>  <!-- Campo para senha -->
                    <input type="submit" value="Submit">  <!-- Botão para enviar o formulário -->
                </form>
            </body>
        </html>
    ''')

# View para processar o login
@view_config(route_name='login', request_method='POST')
def login_submit(request: Request):
    # Obtém os dados do formulário enviados pelo usuário
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Verificação de credenciais (exemplo simples)
    if username == 'admin' and password == 'password':
        # Se as credenciais estiverem corretas, redireciona para a página de boas-vindas
        request.response.status = 302  # Define o status de redirecionamento
        request.response.headers['Location'] = request.route_url('welcome', username=username)  # Define a URL de redirecionamento
        return request.response  # Retorna a resposta com o redirecionamento
    else:
        # Se as credenciais forem inválidas, retorna uma mensagem de erro
        return Response('Invalid username or password! Please <a href="/">try again</a>.')

# View para exibir a página de boas-vindas
@view_config(route_name='welcome')
def welcome_view(request: Request):
    username = request.matchdict.get('username')  # Obtém o nome de usuário a partir da URL
    return Response(f'<h1>Welcome, {username}!</h1>')  # Retorna uma mensagem de boas-vindas

if __name__ == '__main__':
    with Configurator() as config:  # Cria uma nova configuração
        config.add_route('login', '/')  # Define a rota para a página de login
        config.add_view(login_form, route_name='login', request_method='GET')  # View para o método GET (exibe o formulário)
        config.add_view(login_submit, route_name='login', request_method='POST')  # View para o método POST (processa o login)
        config.add_route('welcome', '/welcome/{username}')  # Define a rota para a página de boas-vindas com um parâmetro
        config.add_view(welcome_view, route_name='welcome')  # View para a página de boas-vindas
        app = config.make_wsgi_app()  # Cria a aplicação WSGI a partir da configuração
    server = make_server('0.0.0.0', 6543, app)  # Cria o servidor na porta 6543, escutando em todas as interfaces
    print("Server is running on http://localhost:6543")  # Informa que o servidor está rodando
    server.serve_forever()  # Mantém o servidor rodando até ser interrompido
