function process_inputs() {
  var entry_text = document.getElementById("date_input").value
  document.getElementById('date_input').value = ''

  var elem_arr = []
  for (var i = 1; i <= 2; i++)
  {
    selectElement = document.querySelector(`#select${i}`)
    output = selectElement.options[selectElement.selectedIndex].value
    selectElement.selectedIndex = null
    if (output.length == 0) {
      window.alert("Please make all selections.")
      return
    }
    elem_arr.push(output)
  }

  let isValidDate = Date.parse(entry_text)
  if (isNaN(isValidDate)) {
    window.alert("Please enter a valid input for date: yyyy-mm-dd.")
    $(`#select1`).prop('selectedIndex', 0)
    $(`#select2`).prop('selectedIndex', 0)
    $(`#select1`).material_select();
    $(`#select2`).material_select();
    return
  }

  window.location.replace(`../priceSearch/${elem_arr[0]}+${elem_arr[1]}+${entry_text}`)
}