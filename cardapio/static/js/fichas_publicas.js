// Dados dos pratos
var pratosData = {};

// Funções
function mostrarPratos(categoriaId, categoriaNome, categoriaCor) {
    console.log('Função mostrarPratos chamada com:', categoriaId, categoriaNome);
    console.log('Dados disponíveis:', pratosData);
    
    document.getElementById('categoriasSection').style.display = 'none';
    document.getElementById('pratosSection').style.display = 'block';
    document.getElementById('pratosTitle').textContent = categoriaNome;
    
    var pratosGrid = document.getElementById('pratosGrid');
    pratosGrid.innerHTML = '';
    
    var pratos = pratosData[categoriaId] || [];
    console.log('Pratos encontrados:', pratos);
    
    if (pratos.length === 0) {
        pratosGrid.innerHTML = '<p style="text-align: center; color: var(--text-secondary); padding: 40px;">Nenhum prato encontrado nesta categoria.</p>';
        return;
    }
    
    for (var i = 0; i < pratos.length; i++) {
        var prato = pratos[i];
        var pratoCard = document.createElement('div');
        pratoCard.className = 'prato-card';
        pratoCard.innerHTML = 
            '<img src="' + prato.imagem + '" alt="' + prato.nome + '" class="prato-image" onerror="this.src=\'https://via.placeholder.com/400x200?text=Sem+Imagem\'">' +
            '<div class="prato-content">' +
                '<div class="prato-header">' +
                    '<h3 class="prato-name">' + prato.nome + '</h3>' +
                    '<span class="prato-price">R$ ' + prato.preco.toFixed(2) + '</span>' +
                '</div>' +
                '<p class="prato-description">' + prato.descricao + '</p>' +
                '<div class="prato-meta">' +
                    '<div class="meta-item"><i class="bi bi-fire"></i><span>' + prato.calorias + ' cal</span></div>' +
                    '<div class="meta-item"><i class="bi bi-clock"></i><span>' + prato.tempo_preparo + ' min</span></div>' +
                    (prato.vegetariano ? '<div class="meta-item"><i class="bi bi-leaf"></i><span>Vegetariano</span></div>' : '') +
                    (prato.vegano ? '<div class="meta-item"><i class="bi bi-tree"></i><span>Vegano</span></div>' : '') +
                    (prato.sem_gluten ? '<div class="meta-item"><i class="bi bi-shield-check"></i><span>Sem Glúten</span></div>' : '') +
                    (prato.sem_lactose ? '<div class="meta-item"><i class="bi bi-droplet"></i><span>Sem Lactose</span></div>' : '') +
                '</div>' +
                '<button class="ficha-btn" onclick="abrirFicha(' + prato.id + ')">' +
                    '<i class="bi bi-clipboard-data"></i> Ver Ficha Técnica' +
                '</button>' +
            '</div>';
        pratosGrid.appendChild(pratoCard);
    }
}

function testeCategoria() {
    console.log('Teste de categoria funcionando!');
    mostrarPratos(1, 'Teste', '#ff6b6b');
}

function voltarCategorias() {
    document.getElementById('pratosSection').style.display = 'none';
    document.getElementById('categoriasSection').style.display = 'block';
}

function pesquisarPratos() {
    var query = document.getElementById('pesquisaInput').value.trim();
    if (query.length < 2) {
        alert('Digite pelo menos 2 caracteres para pesquisar.');
        return;
    }
    console.log('Pesquisando por:', query);
}

function abrirFicha(pratoId) {
    console.log('Abrindo ficha do prato:', pratoId);
}

function fecharFicha() {
    document.getElementById('fichaModal').classList.remove('active');
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM carregado, funções definidas');
});
