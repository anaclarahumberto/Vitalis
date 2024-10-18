function mascararTelefone(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 11) valor = valor.substr(0, 11);
    if (valor.length > 10) {
        valor = valor.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3");
    } else if (valor.length > 6) {
        valor = valor.replace(/^(\d{2})(\d{4})(\d{0,4})$/, "($1) $2-$3");
    } else if (valor.length > 2) {
        valor = valor.replace(/^(\d{2})(\d{0,5})$/, "($1) $2");
    } else {
        valor = valor.replace(/^(\d*)$/, "($1");
    }
    input.value = valor;
}

function mascararCPF(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 11) valor = valor.substr(0, 11);
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
    if (valor.length == 13) {
        valor = valor.replace(/(\d{3})(\d{2})$/, "$1-$2");
    } else {
        valor = valor.replace(/(\d{3})(\d{1})$/, "$1-$2");
    }
    input.value = valor;
}

function mascararCNPJ(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 14) valor = valor.substr(0, 14);
    valor = valor.replace(/^(\d{2})(\d)/, "$1.$2");
    valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
    valor = valor.replace(/\.(\d{3})(\d)/, ".$1/$2");
    valor = valor.replace(/(\d{4})(\d)/, "$1-$2");
    input.value = valor;
}

function mascararCNS(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, ""); // Remove tudo que não for dígito
    if (valor.length > 15) valor = valor.substr(0, 15); // Limita a 15 dígitos
    valor = valor.replace(/(\d{3})(\d)/, "$1 $2"); // Adiciona um espaço após os primeiros 3 dígitos
    valor = valor.replace(/(\d{3}) (\d{3})(\d)/, "$1 $2 $3"); // Adiciona espaço após o segundo bloco de 3 dígitos
    valor = valor.replace(/(\d{3}) (\d{3}) (\d{3})(\d)/, "$1 $2 $3 $4"); // Adiciona espaço após o terceiro bloco
    valor = valor.replace(/(\d{3}) (\d{3}) (\d{3}) (\d{3})(\d)/, "$1 $2 $3 $4 $5"); // Adiciona espaço após o quarto bloco
    input.value = valor; // Atualiza o valor do input
}

function mascararReg(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 6) {
        valor = valor.substr(0, 6);
    }
    input.value = valor;
}

function mascararCEP(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 8) valor = valor.substr(0, 8);
    valor = valor.replace(/(\d{5})(\d)/, "$1-$2");
    input.value = valor;
}

function mascararCartao(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 16) valor = valor.substr(0, 16);
    valor = valor.replace(/(\d{4})(\d)/, "$1 $2");
    valor = valor.replace(/(\d{4}) (\d{4})(\d)/, "$1 $2 $3");
    valor = valor.replace(/(\d{4}) (\d{4}) (\d{4})(\d)/, "$1 $2 $3 $4");
    input.value = valor;
}

function mascararMesAno(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 4) valor = valor.substr(0, 4);
    valor = valor.replace(/(\d{2})(\d)/, "$1/$2");
    input.value = valor;
}
function mascararMesAnoMaior(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 6) valor = valor.substr(0, 6);
    valor = valor.replace(/(\d{2})(\d)/, "$1/$2");
    input.value = valor;
}

function mascararData(input) {
    let valor = input.value;
    valor = valor.replace(/\D/g, "");
    if (valor.length > 8) valor = valor.substr(0, 8);
    valor = valor.replace(/(\d{2})(\d)/, "$1/$2");
    valor = valor.replace(/(\d{2})(\d)/, "$1/$2");
    input.value = valor;
}

function mascararNome(input) {
    let valor = input.value;
    valor = valor.replace(/[^a-zA-ZÀ-ú\s]/g, "");
    let preposicoes = ["de", "do", "da", "das", "dos"];
    let palavras = valor.split(" ");
    for (let i = 0; i < palavras.length; i++) {
        if (preposicoes.indexOf(palavras[i].toLowerCase()) === -1) {
            palavras[i] = palavras[i].charAt(0).toUpperCase() + palavras[i].substring(1).toLowerCase();
        } else {
            palavras[i] = palavras[i].toLowerCase();
        }
    }
    valor = palavras.join(" ");
    input.value = valor;
}

function mascararEndereco(input) {
    let valor = input.value;
    // Permite também dígitos (0-9)
    valor = valor.replace(/[^a-zA-ZÀ-ú0-9\s]/g, "");
    let preposicoes = ["de", "do", "da", "das", "dos"];
    let palavras = valor.split(" ");
    for (let i = 0; i < palavras.length; i++) {
        if (preposicoes.indexOf(palavras[i].toLowerCase()) === -1) {
            palavras[i] = palavras[i].charAt(0).toUpperCase() + palavras[i].substring(1).toLowerCase();
        } else {
            palavras[i] = palavras[i].toLowerCase();
        }
    }
    valor = palavras.join(" ");
    input.value = valor;
}


function aplicarMascaras() {
    const inputs = document.querySelectorAll('input[data-mask]');
    inputs.forEach(input => {
        const maskType = input.getAttribute('data-mask');
        input.addEventListener('input', () => {
            switch (maskType) {
                case 'telefone':
                    mascararTelefone(input);
                    break;
                case 'cpf':
                    mascararCPF(input);
                    break;
                case 'cnpj':
                    mascararCNPJ(input);
                    break;
                case 'cns':
                    mascararCNS(input);
                    break;
                case 'reg':
                    mascararReg(input);
                    break;
                case 'cep':
                    mascararCEP(input);
                    break;
                case 'cartao':
                    mascararCartao(input);
                    break;
                case 'mes_ano':
                    mascararMesAno(input);
                    break;
                case 'mes_ano_maior':
                    mascararMesAnoMaior(input);
                    break;
                case 'data':
                    mascararData(input);
                    break;
                case 'nome':
                    mascararNome(input);
                    break;
                case 'endereco':
                    mascararEndereco(input);
                    break;
            }
        });
    });
}

aplicarMascaras();