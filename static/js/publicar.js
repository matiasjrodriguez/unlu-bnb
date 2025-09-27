document.getElementById('publicarForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
        titulo: document.getElementById('titulo').value,
        descripcion: document.getElementById('descripcion').value,
        barrio: document.getElementById('barrio').value,
        calle: document.getElementById('calle').value,
        ambientes: parseInt(document.getElementById('ambientes').value),
        balcon: parseInt(document.getElementById('balcon').value),
        precio: parseInt(document.getElementById('precio').value)
    };

    fetch('/api/publicar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(response => {
        alert(response.message || 'Publicación creada con éxito');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al crear la publicación');
    });
});
