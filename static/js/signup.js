document.getElementById('signupForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        username: document.getElementById('username').value,
        role: parseInt(document.getElementById('role').value)
    };

    fetch('/api/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(response => {
        alert(response.message || 'Registro exitoso');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un problema con el registro');
    });
});