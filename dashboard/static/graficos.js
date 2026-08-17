let grafico = null;

const botao = document.getElementById("btnCarregar");

botao.addEventListener("click", carregarDados);


function carregarDados() {

    const sensor =
        document.getElementById("sensor").value;

    const inicio =
        document.getElementById("inicio").value;

    const fim =
        document.getElementById("fim").value;

    const intervalo =
        document.getElementById("intervalo").value;


    /*
     * Se nenhuma data foi informada,
     * carrega todo o histórico.
     */

    if (!inicio && !fim) {

        carregarHistoricoCompleto(
            sensor,
            intervalo
        );

        return;
    }


    /*
     * Se apenas uma das datas foi preenchida,
     * solicita as duas.
     */

    if (!inicio || !fim) {

        alert(
            "Informe a data inicial e a data final, ou deixe as duas em branco para carregar todo o histórico."
        );

        return;
    }


    /*
     * Verifica se o período é válido.
     */

    if (inicio > fim) {

        alert(
            "A data inicial não pode ser maior que a data final."
        );

        return;
    }


    /*
     * Carrega o período selecionado.
     */

    fetch(
        `/api/dados?coluna=${sensor}` +
        `&inicio=${inicio}` +
        `&fim=${fim}` +
        `&intervalo=${intervalo}`
    )

        .then(resposta => resposta.json())

        .then(dados => {

            if (dados.erro) {

                alert(dados.erro);

                return;
            }


            desenharGrafico(
                sensor,
                dados.tempo,
                dados.valores
            );


            atualizarInformacoes(
                sensor,
                inicio,
                fim,
                intervalo
            );

        })

        .catch(erro => {

            console.error(erro);

            alert(
                "Não foi possível carregar os dados."
            );

        });
}


/*
 * ==========================================
 * HISTÓRICO COMPLETO
 * ==========================================
 */

function carregarHistoricoCompleto(
    sensor,
    intervalo
) {

    /*
     * Agora também envia o intervalo
     * para a API.
     */

    fetch(
        `/api/dados?coluna=${sensor}` +
        `&intervalo=${intervalo}`
    )

        .then(resposta => resposta.json())

        .then(dados => {

            if (dados.erro) {

                alert(dados.erro);

                return;
            }


            desenharGrafico(
                sensor,
                dados.tempo,
                dados.valores
            );


            atualizarInformacoesHistorico(
                sensor,
                dados.tempo,
                intervalo
            );

        })

        .catch(erro => {

            console.error(erro);

            alert(
                "Não foi possível carregar os dados."
            );

        });
}


/*
 * ==========================================
 * INFORMAÇÕES DO HISTÓRICO
 * ==========================================
 */

function atualizarInformacoesHistorico(
    sensor,
    tempo,
    intervalo
) {

    const titulo =
        document.getElementById(
            "titulo-grafico"
        );


    const periodo =
        document.getElementById(
            "periodo-grafico"
        );


    const nome =
        obterNomeSensor(sensor);


    const unidade =
        obterUnidade(sensor);


    titulo.textContent =
        `${nome} (${unidade})`;


    /*
     * Mostra o período real dos dados.
     */

    if (tempo.length > 0) {

        const primeiraData =
            tempo[0];

        const ultimaData =
            tempo[tempo.length - 1];


        periodo.textContent =
            `Histórico completo · ` +
            `${primeiraData} até ${ultimaData}` +
            ` · ${obterNomeIntervalo(intervalo)}`;

    }

    else {

        periodo.textContent =
            "Nenhum dado disponível.";

    }
}


/*
 * ==========================================
 * DESENHA O GRÁFICO
 * ==========================================
 */

function desenharGrafico(
    nome,
    tempo,
    valores
) {

    const ctx =
        document
            .getElementById("grafico")
            .getContext("2d");


    if (grafico !== null) {

        grafico.destroy();

    }


    grafico = new Chart(ctx, {

        type: "line",

        data: {

            labels: tempo,

            datasets: [

                {

                    label: obterNomeSensor(nome),

                    data: valores,

                    borderWidth: 2,

                    pointRadius: 0,

                    pointHoverRadius: 5,

                    tension: 0.25,

                    fill: true

                }

            ]

        },


        options: {

            responsive: true,

            maintainAspectRatio: false,

            interaction: {

                mode: "index",

                intersect: false

            },


            plugins: {

                legend: {

                    display: false

                },

                tooltip: {

                    mode: "index",

                    intersect: false

                }

            },


            scales: {

                x: {

                    ticks: {

                        maxTicksLimit: 15

                    }

                },


                y: {

                    beginAtZero: false

                }

            }

        }

    });
}


/*
 * ==========================================
 * NOME DOS SENSORES
 * ==========================================
 */

function obterNomeSensor(sensor) {

    const nomes = {

        "IRRADIANCE":
            "Irradiância",

        "TA":
            "Temperatura",

        "RH":
            "Umidade",

        "PA":
            "Pressão",

        "WD_SPD":
            "Velocidade do vento"

    };


    return nomes[sensor] || sensor;
}


/*
 * ==========================================
 * UNIDADES
 * ==========================================
 */

function obterUnidade(sensor) {

    const unidades = {

        "IRRADIANCE":
            "W/m²",

        "TA":
            "°C",

        "RH":
            "%",

        "PA":
            "hPa",

        "WD_SPD":
            "m/s"

    };


    return unidades[sensor] || "";
}


/*
 * ==========================================
 * INFORMAÇÕES DO PERÍODO
 * ==========================================
 */

function atualizarInformacoes(
    sensor,
    inicio,
    fim,
    intervalo
) {

    const titulo =
        document.getElementById(
            "titulo-grafico"
        );


    const periodo =
        document.getElementById(
            "periodo-grafico"
        );


    const nome =
        obterNomeSensor(sensor);


    const unidade =
        obterUnidade(sensor);


    titulo.textContent =
        `${nome} (${unidade})`;


    periodo.textContent =
        `${formatarData(inicio)}` +
        ` até ` +
        `${formatarData(fim)}` +
        ` · ` +
        `${obterNomeIntervalo(intervalo)}`;
}


/*
 * ==========================================
 * FORMATA DATA
 * ==========================================
 */

function formatarData(data) {

    const partes =
        data.split("-");

    return `${partes[2]}/${partes[1]}/${partes[0]}`;
}


/*
 * ==========================================
 * NOME DO INTERVALO
 * ==========================================
 */

function obterNomeIntervalo(intervalo) {

    const nomes = {

        "minuto":
            "Minuto a minuto",

        "5min":
            "A cada 5 minutos",

        "15min":
            "A cada 15 minutos",

        "30min":
            "A cada 30 minutos",

        "hora":
            "Hora a hora",

        "dia":
            "Dia a dia"

    };


    return nomes[intervalo] || intervalo;
}