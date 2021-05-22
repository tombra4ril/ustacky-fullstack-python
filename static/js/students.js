const students = (() => {
  const actions = document.querySelectorAll("span.details")
  const name_search = document.querySelector("#search-div input[name=name]")
  const status_search = document.querySelector("#search-div select[name=status]")
  const gender_search = document.querySelector("#search-div select[name=gender]")
  const jamb_search = document.querySelector("#search-div input[name=jamb]")
  const form = document.querySelector("#search-div")

  // operations for searching for a particular person
  form.addEventListener("submit", (event) => {
    event.preventDefault()
    // sanitize params
    let name = name_search.value.trim()
    let status = status_search.value.trim()
    let gender = gender_search.value.trim()
    let jamb = jamb_search.value.trim()

    // create query parameters and redirect
    window.location.href = window.location.pathname + `?` + new URLSearchParams({
      name: name,
      status: status,
      gender: gender,
      jamb: jamb
    })
  })

  // actions column operations
  actions.forEach(element => {
    element.addEventListener("click", (event) => {
      window.location.href = `/admin/students/${element.id}`
    })
  })
})()