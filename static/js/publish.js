function Publish(id,u){
    var e = document.getElementById("p-"+id)

    e.innerHTML = e.innerHTML+" .....Publishing"

    $.ajax({
        data: {
          to_publish: id
        },
        type: 'POST',
        url: '/publish'
      })
    .done(function (data) {
    if (data.success){
        // e.style.display = "none"
        e.remove()
        var new_element = document.createElement("div");
        new_element.id = 'p-'+id
        new_element.className = "e-box"
        new_element.innerHTML = `<a class="p-link" href="/notes?name=${id}">${id}</a><button class='btn-1' onclick="UnPublish('${id}','${u}')">Un-Publish</button>
        
        <button class="btn-1 btn-sm btn-primary" id="b-{{loop.index}}" onclick="copy('/public?name=${id}&username=${u}','b-{{loop.index}}')">Copy Url</button>
        
        
        
        
        
        
          `
          console.log(new_element)
      
    
        document.getElementById("published").appendChild(new_element)
    
    
    }
    
    })
}
function UnPublish(id,u){
    var e = document.getElementById("p-"+id)

    e.innerHTML = e.innerHTML+"Un Publishing"



  console.log(e.innerHTML)







    $.ajax({
        data: {
          un_publish: id
        },
        type: 'POST',
        url: '/publish'
      })
    .done(function (data) {
    if (data.success){
        e.remove()
        var new_element = document.createElement("div");
        new_element.className = "e-box"
        new_element.id = 'p-'+id


        new_element.innerHTML = `<a class="p-link" href="/notes?name=${id}">${id}</a><button class='btn-1' onclick="Publish('${id}','${u}')">Publish</button>`
    
        document.getElementById("unpublished").appendChild(new_element)
    }
    
    })
}

function copy(url,id){
	element = document.getElementById(id)
  url = window.location.host + url
	// console.log(url,id)
	navigator.clipboard.writeText(url)
	element.innerHTML = "Copied"
	setTimeout(() => {
		element.innerHTML = "Copy Url"
	}, 5000);
}


function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}













var editor_data = document.getElementById('editorData').innerHTML


function DownloadHtml(filename){
  download(filename+'.html',editor_data)
}

function downloadFile(filename, base64Url) {
  var a = document.createElement("a"); //Create <a>
    a.href = base64Url //Image Base64 Goes here
    a.download = filename; //File name Here
    a.click(); //Downloaded file
    a.remove();

}


function DownloadPdf(filename){
  $.ajax({
    data: {
      filename: filename,
      editor_data:editor_data
    },
    type: 'POST',
    url: '/download_pdf'
  })
.done(function (data) {
 if(data.success === true){
  downloadFile(filename+'.pdf',data.pdf_download)
 }
})

}