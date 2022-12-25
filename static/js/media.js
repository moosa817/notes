function SwitchModalData(url,type){
	o = ['png','jpg','jpeg','wbep','icon','xml','tiff','gif']
	if(type === "mp4" || type==="ogg" || type==="webm"){
		document.getElementById("modal-body").innerHTML = `<video src='${url}' controls></video>'`
	}
	else if(o.includes(type)){
		document.getElementById("modal-body").innerHTML = `<img src='${url}' class='img-modal'>`
	}
	else{
		document.getElementById("modal-body").innerHTML = `<a href='${url}' target='_blank'>View File</a>`
	}
}


function copy(url,id){
	element = document.getElementById(id)
	console.log(url,id)
	navigator.clipboard.writeText(url)
	element.innerHTML = "Copied"
	setTimeout(() => {
		element.innerHTML = "Copy Url"
	}, 5000);
}
