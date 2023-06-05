const fotos = document.querySelectorAll('.foto')
const modalFoto = document.querySelector('.modalFoto')
const modalFotoFoto = document.querySelector('.modalFoto img')

fotos.forEach(foto=>{

    foto.addEventListener('click', (e)=>{
        e.preventDefault()  
        modalFotoFoto.src = foto.id
        modalFoto.classList.add('modal--show')
    })
})

for(let cerrarModal of cerrarModales){

    cerrarModal.addEventListener('click', (e)=>{
        e.preventDefault()
        modalFoto.classList.remove('modal--show')
    })
}