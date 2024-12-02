// Simulação de banco de dados de usuários
const usuarios = [
    { email: 'usuario@cinema.com', senha: '12345' }
];

// Função para simular o login
document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const usuario = usuarios.find(u => u.email === email && u.senha === senha);

    if (usuario) {
        // Usuário encontrado, login bem-sucedido
        localStorage.setItem("usuarioAutenticado", JSON.stringify(usuario));
        window.location.href = 'PiVendas.html';  // Redireciona para a página de vendas
    } else {
        // Senha ou e-mail incorretos
        alert('E-mail ou senha inválidos!');
    }
});

// Verificar se o usuário está autenticado antes de acessar a página de vendas
if (window.location.href.includes('PiVendas.html')) {
    const usuarioAutenticado = localStorage.getItem("usuarioAutenticado");
    if (!usuarioAutenticado) {
        window.location.href = 'PiLogin.html';  // Redireciona para login se não autenticado
    }
}
