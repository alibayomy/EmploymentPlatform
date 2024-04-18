function filterApplications(event){
    searchParam = $('#filterID').val()
    main_url = window.location.protocol + "//" + window.location.host + window.location.pathname
    url = main_url+`?filter=${searchParam}`
    window.location.replace(url)
    $('#filterID').val(searchParam)
 }
 