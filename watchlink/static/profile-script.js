const icon_sidebar = document.querySelector('.sidebar-icon');
const sidebar = document.querySelector('.sidebar');
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

};

