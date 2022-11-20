// index.html , file rename 
// const paragraph = document.getElementById("edit");
o = document.getElementsByClassName("end-btn")
for (var i = 0; i < o.length; i++) {
    o[i].style.display = "none"
}




function MakeEditable(id) {
  var paragraph = document.getElementById(id);
  paragraph.contentEditable = true;
  paragraph.style.backgroundColor = "#222222";
  paragraph.focus();

  myArray = id.split("-");

  id_no = myArray[1]
//   console.log(id_no)
  edit_id = "edit-button-"+id_no
  end_id = "end-button-"+id_no
document.getElementById(end_id).style.display = "inline-block";
  document.getElementById(edit_id).style.display = "none";
};

function StopEditable(id) {
  var paragraph = document.getElementById(id);
  paragraph.contentEditable = false;
  paragraph.style.backgroundColor = "#333333";
  para = document.getElementById("paragraph")
  console.log(paragraph.innerHTML)




  id_no = myArray[1]
  console.log(id_no)
  edit_id = "edit-button-"+id_no
  end_id = "end-button-"+id_no
  document.getElementById(edit_id).style.display = "inline-block";
document.getElementById(end_id).style.display = "none";


input1 = paragraph.innerHTML
input2 = id_no
}

elements = document.getElementsByClassName("edits");

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('keypress', (evt) => {
    if (evt.which === 13) {
        evt.preventDefault();
    }
    })}