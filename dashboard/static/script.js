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

* Atualiza a cada 1 segundo
  */

setInterval(
atualizarSensores,
1000
);

/*

* Primeira atualização
  */

atualizarSensores();
