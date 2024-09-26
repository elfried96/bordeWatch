// Ouvrir le sélecteur de fichier lorsque l'utilisateur clique sur "Select Image"
document.querySelector('.select-image').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

// Prévisualiser l'image sélectionnée
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.size < 2 * 1024 * 1024) { // Limite de taille : 2MB
        const reader = new FileReader();
        reader.onload = function(e) {
            document.querySelector('.img-area').style.backgroundImage = `url(${e.target.result})`;
            document.querySelector('.img-area').innerHTML = ''; // Supprime l'icône et le texte
        };
        reader.readAsDataURL(file);
    } else {
        alert('L\'image doit faire moins de 2MB');
    }
});
