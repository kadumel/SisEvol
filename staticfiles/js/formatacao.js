/**
 * Funções utilitárias para formatação de valores monetários
 */

// Função principal para formatar valor monetário com ponto de milhar e vírgula decimal
function formatarValorMonetario(valor) {
    if (valor === null || valor === undefined || valor === '') {
        return '0,00';
    }
    
    // Converter para string se não for
    var valorStr = valor.toString().trim();
    
    // Se já está formatado corretamente, retornar como está
    if (/^-?\d{1,3}(\.\d{3})*,\d{2}$/.test(valorStr)) {
        return valorStr;
    }
    
    // Se é apenas um número simples (sem formatação), formatar diretamente
    if (/^-?\d+$/.test(valorStr)) {
        return formatarNumeroSimples(valorStr);
    }
    
    // Se é um número decimal simples (ex: 123.45), formatar
    if (/^-?\d+\.\d+$/.test(valorStr)) {
        return formatarNumeroDecimal(valorStr);
    }
    
    // Verificar se é um valor negativo
    var isNegativo = valorStr.startsWith('-');
    
    // Remover o sinal negativo temporariamente para processamento
    if (isNegativo) {
        valorStr = valorStr.substring(1);
    }
    
    // Limpar o valor - remover caracteres não numéricos exceto vírgula e ponto
    valorStr = valorStr.replace(/[^\d,\.]/g, '');
    
    // Se não há números, retornar zero
    if (!/\d/.test(valorStr)) {
        return '0,00';
    }
    
    // Processar vírgulas e pontos
    var numero;
    
    // Se há vírgula, usar como separador decimal
    if (valorStr.includes(',')) {
        var partes = valorStr.split(',');
        var parteInteira = partes[0].replace(/\./g, ''); // Remover pontos da parte inteira
        var parteDecimal = partes[1] || '00';
        
        // Limitar parte decimal a 2 dígitos - EVITAR padEnd
        if (parteDecimal.length === 1) {
            parteDecimal = parteDecimal + '0';
        } else if (parteDecimal.length > 2) {
            parteDecimal = parteDecimal.substring(0, 2);
        }
        
        numero = parseFloat(parteInteira + '.' + parteDecimal);
    } else {
        // Se não há vírgula, tratar pontos como separadores de milhar
        var valorLimpo = valorStr.replace(/\./g, '');
        numero = parseFloat(valorLimpo);
    }
    
    // Verificar se é um número válido
    if (isNaN(numero)) {
        return '0,00';
    }
    
    // Aplicar sinal negativo se necessário
    if (isNegativo) {
        numero = -numero;
    }
    
    // Usar formatação manual para garantir o ponto de milhar
    return formatarValorManual(numero);
}

// Função para formatar números simples (inteiros)
function formatarNumeroSimples(numeroStr) {
    var isNegativo = numeroStr.startsWith('-');
    var numero = Math.abs(parseInt(numeroStr));
    
    var numeroFormatado = numero.toString();
    var resultado = '';
    
    // Adicionar pontos de milhar
    for (var i = numeroFormatado.length - 1, j = 0; i >= 0; i--, j++) {
        if (j > 0 && j % 3 === 0) {
            resultado = '.' + resultado;
        }
        resultado = numeroFormatado[i] + resultado;
    }
    
    resultado = resultado + ',00';
    
    if (isNegativo) {
        resultado = '-' + resultado;
    }
    
    return resultado;
}

// Função para formatar números decimais
function formatarNumeroDecimal(numeroStr) {
    var isNegativo = numeroStr.startsWith('-');
    var partes = numeroStr.split('.');
    var parteInteira = Math.abs(parseInt(partes[0]));
    var parteDecimal = partes[1] || '00';
    
    // Garantir 2 dígitos decimais
    if (parteDecimal.length === 1) {
        parteDecimal = parteDecimal + '0';
    } else if (parteDecimal.length > 2) {
        parteDecimal = parteDecimal.substring(0, 2);
    }
    
    var numeroFormatado = parteInteira.toString();
    var resultado = '';
    
    // Adicionar pontos de milhar
    for (var i = numeroFormatado.length - 1, j = 0; i >= 0; i--, j++) {
        if (j > 0 && j % 3 === 0) {
            resultado = '.' + resultado;
        }
        resultado = numeroFormatado[i] + resultado;
    }
    
    resultado = resultado + ',' + parteDecimal;
    
    if (isNegativo) {
        resultado = '-' + resultado;
    }
    
    return resultado;
}

// Função manual para formatação com ponto de milhar (mais confiável)
function formatarValorManual(valor) {
    if (valor === null || valor === undefined || valor === '') {
        return '0,00';
    }
    
    var numero = typeof valor === 'string' ? parseFloat(valor.replace(/\./g, '').replace(',', '.')) : parseFloat(valor);
    
    if (isNaN(numero)) {
        return '0,00';
    }
    
    // Verificar se é negativo
    var isNegativo = numero < 0;
    if (isNegativo) {
        numero = Math.abs(numero);
    }
    
    // Formatação manual com ponto de milhar - EVITAR toFixed
    var numeroStr = numero.toString();
    var partes = numeroStr.split('.');
    var parteInteira = partes[0];
    var parteDecimal = partes[1] || '00';
    
    // Garantir que parte decimal tenha 2 dígitos
    if (parteDecimal.length === 1) {
        parteDecimal = parteDecimal + '0';
    } else if (parteDecimal.length > 2) {
        parteDecimal = parteDecimal.substring(0, 2);
    }
    
    // Adicionar pontos de milhar
    var parteInteiraFormatada = '';
    for (var i = parteInteira.length - 1, j = 0; i >= 0; i--, j++) {
        if (j > 0 && j % 3 === 0) {
            parteInteiraFormatada = '.' + parteInteiraFormatada;
        }
        parteInteiraFormatada = parteInteira[i] + parteInteiraFormatada;
    }
    
    var resultado = parteInteiraFormatada + ',' + parteDecimal;
    
    // Adicionar sinal negativo se necessário
    if (isNegativo) {
        resultado = '-' + resultado;
    }
    
    return resultado;
}

// Função para converter valor formatado de volta para número
function converterValorFormatado(valorFormatado) {
    if (!valorFormatado) {
        return 0;
    }
    
    try {
        var valorStr = valorFormatado.toString().trim();
        
        // Se já é um número simples, retornar diretamente
        if (/^-?\d+(\.\d+)?$/.test(valorStr)) {
            return parseFloat(valorStr);
        }
        
        // Verificar se é negativo
        var isNegativo = valorStr.startsWith('-');
        if (isNegativo) {
            valorStr = valorStr.substring(1);
        }
        
        // Remover pontos de milhar e substituir vírgula por ponto
        var valorNumerico = valorStr.replace(/\./g, '').replace(',', '.');
        var numero = parseFloat(valorNumerico);
        
        // Verificar se é um número válido
        if (isNaN(numero)) {
            console.warn('Valor inválido convertido para 0:', valorFormatado);
            return 0;
        }
        
        // Aplicar sinal negativo se necessário
        if (isNegativo) {
            numero = -numero;
        }
        
        return numero;
    } catch (error) {
        console.error('Erro ao converter valor formatado:', valorFormatado, error);
        return 0;
    }
}

// Função para formatar valores em uma tabela
function formatarValoresTabela(seletorTabela, indiceColuna) {
    var tabela = document.querySelector(seletorTabela);
    if (!tabela) return;
    
    var linhas = tabela.querySelectorAll('tbody tr');
    
    linhas.forEach(function(linha) {
        var colunas = linha.querySelectorAll("td");
        if (colunas[indiceColuna] && colunas[indiceColuna].innerText) {
            var valorOriginal = colunas[indiceColuna].innerText;
            var valorFormatado = formatarValorMonetario(valorOriginal);
            colunas[indiceColuna].innerText = valorFormatado;
            
            // Adicionar classe para estilização
            colunas[indiceColuna].classList.add('valor-formatado');
        }
    });
}

// Função melhorada para aplicar formatação em tempo real em inputs
function aplicarFormatacaoInput(input) {
    // Definir o input como texto para evitar validação numérica
    input.type = 'text';
    
    // Remover atributos que podem causar validação
    input.removeAttribute('min');
    input.removeAttribute('max');
    input.removeAttribute('step');
    
    // Formatar valor inicial se existir - APENAS se não estiver vazio
    if (input.value && input.value.trim() !== '') {
        // Verificar se já está formatado
        if (!/^-?\d{1,3}(\.\d{3})*,\d{2}$/.test(input.value)) {
            var valorInicial = converterValorFormatado(input.value);
            if (valorInicial !== 0) {
                input.value = formatarValorMonetario(valorInicial);
            }
        }
    }
    
    // Evento de digitação - MANTER SIMPLES
    input.addEventListener('input', function(e) {
        var valor = e.target.value;
        
        // Permitir apenas números, vírgula, ponto e sinal negativo
        valor = valor.replace(/[^\d,\.\-]/g, '');
        
        // Verificar se há sinal negativo
        var isNegativo = valor.startsWith('-');
        if (isNegativo) {
            valor = valor.substring(1);
        }
        
        // Se há mais de uma vírgula, manter apenas a primeira
        var virgulas = (valor.match(/,/g) || []).length;
        if (virgulas > 1) {
            var partes = valor.split(',');
            valor = partes[0] + ',' + partes.slice(1).join('');
        }
        
        // Se há mais de um ponto, manter apenas os pontos de milhar
        var pontos = (valor.match(/\./g) || []).length;
        if (pontos > 1) {
            // Remover todos os pontos e adicionar apenas os de milhar
            var semPontos = valor.replace(/\./g, '');
            if (semPontos.length > 3) {
                var formatada = '';
                for (var i = semPontos.length - 1, j = 0; i >= 0; i--, j++) {
                    if (j > 0 && j % 3 === 0) {
                        formatada = '.' + formatada;
                    }
                    formatada = semPontos[i] + formatada;
                }
                valor = formatada;
            } else {
                valor = semPontos;
            }
        }
        
        // Recolocar sinal negativo se necessário
        if (isNegativo) {
            valor = '-' + valor;
        }
        
        e.target.value = valor;
    });
    
    // Formatar ao perder o foco - APENAS se necessário
    input.addEventListener('blur', function(e) {
        var valor = e.target.value;
        if (valor && valor.trim() !== '') {
            // Verificar se já está formatado corretamente
            if (!/^-?\d{1,3}(\.\d{3})*,\d{2}$/.test(valor)) {
                var numero = converterValorFormatado(valor);
                if (numero !== 0) {
                    e.target.value = formatarValorMonetario(numero);
                }
            }
        }
    });
    
    // Permitir teclas especiais
    input.addEventListener('keydown', function(e) {
        // Permitir: backspace, delete, tab, escape, enter, ctrl+a, ctrl+c, ctrl+v, ctrl+x
        var teclasPermitidas = [8, 9, 27, 13, 46]; // backspace, tab, escape, enter, delete
        var ctrlTeclas = [65, 67, 86, 88]; // ctrl+a, ctrl+c, ctrl+v, ctrl+x
        
        if (teclasPermitidas.includes(e.keyCode) || 
            (e.ctrlKey && ctrlTeclas.includes(e.keyCode))) {
            return true;
        }
        
        // Permitir números, vírgula, ponto e sinal negativo
        if ((e.keyCode >= 48 && e.keyCode <= 57) || // números 0-9
            (e.keyCode >= 96 && e.keyCode <= 105) || // números do teclado numérico
            e.keyCode === 188 || // vírgula
            e.keyCode === 190 || // ponto
            e.keyCode === 110 || // ponto do teclado numérico
            e.keyCode === 189 || // hífen/sinal negativo
            e.keyCode === 109) { // hífen do teclado numérico
            return true;
        }
        
        // Bloquear outras teclas
        e.preventDefault();
        return false;
    });
    
    // Adicionar atributo para indicar que é um campo de valor
    input.setAttribute('data-tipo', 'valor');
    input.setAttribute('inputmode', 'decimal');
    
    // Adicionar atributo para evitar validação HTML5
    input.setAttribute('novalidate', 'true');
}

// Função para formatar valores em elementos específicos
function formatarElementosValor(seletor) {
    var elementos = document.querySelectorAll(seletor);
    
    elementos.forEach(function(elemento) {
        if (elemento.innerText) {
            var valorFormatado = formatarValorMonetario(elemento.innerText);
            elemento.innerText = valorFormatado;
            elemento.classList.add('valor-formatado');
        }
    });
}

// Exportar funções para uso global
window.formatarValorMonetario = formatarValorMonetario;
window.formatarValorManual = formatarValorManual;
window.converterValorFormatado = converterValorFormatado;
window.formatarValoresTabela = formatarValoresTabela;
window.aplicarFormatacaoInput = aplicarFormatacaoInput;
window.formatarElementosValor = formatarElementosValor; 