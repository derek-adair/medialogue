$(function(){
  var grid = new Muuri('.grid', {dragEnabled: true }),
    add_to_album_modal = $("#add-to-album-modal").modal({"keyboard": false, "show": (window.location.hash == "#add-to-album")});
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  axios.defaults.xsrfCookieName = "csrftoken";

  /********************************************************************
   * Add To Album Modal Stuff
   *******************************************************************/
	add_to_album_modal.on('hidden.bs.modal', function(e){
		// remove add-to-modal hash without refreshing
    history.pushState("", document.title, window.location.pathname + window.location.search);
	})
  $("#open-media-model").click(function(e){
    add_to_album_modal.modal('show')
	})
  $("#add-to-album").click(function(e){
    let mediaForm = $("form#add-to-album-form"),
        post_url = mediaForm.attr("action"),
        filelistInputs = mediaForm.find(":input[name=filepond]"),
        filelist = [],
        bodyFormData = new FormData();

  filelistInputs.each(function(i, el){
    bodyFormData.append("filelist", $(el).val())
  })
    axios({
      method: "POST",
      url: post_url,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" },
    }).then(function (response){
      if (response.status == 200){
         window.location = `/album/${response.data.slug}`
      }
    });
  })

  /********************************************************************
   * Muuri Grid
   *******************************************************************/
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
    }).then(function (response){
      console.log(response)
    });
  });

});

/********************************************************************
 * FilePond / upload stuff
 *******************************************************************/
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
