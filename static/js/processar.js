const optionLabel = document.querySelectorAll('.option');
const optionTitleLabel = document.querySelector('.option_title');
const valorFinal = document.querySelector('.valorFinal');
const descontoPagameto = document.querySelector('.desconto_pagamento_cell');

const DescontosDic = JSON.parse(document.getElementById("descontos-data").textContent);
// document.querySelector('.test').textContent = parseFloat(DescontosDic).toFixed(2);
// document.querySelector('.test').textContent = `- R$ ${DescontosDic.desc_credito_list[0]}`;
var TotalCredito = document.getElementById("total-credito-data").textContent;
var descontoCreditoInit = DescontosDic.desconto_credito;

optionLabel.forEach(e => {        
    e.addEventListener('click', function () {
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

        if (e.querySelector('input').value !== "dinheiro") {
            document.querySelector('.desconto_pagamento_row').style.display = "none";
        }
        else {
            document.querySelector('.desconto_pagamento_row').style.display = "table-row";
            document.querySelector('.desconto_pagamento_cell').textContent = `- R$ ${String(DescontosDic.desconto_dinheiro).replace(".", ",")}`;
            document.querySelector('.desconto_a_vista_row').style.display = "table-row";
            
            // e.querySelectorAll('.methods > .option_parcelas select').forEach(t => {
            //     t.value = "1";
            // });
        }
        
        // e.querySelector('.option_title').classList.add("selected");

        valorFinal.textContent = e.querySelector('.option_title .total_normal').textContent;

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

                e.querySelector('.methods > .option_parcelas').style.display = "block";
                e.querySelector('.methods > .option_parcelas select').name = "parcelas";
                // e.querySelector('.methods > .option_parcelas select').value = "1";

                // document.querySelector('.test').textContent = `${(DescontosDic.desc_credito_list[e.querySelector('.methods > .option_parcelas select').value - 1] * DescontosDic.total_bruto).toFixed(2)}`;
                DescontosDic.desconto_credito = (DescontosDic.desc_credito_list[e.querySelector('.methods > .option_parcelas select').value - 1] * DescontosDic.total_bruto).toFixed(2);

                TotalCredito = parseFloat(TotalCredito) + parseFloat(descontoCreditoInit) - parseFloat(DescontosDic.desconto_credito);
                descontoCreditoInit = DescontosDic.desconto_credito;
                e.querySelector('.methods > .credito .total_credito').textContent = `R$${(parseFloat(TotalCredito).toFixed(2)).replace(".", ",").trim()}`;

                e.querySelector('.methods > .option_parcelas .total_normal').textContent = e.querySelector('.methods > .option_parcelas select').value + "x R$" +  ((parseFloat(e.querySelector('.methods > .credito .total_normal').innerText.replace("R$", "").replace(".", "").replace(",", ".").trim()) / parseFloat(e.querySelector('.methods > .option_parcelas select').value)).toFixed(2)).replace(".", ",");
                
                if (descontoCreditoInit != 0) {
                    document.querySelector('.desconto_pagamento_row').style.display = "table-row";
                    document.querySelector('.desconto_pagamento_cell').textContent = `- R$ ${DescontosDic.desconto_credito.replace(".", ",")}`;
                }
                
                document.querySelector('.desconto_a_vista_row').style.display = "none";

                valorFinal.textContent = e.querySelector('.methods > .credito .total_normal').textContent;
                // if (e.querySelector('.methods > .option_parcelas select').value !== "1") {
                //     document.querySelector('.desconto_a_vista_row').style.display = "none";
                // }
                // else {
                //     document.querySelector('.desconto_a_vista_row').style.display = "table-row";
                // }
            }
            else {
                e.querySelector('.methods > .option_parcelas select').value = "1";
                document.querySelector('.desconto_a_vista_row').style.display = "table-row";

                // TotalCredito = parseFloat(TotalCredito) + parseFloat(descontoCreditoInit) - parseFloat((DescontosDic.desc_credito_list[0] * DescontosDic.total_bruto));
                // e.querySelector('.methods > .credito .total_credito').textContent = `R$${(parseFloat(TotalCredito).toFixed(2)).replace(".", ",").trim()}`;

                e.querySelector('.methods > .option_parcelas').style.display = "none";
            }
        }

        document.getElementById("total_final").value = valorFinal.textContent.replace("R$", "").replace(".", "").replace(",", ".").trim()
        if (document.querySelector('.desconto_pagamento_row').style.display === "none") {
            descontoPagameto.textContent = "- R$ 0,00";
        }
        let descontoPagamentoTot = parseFloat(descontoPagameto.textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim());
        if  (document.querySelector('.desconto_a_vista_row').style.display !== "none") {
            descontoPagamentoTot += parseFloat(document.querySelector('.desconto_a_vista_cell').textContent.replace("- R$", "").replace(".", "").replace(",", ".").trim());
        }
        document.getElementById("desconto_pagamento").value = descontoPagamentoTot;
    });
});