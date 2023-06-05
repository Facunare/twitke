const flagsElement = document.getElementById('flags');
const textsToChange = document.querySelectorAll("[data-section]");
var id = flagsElement.getAttribute('tweet-id');
console.log(id)

const changeLanguage = async language=>{
    if(id == 'False'){
      console.log("falso")
      requestJson = await fetch(`/media/${language}.json`);
    }else if(id == 'True'){
      console.log("verdadero")
      requestJson = await fetch(`/media/en.json`);
    }
    const texts = await requestJson.json();
    
    for(const textToChange of textsToChange){
        const section = textToChange.dataset.section;
        const value = textToChange.dataset.value;
        console.log("hola" + value)
        if (value === "placeholderArea") {
            console.log("hola" + value)
            textToChange.setAttribute("placeholder", texts[section][value]);
          } else {
            textToChange.innerHTML = texts[section][value];
          }
    }



}
flagsElement.addEventListener("click", (e) =>{
    changeLanguage(e.target.parentElement.dataset.language);
});