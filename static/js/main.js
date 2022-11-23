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


  // document.reload();
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




  window.location.reload();

})




});


// to stop the browser from resubmit
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
}

elements = document.getElementsByName("fadeOut")

setTimeout(function() {
  $('div[name=fadeOut]').fadeOut('fast');
}, 20000);