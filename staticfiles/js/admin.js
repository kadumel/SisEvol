


(function($) {
    $(document).ready(function() {


                // Pega o token CSRF da meta tag
                var csrfToken = $('meta[name="csrf-token"]').attr('content');

                console.log("Token CSRF:", csrfToken);


        // Função para verificar o status da tarefa
        function verificarStatusTarefa() {
            $.ajax({
                url: '/status_tarefa',  // URL para verificar o status
                type: 'POST',
                data: { teste: 'teste'},
                beforeSend: function(xhr) {
                    // Adiciona o token CSRF ao cabeçalho da requisição
                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                },
                success: function(response) {

                    var tabela = document.getElementById('result_list')
                    var linhas = document.querySelectorAll('tbody tr');

                    // Exibindo o status da tarefa
                    response.forEach(element => {
                        linhas.forEach(linha => {
                            var id = linha.querySelectorAll("th")
                            var colunas = linha.querySelectorAll("td")

                            if (id[0].innerText == element.id) {

                                switch (element.status_processo) {
                                    case 'E':
                                        colunas[4].innerText = 'Executando';

                                        var loadingGif = document.createElement("img");
                                        loadingGif.src = "https://i.gifer.com/ZZ5H.gif"; // URL do GIF
                                        loadingGif.width = 20;
                                        loadingGif.style.marginLeft = "5px"

                                        colunas[4].appendChild(loadingGif)
                                        break;
                                    case 'P':
                                        colunas[4].innerText = 'Parado';
                                        break;
                                    case 'F':
                                        colunas[4].innerText = 'Falhou';
                                        break;
                                    case 'S':
                                        colunas[4].innerText = 'Finalizado';
                                        break;
                                }

                                if (element.inicio != null){
                                    colunas[5].innerText = element.inicio.substring(8,10)+'/'+element.inicio.substring(5,7)+'/'+ element.inicio.substring(0,4)+' '+element.inicio.substring(11,19)
                                }else{
                                    colunas[5].innerText = ''
                                }
                                console.log( 'Hora final - '+element.fim)
                                if (element.fim != null){
                                    colunas[6].innerText = element.fim.substring(8,10)+'/'+element.fim.substring(5,7)+'/'+ element.fim.substring(0,4)+' '+element.fim.substring(11,19)
                                }else{
                                    colunas[6].innerText = ''
                                }
                            }
                        })                              
                    });
                    
                },
                error: function() {
                    console.log('Erro ao verificar o status da tarefa');
                }
            });
        }

        // var tabela = document.getElementById('result_list')
        // var linha = document.getelementbytagName('tr');
        // var tesult = ''

        // Usar setInterval para chamar a função de 5 em 5 segundos
        setInterval(verificarStatusTarefa, 5000);
    });
})(django.jQuery);
