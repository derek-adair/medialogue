$(function(){
  var grid = new Muuri('.grid', {dragEnabled: true }),
    add_to_album_modal = $("#add-to-album-modal").modal({"keyboard": false, "show": (window.location.hash == "#add-to-album")});
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  axios.defaults.xsrfCookieName = "csrftoken";
  
	add_to_album_modal.on('hidden.bs.modal', function(e){
		// remove add-to-modal hash without refreshing
    history.pushState("", document.title, window.location.pathname + window.location.search);
	})
  $("#add-to-album").click(function(e){
    add_to_album_modal.modal('show')
	})
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
FilePond.registerPlugin(
  FilePondPluginImagePreview,
);

// Select the file input and use 
// create() to turn it into a pond
const pond = FilePond.create(
    document.getElementById('attachments'), {
        onaddfilestart: (file) => { isLoadingCheck(); },
        onprocessfile: (files) => { isLoadingCheck(); } 
    }
);
function isLoadingCheck(){
    var isLoading = pond.getFiles().filter(x=>x.status !== 5).length !== 0,
        submitBtn = document.querySelector('form [type="submit"]')
    
    if(isLoading) {
        submitBtn.setAttribute("disabled", "disabled");
    } else {
        submitBtn.removeAttribute("disabled");
    }
}
FilePond.setOptions({
    server: {
	url: window.location.origin + '/fp',
	headers: {
	    'X-CSRFToken': csrftoken
	},
        process: '/process/',
        patch: '/patch/',
        revert: '/revert/',
        fetch: '/fetch/?target='
    },
});
