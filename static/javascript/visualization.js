function getSelections() {

  var fuel_type =  $(`#select1`).val()

  var area_list = $(`#select2`).val()

  $(`#select1`).prop('selectedIndex', 0)
  $(`#select2`).prop('selectedIndex', 0)
  $(`#select1`).material_select();
  $(`#select2`).material_select();


  var area = ""
  for (i = 0; i < area_list.length; i++) {
    area = area.concat('+', area_list[i])
  }

  if (fuel_type == null || area_list.length == 0){
    window.alert("Please make all selections.")
    return
  }

  window.location.replace(`../visualization/${fuel_type}${area}`)
}