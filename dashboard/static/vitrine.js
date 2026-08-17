let grafico = null;


async function carregarVitrine() {

    try {

        const resposta = await fetch("/api/vitrine");

        const dados = await resposta.json();


        if (dados.erro) {

            console.error(dados.erro);

            return;

        }


        // -----------------------------------------
        // DATA / HORA
        // -----------------------------------------

        document.getElementById("dataHora").textContent =
            dados.ultima_atualizacao;


        // -----------------------------------------
        // IRRADIÂNCIA ATUAL
        // -----------------------------------------

        document.getElementById("irradiancia").textContent =
            Number(dados.irradiancia_atual).toFixed(2);


        // -----------------------------------------
        // GRÁFICO
        // -----------------------------------------

        desenharGrafico(
            dados.grafico.tempo,
            dados.grafico.irradiancia
        );


    } catch (erro) {

        console.error(
            "Erro ao carregar dados:",
            erro
        );

    }

}


function desenharGrafico(tempo, irradiancia) {

    const canvas =
        document.getElementById(
            "graficoIrradiancia"
        );

    const ctx = canvas.getContext("2d");


    // Se já existe um gráfico,
    // destrói antes de criar outro

    if (grafico !== null) {

        grafico.destroy();

    }


    grafico = new Chart(ctx, {

        type: "line",

        data: {

            labels: tempo,

            datasets: [

                {

                    label: "Irradiância (W/m²)",

                    data: irradiancia,

                    borderWidth: 2,

                    tension: 0.2,

                    pointRadius: 2

                }

            ]

        },


        options: {

            responsive: true,

            maintainAspectRatio: false,


            scales: {

                x: {

                    title: {

                        display: true,

                        text: "Horário"

                    }

                },


                y: {

                    beginAtZero: true,

                    title: {

                        display: true,

                        text: "Irradiância (W/m²)"

                    }

                }

            },


            plugins: {

                legend: {

                    display: true

                }

            }

        }

    });

}


// Carrega imediatamente

carregarVitrine();


// Atualiza a cada 60 segundos

setInterval(
    carregarVitrine,
    60000
);