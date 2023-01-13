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

    email = document.getElementById('email-'+id_no)

  $.ajax({
    data: {
      input1: input1,
      input2: input2,
      email:email.innerHTML
    },
    type: 'POST',
    url: '/admin'
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

function SwitchView(id) {
  elem = document.getElementById(id)
  elem.innerHTML = elem.getAttribute('data')

}
function showInfo(ip){
  body = document.getElementById('modal-body2')


  $.ajax({
    data: {
      "get": 'a',
    },
    type: 'POST',
    url: '/get_info'
  })
.done(function (data) {
 
      country = data["country"]

      regionname = data["region"]
      city = data["city"]
      zip = data["postal"]
      loc= data["loc"]
      timezone = data["timezone"]
      isp = data["org"]

      html = `<b>Country</b>: ${country}<br>
              <b>Region Name</b>: ${regionname}<br>
              <b>City</b>: ${city}<br>
              <b>Zip Code</b>: ${zip}<br>
              <b>Location</b> : ${loc}<br>
              <b>Timezone</b>: ${timezone}<br>
              <b>ISP</b> : ${isp}<br>
      `

      body.innerHTML= html
      // console.log(body)
  })
 
}