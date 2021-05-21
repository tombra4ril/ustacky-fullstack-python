const portal_modal = (() => {
  // get elements for the modal dialog box
  const modal = document.querySelector("#modal")
  const modal_content = modal.querySelector(".modal-text")
  const modal_close = modal.querySelector(".modal-close")
  let timer_event

  // close modal box click event
  modal_close.addEventListener("click", hide_modal)

  // displays modal box when there is an error
  function show_modal(message){
    // remove the modal box and clear the timer function
    modal.classList.remove("show")
    clearTimeout(timer_event)
    // show the modal box
    modal_content.textContent = message
    modal.classList.add("show")
    // hide modal after 10 seconds
    timer_event = setTimeout(hide_modal, 10000)
  }

  // hides modal box
  function hide_modal(){
    modal.classList.remove("show")
  }

  return {
    show: show_modal
  }
})()