document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(response => {
        alert(response.message || 'Inicio de sesión exitoso');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema al iniciar sesión');
    });
});