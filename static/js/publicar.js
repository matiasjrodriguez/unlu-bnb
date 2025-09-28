document.getElementById('publicarForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const form = document.getElementById('publicarForm');
    const formData = new FormData(form);

    fetch('/api/publicar', {
        method: 'POST',
        body: formData
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
