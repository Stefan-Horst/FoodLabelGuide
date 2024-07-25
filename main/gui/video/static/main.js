let lblCounter = 0;

// event for new label data
const sourceLbl = new EventSource('/lbl');
sourceLbl.onmessage = (event) => {
  const parent = document.getElementById("labels-accordion");
  
  // if no label data just clear all existing labels
  if (event.data === "clear") {
    parent.replaceChildren();
    return;
  }

  // if label exists create new element from template and insert it into dom
  const template = document.querySelector("#label-template");
  const newLabelElement = template.content.cloneNode(true);

  const img_path = JSON.parse(event.data).img_path;
  const name = JSON.parse(event.data).name;
  const description = JSON.parse(event.data).description;

  // set element content
  let btnText = newLabelElement.querySelector("#clabel");
  btnText.textContent = name;

  let cdiv = newLabelElement.querySelector("#cdiv");
  cdiv.textContent = description;

  let img = newLabelElement.querySelector("#cimg");
  img.src = img_path;
  img.alt = name;

  // set element unique ids for bootstrap
  id = "collapse" + lblCounter;

  let btn = newLabelElement.querySelector("button");
  btn.setAttribute("data-bs-target", "#" + id);
  btn.setAttribute("aria-controls", id);

  let contentDiv = newLabelElement.querySelector("#collapse");
  contentDiv.id = id;

  parent.appendChild(newLabelElement);
  lblCounter++;
};
