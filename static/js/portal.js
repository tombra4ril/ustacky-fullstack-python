const portal = (() => {
  // get elements
  const state = document.getElementById("state")
  const lga = document.getElementById("lga")
  const jamb = document.getElementById("jamb")
  const form = document.querySelector("form")
  const inputs_text = document.querySelectorAll("input[type=text], textarea")
  let states_lga = []
  
  // operation on the form
  form.addEventListener("submit", (event) => {
    event.preventDefault()
    // validate inputs field that should contain texts
    for(let input of inputs_text){
      if(input.value.trim() === "")
      input.focus()
    }
    // send the form data
    const body = new FormData(form)
    // append the image to the formdata
    let image = form.querySelector("input[type=file").files[0]
    fetch("/api/register", {
      method: "post",
      body: body,
      headers: {
        // "Content-Type": "multipart/form-data; charset=utf-8; boundary=--ToMbRa--"
      }
    })
    .then(response => response.json())
    .then(data => {
      if(data["status"] === "success"){
        window.location.href = "/admin/dashboard/"
      }else{
        console.log(`Failed: ${data["message"]}`)
        // display error message
        portal_modal["show"](`${data['message']}. Try again!`)
      }
    })
    .catch(error => {
      console.log(`Error: ${error}`)
      // display the error message
      portal_modal["show"]("Failed to register. Try again!")
    })
  })

  // operation for the jamb score
  jamb.addEventListener("change", (event) => {
    event.preventDefault()
    let value = event.target.value

  })

  // function to create a new option with data
  function create_option(select_element, text){
    const option = document.createElement("option")
    const text_node = document.createTextNode(text)
    option.appendChild(text_node)
    option.value = text
    select_element.appendChild(option)
  }

  // fetch states and lga
  fetch("/api/get-states-lga")
  .then(response => response.json())
  .then(data => {
    states_lga = data
    // append options to the select element
    if(states_lga.length > 0){
      states_lga.forEach(item => {
        let option_text = item["state"]
        create_option(state, option_text)
      })
    }
    state.value = "select-state"
    state.addEventListener("change", () => {
      // find the object of the states with its local governments
      let state_lga_item = (states_lga.filter((item) => item["state"] === state.value))[0]
      let local = state_lga_item["local"]
      // populate the local goverment select element
      if(local.length > 0){
        // remove all child nodes of the lga select elment except the first one
        while(lga.childElementCount > 1){
          lga.removeChild(lga.lastChild)
        }
        local.forEach(l => {
          create_option(lga, l)
        })
      }
    })
  })
  .catch(error => console.log(`Error: occured while fetching states and their lga!\n${error}`))
})()