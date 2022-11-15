$(document).ready(function() {
    $("nav ul li [href]").each(function() {
        if (this.href == window.location.href) {
            $(this).addClass("active-link");
        }
    });

});

// On page load set the theme.
// localStorage.setItem('theme', 0);

// 0 is dark theme, 1 is light theme



$(document).ready(function() {
n = localStorage.getItem('theme');
console.log(n)

if (n== null){
  n = 0;
  localStorage.setItem('theme', n);
}


if (n == 1){
  var element = document.body;

  element.classList.toggle("light-mode");
  document.getElementById('footer').classList.toggle('light-footer');
  document.getElementById('nav').classList.toggle('light-nav');
  document.getElementById('signup').classList.toggle('signup-light');



}
});


$(document).ready(function(){
const checkbox = document.getElementById('checkbox');

checkbox.addEventListener('change', ()=>{
  document.body.classList.toggle('light-mode');
  document.getElementById('footer').classList.toggle('light-footer');
  document.getElementById('nav').classList.toggle('light-nav');

  if (document.getElementById('signup') != null){
  classList.toggle('signup-light');
  }

  if (n == 0) {
    n = 1;
    localStorage.setItem('theme', n);
  }
  else{
    n = 0;
    localStorage.setItem('theme', n);
  }
  console.log(localStorage.getItem('theme'))




})




});


//pop up
// $(function(){
//   var overlay = $('<div id="overlay"></div>');
//   overlay.show();
//   overlay.appendTo(document.body);
//   $('.popup').show();
//   $('.close').click(function(){
//   $('.popup').hide();
//   overlay.appendTo(document.body).remove();
//   return false;
//   });
  
  
   
  
//   $('.x').click(function(){
//   $('.popup').hide();
//   overlay.appendTo(document.body).remove();
//   return false;
//   });
//   });

