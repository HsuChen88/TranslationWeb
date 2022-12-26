let startBtn = document.getElementById("speak");
if (startBtn) {
  startBtn.addEventListener("click", function() {
    document.getElementById("start-message").innerHTML = "Start Recording...";
  })
}

let inputElement = document.getElementById("input-file");
inputElement.addEventListener("change", handleFiles);
function handleFiles() {
  let fileList = this.files; /* now you can work with the file list */
  let filename = fileList[0]['name'];
  console.log("uploaded file name: ", filename);
  document.getElementById("uploaded-message").innerHTML = filename;
}

