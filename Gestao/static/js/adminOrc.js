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
                
                // Formatar para o padrão esperado pelo Django (YYYY-MM)
                var dataFormatada = anoAtual + '-' + (mesAtual < 10 ? '0' + mesAtual : mesAtual);
                
                // Verificar se já existe um parâmetro de data na URL
                var urlParams = new URLSearchParams(window.location.search);
                var dataParam = urlParams.get('data__year') || urlParams.get('data__month') || urlParams.get('data__day');
                
                // Se não há parâmetro de data na URL, redirecionar para o mês atual
                if (!dataParam) {
                    var novaUrl = window.location.pathname + '?data__year=' + anoAtual + '&data__month=' + mesAtual;
                    window.location.href = novaUrl;
                }
            }
        }

        // Função para formatar valores em inputs da coluna 4
        function formatarInputsColuna4() {
            var tabela = document.getElementById('result_list');
            if (!tabela) return;
            
            var linhas = tabela.querySelectorAll('tbody tr');
            
            linhas.forEach(function(linha) {
                var colunas = linha.querySelectorAll("td");
                if (colunas[4]) {
                    // Procurar por inputs dentro da coluna 4
                    var inputs = colunas[4].querySelectorAll('input[type="text"], input[type="number"]');
                    
                    inputs.forEach(function(input) {
                        // Verificar se já foi formatado
                        if (input.classList.contains('valor-input')) {
                            return; // Já foi formatado, pular
                        }
                        
                        // Converter para input text para evitar validação numérica
                        input.type = 'text';
                        
                        // Remover atributos de validação HTML5
                        input.removeAttribute('min');
                        input.removeAttribute('max');
                        input.removeAttribute('step');
                        input.removeAttribute('pattern');
                        input.setAttribute('novalidate', 'true');
                        
                        // Definir largura diretamente
                        input.style.width = '200px';
                        input.style.height = '35px';
                        input.style.fontSize = '14px';
                        input.style.padding = '6px 12px';
                        input.style.boxSizing = 'border-box';
                        
                        // Aplicar formatação automática no input - APENAS se não estiver vazio
                        if (input.value && input.value.trim() !== '' && input.value !== '0') {
                            // Verificar se já está formatado
                            if (!/^-?\d{1,3}(\.\d{3})*,\d{2}$/.test(input.value)) {
                                aplicarFormatacaoInput(input);
                                
                                // Formatar o valor atual se existir (apenas se não estiver vazio)
                                var valorFormatado = formatarValorMonetario(input.value);
                                input.value = valorFormatado;
                            }
                        } else {
                            // Se está vazio, apenas aplicar formatação básica
                            aplicarFormatacaoInput(input);
                        }
                        
                        // Adicionar classe para estilização
                        input.classList.add('valor-input');
                    });
                }
            });
        }

        // Função para debug - verificar valores antes do envio
        function debugValoresAntesEnvio() {
            var inputsValor = document.querySelectorAll('input[data-tipo="valor"], .valor-input');
            console.log('=== DEBUG: Valores antes do envio ===');
            
            inputsValor.forEach(function(input, index) {
                var valorOriginal = input.value;
                var valorConvertido = converterValorFormatado(valorOriginal);
                console.log(`Input ${index + 1}: "${valorOriginal}" -> ${valorConvertido}`);
            });
            console.log('=== FIM DEBUG ===');
        }

        // Função para formatar colunas conta
        function formatarColunasConta() {
            var tabela = document.getElementById('result_list');
            if (!tabela) return;
            
            var linhas = tabela.querySelectorAll('tbody tr');
            
            linhas.forEach(function(linha) {
                var colunas = linha.querySelectorAll("td");
                
                // Formatar coluna conta (3ª coluna - índice 2)
                if (colunas[2]) {
                    formatarCelulaTexto(colunas[2], 'conta-texto');
                }
            });
        }

        // Função auxiliar para formatar células de texto
        function formatarCelulaTexto(celula, classeTexto) {
            // Verificar se já tem formatação aplicada
            if (celula.classList.contains('texto-formatado')) {
                return;
            }
            
            // Obter o texto da célula
            var textoOriginal = celula.textContent.trim();
            
            if (textoOriginal && textoOriginal.length > 0) {
                // Criar elemento span para o texto
                var spanTexto = document.createElement('span');
                spanTexto.className = classeTexto;
                spanTexto.textContent = textoOriginal;
                spanTexto.title = textoOriginal; // Tooltip com texto completo
                
                // Limpar a célula e adicionar o span formatado
                celula.innerHTML = '';
                celula.appendChild(spanTexto);
                
                // Marcar como formatado
                celula.classList.add('texto-formatado');
            }
        }

        // Função para lidar com o Django admin changelist
        function configurarAdminChangelist() {
            // Interceptar o envio do formulário de mudança em lote
            var formChangelist = document.querySelector('#changelist-form');
            if (formChangelist) {
                formChangelist.addEventListener('submit', function(e) {
                    var inputsValor = this.querySelectorAll('input[data-tipo="valor"], .valor-input');
                    if (inputsValor.length > 0) {
                        console.log('Formulário changelist - convertendo valores...');
                        converterValoresAntesEnvio();
                    }
                });
            }
            
            // Interceptar cliques nos botões de ação
            var botoesAcao = document.querySelectorAll('input[type="submit"][value="Salvar"]');
            botoesAcao.forEach(function(botao) {
                botao.addEventListener('click', function(e) {
                    var form = this.closest('form');
                    if (form) {
                        var inputsValor = form.querySelectorAll('input[data-tipo="valor"], .valor-input');
                        if (inputsValor.length > 0) {
                            console.log('Botão Salvar do changelist - convertendo valores...');
                            converterValoresAntesEnvio();
                        }
                    }
                });
            });
        }

        // Função para converter valores formatados antes do envio
        function converterValoresAntesEnvio() {
            var inputsValor = document.querySelectorAll('input[data-tipo="valor"], .valor-input');
            
            // Debug dos valores
            debugValoresAntesEnvio();
            
            inputsValor.forEach(function(input) {
                if (input.value && input.value.trim() !== '') {
                    try {
                        var numero = converterValorFormatado(input.value);
                        
                        // Verificar se o número é válido
                        if (!isNaN(numero)) {
                            // Atualizar o valor do input original com o número
                            // Usar conversão direta para evitar problemas com toString
                            if (numero === Math.floor(numero)) {
                                // Se é um número inteiro
                                input.value = Math.floor(numero);
                            } else {
                                // Se é um número decimal
                                input.value = numero;
                            }
                            
                            // Remover formatação temporariamente
                            input.classList.remove('valor-input');
                            input.classList.add('valor-temp');
                            
                            console.log('Valor convertido:', input.name, numero);
                        } else {
                            console.warn('Valor inválido encontrado:', input.value);
                        }
                    } catch (error) {
                        console.error('Erro ao converter valor:', input.value, error);
                        // Em caso de erro, manter o valor original
                    }
                } else {
                    // Se o campo está vazio, definir como 0
                    input.value = 0;
                    input.classList.remove('valor-input');
                    input.classList.add('valor-temp');
                }
            });
        }

        // Função para restaurar inputs após envio
        function restaurarInputsAposEnvio() {
            var inputsTemp = document.querySelectorAll('input.valor-temp');
            
            inputsTemp.forEach(function(input) {
                // Restaurar classe original
                input.classList.remove('valor-temp');
                input.classList.add('valor-input');
                
                // Reaplicar formatação se necessário - APENAS se não estiver vazio
                if (input.value && input.value !== '0' && input.value !== 0) {
                    try {
                        // Verificar se já está formatado
                        if (!/^-?\d{1,3}(\.\d{3})*,\d{2}$/.test(input.value)) {
                            var valorFormatado = formatarValorMonetario(input.value);
                            input.value = valorFormatado;
                        }
                    } catch (error) {
                        console.error('Erro ao restaurar formatação:', error);
                    }
                }
            });
        }

        // Função para prevenir validação HTML5 em inputs de valor
        function prevenirValidacaoHTML5() {
            // Interceptar evento invalid para inputs de valor
            document.addEventListener('invalid', function(e) {
                var input = e.target;
                if (input.classList.contains('valor-input') || input.getAttribute('data-tipo') === 'valor') {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }
            }, true);
            
            // Interceptar evento beforeinput para inputs de valor
            document.addEventListener('beforeinput', function(e) {
                var input = e.target;
                if (input.classList.contains('valor-input') || input.getAttribute('data-tipo') === 'valor') {
                    // Permitir apenas entrada de números, vírgula, ponto e hífen
                    if (e.data && !/^[\d,\.\-]$/.test(e.data)) {
                        e.preventDefault();
                        return false;
                    }
                }
            }, true);
            
            // Desabilitar validação em formulários que contêm inputs de valor
            var forms = document.querySelectorAll('form');
            forms.forEach(function(form) {
                var inputsValor = form.querySelectorAll('.valor-input, input[data-tipo="valor"]');
                if (inputsValor.length > 0) {
                    form.setAttribute('novalidate', 'true');
                }
            });
        }

        // Inicializar funcionalidades
        configurarDateHierarchyMesAtual();
        formatarInputsColuna4();
        formatarColunasConta();
        configurarAdminChangelist();

        // Adicionar event listeners para formulários
        document.addEventListener('submit', function(e) {
            // Verificar se é um formulário que contém inputs de valor
            var form = e.target;
            var inputsValor = form.querySelectorAll('input[data-tipo="valor"], .valor-input');
            
            if (inputsValor.length > 0) {
                console.log('Convertendo valores antes do envio...');
                converterValoresAntesEnvio();
                
                // Pequeno delay para garantir que a conversão seja aplicada
                setTimeout(function() {
                    console.log('Enviando formulário...');
                }, 50);
            }
        });
        
        // Adicionar event listener específico para o formulário de mudança em lote
        document.addEventListener('click', function(e) {
            if (e.target && e.target.type === 'submit' && e.target.value === 'Salvar') {
                var form = e.target.closest('form');
                if (form) {
                    var inputsValor = form.querySelectorAll('input[data-tipo="valor"], .valor-input');
                    if (inputsValor.length > 0) {
                        console.log('Botão Salvar clicado - convertendo valores...');
                        converterValoresAntesEnvio();
                    }
                }
            }
        });
        
        // Restaurar inputs após carregamento da página (caso de redirecionamento)
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                restaurarInputsAposEnvio();
            }, 100);
        });
        
        // Restaurar inputs após mudanças via AJAX
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    setTimeout(function() {
                        restaurarInputsAposEnvio();
                        formatarColunasConta();
                    }, 100);
                }
            });
        });
        
        // Observar mudanças no documento
        observer.observe(document.body, { childList: true, subtree: true });

        // Prevenir validação HTML5
        prevenirValidacaoHTML5();
        
        // Aplicar formatação inicial após um pequeno delay
        setTimeout(function() {
            formatarColunasConta();
        }, 200);
    });
})(django.jQuery);
