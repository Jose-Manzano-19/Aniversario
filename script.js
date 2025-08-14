// Configuración de tiempos (en milisegundos)
const textoDuracion = 5000; // 5 segundos para el texto
const fotosDuracion = 3000; // 3 segundos cada foto
const fotos = ["img/foto1.jpg", "img/foto2.jpg", "img/foto3.jpg"];

// Etapa 1 -> Abrir carta
function openEnvelope() {
    document.querySelector(".envelope").classList.add("open");
    setTimeout(() => {
        document.getElementById("stage1").classList.add("hidden");
        mostrarTexto();
    }, 1000);
}

// Etapa 2 -> Texto romántico
function mostrarTexto() {
    document.getElementById("stage2").classList.remove("hidden");
    const texto = "Un año juntos, y cada día te amo un poquito más. 💖";
    let i = 0;
    const loveTextEl = document.getElementById("loveText");

    function escribir() {
        if (i < texto.length) {
            loveTextEl.innerHTML += texto.charAt(i);
            i++;
            setTimeout(escribir, 50);
        }
    }
    escribir();

    setTimeout(() => {
        document.getElementById("stage2").classList.add("hidden");
        mostrarFotos();
    }, textoDuracion);
}

// Etapa 3 -> Galería
function mostrarFotos() {
    document.getElementById("stage3").classList.remove("hidden");
    let index = 0;
    const imgEl = document.getElementById("photoSlide");

    const intervalo = setInterval(() => {
        index++;
        if (index >= fotos.length) {
            clearInterval(intervalo);
            document.getElementById("stage3").classList.add("hidden");
            mostrarFinal();
        } else {
            imgEl.src = fotos[index];
        }
    }, fotosDuracion);
}

// Etapa 4 -> Final
function mostrarFinal() {
    document.getElementById("stage4").classList.remove("hidden");
}
