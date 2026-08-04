function atualizarSensores(){

    fetch("/status")

    .then(resposta => resposta.json())

    .then(dados => {


        let area = document.getElementById("sensores");


        area.innerHTML = "";


        for(let sensor in dados.sensores){


            let item = dados.sensores[sensor];


            area.innerHTML += `

            <div class="card ${item.status}">

                <h2>${sensor}</h2>

                <p>${item.valor}</p>

                <strong>
                    ${item.status}
                </strong>

            </div>

            `;

        }


    });


}


// atualiza a cada 1 segundo

setInterval(
    atualizarSensores,
    1000
);


// primeira atualização

atualizarSensores();