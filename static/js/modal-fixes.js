/**
 * Remoção de backdrop dos modais
 * Este arquivo desabilita completamente o backdrop dos modais Bootstrap
 */

// Função para remover todos os backdrops
function removeAllBackdrops() {
  const backdrops = document.querySelectorAll('.modal-backdrop');
  backdrops.forEach(backdrop => backdrop.remove());
}

// Função para forçar fechamento de modal
function forceCloseModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    const modalInstance = bootstrap.Modal.getInstance(modal);
    if (modalInstance) {
      modalInstance.hide();
    } else {
      $(modal).modal('hide');
    }
  }
  
  // Remover backdrops
  removeAllBackdrops();
  
  // Remover classes do body
  document.body.classList.remove('modal-open');
  document.body.style.paddingRight = '';
}

// Função de emergência para fechar todos os modais
function forceCloseAllModals() {
  $('.modal').modal('hide');
  removeAllBackdrops();
  document.body.classList.remove('modal-open');
  document.body.style.paddingRight = '';
}

// Função para verificar se há modais abertos
function hasOpenModals() {
  return document.querySelectorAll('.modal.show').length > 0;
}

// Inicializar remoção de backdrop quando o documento estiver pronto
$(document).ready(function() {
  // Remover backdrops quando qualquer modal for aberto
  $('.modal').on('show.bs.modal', function() {
    removeAllBackdrops();
  });

  // Remover backdrops quando qualquer modal for fechado
  $('.modal').on('hidden.bs.modal', function() {
    removeAllBackdrops();
    document.body.classList.remove('modal-open');
    document.body.style.paddingRight = '';
  });

  // Adicionar tecla de escape para fechar modais
  $(document).on('keydown', function(e) {
    if (e.key === 'Escape') {
      $('.modal.show').modal('hide');
    }
  });

  // Remover backdrops periodicamente
  setInterval(function() {
    removeAllBackdrops();
  }, 500);

  // Remover backdrops quando a janela ganhar foco
  $(window).on('focus', function() {
    removeAllBackdrops();
  });
});

// Função para abrir modal com segurança
function safeOpenModal(modalId) {
  // Fechar todos os modais abertos primeiro
  $('.modal.show').modal('hide');
  
  // Aguardar um pouco e então abrir o novo modal
  setTimeout(function() {
    $('#' + modalId).modal('show');
  }, 150);
}

// Função para fechar modal com segurança
function safeCloseModal(modalId) {
  const modal = $('#' + modalId);
  if (modal.length > 0) {
    modal.modal('hide');
    removeAllBackdrops();
  }
}

// Exportar funções para uso global
window.modalFixes = {
  removeAllBackdrops: removeAllBackdrops,
  forceCloseModal: forceCloseModal,
  forceCloseAllModals: forceCloseAllModals,
  hasOpenModals: hasOpenModals,
  safeOpenModal: safeOpenModal,
  safeCloseModal: safeCloseModal
};

// Função de emergência global
window.forceCloseModal = forceCloseAllModals; 