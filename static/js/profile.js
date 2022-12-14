// /js for image upload page
// document.getElementById("Hidenews").style.display = "none";
// document.getElementById("tab1").className = "highlight";
// document.getElementById("header").innerHTML = "Crafts";
var name_url 
//Set classes and page ^ v
document.getElementById("tab1").addEventListener("click", highlight1);
document.getElementById("tab2").addEventListener("click", highlight2);


document.getElementById("toChange").innerHTML = document.getElementById("page1").innerHTML


//What happens when you click on tab 1:
function highlight1() {
  // console.log(name_url)
  document.getElementById("tab1").className = "highlight";
  // document.getElementById("tab2").className = "none";
  // document.getElementById("header").innerHTML = "Crafts";
  document.getElementById("toChange").innerHTML =
    document.getElementById("page1").innerHTML
}
//What happens when you click on tab 2:
function highlight2() {
  document.getElementById("tab2").className = "highlight";
  // document.getElementById("tab1").className = "none";
  // document.getElementById("header").innerHTML = "News page";
  document.getElementById("toChange").innerHTML =
  document.getElementById("page2").innerHTML
  

}


//end 
function readURL(input) {
  if (input.files && input.files[0]) {
    document.getElementById('url-submit').style.display = 'inline-block';
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#blah')
              .attr('src', e.target.result);
      };

      reader.readAsDataURL(input.files[0]);
  }
}

//on add click
$('#add').click(function(){
  // $('[name="thumbnail"]').on('change', function() {
    p = document.getElementById('url').value
    document.getElementById('url-error').style.display = 'none';
    console.log(p)
  
    a = $('img.preview').prop('src', p);
    document.getElementById('url-submit').style.display = 'block';
    console.log(a)
  });


  $("#form1 :input").on('input', function() {
  v = document.getElementById('del-field').value
  if (v === "DELETE MY ACCOUNT"){
    document.getElementById('del-btn').style.display = "block"
  }
  });


// profile_edit js

function update(){
  username = document.getElementById('username').value
  old_pwd = document.getElementById('old_pwd').value
  new_pwd = document.getElementById('new_pwd').value
  document.getElementById('edit-success').style.display = 'block'
  document.getElementById('edit-success').innerHTML = 'Updating..'
  document.getElementById('edit-error').style.display = "none";



  $.ajax({
    data: {
      username: username,
      old_pwd: old_pwd,
      new_pwd: new_pwd
    },
    type: 'POST',
    url: '/profile_edit'
  })
.done(function (data) {
  console.log(data)
  if(data.error){
  document.getElementById('edit-success').style.display = 'none'

    document.getElementById('edit-error').style.display = "block";
    document.getElementById('edit-error').innerHTML = data.error
  }
  if (data.success){
    document.getElementById('edit-error').style.display = "none";
    document.getElementById('edit-success').style.display = 'block'

    document.getElementById('edit-success').innerHTML = data.success


  }
  if(data.nothing){
    document.getElementById('edit-success').style.display = 'none'
    document.getElementById('edit-error').style.display = "none";


  }

})
};