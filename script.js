const clear_icon = document.querySelector(".clear");

clear_icon.onclick = () =>
{
  document.getElementById("search").value = "";
};



var i=0;

setInterval(()=>{

    document.getElementById("Animated-container").style.background="linear-gradient(45deg, rgba(49,226,215,1) 0%, rgba(253,29,199,0.4) "+i*1+"%, darkorchid 100%)";
    document.getElementById("Animated-container").style.backgroundRepeat="no-repeat";
    
    
    
     i++;
     
     
    if(i==100){
        
        i=0;      
               
    }
   
    
},100);

JavaScript
const messageBox = document.querySelector(".message-box");
const userIcon = document.querySelector(".user-icon");

let timer;

userIcon.onclick = () => {
  messageBox.classList.toggle('active');
  if (messageBox.classList.contains('active')) {
    clearTimeout(timer);
  } else {
    timer = setTimeout(() => {
      messageBox.classList.remove('active');
    }, 6000);
  }
};

messageBox.addEventListener('mouseenter', () => {
  clearTimeout(timer);
});

messageBox.addEventListener('mouseleave', () => {
  timer = setTimeout(() => {
    messageBox.classList.remove('active');
  }, 200);
});
