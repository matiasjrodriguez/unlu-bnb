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
    .then(res => {
        if (res.status === 200) {
            window.location.href = '/dashboard';
        } else {
            return res.json().then(response => {
                alert(response.message || 'Error en el registro');
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema con el registro');
    });
});