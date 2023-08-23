window.onload = enableTooltips();

function enableTooltips() {
  // Enable tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })
}

function setDataSource(client, type) {
  document.querySelectorAll(`.${type}-data`).forEach(el => {
    el.classList.add("d-none")
  });
  document.querySelectorAll(`.${client}`).forEach(el => {
    el.classList.remove("d-none")
  });
}
