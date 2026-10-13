```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Zona de Combate 3D</title>

<style>
*{box-sizing:border-box}

body{
    margin:0;
    overflow:hidden;
    background:#000;
    font-family:Arial,sans-serif;
}

canvas{display:block}

#inicio,#gameOver{
    position:fixed;
    inset:0;
    z-index:100;
    background:radial-gradient(circle,#263b45,#050708);
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
}

#gameOver{display:none}

h1{font-size:48px}

button{
    padding:15px 45px;
    border:0;
    border-radius:8px;
    background:#238b4b;
    color:white;
    font-size:20px;
    font-weight:bold;
    cursor:pointer;
}

#hud{
    position:fixed;
    top:18px;
    left:18px;
    z-index:20;
    color:white;
    font-size:17px;
    line-height:1.7;
    text-shadow:2px 2px 5px #000;
    pointer-events:none;
}

#barra{
    width:230px;
    height:19px;
    border:2px solid white;
    background:#222;
    border-radius:10px;
    overflow:hidden;
}

#barraVida{
    width:100%;
    height:100%;
    background:#35df54;
}

#mira{
    position:fixed;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    z-index:30;
    color:white;
    font-size:28px;
    text-shadow:0 0 5px black;
    pointer-events:none;
}

#mensaje{
    position:fixed;
    left:50%;
    top:18%;
    transform:translateX(-50%);
    z-index:40;
    color:white;
    font-size:28px;
    font-weight:bold;
    text-shadow:2px 2px 6px #000;
    display:none;
}

#ayuda{
    position:fixed;
    bottom:15px;
    left:50%;
    transform:translateX(-50%);
    z-index:20;
    background:rgba(0,0,0,.55);
    padding:8px 18px;
    border-radius:7px;
    color:white;
    font-size:14px;
}
</style>
</head>

<body>

<div id="inicio">
<h1>⚔️ ZONA DE COMBATE</h1>

<p>
<b>W A S D</b> — Movimiento<br>
<b>ESPACIO</b> — Saltar<br>
<b>CTRL</b> — Agacharse<br>
<b>CLICK IZQUIERDO</b> — Disparar<br>
<b>R</b> — Recargar<br>
<b>1 / 2 / 3</b> — Cambiar arma<br>
<b>MOUSE</b> — Mirar
</p>

<button onclick="iniciarJuego()">JUGAR</button>
</div>

<div id="gameOver">
<h1>☠️ GAME OVER</h1>
<p>Puntos: <b id="puntosFinales">0</b></p>
<button onclick="location.reload()">JUGAR DE NUEVO</button>
</div>

<div id="hud">

❤️ Vida:
<span id="vida">100</span>

<div id="barra">
<div id="barraVida"></div>
</div>

🏆 Puntos:
<span id="puntos">0</span>

<br>

🤖 Enemigos:
<span id="enemigos">4</span>

<br>

🔫 Arma:
<span id="armaHUD">Rifle táctico</span>

<br>

💥 Balas:
<span id="municion">15 / 15</span>

</div>

<div id="mira">+</div>
<div id="mensaje"></div>

<div id="ayuda">
W A S D · ESPACIO · CTRL · CLICK · R · 1/2/3
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>

<script>

/* =====================================================
   VARIABLES
===================================================== */

let escena;
let camara;
let renderer;
let jugador;

let armaVisual;

let enemigos=[];
let botiquines=[];
let obstaculos=[];

let vida=100;
let puntos=0;

let juegoActivo=false;

let velocidad=.13;
let velocidadVertical=0;

let enElSuelo=true;
let agachado=false;

let rotacionX=0;
let rotacionY=0;

let ultimaBala=0;

const teclas={};

const CAPACIDAD_CARGADOR=15;

let balas=15;
let recargando=false;


/* =====================================================
   ARMAS
===================================================== */

const armas={

1:{
nombre:"Rifle táctico",
cadencia:180,
dano:1,
alcance:55
},

2:{
nombre:"Pistola",
cadencia:350,
dano:1,
alcance:40
},

3:{
nombre:"Blaster",
cadencia:90,
dano:2,
alcance:60
}

};

let armaActual=1;


/* =====================================================
   AUDIO
===================================================== */

let audioContext=null;

function iniciarAudio(){

if(!audioContext){

audioContext=
new(
window.AudioContext||
window.webkitAudioContext
)();

}

if(audioContext.state==="suspended"){
audioContext.resume();
}

}


function sonidoDisparo(){

iniciarAudio();

const ahora=audioContext.currentTime;

const osc=audioContext.createOscillator();
const gain=audioContext.createGain();

osc.type="sawtooth";

osc.frequency.setValueAtTime(
170,
ahora
);

osc.frequency.exponentialRampToValueAtTime(
45,
ahora+.13
);

gain.gain.setValueAtTime(
.35,
ahora
);

gain.gain.exponentialRampToValueAtTime(
.001,
ahora+.14
);

osc.connect(gain);
gain.connect(audioContext.destination);

osc.start(ahora);
osc.stop(ahora+.14);

}


function sonidoBotiquin(){

iniciarAudio();

const ahora=audioContext.currentTime;

const osc=audioContext.createOscillator();
const gain=audioContext.createGain();

osc.type="sine";

osc.frequency.setValueAtTime(
450,
ahora
);

osc.frequency.exponentialRampToValueAtTime(
900,
ahora+.25
);

gain.gain.setValueAtTime(
.3,
ahora
);

gain.gain.exponentialRampToValueAtTime(
.001,
ahora+.3
);

osc.connect(gain);
gain.connect(audioContext.destination);

osc.start(ahora);
osc.stop(ahora+.3);

}


function sonidoRecarga(){

iniciarAudio();

const ahora=audioContext.currentTime;

const osc=audioContext.createOscillator();
const gain=audioContext.createGain();

osc.type="square";

osc.frequency.setValueAtTime(
250,
ahora
);

osc.frequency.setValueAtTime(
400,
ahora+.15
);

osc.frequency.setValueAtTime(
550,
ahora+.3
);

gain.gain.setValueAtTime(
.18,
ahora
);

gain.gain.exponentialRampToValueAtTime(
.001,
ahora+.45
);

osc.connect(gain);
gain.connect(audioContext.destination);

osc.start(ahora);
osc.stop(ahora+.45);

}


/* =====================================================
   INICIO
===================================================== */

function iniciarJuego(){

iniciarAudio();

document.getElementById(
"inicio"
).style.display="none";

juegoActivo=true;

crearJuego();

document.body.requestPointerLock();

}


/* =====================================================
   CREAR JUEGO
===================================================== */

function crearJuego(){

escena=new THREE.Scene();

escena.background=
new THREE.Color(0x86a4b8);

escena.fog=
new THREE.Fog(
0x86a4b8,
35,
110
);


camara=
new THREE.PerspectiveCamera(
75,
innerWidth/innerHeight,
.1,
300
);


renderer=
new THREE.WebGLRenderer({
antialias:true
});

renderer.setSize(
innerWidth,
innerHeight
);

renderer.setPixelRatio(
Math.min(devicePixelRatio,2)
);

renderer.shadowMap.enabled=true;

renderer.shadowMap.type=
THREE.PCFSoftShadowMap;

renderer.outputColorSpace=
THREE.SRGBColorSpace;

renderer.toneMapping=
THREE.ACESFilmicToneMapping;

renderer.toneMappingExposure=1.15;

document.body.appendChild(
renderer.domElement
);


/* LUCES */

const ambiente=
new THREE.HemisphereLight(
0xddeeff,
0x26351f,
2
);

escena.add(ambiente);


const sol=
new THREE.DirectionalLight(
0xffffff,
2.5
);

sol.position.set(
-20,
45,
15
);

sol.castShadow=true;

sol.shadow.mapSize.width=2048;
sol.shadow.mapSize.height=2048;

escena.add(sol);


crearMapa();

crearJugador();


for(let i=0;i<4;i++){
crearEnemigo();
}


for(let i=0;i<7;i++){
crearBotiquin();
}


cambiarArma(1);

actualizarHUD();

animar();

}


/* =====================================================
   MAPA
===================================================== */

function crearMapa(){

const suelo=
new THREE.Mesh(

new THREE.BoxGeometry(
80,1,80
),

new THREE.MeshStandardMaterial({
color:0x40583a,
roughness:.95
})

);

suelo.position.y=-.5;

suelo.receiveShadow=true;

escena.add(suelo);


crearPared(0,3,-40,80,6,1);
crearPared(0,3,40,80,6,1);
crearPared(-40,3,0,1,6,80);
crearPared(40,3,0,1,6,80);


/* OBSTÁCULOS */

for(let i=0;i<24;i++){

const ancho=2+Math.random()*3;
const profundidad=2+Math.random()*3;
const alto=2+Math.random()*3;

const objeto=
new THREE.Mesh(

new THREE.BoxGeometry(
ancho,
alto,
profundidad
),

new THREE.MeshStandardMaterial({
color:0x555b5d,
roughness:.75,
metalness:.15
})

);

objeto.position.set(
Math.random()*64-32,
alto/2,
Math.random()*64-32
);

objeto.castShadow=true;
objeto.receiveShadow=true;

escena.add(objeto);

obstaculos.push({

mesh:objeto,

minX:
objeto.position.x-ancho/2,

maxX:
objeto.position.x+ancho/2,

minZ:
objeto.position.z-profundidad/2,

maxZ:
objeto.position.z+profundidad/2

});

}

}


/* =====================================================
   PAREDES
===================================================== */

function crearPared(
x,y,z,
ancho,alto,profundidad
){

const pared=
new THREE.Mesh(

new THREE.BoxGeometry(
ancho,
alto,
profundidad
),

new THREE.MeshStandardMaterial({
color:0x242b2e,
roughness:.7
})

);

pared.position.set(x,y,z);

pared.castShadow=true;
pared.receiveShadow=true;

escena.add(pared);

obstaculos.push({

mesh:pared,

minX:x-ancho/2,
maxX:x+ancho/2,

minZ:z-profundidad/2,
maxZ:z+profundidad/2

});

}


/* =====================================================
   JUGADOR
===================================================== */

function crearJugador(){

jugador=
new THREE.Object3D();

jugador.position.set(
0,
1.7,
20
);

escena.add(jugador);

jugador.add(camara);

camara.position.set(0,0,0);

}


/* =====================================================
   COLISIONES
===================================================== */

function puedeMoverse(x,z){

const radio=.55;

if(
x<-37+radio||
x>37-radio||
z<-37+radio||
z>37-radio
){
return false;
}


for(
const o of obstaculos
){

if(

x+radio>o.minX&&
x-radio<o.maxX&&
z+radio>o.minZ&&
z-radio<o.maxZ

){

return false;

}

}

return true;

}


/* =====================================================
   MOVIMIENTO DEL JUGADOR
===================================================== */

function moverJugador(){

if(!juegoActivo)return;

let vel=velocidad;

if(agachado)
vel*=.5;


/* W ADELANTE */

if(teclas["KeyW"]){

const x=
-Math.sin(jugador.rotation.y)*vel;

const z=
-Math.cos(jugador.rotation.y)*vel;

intentarMovimiento(x,z);

}


/* S ATRÁS */

if(teclas["KeyS"]){

const x=
Math.sin(jugador.rotation.y)*vel;

const z=
Math.cos(jugador.rotation.y)*vel;

intentarMovimiento(x,z);

}


/* A IZQUIERDA */

if(teclas["KeyA"]){

const x=
-Math.cos(jugador.rotation.y)*vel;

const z=
Math.sin(jugador.rotation.y)*vel;

intentarMovimiento(x,z);

}


/* D DERECHA */

if(teclas["KeyD"]){

const x=
Math.cos(jugador.rotation.y)*vel;

const z=
-Math.sin(jugador.rotation.y)*vel;

intentarMovimiento(x,z);

}


/* GRAVEDAD */

velocidadVertical-=.01;

jugador.position.y+=
velocidadVertical;


if(jugador.position.y<=1.7){

jugador.position.y=1.7;

velocidadVertical=0;

enElSuelo=true;

}


camara.position.y=
agachado?-0.5:0;

}


/* =====================================================
   MOVIMIENTO CON COLISIÓN
===================================================== */

function intentarMovimiento(dx,dz){

const nuevoX=
jugador.position.x+dx;

const nuevoZ=
jugador.position.z+dz;


if(
puedeMoverse(nuevoX,nuevoZ)
){

jugador.position.x=nuevoX;
jugador.position.z=nuevoZ;

return;

}


if(
puedeMoverse(
nuevoX,
jugador.position.z
)
){

jugador.position.x=nuevoX;

}


if(
puedeMoverse(
jugador.position.x,
nuevoZ
)
){

jugador.position.z=nuevoZ;

}

}


/* =====================================================
   ENEMIGO HUMANOIDE
===================================================== */

function crearEnemigo(){

const enemigo=
new THREE.Group();


/* TORSO */

const torso=
new THREE.Mesh(

new THREE.BoxGeometry(
.9,
1.25,
.55
),

new THREE.MeshStandardMaterial({
color:0x354d65,
roughness:.8
})

);

torso.position.y=.75;

torso.castShadow=true;

enemigo.add(torso);


/* CABEZA */

const cabeza=
new THREE.Mesh(

new THREE.SphereGeometry(
.38,
20,
20
),

new THREE.MeshStandardMaterial({
color:0xc58e70,
roughness:.8
})

);

cabeza.position.y=1.65;

cabeza.castShadow=true;

enemigo.add(cabeza);


/* CASCO */

const casco=
new THREE.Mesh(

new THREE.SphereGeometry(
.4,
20,
12,
0,
Math.PI*2,
0,
Math.PI/2
),

new THREE.MeshStandardMaterial({
color:0x20282c,
roughness:.65
})

);

casco.position.y=1.82;

enemigo.add(casco);


/* BRAZO IZQUIERDO */

const brazoIzq=
crearExtremidad();

brazoIzq.position.set(
-.63,
.7,
0
);

brazoIzq.rotation.z=-.12;

enemigo.add(brazoIzq);


/* BRAZO DERECHO */

const brazoDer=
crearExtremidad();

brazoDer.position.set(
.63,
.7,
0
);

brazoDer.rotation.z=.12;

enemigo.add(brazoDer);


/* PIERNAS */

const piernaIzq=
crearPierna();

piernaIzq.position.set(
-.25,
-.35,
0
);

enemigo.add(piernaIzq);


const piernaDer=
crearPierna();

piernaDer.position.set(
.25,
-.35,
0
);

enemigo.add(piernaDer);


/* ARMA */

const arma=
crearArma();

arma.position.set(
.5,
.65,
-.45
);

arma.rotation.x=
Math.PI/2;

enemigo.add(arma);


/* POSICIÓN */

do{

enemigo.position.x=
Math.random()*60-30;

enemigo.position.z=
Math.random()*60-30;

}while(

!puedeMoverse(
enemigo.position.x,
enemigo.position.z
)||

enemigo.position.distanceTo(
jugador.position
)<12

);


enemigo.position.y=1;

enemigo.userData.vida=3;

enemigo.userData.ultimoDisparo=0;

enemigo.userData.direccion=
Math.random()*Math.PI*2;

enemigo.userData.cambioDireccion=0;

enemigo.userData.velocidad=
.025+Math.random()*.025;

escena.add(enemigo);

enemigos.push(enemigo);

}


/* =====================================================
   PARTES HUMANOIDE
===================================================== */

function crearExtremidad(){

const brazo=
new THREE.Mesh(

new THREE.BoxGeometry(
.25,
1,
.25
),

new THREE.MeshStandardMaterial({
color:0x354d65
})

);

brazo.castShadow=true;

return brazo;

}


function crearPierna(){

const pierna=
new THREE.Mesh(

new THREE.BoxGeometry(
.28,
1.05,
.3
),

new THREE.MeshStandardMaterial({
color:0x252f38
})

);

pierna.castShadow=true;

return pierna;

}


/* =====================================================
   ARMA DETALLADA
===================================================== */

function crearArma(){

const grupo=
new THREE.Group();


const cuerpo=
new THREE.Mesh(

new THREE.BoxGeometry(
.24,
.27,
1.25
),

new THREE.MeshStandardMaterial({

color:0x181b1d,
metalness:.8,
roughness:.25

})

);

cuerpo.position.z=-.55;

grupo.add(cuerpo);


/* PARTE SUPERIOR */

const superior=
new THREE.Mesh(

new THREE.BoxGeometry(
.18,
.12,
.9
),

new THREE.MeshStandardMaterial({

color:0x303438,
metalness:.9,
roughness:.2

})

);

superior.position.set(
0,
.18,
-.5
);

grupo.add(superior);


/* CAÑÓN */

const canon=
new THREE.Mesh(

new THREE.CylinderGeometry(
.055,
.07,
.65,
16
),

new THREE.MeshStandardMaterial({

color:0x090a0b,
metalness:.95,
roughness:.18

})

);

canon.rotation.x=
Math.PI/2;

canon.position.z=-1.35;

grupo.add(canon);


/* CARGADOR */

const cargador=
new THREE.Mesh(

new THREE.BoxGeometry(
.17,
.5,
.25
),

new THREE.MeshStandardMaterial({
color:0x242729,
metalness:.4
})

);

cargador.position.set(
0,
-.35,
-.55
);

cargador.rotation.x=-.15;

grupo.add(cargador);


/* MIRA */

const mira=
new THREE.Mesh(

new THREE.BoxGeometry(
.08,
.1,
.35
),

new THREE.MeshStandardMaterial({
color:0x080909
})

);

mira.position.set(
0,
.29,
-.55
);

grupo.add(mira);

return grupo;

}


/* =====================================================
   BOTIQUINES
===================================================== */

function crearBotiquin(){

const botiquin=
new THREE.Group();


const caja=
new THREE.Mesh(

new THREE.BoxGeometry(
1,
.35,
.75
),

new THREE.MeshStandardMaterial({
color:0xffffff
})

);

caja.castShadow=true;

botiquin.add(caja);


const mat=
new THREE.MeshBasicMaterial({
color:0xff2222
});


const vertical=
new THREE.Mesh(

new THREE.BoxGeometry(
.18,
.04,
.5
),

mat
);


const horizontal=
new THREE.Mesh(

new THREE.BoxGeometry(
.5,
.04,
.18
),

mat
);


vertical.position.y=.19;
horizontal.position.y=.19;

botiquin.add(vertical);
botiquin.add(horizontal);


do{

botiquin.position.x=
Math.random()*60-30;

botiquin.position.z=
Math.random()*60-30;

}while(

!puedeMoverse(
botiquin.position.x,
botiquin.position.z
)

);


botiquin.position.y=.3;

escena.add(botiquin);

botiquines.push(botiquin);

}


/* =====================================================
   RECOGER BOTIQUÍN
===================================================== */

function comprobarBotiquines(){

for(
let i=botiquines.length-1;
i>=0;
i--
){

const b=
botiquines[i];

const distancia=
jugador.position.distanceTo(
b.position
);


if(
distancia<1.5&&
vida<100
){

vida=
Math.min(
100,
vida+30
);

puntos+=25;

sonidoBotiquin();

mostrarMensaje(
"🩹 +30 VIDA"
);


escena.remove(b);

botiquines.splice(i,1);


setTimeout(
()=>{

if(juegoActivo)
crearBotiquin();

},
5000
);

}

}

}


/* =====================================================
   CAMBIAR ARMA
===================================================== */

function cambiarArma(numero){

if(recargando)return;

armaActual=numero;

document.getElementById(
"armaHUD"
).textContent=
armas[numero].nombre;


if(armaVisual)
camara.remove(armaVisual);


armaVisual=
crearArma();


armaVisual.position.set(
.55,
-.55,
-.9
);

armaVisual.rotation.set(
0,
0,
0
);


camara.add(armaVisual);

actualizarHUD();

}


/* =====================================================
   RECARGAR
===================================================== */

function recargar(){

if(
recargando||
balas===CAPACIDAD_CARGADOR||
!juegoActivo
)return;


recargando=true;

mostrarMensaje(
"🔄 RECARGANDO..."
);

sonidoRecarga();


setTimeout(
()=>{

balas=
CAPACIDAD_CARGADOR;

recargando=false;

mostrarMensaje(
"🔫 ¡LISTO!"
);

actualizarHUD();

},
1200
);

}


/* =====================================================
   TECLADO
===================================================== */

document.addEventListener(
"keydown",
function(e){

teclas[e.code]=true;


/* RECARGA */

if(e.code==="KeyR"){
recargar();
}


/* ARMAS */

if(e.code==="Digit1"){
cambiarArma(1);
}

if(e.code==="Digit2"){
cambiarArma(2);
}

if(e.code==="Digit3"){
cambiarArma(3);
}


/* SALTO */

if(
e.code==="Space"&&
enElSuelo&&
juegoActivo
){

e.preventDefault();

velocidadVertical=.23;

enElSuelo=false;

}


/* CTRL */

if(
e.code==="ControlLeft"||
e.code==="ControlRight"
){

agachado=true;

}

});


document.addEventListener(
"keyup",
function(e){

teclas[e.code]=false;


if(
e.code==="ControlLeft"||
e.code==="ControlRight"
){

agachado=false;

}

});


/* =====================================================
   MOUSE
===================================================== */

document.addEventListener(
"mousemove",
function(e){

if(
!juegoActivo||
document.pointerLockElement!==document.body
)return;


rotacionY-=
e.movementX*.002;

rotacionX-=
e.movementY*.002;


rotacionX=
Math.max(
-1.45,
Math.min(
1.45,
rotacionX
)
);


jugador.rotation.y=
rotacionY;

camara.rotation.x=
rotacionX;

});


/* =====================================================
   DISPARO
===================================================== */

document.addEventListener(
"mousedown",
function(e){

if(
e.button===0&&
juegoActivo
){

disparar();

}

});


function disparar(){

if(recargando)return;


if(balas<=0){

mostrarMensaje(
"🚫 SIN BALAS — PRESIONA R"
);

return;

}


const ahora=
performance.now();

const arma=
armas[armaActual];


if(
ahora-ultimaBala<
arma.cadencia
){

return;

}


ultimaBala=ahora;

balas--;

actualizarHUD();

sonidoDisparo();


const origen=
camara.getWorldPosition(
new THREE.Vector3()
);


const direccion=
camara.getWorldDirection(
new THREE.Vector3()
);


crearRastro(
origen,
direccion,
arma.alcance
);


crearChispas(
origen,
direccion
);


const raycaster=
new THREE.Raycaster();

raycaster.setFromCamera(
new THREE.Vector2(0,0),
camara
);


const objetos=[];


enemigos.forEach(
enemigo=>{

enemigo.traverse(
objeto=>{

if(objeto.isMesh){

objeto.userData.enemigo=
enemigo;

objetos.push(objeto);

}

});

});


const impactos=
raycaster.intersectObjects(
objetos,
false
);


if(impactos.length>0){

const enemigo=
impactos[0]
.object
.userData
.enemigo;


if(enemigo){

enemigo.userData.vida-=
arma.dano;


crearImpacto(
impactos[0].point
);


if(
enemigo.userData.vida<=0
){

eliminarEnemigo(enemigo);

}

}

}

}


/* =====================================================
   RASTRO
===================================================== */

function crearRastro(
origen,
direccion,
distancia
){

const fin=
origen.clone().add(
direccion.clone()
.multiplyScalar(distancia)
);


const geo=
new THREE.BufferGeometry()
.setFromPoints([
origen,
fin
]);


const mat=
new THREE.LineBasicMaterial({
color:0xffcc44,
transparent:true,
opacity:.9
});


const linea=
new THREE.Line(
geo,
mat
);

escena.add(linea);


setTimeout(
()=>{

escena.remove(linea);

geo.dispose();
mat.dispose();

},
90
);

}


/* =====================================================
   CHISPAS
===================================================== */

function crearChispas(
posicion,
direccion
){

for(let i=0;i<8;i++){

const chispa=
new THREE.Mesh(

new THREE.SphereGeometry(
.035,
6,
6
),

new THREE.MeshBasicMaterial({
color:0xffcc33
})

);

chispa.position.copy(posicion);

chispa.userData.vel=
new THREE.Vector3(

direccion.x+
(Math.random()-.5)*.8,

direccion.y+
(Math.random()-.5)*.8,

direccion.z+
(Math.random()-.5)*.8

).multiplyScalar(.3);

escena.add(chispa);

let tiempo=0;

function mover(){

if(!chispa.parent)return;

chispa.position.add(
chispa.userData.vel
);

chispa.userData.vel.y-=.02;

tiempo+=16;

if(tiempo>250){

escena.remove(chispa);

return;

}

requestAnimationFrame(mover);

}

mover();

}

}


/* =====================================================
   IMPACTO
===================================================== */

function crearImpacto(posicion){

const luz=
new THREE.PointLight(
0xffaa33,
8,
3
);

luz.position.copy(posicion);

escena.add(luz);

setTimeout(
()=>escena.remove(luz),
100
);

}


/* =====================================================
   MOVIMIENTO DE ENEMIGOS
===================================================== */

function moverEnemigos(){

const ahora=
performance.now();


enemigos.forEach(
enemigo=>{

/* CAMBIAR DIRECCIÓN */

if(
ahora>
enemigo.userData.cambioDireccion
){

enemigo.userData.direccion+=
(Math.random()-.5)*2;

enemigo.userData.cambioDireccion=
ahora+
1000+
Math.random()*2500;

}


/* SI ESTÁ CERCA DEL JUGADOR,
   LO PERSIGUE */

const distancia=
enemigo.position.distanceTo(
jugador.position
);


if(
distancia<16
){

const dx=
jugador.position.x-
enemigo.position.x;

const dz=
jugador.position.z-
enemigo.position.z;

enemigo.userData.direccion=
Math.atan2(dx,dz);

}


/* MOVIMIENTO */

const vel=
enemigo.userData.velocidad;

const dx=
Math.sin(
enemigo.userData.direccion
)*vel;

const dz=
Math.cos(
enemigo.userData.direccion
)*vel;


const nuevoX=
enemigo.position.x+dx;

const nuevoZ=
enemigo.position.z+dz;


if(
puedeMoverse(
nuevoX,
nuevoZ
)
){

enemigo.position.x=
nuevoX;

enemigo.position.z=
nuevoZ;

}else{

enemigo.userData.direccion+=
Math.PI/2;

}


/* MIRAR HACIA DONDE CAMINA */

enemigo.rotation.y=
enemigo.userData.direccion;


/* ANIMACIÓN SIMPLE DE CAMINAR */

const tiempo=
performance.now()*.008;

const piernas=
enemigo.children.filter(
objeto=>
objeto.geometry &&
objeto.geometry.type==="BoxGeometry"
);


/* ATAQUE */

if(distancia<25){

dispararEnemigo(enemigo);

}

});

}


/* =====================================================
   DISPARO ENEMIGO
===================================================== */

function dispararEnemigo(enemigo){

const ahora=
performance.now();


if(
ahora-
enemigo.userData.ultimoDisparo<
1800
)return;


enemigo.userData.ultimoDisparo=
ahora;


const origen=
enemigo.position.clone();

origen.y+=.7;


const direccion=
new THREE.Vector3();


direccion.subVectors(
jugador.position,
origen
);


direccion.normalize();


/* MALA PUNTERÍA */

direccion.x+=
(Math.random()-.5)*.35;

direccion.y+=
(Math.random()-.5)*.25;

direccion.z+=
(Math.random()-.5)*.35;

direccion.normalize();


sonidoDisparo();

crearRastro(
origen,
direccion,
20
);

crearChispas(
origen,
direccion
);


const haciaJugador=
new THREE.Vector3();


haciaJugador.subVectors(
jugador.position,
origen
);


const distancia=
haciaJugador.length();

haciaJugador.normalize();


const precision=
direccion.dot(
haciaJugador
);


if(
distancia<25&&
precision>.97
){

recibirDano(
agachado?4:8
);

}

}


/* =====================================================
   DAÑO
===================================================== */

function recibirDano(dano){

vida-=dano;

vida=
Math.max(
0,
vida
);


actualizarHUD();


document.body.style.boxShadow=
"inset 0 0 100px red";


setTimeout(
()=>{
document.body.style.boxShadow=
"none";
},
100
);


if(vida<=0){

perderJuego();

}

}


/* =====================================================
   ELIMINAR ENEMIGO
===================================================== */

function eliminarEnemigo(enemigo){

escena.remove(enemigo);

enemigos=
enemigos.filter(
e=>e!==enemigo
);

puntos+=100;

mostrarMensaje(
"+100 PUNTOS"
);


setTimeout(
()=>{

if(juegoActivo)
crearEnemigo();

},
1500
);


actualizarHUD();

}


/* =====================================================
   GAME OVER
===================================================== */

function perderJuego(){

juegoActivo=false;

document.exitPointerLock();

document.getElementById(
"puntosFinales"
).textContent=puntos;

document.getElementById(
"gameOver"
).style.display="flex";

}


/* =====================================================
   HUD
===================================================== */

function actualizarHUD(){

document.getElementById(
"vida"
).textContent=vida;

document.getElementById(
"puntos"
).textContent=puntos;

document.getElementById(
"enemigos"
).textContent=enemigos.length;

document.getElementById(
"armaHUD"
).textContent=
armas[armaActual].nombre;

document.getElementById(
"municion"
).textContent=
balas+
" / "+
CAPACIDAD_CARGADOR;

document.getElementById(
"barraVida"
).style.width=
vida+"%";


if(vida<=30){

document.getElementById(
"barraVida"
).style.background=
"#ff3333";

}else{

document.getElementById(
"barraVida"
).style.background=
"#38e85c";

}

}


/* =====================================================
   MENSAJE
===================================================== */

function mostrarMensaje(texto){

const mensaje=
document.getElementById(
"mensaje"
);

mensaje.textContent=texto;

mensaje.style.display="block";

setTimeout(
()=>{
mensaje.style.display="none";
},
700
);

}


/* =====================================================
   ANIMACIÓN
===================================================== */

function animar(){

requestAnimationFrame(animar);

if(!juegoActivo)return;

moverJugador();

moverEnemigos();

comprobarBotiquines();

actualizarHUD();

renderer.render(
escena,
camara
);

}


/* =====================================================
   RESIZE
===================================================== */

window.addEventListener(
"resize",
function(){

if(!camara)return;

camara.aspect=
innerWidth/innerHeight;

camara.updateProjectionMatrix();

renderer.setSize(
innerWidth,
innerHeight
);

});

</script>

</body>
</html>
```