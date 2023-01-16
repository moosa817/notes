function SwitchModalData(url, type) {
  o = ['png', 'jpg', 'jpeg', 'webp', 'icon', 'xml', 'tiff', 'gif']
  if (type === "mp4" || type === "ogg" || type === "webm") {
    document.getElementById("modal-body").innerHTML = `<video src='${url}' controls width="100%"></video>'`
  }
  else if (o.includes(type)) {
    document.getElementById("modal-body").innerHTML = `<img src='${url}' class='img-modal'>`
  }
  else {
    document.getElementById("modal-body").innerHTML = `<a href='${url}' target='_blank'>View File</a>`
  }
}


function copy(url, id) {
  element = document.getElementById(id)
  // console.log(url, id)
  navigator.clipboard.writeText(url)
  element.innerHTML = "Copied"
  setTimeout(() => {
    element.innerHTML = "Copy Url"
  }, 5000);
}

function ShowDelete(path) {
  document.getElementById("modal-body").innerHTML = `'You Sure you want to Delete ${path}'
	<form method="POST">
	<input type="hidden" value="${path}" name="delete-file">
	<button class="btn btn-danger" type="submit">Delete</button>
	</form>
	
	
	`

  // console.log("name")
}


function UploadShow() {







  document.getElementById("modal-body").innerHTML = `<form method="post" class="url-form" enctype="multipart/form-data">
	<!-- HTML code -->
<input type="file" id="file-input" name="file-input">
<div id="preview"></div>

	<input id="url-submit" class="submit-url" type="submit" value="Submit">
  </form>
`
  var input = document.getElementById('file-input');
  var preview = document.getElementById('preview');

  // Add an event listener to the input element
  input.addEventListener('change', function () {
    document.getElementById('url-submit').style.display = 'block'
    // Get the selected file
    var file = input.files[0];

    // Check if the file is an image
    if (file.type.match(/image.*/)) {
      // Use the FileReader API to read the file as a data URL
      var reader = new FileReader();
      reader.addEventListener('load', function () {
        // Create an image element and set its src attribute to the data URL
        var img = document.createElement('img');
        img.src = reader.result;
        // Append the image element to the preview element
        preview.innerHTML = img.outerHTML;
      });
      reader.readAsDataURL(file);
    } else if (file.type.match(/video.*/)) {
      // Use the FileReader API to read the file as a data URL
      var reader = new FileReader();
      reader.addEventListener('load', function () {
        // Create a video element and set its src attribute to the data URL
        var video = document.createElement('video');
        video.src = reader.result;
        video.controls = true;
        // Append the video element to the preview element
        preview.innerHTML = video.outerHTML;
      });
      reader.readAsDataURL(file);
    }
  });




}

$('#sync').click(function () {
  this.innerHTML = "Syncing Plz Wait"
  console.log("syncing")
  $.ajax({
    data: {
      sync: true,
    },
    type: 'POST',
    url: '/media'
  })
    .done(function (data) {
      if(data.success){
        console.log("here iam")
        document.getElementById('sync').innerHTML = "Synced"
        document.getElementById('synctime').innerHTML = data.time
      }
      else{
        document.getElementById('sync').innerHTML = "Sync Failed"
      }
     })


})

  // JavaScript code
