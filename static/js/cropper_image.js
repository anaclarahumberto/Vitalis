let cropper;

document.getElementById('alterarFoto').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('inputFoto').click();
});

document.getElementById('inputFoto').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.getElementById('imagemParaCorte');
            img.src = e.target.result;
            $('#modalCortar').modal('show'); // Exibe o modal ao carregar a imagem

            if (cropper) {
                cropper.destroy(); // Destrói o cropper anterior, se houver
            }

            // Inicializa o Cropper.js com as opções corretas
            cropper = new Cropper(img, {
                aspectRatio: 1, // Proporção 1:1 para o corte quadrado
                viewMode: 3, // Limita a imagem dentro do canvas
                dragMode: 'move', // Permite mover a imagem
                autoCropArea: 1, // A área de corte ocupará o máximo possível
                cropBoxMovable: false, // Impede o movimento da área de corte
                cropBoxResizable: false, // Impede o redimensionamento da área de corte
                zoomable: true, // Permite o zoom
                movable: true, // Permite mover a imagem
                background: false, // Remove o fundo escuro ao redor
                guides: false, // Remove guias de linha no cropper
                center: false, // Remove a linha central
                highlight: false, // Remove destaque fora da área de corte
                modal: false, // Remove o "escurecimento" ao redor da área de corte
            });
        }
        reader.readAsDataURL(file);
    }
});

document.getElementById('salvarCorte').addEventListener('click', function() {
    // Obtém o canvas da imagem cortada
    const canvas = cropper.getCroppedCanvas({
        width: 300,
        height: 300
    });

    // Converte o canvas para Blob (pode ser enviado ou exibido)
    canvas.toBlob(function(blob) {
        const url = URL.createObjectURL(blob);
        document.getElementById('fotoPerfil').src = url; // Exibe a imagem cortada no perfil
        const fileInput = document.getElementById('foto_perfil_blob');

        // Ler o Blob como Data URL
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function() {
            fileInput.value = reader.result; // Armazenar o Data URL no campo oculto
        };

        $('#modalCortar').modal('hide'); // Fecha o modal ao salvar a imagem cortada
    }, 'image/png', 0.9); // Qualidade da imagem PNG em 90%
});
