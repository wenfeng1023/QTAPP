$(document).ready(function () {
    if (isMobile()) {
        $('#mobile_bar').css({ display: 'block' })
    }
})

function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
        (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
}

function hideMobileBar() {
    $('#mobile_bar').css({ display: 'none' })
}

function openMobileApp(host) {
    if (typeof currentPage === 'undefined' || currentPage === null) {
        window.location.href = `${host}/read?type=bible`
    } else {
        let current = currentPage.verseList['Content'][currentPage.verse]
        window.location.href = `${host}/read?type=bible&val1=${current.Book}&val2=${current.Chapter}&val3=${current.Verse}`
    }
}