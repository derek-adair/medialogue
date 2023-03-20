/********************************************************************
 * Common Filepond Config / implementation
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
