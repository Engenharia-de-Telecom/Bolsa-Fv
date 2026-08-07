let grafico = null;

const botao = document.getElementById("btnCarregar");

botao.addEventListener("click", carregarDados);

function carregarDados() {

    const sensor = document.getElementById("sensor").value;
    const inicio = document.getElementById("inicio").value;
    const fim    = document.getElementById("fim").value;

    fetch(`/api/dados?coluna=${sensor}&inicio=${inicio}&fim=${fim}`)

        .then(resposta => resposta.json())

        .then(dados => {

            desenharGrafico(
                sensor,
                dados.tempo,
                dados.valores
            );

        })

        .catch(erro => {

            console.error(erro);

        });

}

function desenharGrafico(nome, tempo, valores) {

    const ctx = document
        .getElementById("grafico")
        .getContext("2d");

    if (grafico != null) {
        grafico.destroy();
    }

    grafico = new Chart(ctx, {

        type: "line",

        data: {

            labels: tempo,

            datasets: [

                {

                    label: nome,

                    data: valores,

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: false

                }

            }

        }

    });

}