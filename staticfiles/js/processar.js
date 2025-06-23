// TODO: Tenta entender e comentar essa merda
const optionLabel = document.querySelectorAll('.option');
const optionTitleLabel = document.querySelector('.option_title');
const valorFinal = document.querySelectorAll('.valorFinal');
const descontoPagameto = document.querySelectorAll('.desconto_pagamento_cell');
let descontoVistaBool = true;

const DescontosDic = JSON.parse(document.getElementById("descontos-data").textContent);
// document.querySelector('.test').textContent = parseFloat(DescontosDic).toFixed(2);
// document.querySelector('.test').textContent = `- R$ ${DescontosDic.desc_credito_list[0]}`;
var TotalCredito = document.getElementById("total-credito-data").textContent;
var descontoCreditoInit = DescontosDic.desconto_credito;

var vf_check_parcelas = Math.trunc(parseFloat(valorFinal[0].textContent.replace("R$ ", "").replace(",", ".").trim()) / 70);
// document.querySelector('.test').textContent = "cu";

const preco_pagamento_main = document.querySelectorAll(".preco_metodo");

optionLabel.forEach((e, i) => {
    e.addEventListener('input', function () {
        optionLabel.forEach(t => {
            t.classList.remove("selected");

            t.querySelector('.option_title').classList.remove("selected");
            if (t.querySelector('.methods')) {
                t.querySelector('.methods').style.display = "none";
                t.querySelector('.methods > .option_parcelas select').name = "";
                // t.querySelector('.methods > .option_parcelas select').value = "";
            }
            
        });
        e.classList.add("selected");

        // Mostra  os valores "main" dos outros metodos de pagamento
        preco_pagamento_main.forEach(ppm => {
            ppm.style.display = "inline";
        });

        if (e.querySelector('input').value !== "dinheiro") {
            // document.querySelectorAll('.desconto_pagamento_row').forEach(t => {
            //     t.style.display = "none";
            // });
            document.querySelectorAll('.desconto_a_vista_row').forEach(t => {
                t.style.display = "none";
            });
            document.querySelectorAll('.desconto_pagamento_cell').forEach(t => {
                // t.textContent = `- R$ ${String(DescontosDic.desconto_dinheiro).replace(".", ",")}`;
                t.textContent = document.querySelector('.desconto_a_vista_cell').textContent;
            });

            // Esconde os valores "main" do metodo de pagamento selecionado
            preco_pagamento_main[(2 * i)].style.display = "none";
            preco_pagamento_main[((2 * i) + 1)].style.display = "none";
        }
        else {
            document.querySelectorAll('.desconto_pagamento_row').forEach(t => {
                t.style.display = "table-row";
            });
            document.querySelectorAll('.desconto_pagamento_cell').forEach(t => {
                // t.textContent = `- R$ ${String(DescontosDic.desconto_dinheiro).replace(".", ",")}`;
                t.textContent = `- R$ ${String(DescontosDic.desconto_dinheiro + parseFloat(document.querySelector('.desconto_a_vista_cell').textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim())).replace(".", ",")}`;
            });
            // document.querySelectorAll('.desconto_a_vista_row').forEach(t => {
            //     t.style.display = "table-row";
            // });
            
            // e.querySelectorAll('.methods > .option_parcelas select').forEach(t => {
            //     t.value = "1";
            // });
        }
        
        // e.querySelector('.option_title').classList.add("selected");

        valorFinal.forEach(t => {
            t.textContent = e.querySelector('.option_title .total_normal').textContent;
        });

        if (e.querySelector('.methods')) {
            // if (window.getComputedStyle(e.querySelector('.methods')).display === "none") {
            //     e.querySelector('.methods > .option_method input').checked = true;
            // }
            // else {
            //     e.querySelector('.methods > .option_method input').checked = false;
            // }
            e.querySelector('.methods').style.display = "block";

            if (e.querySelector('.methods > .credito  input').checked) {
                // valorFinal.textContent = e.querySelector('.methods > .credito .total_normal').textContent;

                // Fala João (Guilherme ou Marcelo ou Augusto) Pra fazer as parcelas voltarem no pagamento em credito online tu tem que comentar esse if e descomentar a linha embaixo
                if (e.querySelector('.payment_place').textContent === "Pagar na loja") {
                    e.querySelector('.methods > .option_parcelas').style.display = "block";
                }
                // e.querySelector('.methods > .option_parcelas').style.display = "block";
                
                e.querySelector('.methods > .option_parcelas select').name = "parcelas";
                // if (e.querySelector('.payment_place').textContent !== "Pagar na loja") {
                //     e.querySelector('.methods > .option_parcelas select').value = "1";
                // }
                // e.querySelector('.methods > .option_parcelas select').value = "1";

                // document.querySelector('.test').textContent = `${(DescontosDic.desc_credito_list[e.querySelector('.methods > .option_parcelas select').value - 1] * DescontosDic.total_bruto).toFixed(2)}`;
                DescontosDic.desconto_credito = (DescontosDic.desc_credito_list[e.querySelector('.methods > .option_parcelas select').value - 1] * DescontosDic.total_bruto).toFixed(2);

                TotalCredito = parseFloat(TotalCredito) + parseFloat(descontoCreditoInit) - parseFloat(DescontosDic.desconto_credito);
                descontoCreditoInit = DescontosDic.desconto_credito;
                e.querySelector('.methods > .credito .total_credito').textContent = `R$${(parseFloat(TotalCredito).toFixed(2)).replace(".", ",").trim()}`;

                e.querySelector('.methods > .option_parcelas .total_normal').textContent = e.querySelector('.methods > .option_parcelas select').value + "x R$" +  ((parseFloat(e.querySelector('.methods > .credito .total_normal').innerText.replace("R$", "").replace(".", "").replace(",", ".").trim()) / parseFloat(e.querySelector('.methods > .option_parcelas select').value)).toFixed(2)).replace(".", ",");
                
                if (descontoCreditoInit != 0) {
                    document.querySelectorAll('.desconto_pagamento_row').forEach(t => {
                        t.style.display = "table-row";
                    });
                    document.querySelectorAll('.desconto_pagamento_cell').forEach(t => {
                        t.textContent = `- R$ ${DescontosDic.desconto_credito.replace(".", ",")}`;
                    });
                }
                
                // document.querySelectorAll('.desconto_a_vista_row').forEach(t => {
                //     t.style.display = "none";
                // });
                descontoVistaBool = false;

                valorFinal.forEach(t => {
                    t.textContent = e.querySelector('.methods > .credito .total_normal').textContent.replace("R$", "R$ ");
                });
                // if (e.querySelector('.methods > .option_parcelas select').value !== "1") {
                //     document.querySelector('.desconto_a_vista_row').style.display = "none";
                // }
                // else {
                //     document.querySelector('.desconto_a_vista_row').style.display = "table-row";
                // }

                vf_check_parcelas = Math.trunc(parseFloat(valorFinal[0].textContent.replace("R$ ", "").replace(",", ".").trim()) / 70);
                // document.querySelector('.test').textContent = valorFinal[0].textContent.replace("R$ ", "").replace(",", ".").trim() + " " + vf_check_parcelas;
                e.querySelectorAll('.methods > .option_parcelas option').forEach(t =>{
                    if (parseInt(t.value) > vf_check_parcelas){
                        t.style.display = "none";
                    }
                    else {
                        t.style.display = "block";
                    }
                });
                
            }
            else {
                e.querySelector('.methods > .option_parcelas select').value = "1";
                // document.querySelectorAll('.desconto_a_vista_row').forEach(t => {
                //     t.style.display = "table-row";
                // });
                descontoVistaBool = true;

                // TotalCredito = parseFloat(TotalCredito) + parseFloat(descontoCreditoInit) - parseFloat((DescontosDic.desc_credito_list[0] * DescontosDic.total_bruto));
                // e.querySelector('.methods > .credito .total_credito').textContent = `R$${(parseFloat(TotalCredito).toFixed(2)).replace(".", ",").trim()}`;

                e.querySelectorAll('.methods > .option_parcelas').forEach(t => {
                    t.style.display = "none";
                });
            }
        }

        // Olhar melhor pro mobile
        document.getElementById("total_final").value = valorFinal[0].textContent.replace("R$", "").replace(".", "").replace(",", ".").trim()
        let desconto_pagamento_row = document.querySelectorAll('.desconto_pagamento_row');
        if (desconto_pagamento_row[0].style.display === "none") {
            descontoPagameto[0].textContent = "- R$ 0,00";
        }
        if (desconto_pagamento_row[1].style.display === "none") {
            descontoPagameto[1].textContent = "- R$ 0,00";
        }
        // let descontoPagamentoTot = parseFloat(descontoPagameto[0].textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim());
        // let desconto_a_vista_row = document.querySelectorAll('.desconto_a_vista_row');
        // if ((desconto_a_vista_row[0].style.display !== "none") || (desconto_a_vista_row[1].style.display !== "none")) {
        // if (descontoVistaBool) {
        //     descontoPagamentoTot += parseFloat(document.querySelector('.desconto_a_vista_cell').textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim());
        // }
        // document.querySelector(".test").textContent = parseFloat(descontoPagameto[1].textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim());
        // document.getElementById("desconto_pagamento").value = descontoPagamentoTot;
        document.getElementById("desconto_pagamento").value = parseFloat(descontoPagameto[0].textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim());
    });
});

// Termos e condições
//// Ativa/desativa o botão 
const termosCondCheck = document.getElementById("termos_condicoes");

termosCondCheck.addEventListener("click", () => {
    if (termosCondCheck.checked) {
        document.getElementById("btnComprar").disabled = false;
        document.querySelector(".botaoStatusInput").value = 'abled';
    }
    else {
        document.getElementById("btnComprar").disabled = true;
        document.querySelector(".botaoStatusInput").value = 'disabled';
    }
});

//// Popup
const termosCondBtn = document.getElementById("termos_condicoes_btn");
const termosCondJanela = document.querySelector(".termos_condicoes_janela");
const termosCondJanelaClose = document.querySelector(".termos_condicoes_janela_close");

termosCondBtn.addEventListener("click", () => {
    if (termosCondJanela.style.display === "none") {
        termosCondJanela.style.display = "block";
    }
    else {
        termosCondJanela.style.display = "none";
    }
});

termosCondJanelaClose.addEventListener("click", () => {
    if (termosCondJanela.style.display === "none") {
        termosCondJanela.style.display = "block";
    }
    else {
        termosCondJanela.style.display = "none";
    }
});

//// Mensagem caso tente comprar sem concordar com os termos
window.onload = function () {
    let messageDiv = document.getElementById("messages");
    let messages = messageDiv.getAttribute("data-messages");

    if (messages) {
        try {
            let parsedMessages = JSON.parse(messages);
            parsedMessages.forEach(msg => {
                alert(msg.text);
            });
        } catch (error) {
            console.error("Error parsing messages:", error);
        }
    }
};