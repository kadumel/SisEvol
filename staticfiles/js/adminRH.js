(function($) {
    $(document).ready(function() {

        // Função para configurar date_hierarchy para o mês atual
        function configurarDateHierarchyMesAtual() {
            // Verificar se existe date_hierarchy na página
            var dateHierarchy = $('.date-hierarchy');
            if (dateHierarchy.length > 0) {
                // Obter o mês e ano atual
                var hoje = new Date();
                var mesAtual = hoje.getMonth() + 1; // getMonth() retorna 0-11
                var anoAtual = hoje.getFullYear();
                
                // Verificar se já existe um parâmetro de data na URL
                var urlParams = new URLSearchParams(window.location.search);
                var dataParam = urlParams.get('data__year') || urlParams.get('data__month') || urlParams.get('data__day');
                var diaEventoParam = urlParams.get('dia_evento__data__year') || urlParams.get('dia_evento__data__month') || urlParams.get('dia_evento__data__day');
                
                // Se não há parâmetro de data na URL, redirecionar para o mês atual
                if (!dataParam && !diaEventoParam) {
                    var novaUrl = window.location.pathname + '?data__year=' + anoAtual + '&data__month=' + mesAtual;
                    window.location.href = novaUrl;
                }
            }
        }

        // Inicializar funcionalidades
        configurarDateHierarchyMesAtual();
        
    });
})(django.jQuery); 