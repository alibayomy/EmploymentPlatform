

function filterApplications(event){
    searchParam = $('#filterID').val()
    window.location.href = `/jobs/job-applications/1/?filter=${searchParam}`
    $('#filterID').val(searchParam)
}