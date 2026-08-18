let graficoDia = null;

function atualizarSensores() {


fetch("/status")

    .then(resposta => resposta.json())

    .then(dados => {

        let area = document.getElementById("sensores");

        area.innerHTML = "";


        /*
         * Configuração visual dos sensores
         */

        const configuracao = {

            "IRRADIANCE": {
                nome: "Irradiância",
                icone: "☀️",
                unidade: "W/m²"
            },

            "PA": {
                nome: "Pressão Atmosférica",
                icone: "🌡️",
                unidade: "hPa"
            },

            "RH": {
                nome: "Umidade Relativa",
                icone: "💧",
                unidade: "%"
            },

            "TA": {
                nome: "Temperatura do Ar",
                icone: "🌡️",
                unidade: "°C"
            },

            "RAIN_INT": {
                nome: "Intensidade da Chuva",
                icone: "🌧️",
                unidade: ""
            },

            "RAIN_DUR": {
                nome: "Duração da Chuva",
                icone: "🌧️",
                unidade: "min"
            },

            "RAIN_AMOUNT": {
                nome: "Precipitação",
                icone: "💧",
                unidade: "mm"
            },

            "WD_DIR": {
                nome: "Direção do Vento",
                icone: "🧭",
                unidade: "°"
            },

            "WD_SPD": {
                nome: "Velocidade do Vento",
                icone: "💨",
                unidade: "m/s"
            }

        };


        /*
         * Cria os cards
         */

        for (let sensor in dados.sensores) {

            /*
             * Não mostra DATE-TIME como sensor
             */

            if (sensor === "DATE-TIME") {
                continue;
            }


            let item = dados.sensores[sensor];

            let config = configuracao[sensor] || {

                nome: sensor,
                icone: "📊",
                unidade: ""

            };


            let valor = item.valor;


            /*
             * Se o sensor estiver offline,
             * mostra uma indicação mais clara
             */

            if (item.status === "offline") {

                valor = "Offline";

            }


            area.innerHTML += `

                <div class="card ${item.status}">

                    <h3>
                        ${config.icone}
                        ${config.nome}
                    </h3>

                    <p class="valor">

                        ${valor}

                        ${
                            item.status === "online" &&
                            config.unidade !== ""
                            ?
                            `<span class="unidade">${config.unidade}</span>`
                            :
                            ""
                        }

                    </p>

                    <strong>

                        ${
                            item.status === "online"
                            ?
                            "● Online"
                            :
                            "● Offline"
                        }

                    </strong>

                </div>

            `;

        }


        /*
         * Atualiza a última atualização
         */

        let ultimaAtualizacao =
            document.getElementById("ultima-atualizacao");


        if (ultimaAtualizacao) {

            ultimaAtualizacao.textContent =
                "Última atualização: " +
                dados.ultima_atualizacao;

        }


        /*
         * Atualiza o status geral da estação
         */

        let statusEstacao =
            document.getElementById("status-estacao");


        if (statusEstacao) {

            let indicador =
                statusEstacao.querySelector(".status-indicador");

            let texto =
                statusEstacao.querySelector("span:last-child");


            /*
             * Verifica se existe algum sensor offline
             */

            let algumOffline = Object.values(dados.sensores)
                .some(sensor => sensor.status === "offline");


            if (algumOffline) {

                statusEstacao.style.backgroundColor = "#fef2f2";
                statusEstacao.style.color = "#991b1b";

                indicador.style.backgroundColor = "#ef4444";

                texto.textContent = "Sensores com problema";

            }

            else {

                statusEstacao.style.backgroundColor = "#f0fdf4";
                statusEstacao.style.color = "#166534";

                indicador.style.backgroundColor = "#22c55e";

                texto.textContent = "Estação online";

            }

        }

    })

    .catch(erro => {

        console.error(
            "Erro ao obter status dos sensores:",
            erro
        );

    });


}

/*
 * Primeira atualização
 */
atualizarSensores();
atualizarGraficoDia();


/*
 * Atualiza o gráfico a cada 1 minuto
 */
setInterval(
    atualizarGraficoDia,
    60000
);
// =====================================================
// GRÁFICO DO DIA
// =====================================================

function atualizarGraficoDia() {

    fetch("/api/grafico-dia")

        .then(resposta => resposta.json())

        .then(dados => {

            if (dados.erro) {

                console.error(dados.erro);

                return;
            }


            // -----------------------------------------
            // Atualiza o título do gráfico
            // -----------------------------------------

            const dataGrafico =
                document.getElementById(
                    "data-grafico-dia"
                );


            if (dataGrafico) {

                dataGrafico.textContent =
                    `Dados de ${dados.data}`;

            }


            // -----------------------------------------
            // Cria o gráfico
            // -----------------------------------------

            const canvas =
                document.getElementById(
                    "grafico-dia"
                );


            if (!canvas) {
                return;
            }


            const ctx =
                canvas.getContext("2d");


            // -----------------------------------------
            // Destrói o gráfico anterior
            // -----------------------------------------

            if (graficoDia !== null) {

                graficoDia.destroy();

            }


            // -----------------------------------------
            // Cria novo gráfico
            // -----------------------------------------

            graficoDia = new Chart(ctx, {

                type: "line",

                data: {

                    labels: dados.tempo,

                    datasets: [

                        {
                            label: "Irradiância",

                            data: dados.irradiancia,

                            borderWidth: 2,

                            pointRadius: 0,

                            pointHoverRadius: 5,

                            tension: 0.25,

                            yAxisID: "yIrradiancia"
                        },

                        {
                            label: "Temperatura",

                            data: dados.temperatura,

                            borderWidth: 2,

                            pointRadius: 0,

                            pointHoverRadius: 5,

                            tension: 0.25,

                            yAxisID: "yTemperatura"
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

                            display: true,

                            position: "top"

                        },

                        tooltip: {

                            mode: "index",

                            intersect: false

                        }

                    },


                    scales: {

                        x: {

                            title: {

                                display: true,

                                text: "Hora"

                            },

                            ticks: {

                                maxTicksLimit: 15

                            }

                        },


                        yIrradiancia: {

                            type: "linear",

                            position: "left",

                            title: {

                                display: true,

                                text: "Irradiância (W/m²)"

                            },

                            beginAtZero: true

                        },


                        yTemperatura: {

                            type: "linear",

                            position: "right",

                            title: {

                                display: true,

                                text: "Temperatura (°C)"

                            },

                            grid: {

                                drawOnChartArea: false

                            }

                        }

                    }

                }

            });

        })

        .catch(erro => {

            console.error(
                "Erro ao carregar gráfico do dia:",
                erro
            );

        });

}
