const clear_icon = document.querySelector(".clear");

const icon_sidebar = document.getElementById('menu-button');
const sidebar = document.getElementById('sidebar');
const close_sidebar = document.getElementById('close-sidebar');

icon_sidebar.onclick = () =>
{
  sidebar.classList.toggle('active');
};

close_sidebar.onclick = () => 
{
   
    if (sidebar.classList.contains('active')) {
        sidebar.classList.remove('active');
    };
    icon_sidebar.style.visibility = "visible";
};

var i = 0;
var increment = 1;

setInterval(() => {
  document.getElementById("Animated-container").style.background = "linear-gradient(45deg, rgba(49,226,215,1) 0%, rgba(253,29,199,0.4) " + i + "%, darkorchid 100%)";

  i += increment;

  if (i >= 100 || i <= 0) {
    increment *= -1;
  }
}, 100);
