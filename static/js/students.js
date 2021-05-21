const students = (() => {
  const actions = document.querySelectorAll("span.details")

  // actions column operations
  actions.forEach(element => {
    element.addEventListener("click", (event) => {
      window.location.href = `/admin/students/${element.id}`
    })
  })
})()