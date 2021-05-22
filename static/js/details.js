const details = (() => {
  // get elements
  const select = document.querySelector("#status")
  const status_element = document.querySelector(".student-header > div:last-child span")

  // add listener when the user changes the select option
  select.addEventListener("change", () => {
    // get the id of the user
    let id = select.getAttribute("data")
    // get the value the user selected
    let body = select.value
    // change the status of the student
    fetch(`/api/status/${id}`, {
      method: "post",
      headers:{
        "Content-Type": "application/json",
      },
      "body": JSON.stringify({
        "status": body
      })
    })
    .then(response => response.json())
    .then(data => {
      if(data["status"] === "success"){
        // status_element.textContent = body
        // refresh page
        window.location.href = `/admin/students/${id}`
      }else{
        portal_modal["show"]("Failed to Edit Status of User. Try again!")
      }
    })
    .catch(error => console.log("Failed to change status of student"))
  })
})()