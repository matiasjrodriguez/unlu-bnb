document.getElementById('signupForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        role: parseInt(document.getElementById('role').value)
    };

    fetch('/api/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => {
        return res.json().then(response=> {
            if (res.status === 200) {
                if (response.rol === 1) {
                    window.location.href = '/feed';
                } else {
                    window.location.href = '/dashboard';
                }
            } else {
                alert(response.message || 'Error en el registro');
            }
        }

        )
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema con el registro');
    });
});