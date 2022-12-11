// index.html , file rename 
// const paragraph = document.getElementById("edit");
o = document.getElementsByClassName("end-btn")
for (var i = 0; i < o.length; i++) {
  o[i].style.display = "none"
}


var orignal_para;

function MakeEditable(id) {
  orignal_para = document.getElementById(id).innerHTML;
  var paragraph = document.getElementById(id);

  paragraph.contentEditable = true;
  paragraph.style.backgroundColor = "#222222";
  paragraph.focus();

  myArray = id.split("-");

  id_no = myArray[1]
  //   console.log(id_no)
  edit_id = "edit-button-" + id_no
  end_id = "end-button-" + id_no
  document.getElementById(end_id).style.display = "inline-block";
  document.getElementById(edit_id).style.display = "none";
};

function StopEditable(id) {
  var paragraph = document.getElementById(id);
  paragraph.contentEditable = false;
  paragraph.style.backgroundColor = "#333333";
  para = document.getElementById("paragraph")
  // console.log(paragraph.innerHTML)




  id_no = myArray[1]
  // console.log(id_no)
  edit_id = "edit-button-" + id_no
  end_id = "end-button-" + id_no
  document.getElementById(edit_id).style.display = "inline-block";
  document.getElementById(end_id).style.display = "none";



  input1 = paragraph.innerHTML
  input2 = orignal_para


  input1 = input1.replace(/&nbsp;/g,'');
  input2 = input2.replace(/&nbsp;/g,'');

  console.log(input1)
  console.log(input2)

  $.ajax({
    data: {
      input1: input1,
      input2: input2
    },
    type: 'POST',
    url: '/edit_name'
  })
.done(function (data) {
  if (data.error){
    document.getElementById('error').style.display = "block";
    document.getElementById('error').innerHTML = data.error
    paragraph.innerHTML = orignal_para
  }

  

})};






elements = document.getElementsByClassName("edits");

for (var i = 0; i < elements.length; i++) {
  elements[i].addEventListener('keypress', (evt) => {
    if (evt.which === 13) {
      evt.preventDefault();
    }
  })
};
var f 
var id_no
function open_delete(id){
  myArray = id.split("-");
  id_no = myArray[1]
  f = document.getElementById(id).innerHTML
  document.getElementById("modal-body").innerHTML  = "You Sure you want to delete " + f

}
// file delete
function delete_name(){
  $.ajax({
    data: {
      delete_input: f
    },
    type: 'POST',
    url: '/delete_name'
  })
.done(function (data) {
 if (data.success === true){
  e_id = "f-"+id_no
  console.log(e_id)
  document.getElementById(e_id).remove()
}
})};



function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}






// file download 
var file_name
function download_name(id){
  file_name = document.getElementById(id).innerHTML
  $.ajax({
    data: {
      download_file: file_name
    },
    type: 'POST',
    url: '/download_name'
  })
.done(function (data) {
 if(data.success === true){
  filename = file_name+".html"
    download(filename,data.data)
 }
})

}