$(function(){
  var grid = new Muuri('.grid', {dragEnabled: true });
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  axios.defaults.xsrfCookieName = "csrftoken";

  grid.on('dragReleaseEnd', function (item) {
    let order = grid.getItems().indexOf(item),
      item_id = item.getElement().getAttribute("data-item-id"),
      post_url = `/api/reorder-media/${item_id}/`,
      bodyFormData = new FormData();

    bodyFormData.append('order', order)

    axios({
      method: "POST",
      url: post_url,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" },
    }).then(function (response){
      console.log(response)
    });
  });

});
