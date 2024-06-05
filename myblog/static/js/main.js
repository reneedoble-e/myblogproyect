document.getElementById('postForm').addEventListener('submit', function(e) {
    e.preventDefault();
    console.log('Formulario enviado')
    const usuario = document.querySelector('h1').textContent.split(' ')[1];
    const titulo = document.getElementById('titulo').value;
    const texto = document.getElementById('texto').value;

    console.log(`Usuario: ${usuario}, Titulo: ${titulo}, Texto: ${texto}`);
   
    fetch(`/posteos/${usuario}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `titulo=${encodeURIComponent(titulo)}&texto=${encodeURIComponent(texto)}`
    })
    .then(response => {
        if (response.ok) {
            console.log('Post creado exitosamente')
            document.getElementById('titulo').value = '';
            document.getElementById('texto').value = '';
            loadPosts();
        } else {
            console.log('Error al crear el post');
        }

    })
    .catch(error => {
        console.error('Error en la solicitud fetch:', error)
    });    
});

    function loadPosts() {
        const usuario = document.querySelector('h1').textContent.split(' ')[1];
        fetch(`/posteos/${usuario}`)
            .then(response => response.json())
            .then(data => {
                console.log('Posts cargados:', data)
                const postsContainer = document.getElementById('postsContainer');
                postsContainer.innerHTML = '';
                data.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.innerHTML = `<h2>${post.titulo}</h2><p>${post.texto}</p>`;
                    postsContainer.appendChild(postElement);

            });
        })
        .catch(error => {
            console.error('Error al cargar los posts:', error)
        })
    }

document.addEventListener('DOMContentLoaded', loadPosts);