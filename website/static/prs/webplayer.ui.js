var baseUrl = null;

var bible = null;

var popupState = [];

var treeNavStack = [];

var currentPage = {
    playlist: null,
    section: null,
    verse: null,
    verseList: null,
    chaptersTitle: null,
    chaptersTitlePsalms: null,
    versesTitle: null,
    introductionCellText: null,
    availableBiblesTitle: null,
    showTimingMarks: false,
    isIntroduction: false,
    hasIntroAudio: false,
    selectedBook: -1,
    HidePurchasePrompt: false,
    cookiePrefix: null,
    IsRightToLeftText: false,
};

var playlistEditor = null;

var presenterMode = false;

const scrollPosition = {
    ABOVE: 'above',
    BELOW: 'below',
    VISIBLE: 'visible'
}

var player = null;

$(document).ready(function () {
    var fontSizeKey = presenterMode ? "presenter_font_size" : "font_size";
    var fontSize = getCookie(fontSizeKey);// Cookies.get(fontSizeKey);
    if (fontSize == null) {
        fontSize = $("#bible_content").css("fontSize");
        Cookies.set(fontSizeKey, fontSize, { expires: 365 });
    }

    var minSize = parseInt($('#font_size_slider').prop('min'));
    var maxSize = parseInt($('#font_size_slider').prop('max'));
    fontSize = parseInt(fontSize);
    if (fontSize < minSize) {
        fontSize = minSize;
    } else if (fontSize > maxSize) {
        fontSize = maxSize;
    }

    $("#bible_content").css("font-size", fontSize + "px");

    $('#font_size_slider').val(fontSize);

    $('#font_size_slider').on('input', function () {
        var v = $(this).val();
        $("#bible_content").css("font-size", v + "px");
        setCookie(fontSizeKey, v + "px", { expires: 365 });//  Cookies.set(fontSizeKey, v + "px", { expires: 365 });
    });

    $("#select_fontfamily").higooglefonts({
        selectedCallback: function (e) {
            console.log(e);
        },
        loadedCallback: function (font) {
            console.log(font);
            /*/////// This is where you should apply font.///////
            /////////////////////////////////////////////////////*/
            $("#bible_content").css("font-family", font); // Change the font-family of the #paragraph
        }
    });

    configurePlaylistSourcName();

    if (bible.AllowBibleSelctionUI) {
        $('#bible_name').addClass('bible_name_clickable');
    }

    $("#bible_content").css("direction", bible.TextDirection);

    var clientID = getCookie('clientid');// Cookies.get('clientid');
    if (clientID) {
        analytics.setUserId(clientID);
    } else {
        analytics.setUserId("");
    }

    var ul = getCookie('language');//Cookies.get('language');
    analytics.setUserProperties({ language: ul });

    analytics.setCurrentScreen("web player");

    if (bible) {
        analytics.logEvent("bible", { action: "selected_bible", label: bible.Name })
    }

    $('.fixed-action-btn').floatingActionButton({
        direction: 'top',
        hoverEnabled: false
    });

    addTimingMarkAdjusters();
    addFootnoteTooltips();

    if (presenterMode) {
        $('verse').hide();
    } else {
        $('#bible_content_wrapper').resizableSafe({
            handleSelector: '.splitter',
            resizeWidth: false,
            onDrag: function (e, $e1, newwitdh, newhieght, opt) {
                var topheight = $('#bible_content_wrapper').height();
                var heightdiff = newhieght - topheight;

                var bottomheight = $('#tree_content_wrapper').height();
                var newbottomheight = bottomheight - heightdiff;

                return newhieght > 200 && newbottomheight > 200;
            }
        });
    }

    addClickHandlers();
    selectCurrentVerse();
    showPlaylistFullscreenButton(currentPage.playlist != null)

    if (currentPage.playlist == null) {
        var book = parseInt(getCookie('book', -1))
        var chapter = parseInt(getCookie('chapter', -1))
        var verse = parseInt(getCookie('verse', 0))

        goToPage(book, chapter, verse, false);
    }
});

function setCookie(name, value) {
    Cookies.set(currentPage.cookiePrefix + "-" + name, value);
}

function getCookie(name, def = null) {
    var value = Cookies.get(currentPage.cookiePrefix + "-" + name);
    if (value) {
        return value;
    }

    return def;
}

function showPlaylistFullscreenButton(show) {
    if (!presenterMode) {
        if (show) {
            $('#playlist_fullscreen_button').show();
        } else {
            $('#playlist_fullscreen_button').hide();
        }
    }
}

function goPlaylistFullscreen() {
    if (currentPage.playlist) {
        window.location.href = `${baseUrl}Presenter?playlist=${currentPage.playlist}&section=${currentPage.section}`
    }
}

function enablePresenterMode() {
    presenterMode = true;
}

function closePlaylist() {
    var book = getCookie('book', -1);//  Cookies.get('book') ?? -1;
    var chapter = getCookie('chapter', -1);// Cookies.get('chapter') ?? -1;
    var verse = getCookie('verse', 0);//Cookies.get('verse') ?? 0;

    goToPage(book, chapter, verse, false);
}

function configurePlaylistSourcName() {
    $('#source_name').off('click');

    if (currentPage.playlist) {
        $('#source_name').addClass('source_name_clickable');
        $('#playlist_name_container').css({ 'visibility': 'visible' });
        $('#source_name').click(function () {
            showPlaylistSections(this);
        });
    } else {
        $('#playlist_name_container').css({ 'visibility': 'hidden' });
        $('#source_name').removeClass('source_name_clickable');
    }
}

function handleToggleShowTimingMarks() {
    currentPage.showTimingMarks = !currentPage.showTimingMarks;

    goToPage(currentPage.verseList['Content'][currentPage.verse].Book - 1,
        currentPage.verseList['Content'][currentPage.verse].Chapter - 1,
        currentPage.verseList['Content'][currentPage.verse].Verse - 1,
        false,
        false);

    hideMenu(true);
}

function addTimingMarkAdjusters() {
    if (currentPage.showTimingMarks) {
        $('verse').each(function (index) {
            $('<div id="tm_' + index + '" class="tm_range">' + currentPage.verseList['Content'][index].AudioStart + ' - ' + currentPage.verseList['Content'][index].AudioEnd + '<span id="ct_' + index + '" class="tm_timer"> </span></div>').insertBefore(this);
        });
    }
}

function addFootnoteTooltips() {
    //$('.footnote').each(function (index) {
    //    //$(this).addClass('tooltip');
    //    //this.innerHTML = '<div class="tooltip">X<span class="tooltiptext">this is a test</span></div>';
    //    this.innerHTML = '<sup>+</sup>';
    //    attachNote(this.href, this);
    //});
}

function attachNote(link, elem) {
    var parts = link.split(':');
    var file = parts[parts.length - 1].replace('/#', '#');
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getstudynote',
        dataType: 'json',
        data: {
            file: file
        },
        success: function (data) {
            if (data.NotAuthorized) {
                showPurchaseNotice(data.Message, data.PurchaseLink, data.LinkText);
            } else if (data.Contents) {
                var note = "<sup title='" + data.Contents + "'>*</sup>";
                $(elem).html(data.Contents);
                elem.innerHTML = "<sup title='" + elem.innerHTML + "'>*</sup>";
            }
        },
        error: function (err) {
            alert(err.status);
        }
    });
}

function addClickHandlers() {
    $('verse').off().click(function () {
        currentPage.verse = $('verse').index(this);
        selectCurrentVerse(true);

        if (isPlaying()) {
            stopAudio(currentPage.isIntroduction);
            play();
        }
    });

    $('a[href]:not(.navigation_header *)').off().click(function (event) {
        var preventDefault = true;
        hideAllPopups();

        if (this.href.search('//verse_menu') != -1) {
            if (this.href.includes(".html")) {
                var parts = this.href.split(':');
                var file = parts[parts.length - 1].replace('/#', '#');
                clearTreeNavStack();
                getStudyNote(file);
            }
        } else if (this.hash && this.hash.startsWith('#v')) {
            var matches = this.hash.match(/([0-9]{2})([0-9]{3})([0-9]{3})/);
            goToPage(parseInt(matches[1]) - 1, parseInt(matches[2]) - 1, parseInt(matches[3]) - 1);
        } else if (this.href.startsWith('videos:')) {
            showVideoPopup(this.href);
        } else if (this.href.startsWith('gotourl:')) {
            this.href = this.href.replace('gotourl:', '');
            preventDefault = false;
        } else if (this.href.startsWith('purchase:')) {
            var url = new URL(this.href);
            doPurchase(url.searchParams.get('item'));
            preventDefault = true;
        } else if (this.href.includes("ChangeLanguage")) {
            showLoader(true);
            preventDefault = false;
        } else {
            var url = new URL(this.href);
            var pathName = url.pathname;

            if (pathName.endsWith(".png") || pathName.endsWith(".jpg")) {
                showImagePopup(this.href);
            } else {
                //   var parts = this.href.split('/');
                //   var file = parts[parts.length - 1];
                getStudyNote(pathName + url.hash);
            }
        }

        if (preventDefault) {
            event.preventDefault();
        }
    });

    $('#bible_name').off('click');

    if (bible.AllowBibleSelctionUI) {
        $('#bible_name').click(function () {
            showAvailableBibles(this);
        });
    }
}

function handleAccountClick(loggedIn) {
    if (loggedIn) {
        window.location.href = './Account/Logout';
    } else {
        window.location.href = './Account/Login';
    }
}

function handleManageAccountClick() {
    window.location.href = './Account/Manage';
}

function doPurchase(item) {
    window.location.href = './Player/Purchase?item=' + item;
}

function selectCurrentVerse(animated) {
    if (presenterMode) {
        $("verse[display!='none']").hide();
        $('verse').eq(currentPage.verse).show();
        updatePresenterLocation();
    } else {
        $('.verse_selected').removeClass('verse_selected');
        var elem = $('verse').eq(currentPage.verse);
        elem.addClass('verse_selected');
        updateLocation();
        populateBookRelatedMaterials();
        updateButtons();
        savePosition();

        switch (getScrollPosition(elem)) {
            case scrollPosition.ABOVE:
                $("#bible_content_wrapper").animate({ scrollTop: elem.position().top + elem.height() - $("#bible_content_wrapper").height() + 50 }, animated ? 250 : 0);
                break;
            case scrollPosition.BELOW:
                $("#bible_content_wrapper").animate({ scrollTop: currentPage.verse == 0 ? 0 : elem.position().top - 50 }, animated ? 250 : 0);
                break;
        }
    }
}

function getScrollPosition(elem) {
    try {
        var elemTop = elem.offset().top;
        var elemBottom = elemTop + elem.height();

        var viewportTop = $("#bible_content_wrapper").offset().top;

        var viewportBottom = (viewportTop + $("#bible_content_wrapper").height()) - 20;

        if (elemTop < viewportTop) {
            return scrollPosition.ABOVE;
        } else if (elemBottom > viewportBottom) {
            return scrollPosition.BELOW;
        }
    } catch (ex) {
    }

    return scrollPosition.VISIBLE;
}

function savePosition() {
    setCookie('book', currentPage.verseList['Content'][currentPage.verse].Book - 1);//  Cookies.set('book', currentPage.verseList['Content'][currentPage.verse].Book - 1);
    setCookie('chapter', currentPage.verseList['Content'][currentPage.verse].Chapter - 1);//Cookies.set('chapter', currentPage.verseList['Content'][currentPage.verse].Chapter - 1);
    setCookie('verse', currentPage.verse);//Cookies.set('verse', currentPage.verse);

    var isPlaylist = currentPage.playlist != null && currentPage.section != null;

    $.post(baseUrl + 'syncposition',
        {
            mode: isPlaylist ? 'playlist' : 'normal',
            data1: isPlaylist ? currentPage.playlist : currentPage.verseList['Content'][currentPage.verse].Book - 1,
            data2: isPlaylist ? currentPage.section : currentPage.verseList['Content'][currentPage.verse].Chapter - 1,
            data3: currentPage.verse
        }
    );
}

function populateBookRelatedMaterials() {
    $('#related_materials_book_container').empty();
    if (currentPage.verseList['RelatedMaterials'][currentPage.verse]) {
        $('#related_materials_book').show();
        currentPage.verseList['RelatedMaterials'][currentPage.verse].forEach(function (item, index) {
            var book = currentPage.verseList['Content'][currentPage.verse].Book;
            var template = $('#related_materials_item_template').clone();
            template.attr('id', index);
            template.removeAttr('style');
            template.children('#related_materials_item_template_title').html(item.Name);
            $('#related_materials_book_container').append(template);
        });
    } else {
        $('#related_materials_book').hide();
    }
}

function updateLocation() {
    var book = getBook(currentPage.isIntroduction ? currentPage.selectedBook : currentPage.verseList['Content'][currentPage.verse].Book - 1);
    $('#location_book').html(book.Name);
    if (currentPage.isIntroduction) {
        $('#location_chapter').html(currentPage.introductionCellText);
        $('#location_verse').html('-');
    } else {
        $('#location_chapter').html(currentPage.verseList['Content'][currentPage.verse].Chapter);
        $('#location_verse').css({ visibility: 'visible' });
        $('#location_verse').html(book.Chapters[currentPage.verseList['Content'][currentPage.verse].Chapter - 1].Verses[currentPage.verseList['Content'][currentPage.verse].Verse - 1].Label);
    }
}

function updatePresenterLocation() {
    var book = getBook(currentPage.isIntroduction ? currentPage.selectedBook : currentPage.verseList['Content'][currentPage.verse].Book - 1);
    $('#location').text(`${book.Name} ${currentPage.verseList['Content'][currentPage.verse].Chapter} : ${book.Chapters[currentPage.verseList['Content'][currentPage.verse].Chapter - 1].Verses[currentPage.verseList['Content'][currentPage.verse].Verse - 1].Label}`);
}

function updateButtons() {
    $('#media_time_control').hide();
    if (currentPage.isIntroduction) {
        if (currentPage.hasIntroAudio) {
            $('#media_control_play_pause').removeClass('media_control_play_disabled');
            $('#media_control_play_pause').addClass('media_control_play');
            $('#media_control_play_pause').addClass('media_control_with_hover');
        } else {
            $('#media_control_play_pause').removeClass('media_control_play');
            $('#media_control_play_pause').removeClass('media_control_with_hover');
            $('#media_control_play_pause').addClass('media_control_play_disabled');
        }
    } else if (currentPage.verseList['Content'][currentPage.verse].HasAudio) {
        $('#media_control_play_pause').removeClass('media_control_play_disabled');
        $('#media_control_play_pause').addClass('media_control_play');
        $('#media_control_play_pause').addClass('media_control_with_hover');
    } else {
        $('#media_control_play_pause').removeClass('media_control_play');
        $('#media_control_play_pause').removeClass('media_control_with_hover');
        $('#media_control_play_pause').addClass('media_control_play_disabled');
    }

    if (currentPage.hasNextPage) {
        $('#media_control_step_forward').removeClass('media_control_step_forward_disabled');
        $('#media_control_step_forward').addClass('media_control_step_forward');
        $('#media_control_step_forward').addClass('media_control_with_hover');

        $('#media_control_fast_forward').removeClass('media_control_fast_forward_disabled');
        $('#media_control_fast_forward').addClass('media_control_fast_forward');
        $('#media_control_fast_forward').addClass('media_control_with_hover');
    } else {
        $('#media_control_step_forward').removeClass('media_control_step_forward');
        $('#media_control_step_forward').removeClass('media_control_with_hover');
        $('#media_control_step_forward').addClass('media_control_step_forward_disabled');

        if (currentPage.verse == currentPage.verseList['Content'].length - 1) {
            $('#media_control_fast_forward').removeClass('media_control_fast_forward');
            $('#media_control_fast_forward').removeClass('media_control_with_hover');
            $('#media_control_fast_forward').addClass('media_control_fast_forward_disabled');
        } else {
            $('#media_control_fast_forward').removeClass('media_control_fast_forward_disabled');
            $('#media_control_fast_forward').addClass('media_control_fast_forward');
            $('#media_control_fast_forward').addClass('media_control_with_hover');
        }
    }

    if (currentPage.hasPreviousPage) {
        $('#media_control_step_back').removeClass('media_control_step_back_disabled');
        $('#media_control_step_back').addClass('media_control_step_back');
        $('#media_control_step_back').addClass('media_control_with_hover');

        $('#media_control_rewind').removeClass('media_control_rewind_disabled');
        $('#media_control_rewind').addClass('media_control_rewind');
        $('#media_control_rewind').addClass('media_control_with_hover');
    } else {
        $('#media_control_step_back').removeClass('media_control_step_back');
        $('#media_control_step_back').removeClass('media_control_with_hover');
        $('#media_control_step_back').addClass('media_control_step_back_disabled');

        if (currentPage.verse == 0) {
            $('#media_control_rewind').removeClass('media_control_rewind');
            $('#media_control_rewind').removeClass('media_control_with_hover');
            $('#media_control_rewind').addClass('media_control_rewind_disabled');
        } else {
            $('#media_control_rewind').removeClass('media_control_rewind_disabled');
            $('#media_control_rewind').addClass('media_control_rewind');
            $('#media_control_rewind').addClass('media_control_with_hover');
        }
    }
}

function updatePurchaseNotice() {
    if (currentPage.HidePurchasePrompt) {
        $('#purchase_notice').hide();
    } else {
        $('#purchase_notice').show();
    }
}

function showPurchaseNotice(message, purchaseUrl, linkText) {
    hideMenu(true);
    $('#purchase_alert_title').text(message);
    $('#purchase_alert_action').attr("href", purchaseUrl);
    $('#purchase_alert_action').text(linkText);
    $('#purchase_alert').show();
}

function goPreviousVerse() {
    if (!currentPage.isIntroduction && currentPage.verse > 0) {
        currentPage.verse -= 1;

        var book = getBook(currentPage.verseList['Content'][currentPage.verse].Book - 1)
        var verse = book.Chapters[currentPage.verseList['Content'][currentPage.verse].Chapter - 1].Verses[currentPage.verseList['Content'][currentPage.verse].Verse - 1]

        if (verse.Skipped) {
            goPreviousVerse()
        } else {
            $('verse').eq(currentPage.verse).click();
        }
    } else {
        getPreviousPage(isPlaying(), true);
    }
}

function goNextVerse() {
    if (!currentPage.isIntroduction && currentPage.verse < currentPage.verseList.Count - 1) {
        currentPage.verse += 1;

        var book = getBook(currentPage.verseList['Content'][currentPage.verse].Book - 1)
        var verse = book.Chapters[currentPage.verseList['Content'][currentPage.verse].Chapter - 1].Verses[currentPage.verseList['Content'][currentPage.verse].Verse - 1]
        
        if (verse.Skipped) {
            goNextVerse()
        } else {
            $('verse').eq(currentPage.verse).click();
        }
    } else {
        getNextPage(isPlaying());
    }
}

function goPreviousPage() {
    getPreviousPage(isPlaying());
}

function goNextPage() {
    getNextPage(isPlaying());
}

function getNextPage(autoPlay) {
    if (currentPage.hasNextPage) {
        pause();
        if (currentPage.playlist != null && currentPage.section != null) {
            getPlaylist(currentPage.playlist, currentPage.section + 1, false);
        } else {
            showLoader(true);
            $.ajax({
                type: 'GET',
                url: baseUrl + 'getnextpage',
                dataType: 'json',
                data: {
                    book: currentPage.isIntroduction ? currentPage.selectedBook : currentPage.verseList['Content'][currentPage.verse].Book - 1,
                    chapter: currentPage.isIntroduction ? -1 : currentPage.verseList['Content'][currentPage.verse].Chapter - 1
                },
                success: function (data) {
                    if (data.AjaxFailed) {
                        location = data.Redirect;
                    } else {
                        currentPage.verseList = JSON.parse(data.VerseList);
                        currentPage.isIntroduction = false;
                        currentPage.hasIntroAudio = false;
                        currentPage.playlist = null;
                        currentPage.section = null;
                        currentPage.verse = 0;
                        currentPage.selectedBook = currentPage.verseList['Content'][currentPage.verse].Book - 1;
                        currentPage.hasNextPage = data.HasNextPage;
                        currentPage.hasPreviousPage = data.HasPreviousPage;
                        currentPage.HidePurchasePrompt = currentPage.verseList.HidePurchasePrompt;
                        currentPage.chaptersTitle = data.ChaptersTitle;
                        currentPage.chaptersTitlePsalms = data.ChaptersTitlePsalms;
                        currentPage.versesTitle = data.VersesTitle;
                        currentPage.IsRightToLeftText = data.IsRightToLeftText;

                        $('#bible_content').html(data.HTML);
                        $("#bible_content").css("direction", currentPage.IsRightToLeftText ? "rtl" : "ltr");
                        $('#bible_content_wrapper').scrollTop(0);
                        addClickHandlers();
                        selectCurrentVerse();

                        if (autoPlay) {
                            play();
                        }

                        sendJumpEvent();

                        addTimingMarkAdjusters();
                        addFootnoteTooltips();
                        showLoader(false);
                    }
                },
                error: function (err) {
                    showLoader(false);
                    alert(err.status);
                }
            });
        }
    }
}

function getPreviousPage(autoPlay, startOnLast) {
    if (currentPage.hasPreviousPage) {
        pause();
        if (currentPage.playlist != null && currentPage.section != null) {
            getPlaylist(currentPage.playlist, currentPage.section - 1, startOnLast);
        } else {
            showLoader(true);
            $.ajax({
                type: 'GET',
                url: baseUrl + 'getpreviouspage',
                dataType: 'json',
                data: {
                    book: currentPage.isIntroduction ? currentPage.selectedBook : currentPage.verseList['Content'][currentPage.verse].Book - 1,
                    chapter: currentPage.isIntroduction ? 0 : currentPage.verseList['Content'][currentPage.verse].Chapter - 1
                },
                success: function (data) {
                    if (data.AjaxFailed) {
                        location = data.Redirect;
                    } else {
                        currentPage.verseList = JSON.parse(data.VerseList);
                        currentPage.isIntroduction = false;
                        currentPage.hasIntroAudio = false;
                        currentPage.playlist = null;
                        currentPage.section = null;
                        currentPage.verse = startOnLast ? currentPage.verseList['Content'].length - 1 : 0;
                        currentPage.selectedBook = currentPage.verseList['Content'][currentPage.verse].Book - 1;
                        currentPage.hasNextPage = data.HasNextPage;
                        currentPage.hasPreviousPage = data.HasPreviousPage;
                        currentPage.HidePurchasePrompt = currentPage.verseList.HidePurchasePrompt;
                        currentPage.chaptersTitle = data.ChaptersTitle;
                        currentPage.chaptersTitlePsalms = data.ChaptersTitlePsalms;
                        currentPage.versesTitle = data.VersesTitle;
                        currentPage.IsRightToLeftText = data.IsRightToLeftText;

                        $('#bible_content').html(data.HTML);
                        $('#bible_content_wrapper').scrollTop(startOnLast ? $('#bible_content').height() : 0);
                        $("#bible_content").css("direction", currentPage.IsRightToLeftText ? "rtl" : "ltr");
                        addClickHandlers();
                        selectCurrentVerse();

                        if (autoPlay) {
                            play();
                        }

                        sendJumpEvent();

                        addTimingMarkAdjusters();
                        addFootnoteTooltips();

                        showLoader(false);
                    }
                },
                error: function (err) {
                    showLoader(false);
                    alert(err.status);
                }
            });
        }
    }
}

function sendJumpEvent() {
    var b = currentPage.verseList['Content'][currentPage.verse].Book;
    var book = getBook(b);
    if (book) {
        var ch = currentPage.verseList['Content'][currentPage.verse].Chapter;
        var v = currentPage.verseList['Content'][currentPage.verse].Verse;
        var bookname = book.Name;
        var label = bookname + " " + ch + ":" + v;
        analytics.logEvent("bible", { action: "jump", label: label })
    } else {
        console.log("failed to send jump event.");
    }
}

function goToBookIntroduction(book) {
    showLoader(true);
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getbookintro',
        dataType: 'json',
        data: {
            book: book
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                currentPage.isIntroduction = true;
                currentPage.hasIntroAudio = data.HasIntroAudio;
                currentPage.selectedBook = book;
                currentPage.verseList = null;
                currentPage.playlist = null;
                currentPage.section = null;
                currentPage.verse = null;
                currentPage.hasNextPage = data.HasNextPage;
                currentPage.hasPreviousPage = data.HasPreviousPage;
                currentPage.chaptersTitle = data.ChaptersTitle;
                currentPage.chaptersTitlePsalms = data.ChaptersTitlePsalms;
                currentPage.versesTitle = data.VersesTitle;
                currentPage.IsRightToLeftText = data.IsRightToLeftText;
                stopAudio();
                resetOffset();

                $('#bible_content').html(data.HTML);
                $("#bible_content").css("direction", currentPage.IsRightToLeftText ? "rtl" : "ltr");
                $('#source_name').html(data.Source);

                updateLocation();

                showLoader(false);
            }
        },
        error: function (err) {
            showLoader(false);
            alert(err.status);
        }
    });
}

function goToPage(book, chapter, verse, autoPlay, forceReload) {
    if (forceReload) {
        location.reload();
    } else {
        showLoader(true);
        $.ajax({
            type: 'GET',
            url: baseUrl + 'getpage',
            dataType: 'json',
            data: {
                book: book,
                chapter: chapter
            },
            success: function (data) {
                if (data.AjaxFailed) {
                    location = data.Redirect;
                } else {
                    currentPage.isIntroduction = false;
                    currentPage.hasIntroAudio = false;
                    currentPage.selectedBook = book;
                    currentPage.verseList = JSON.parse(data.VerseList);
                    currentPage.playlist = null;
                    currentPage.section = null;
                    currentPage.verse = verse;
                    currentPage.hasNextPage = data.HasNextPage;
                    currentPage.hasPreviousPage = data.HasPreviousPage;
                    currentPage.HidePurchasePrompt = currentPage.verseList.HidePurchasePrompt;
                    currentPage.chaptersTitle = data.ChaptersTitle;
                    currentPage.chaptersTitlePsalms = data.ChaptersTitlePsalms;
                    currentPage.versesTitle = data.VersesTitle;
                    currentPage.IsRightToLeftText = data.IsRightToLeftText;

                    $('#bible_content').html(data.HTML);
                    $("#bible_content").css("direction", currentPage.IsRightToLeftText ? "rtl" : "ltr");
                    try {
                        $('#bible_content_wrapper').scrollTop(verse > 0 ? $('verse').eq(verse).position().top : 0);
                    } catch (err) {

                    }

                    $('#source_name').html(data.Source);
                    configurePlaylistSourcName();

                    if (!data.ContentOwned) {

                    }

                    addClickHandlers();
                    try {
                        selectCurrentVerse();
                    } catch (err) {
                    }

                    if (autoPlay) {
                        play();
                    } else {
                        pause(); //to reset play button
                    }

                    sendJumpEvent();

                    addTimingMarkAdjusters();
                    addFootnoteTooltips();
                    showLoader(false);
                    showPlaylistFullscreenButton(currentPage.playlist != null);
                }
            },
            error: function (err) {
                showLoader(false);
                alert(err.status);
            }
        });
    }
}

function createSearchElement(id, onkeyupFunction) {
    var search = $('#search_template').clone();
    search.removeAttr('style');
    var languageSearch = search.find('#searchInput').attr('id', id);
    languageSearch.attr("onkeyup", onkeyupFunction);
    languageSearch.attr('onsearch', onkeyupFunction);
    return search;
}

function showAvailableBibles(elem) {
    showAvailableBiblesForLanguage();
}

function countrySearch() {
    var input = document.getElementById('searchCountries');
    var filter = input.value.toUpperCase();
    $('.bible_item').each(function () {
        var name = $(this).attr('name');
        if ((name && name.toUpperCase().indexOf(filter)) > -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

function getLanguageFromCountryElement(elem) {
    var parent = $(elem).closest('.bible_item');
    languages = parent.attr('languages');
    country_name = parent.attr('name');
    country_code = parent.attr('country_code');

    showAvailableBibleLanguages(languages, country_name, country_code);
}

function showAvailableBibleLanguages(languages, country_name, country_code) {
    showPopup();
    $('#popup_header_title').html("Select a language: " + country_name);
    $('#popup_content').empty();
    showPopupSpinner(true);
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getavailablelanguages',
        dataType: 'json',
        data: {
            country_code: country_code,
            country_name: country_name,
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                $('#popup_content').addClass('popup_content_no_padding');
                showPopupSpinner(false);
                var search = createSearchElement("searchLanguages", "languageSearch()");
                $('#popup_content').append(search);
                data.forEach(function (obj) {
                    var elem = $('#bible_language_template').clone();
                    elem.attr('id', obj.ID);
                    elem.attr('name', obj.Name)
                    elem.attr('autonym', obj.Autonym)
                    elem.attr('language', obj.ISO)
                    elem.attr('displayName', obj.DisplayName)
                    elem.removeAttr('style');
                    elem.find('#bible_language_title').html(obj.DisplayName);
                    $('#popup_content').append(elem);
                });
            }
        },
        error: function (err) {
            showPopupSpinner(false);
            alert(err.status);
        }
    });
}

function languageSearch() {
    var input = document.getElementById('searchLanguages');
    var filter = input.value.toUpperCase();
    $('.bible_item').each(function () {
        var displayName = $(this).attr('displayName');
        var name = $(this).attr('name');
        var autonym = $(this).attr('autonym');
        if ((name && name.toUpperCase().indexOf(filter)) > -1 || (autonym && autonym.toUpperCase().indexOf(filter) > -1)) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

function getBiblesFromLanguageElement(elem) {
    var parent = $(elem).closest('.bible_item');
    language = parent.attr('language');
    displayName = parent.attr('displayName');
    showAvailableBiblesForLanguage(language, displayName);
}

function showAvailableBiblesForLanguage(language, displayName) {
    showPopup();

    if (displayName === undefined) {
        $('#popup_header_title').html(currentPage.availableBiblesTitle);
    } else {
        $('#popup_header_title').html(currentPage.availableBiblesTitle + " : " + displayName);
    }
    $('#popup_content').empty();
    showPopupSpinner(true);
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getavailablebibles',
        dataType: 'json',
        data: {
            language_iso: language
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                var search = createSearchElement("searchBibles", "bibleSearch()");
                $('#popup_content').append(search);
                $('#popup_content').addClass('popup_content_no_padding');
                showPopupSpinner(false);
                data.forEach(function (obj) {
                    var elem = $('#bible_item_template').clone();
                    elem.attr('id', obj.ID);
                    elem.attr('isLocal', obj.IsLocal)
                    elem.attr('language', obj.Language.ISO)
                    elem.attr('textType', obj.TextType)
                    elem.attr('textID', obj.TextID)
                    elem.attr('audioID', obj.AudioID)
                    elem.attr('dramatizedAudioID', obj.DramatizedAudioID)
                    elem.attr('bibleName', obj.Name)
                    elem.removeAttr('style');
                    elem.find('#bible_item_title').html(obj.Name);
                    $('#popup_content').append(elem);
                });
            }
        },
        error: function (err) {
            alert(err.status);
        }
    });
}

function bibleSearch() {
    var input = document.getElementById('searchBibles');
    var filter = input.value.toUpperCase();
    $('.bible_item').each(function () {
        var name = $(this).attr('bibleName');
        if (name && name.toUpperCase().indexOf(filter) > -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

function getBibleFromElement(elem) {
    showPopupSpinner(true);
    var parent = $(elem).closest('.bible_item');
    id = parent.attr('id');
    isLocal = parent.attr('isLocal');
    textType = parent.attr('textType');
    textID = parent.attr('textID');
    audioID = parent.attr('audioID');
    dramatizedAudioID = parent.attr('dramatizedAudioID');
    language = parent.attr('language');
    bibleName = parent.attr('bibleName');
    $.ajax({
        type: 'GET',
        url: baseUrl + 'changeBible',
        dataType: 'json',
        data: {
            bibleID: id,
            isLocal: isLocal,
            bibleName: bibleName,
            textType: textType,
            textID: textID,
            audioID: audioID,
            dramatizedAudioID: dramatizedAudioID,
            language: language
        }
        , success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                analytics.logEvent("bible", { screen_name: "change bible", action: "selected_bible", label: bibleName })
                goToPage(data.Book, data.Chapter, data.Verse, false, true);
            }
        }, error: function (err) {
            hideAllPopups();
            alert(err.status);
        }
    });
}

function editPlaylistFromElement(elem) {
    var id = 0;

    if ($(elem).hasClass('playlist_item_button')) {
        var parent = $(elem).closest('.playlist_item');
        id = parent.attr('id');
    } else {
        id = $(elem).attr('pid');
    }

    window.location.href = `${playlistEditor}?edit=${id}`
}

function deletePlaylistFromElement(elem) {
    var id = 0;

    if ($(elem).hasClass('playlist_item_button')) {
        var parent = $(elem).closest('.playlist_item');
        id = parent.attr('id');
    } else {
        id = $(elem).attr('pid');
    }

    var title = $(elem).closest('.playlist_item').find('#playlist_item_title').html();

    if (confirm('Delete playlist ' + title + '?')) {
        $.ajax({
            type: 'DELETE',
            url: baseUrl + 'deleteplaylist' + '?playlistid=' + id,
            success: function (data) {
                showPlaylists($('#popup_header_title').html());
            },
            error: function (err) {
                alert(err.status);
            }
        });
    }
}

function sharePlaylistFromElement(elem) {
    var id = 0;

    if ($(elem).hasClass('playlist_item_button')) {
        var parent = $(elem).closest('.playlist_item');
        id = parent.attr('id');
    } else {
        id = $(elem).attr('pid');
    }

    navigator.clipboard.writeText(baseUrl + 'presenter?playlist=' + id + '&section=0').then(res => {
        $(elem).find('span').fadeTo(250, 1).delay(1500).fadeTo(250, 0)
    })
}

function getPlaylistFromElement(elem) {
    var id = 0;
    var index = 0;

    if ($(elem).hasClass('playlist_item_button')) {
        var parent = $(elem).closest('.playlist_item');
        id = parent.attr('id');
    } else {
        id = $(elem).attr('pid');
        index = $(elem).attr('sindex');
    }

    getPlaylist(id, index, false);
}

function getPlaylist(id, section, startOnLast) {
    hideAllPopups();
    pause();
    showLoader(true);
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getplaylist',
        dataType: 'json',
        data: {
            playlistID: id,
            sectionIndex: section,
            presenterMode: presenterMode
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                currentPage.verseList = JSON.parse(data.VerseList);
                currentPage.playlist = data.CurrentPlaylist;
                currentPage.section = data.CurrentPlaylistSection;
                currentPage.verse = startOnLast ? currentPage.verseList['Content'].length - 1 : 0;
                currentPage.hasNextPage = data.HasNextPage;
                currentPage.hasPreviousPage = data.HasPreviousPage;
                currentPage.HidePurchasePrompt = currentPage.verseList.HidePurchasePrompt;
                currentPage.chaptersTitle = data.ChaptersTitle;
                currentPage.chaptersTitlePsalms = data.ChaptersTitlePsalms;
                currentPage.versesTitle = data.VersesTitle;

                $('#bible_content').html(data.HTML);
                $('#bible_content_wrapper').scrollTop(startOnLast ? $('#bible_content').height() : 0);
                $('#source_name').html(data.Source);

                configurePlaylistSourcName();

                addClickHandlers();
                selectCurrentVerse();
                showLoader(false);
                showPlaylistFullscreenButton(true);

                var label = data.Source;
                analytics.logEvent("bible", { action: "jump", label: label })

                addTimingMarkAdjusters();
                addFootnoteTooltips();
            }
        },
        error: function (err) {
            showLoader(false);
            alert(err.status);
        }
    });
}

function handlePlaylistCreation(title, sectionsName) {
    history.pushState({}, null, location.href.split('?')[0])
    showPlaylists(title, sectionsName);
}

function showPlaylistEditor() {
    window.location.href = playlistEditor
}

function showPlaylists(title, sectionsName) {
    showPopup();
    showLoader(true);
    $('#popup_header_title').html(title);
    $('#popup_content').addClass('popup_content_no_padding');

    $('#popup_back').css({ visibility: 'hidden' });
    if (enablePlaylistEditor) {
        setPopupAction('edit', function () {
            showPlaylistEditor();
        });
    }
    $('#popup_content').empty();

    $('#popup').addClass('popup_gray_background');
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getplaylists',
        dataType: 'json',
        success: function (data) {

            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                $('#popup_content').addClass('popup_content_no_padding');
                data.forEach(function (obj) {
                    var elem = $('#playlist_item_template').clone();
                    elem.attr('id', obj.PlaylistID);
                    elem.removeAttr('style');
                    elem.find('#playlist_item_title').html(obj.Name);
                    elem.find('#playlist_item_section_count').html(obj.SectionCountDisplay);
                    $('#popup_content').append(elem);

                    if (!obj.Editable) {
                        elem.find('#playlist_item_edit').hide();
                        elem.find('#playlist_item_delete').hide();
                        elem.find('#playlist_item_share').hide();
                    }
                });
                showLoader(false);
            }
        },
        error: function (err) {
            showLoader(false);
            alert(err.status);
        }
    });
}

function showPlaylistSections(elem) {
    var title = null;
    var id = null;

    if ($(elem).hasClass('playlist_item_button_sections')) {
        var parent = $(elem).closest('.playlist_item');
        title = parent.find('#playlist_item_title').html();
        id = parent.attr('id');
    } else {
        elem = $('#source_name')
        title = $(elem).text();
        id = currentPage.playlist;
    }

    if (title && id) {
        showPlaylistSectionsFor(title, id);
    }
}

function showPlaylistSectionsFor(title, id) {
    showPopup();
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getplaylistsections',
        dataType: 'json',
        data: {
            playlistid: id
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                $('#popup_header_title').html(title);
                $('#popup_content').addClass('popup_content_no_padding');
                $('#popup_content').empty();
                data.forEach(function (obj, index) {
                    var elem = $('#playlist_section_item_template').clone();
                    elem.removeAttr('id');
                    elem.removeAttr('style');
                    elem.attr('pid', id);
                    elem.attr('sindex', index);
                    elem.children('#playlist_section_item_title').html(obj.Name);
                    elem.children('#playlist_section_item_index').html(obj.Index);
                    $('#popup_content').append(elem);
                });
            }
        },
        error: function (err) {
            alert(err.status);
        }
    });
}

function showBookRelatedMaterial(id) {

    var bookNum = currentPage.verseList['Content'][currentPage.verse].Book - 1;
    var index = parseInt(id);
    var item = currentPage.verseList['RelatedMaterials'][currentPage.verse][index];

    $('#popup_header_title').html(item.Name);
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getrelatedmaterial',
        dataType: 'json',
        data: {
            type: 'book',
            bookNum: bookNum,
            index: index
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else if (data.NotAuthorized) {
                //alert(data.Message);
                showPurchaseNotice(data.Message, data.PurchaseLink, data.LinkText);
            } else {
                showPopup();
                $('#popup_content').removeClass();
                $('#popup_content').addClass('popup_content');
                $('#popup_content').html(data.Material);
                addClickHandlers();
            }
        },
        error: function (err) {
            alert(err.status);
        }
    });
}

function getStudyNote(file) {
    showTree();
    showTreeLoadingSpinner();
    $.ajax({
        type: 'GET',
        url: baseUrl + 'getstudynote',
        dataType: 'json',
        data: {
            file: file
        },
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } if (data.NotAuthorized) {
                hideTreeLoadingSpinner();
                showPurchaseNotice(data.Message, data.PurchaseLink, data.LinkText);
            } else {
                if (data.Contents) {

                    updateTreeNavStack(file);

                    var currentVerse = $('verse').eq(currentPage.verse);
                    var loc = currentVerse.attr("id");
                    $('#tree_back_link').attr("href", '#' + loc);

                    var book = getBook(currentPage.isIntroduction ? currentPage.selectedBook : currentPage.verseList['Content'][currentPage.verse].Book - 1);

                    $('#tree_back_link').text("\u21A9" + book.Name + " " + currentPage.verseList['Content'][currentPage.verse].Chapter + ":" + currentPage.verseList['Content'][currentPage.verse].Verse);
                    $('#tree_content').html(data.Contents);
                    $('#tree_content_inner_wrapper').scrollTop(0);
                    addClickHandlers();
                    hideTreeLoadingSpinner();
                } else {
                    hideTreeLoadingSpinner();
                }
            }
        },
        error: function (err) {
            hideTreeLoadingSpinner();
            alert(err.status);
        }
    });
}

function updateTreeNavVisibility() {
    $("#tree_navBack").css({ visibility: treeCanGoBack() ? 'visible' : 'hidden' });
}

function treeCanGoBack() {
    return treeNavStack.length > 1;
}

function updateTreeNavStack(file) {
    if (treeNavStack[treeNavStack.length - 1] != file) { //don't add item if it is already at the top of our nav stack
        treeNavStack.push(file);
    }
    updateTreeNavVisibility();
}

function treeGoBack() {
    if (treeCanGoBack()) {
        var link = treeNavStack.pop(); //pop current page from top of stack
        link = treeNavStack[treeNavStack.length - 1]; //peek the top

        getStudyNote(link);
    }
    updateTreeNavVisibility();
}

function clearTreeNavStack() {
    treeNavStack = []; //clear stack
    updateTreeNavVisibility();
}

function showTree() {
    updateTreeNavVisibility();
    var treeHeight = $('#tree_content_wrapper').height();
    if (treeHeight <= 80) {
        var oldHeight = $('#bible_content_wrapper').height();
        var newHeight = oldHeight - 300;
        $('#bible_content_wrapper').animate({ 'height': newHeight + 'px' }, 250);
    }
}

function hideTree() {
    clearTreeNavStack();
    var treeHeight = $('#tree_content_wrapper').height();
    if (treeHeight > 48) {
        $('#bible_content_wrapper').animate({ 'height': '100%' }, 250, function () {
            $('#tree_content').html(null);
        });
    }
}

function showTreeLoadingSpinner() {
    $('#tree_content_loading_spinner').show();
}

function hideTreeLoadingSpinner() {
    $('#tree_content_loading_spinner').hide();
}

function getBook(num) {
    var book = null;
    if (num < bible.Testaments[0].Books.length) {
        book = bible.Testaments[0].Books[num];
    } else {
        book = bible.Testaments[1].Books[num - bible.Testaments[0].Books.length];
    }

    return book;
}

function showFastpickerBookGrid() {
    setCookie('fastpicker_format', "grid", { expires: 365 });// Cookies.set('fastpicker_format', "grid", { expires: 365 });
    showFastPicker('books');
}

function showFastpickerBookList() {
    setCookie('fastpicker_format', "list", { expires: 365 });//Cookies.set('fastpicker_format', "list", { expires: 365 });
    showFastPicker('books');
}

function showFastPicker(level, bookNum, chapterNum) {
    showPopup();
    setPopupAction('forward', function () {
        if (level == 'books') {
            goToPage(-1, -1, 0, false);
        } else if (level == 'chapters') {
            goToPage(bookNum, 0, 0, false);
            var position = getBook(bookNum).Name;
            analytics.logEvent("bible", { screen_name: "fast picker", action: "fast_picker", label: position })
        } else if (level == 'verses') {
            goToPage(bookNum, chapterNum, 0, false);
            var position = getBook(bookNum).Name + ' ' + (parseInt(chapterNum) + 1);
            analytics.logEvent("bible", { screen_name: "fast picker", action: "fast_picker", label: position })
        }

        hideAllPopups();
    });

    if (!bookNum) {
        bookNum = currentPage.isIntroduction ? currentPage.selectedBook : currentPage.verseList['Content'][currentPage.verse].Book - 1;
    }

    if (!chapterNum) {
        chapterNum = currentPage.isIntroduction ? 0 : currentPage.verseList['Content'][currentPage.verse].Chapter - 1;

        if (level == 'verses' && currentPage.isIntroduction) {
            level = 'chapters';
        }
    }

    $('#popup_header_title').html('Fast Picker');
    $('#popup_content').addClass('popup_content_no_padding');


    if (level == 'books') {
        $('#popup_back').css({ visibility: 'hidden' });
        $('#popup_content').empty();
        var format = getCookie('fastpicker_format');// Cookies.get('fastpicker_format');
        if (format == null) format = "grid";
        $('#popup_header_title').html(bible.Name);
        $('#grid_list_options').css({ visibility: 'visible' });
        bible.Testaments.forEach(function (testament, index) {
            if (format == "grid") {
                var grid = $('#fast_picker_grid_template').clone();
                grid.removeAttr('style');
                grid.removeAttr('id');
                grid.find('#fast_picker_grid_header').html(testament.Name);
                var indexOffset = index > 0 ? bible.Testaments[index - 1].Books.length : 0;
                testament.Books.forEach(function (book, index) {
                    var item = $('#fast_picker_grid_item_template').clone();
                    item.removeAttr('style');
                    item.removeAttr('id');
                    item.attr('book', index + indexOffset);
                    item.css('background-color', 'rgb(' + book.Color + ')');

                    if (bible.ShowBookCodeInGrid || bible.Language == 'jpn' || bible.Language == 'cmn') {
                        item.html("<ruby>" + book.ShortName + "<rt>" + book.Code + "</rt></ruby>");
                    } else {
                        item.html(book.ShortName);
                    }
                    grid.append(item);
                });
                $('#popup_content').append(grid);
            } else {
                var list = $('#fast_picker_list_template').clone();
                list.removeAttr('style');
                list.removeAttr('id');
                list.find('#fast_picker_list_header').html(testament.Name);
                var indexOffset = index > 0 ? bible.Testaments[index - 1].Books.length : 0;
                testament.Books.forEach(function (book, index) {
                    var item = $('#fast_picker_list_item_template').clone();
                    item.removeAttr('style');
                    item.removeAttr('id');
                    item.attr('book', index + indexOffset);
                    item.css('background-color', 'rgb(' + book.Color + ')');
                    if (bible.ShowBookCodeInGrid || bible.Language == 'jpn' || bible.Language == 'cmn') {
                        item.html(book.Name + " (" + book.Code + ")");
                    } else {
                        item.html(book.Name);
                    }
                    list.append(item);
                });
                $('#popup_content').append(list);
            }
        });
    } else {
        var book = getBook(bookNum);
        if (level == 'chapters') {
            $('#popup_header_title').html(book.Name);
            var grid = $('#fast_picker_grid_template').clone();
            grid.removeAttr('style');
            grid.removeAttr('id');
            if (book.Code == "Psa") {
                grid.find('#fast_picker_grid_header').html(currentPage.chaptersTitlePsalms);
            } else {
                grid.find('#fast_picker_grid_header').html(currentPage.chaptersTitle);
            }

            if (book.HasIntroductionText) {
                var item = $('#fast_picker_grid_item_template').clone();
                item.removeAttr('style');
                item.removeAttr('id');
                item.attr('book', bookNum);
                item.attr('chapter', -1);
                item.css('background-color', 'rgb(' + book.Color + ')');
                item.html(currentPage.introductionCellText);
                grid.append(item);
            }

            book.Chapters.forEach(function (chapter, index) {
                var item = $('#fast_picker_grid_item_template').clone();
                item.removeAttr('style');
                item.removeAttr('id');
                item.attr('book', bookNum);
                item.attr('chapter', index);
                item.html(chapter.Number);
                grid.append(item);
            });
            $('#popup_content').html(grid);
        } else if (level == 'verses') {
            var chapter = book.Chapters[chapterNum];
            $('#popup_header_title').html(book.Name + ' ' + chapter.Number);
            if (chapter.VerseCount == -1) {
                //update verse count is unknown - for remote bibles, we need to query for the text to get the count,
                //we want to be lazy and only do that when we need to.
                $.ajax({
                    type: 'GET',
                    url: baseUrl + 'getversecount',
                    dataType: 'json',
                    data: {
                        book: bookNum,
                        chapter: chapterNum
                    }
                    , success: function (data) {
                        if (data.AjaxFailed) {
                            location = data.Redirect;
                        } else {
                            chapter.VerseCount = data.VerseCount;
                            updateFastPickerVerseGrind(chapter, bookNum, chapterNum)
                        }
                    }, error: function (err) {
                        alert(err.status);
                    }
                });
            } else {
                updateFastPickerVerseGrind(chapter, bookNum, chapterNum)
            }
        }
    }
}

function updateFastPickerVerseGrind(chapter, bookNum, chapterNum) {
    var grid = $('#fast_picker_grid_template').clone();
    grid.removeAttr('style');
    grid.removeAttr('id');
    grid.find('#fast_picker_grid_header').html(currentPage.versesTitle);

    for (var i = 0; i < chapter.VerseCount; i++) {
        var verse = chapter.Verses[i]
        if (!verse.Skipped) {
            var item = $('#fast_picker_grid_item_template').clone();
            item.removeAttr('style');
            item.removeAttr('id');
            item.attr('book', bookNum);
            item.attr('chapter', chapterNum);
            item.attr('verse', i);
            item.html(verse.Label);
            grid.append(item);
        }
    }
    $('#popup_content').html(grid);
}

function fastPickerItemClicked(item) {
    var bookNum = $(item).attr('book');
    var chapterNum = $(item).attr('chapter');
    var verseNum = $(item).attr('verse');

    if (bookNum && chapterNum && verseNum) {
        goToPage(parseInt(bookNum), parseInt(chapterNum), parseInt(verseNum), false);
        hideAllPopups();
        var position = getBook(bookNum).Name + ' ' + (parseInt(chapterNum) + 1) + ':' + (parseInt(verseNum) + 1);
        analytics.logEvent("bible", { screen_name: "fast picker", action: "fast_picker", label: position })
    } else if (bookNum && chapterNum) {
        if (chapterNum == -1) {
            //this is the book introduction
            goToBookIntroduction(parseInt(bookNum));
            hideAllPopups();
            var position = getBook(bookNum).Name + ' Introduction';
            analytics.logEvent("bible", { screen_name: "fast picker", action: "fast_picker", label: position })
        } else {
            //show the chapter content
            showFastPicker('verses', bookNum, chapterNum);
        }
    } else if (bookNum) {
        showFastPicker('chapters', bookNum, chapterNum);
    }
}

function hideAllPopups() {
    hidePopupOverlay();
    hideMenu(false);
    hidePopup();
    hideVideoPopup();
    hideImagePopup();
}

function showPopupOverlay() {
    if ($('#popup_overlay').css('visibility') == 'hidden') {
        $('#popup_overlay').css({ opacity: 0, visibility: 'visible' }).animate({ opacity: 1 }, 250);
    }
}

function hidePopupOverlay() {
    if ($('#popup_overlay').css('visibility') == 'visible') {
        $('#popup_overlay').css({ opacity: 1, visibility: 'visible' }).animate({ opacity: 0 }, 250, function () {
            $('#popup_overlay').css({ visibility: 'hidden' });
        });
    }
}

function showMenu() {
    showPopupOverlay();
    if ($('#side_menu').css('left') != '0') {
        $('#side_menu').animate({ left: 0 }, 250);
        analytics.logEvent("player_menu", { action: "show" })
    }
}

function hideMenu(hideOverlay) {
    if ($('#side_menu').css('left') == '0px') {
        if (hideOverlay) {
            hidePopupOverlay();
        }

        $('#side_menu').animate({ left: '-280px' }, 250);
        analytics.logEvent("player_menu", { action: "hide" })
    }
}

function setPopupAction(icon, handler) {
    if (handler) {
        $('#popup_action').children('.popup_action').text(icon);
        $('#popup_action').css({ visibility: 'visible' });
        $('#popup_action').off().click(handler);
    } else {
        $('#popup_action').css({ visibility: 'hidden' });
    }
}

function showPopupSpinner(show) {
    if (show) {
        $('#popup_content_spinner').css({ visibility: 'visible' });
        $('#popup_content_spinner').css({ height: '3rem' });
    } else {
        $('#popup_content_spinner').css({ visibility: 'hidden' });
        $('#popup_content_spinner').css({ height: '0rem' });
    }
}

function showLoader(show) {
    if (show) {
        $('#loader').css({ visibility: 'visible' });
    } else {
        $('#loader').css({ visibility: 'hidden' });
    }
}

function showPopup() {
    hideMenu(false);
    showPopupSpinner(false);
    $('#grid_list_options').css({ visibility: 'hidden' });
    if ($('#popup').css('visibility') == 'hidden') {
        $('#popup_back').css({ visibility: 'hidden' });
        $('#popup').css({ opacity: 0, visibility: 'visible' }).animate({ opacity: 1 }, 250);
    } else {
        $('#popup_back').css({ visibility: 'visible' });
        var title = $('#popup_header_title').text();
        var html = $('#popup_content').html();
        popupState.push({
            title: title,
            html: html
        });
    }

    showPopupOverlay();
}

function goBackPopup() {
    if (popupState.length > 0) {
        var state = popupState.pop();
        $('#popup_header_title').html(state.title);
        $('#popup_content').html(state.html);

        if (popupState.length == 0) {
            $('#popup_back').css({ visibility: 'hidden' });
        }
    }
}

function hidePopup() {
    if ($('#popup').css('visibility') == 'visible') {
        hidePopupOverlay();
        $('#popup').css({ opacity: 1, visibility: 'visible' }).animate({ opacity: 0 }, 250, function () {
            $('#popup').css({ visibility: 'hidden' });
            //reset to default styles incase of changes
            $('#popup').removeClass();
            $('#popup').addClass('popup');
            $('#popup_content').removeClass();
            $('#popup_content').addClass('popup_content');
            $('#popup_content').empty();
            setPopupAction(null, null);
        });
    }
}

function showImagePopup(file) {
    $('#image_wrapper').html('<img src="' + file + '">');
    if ($('#image_popup').css('visibility') == 'hidden') {
        $('#image_popup').css({ opacity: 0, visibility: 'visible' }).animate({ opacity: 1 }, 250);
    }

    showPopupOverlay();
}

function hideImagePopup() {
    if ($('#image_popup').css('visibility') == 'visible') {
        if (player != null) {
            player.pause();
            player = null;
        }
        hidePopupOverlay();
        $('#image_popup').css({ opacity: 1, visibility: 'hidden' }).animate({ opacity: 0 }, 250, function () {
            $('#image_wrapper').empty();
        });
    }
}

function showVideoPopup(source) {
    var finalLink = "";

    if (source.startsWith("video")) {
        if (source.startsWith("videos")) {
            source = source.replace("videos://", "");
            finalLink = "https://"
        } else {
            source = source.replace("video://", "");
            finalLink = "http://"
        }
        var startTime = "0";
        var endTime = "";
        var index = source.indexOf("/");
        if (index > -1) {
            var range = source.substring(0, index);
            if (range.includes(":")) {
                range = range.substring(0, range.indexOf(":"));
            }
            var match = range.match("^[0-9]+(,[0-9]+)?$")
            if (match) {
                var parts = range.split(",");
                if (parts.length == 2) {
                    startTime = parts[0];
                    endTime = parts[1];
                } else {
                    startTime = parts[0];
                }
                finalLink = finalLink + source.substring(index + 1);
            } else {
                finalLink = finalLink + source;
            }
        } else {
            finalLink = finalLink + source;
        }
    }

    if (finalLink.includes("youtube")) {
        finalLink = finalLink.replace('watch?v=', 'embed/');
    } else if (finalLink.includes("vimeo")) {
        if (!finalLink.includes("?")) {
            finalLink = finalLink + "?";
        } else {
            finalLink = finalLink + "&";
        }
        finalLink = finalLink + "portrait=0&byline=0&title=0";
    }

    if (finalLink.includes(".m3u8")) {
        var id = 'hls-player-' + Math.floor(Math.random() * 100);
        $('#video_wrapper').html('<video-js id="' + id + '" style="position: absolute; width: 100%; height: 100%" class="vjs-deafult-skin" controls></video-js> ');
        player = videojs(id);
        player.src({
            src: finalLink,
            type: 'application/x-mpegURL'
        });
        player.play();
    } else {
        $('#video_wrapper').html('<iframe allowtransparency="true" frameborder="0" scrolling="no" allowfullscreen mozallowfullscreen webkitallowfullscreen oallowfullscreen msallowfullscreen width="50%" height="50%" allow="autoplay; encrypted-media" src="' + finalLink + '"></iframe>');
    }

    if ($('#video_popup').css('visibility') == 'hidden') {
        $('#video_popup').css({ opacity: 0, visibility: 'visible' }).animate({ opacity: 1 }, 250);
    }

    showPopupOverlay();
}

function hideVideoPopup() {
    if ($('#video_popup').css('visibility') == 'visible') {
        if (player != null) {
            player.pause();
            player = null;
        }
        hidePopupOverlay();
        $('#video_popup').css({ opacity: 1, visibility: 'hidden' }).animate({ opacity: 0 }, 250, function () {
            $('#video_wrapper').empty();
        });
    }
}

function playPause() {
    if (isPlaying()) {
        pause();
    } else {
        play();
    }
}

function play() {
    if (currentPage.isIntroduction) {
        $('#media_time_control').show();
        if (currentPage.hasIntroAudio) {
            spinMediaButton();
            playIntroAudio(currentPage.selectedBook, onIntroPositionChanged, onStopped, onFinished);
            $('#media_control_play_pause').removeClass('media_control_play');
            $('#media_control_play_pause').addClass('media_control_pause');
        }
    } else if (currentPage.verseList['Content'][currentPage.verse].HasAudio) {
        $('#media_time_control').hide();
        spinMediaButton();
        playAudio(currentPage.verseList['Content'], currentPage.verse, onPositionChanged, onStopped, onFinished);
        $('#media_control_play_pause').removeClass('media_control_play');
        $('#media_control_play_pause').addClass('media_control_pause');
    }
}

function spinMediaButton(spin) {
    if (spin) {
        $('#media_control_play_pause').addClass('rotate');
    } else {
        $('#media_control_play_pause').removeClass('rotate');
    }
}

function pause() {
    stopAudio(currentPage.isIntroduction);
    $('#media_control_play_pause').addClass('media_control_play');
    $('#media_control_play_pause').removeClass('media_control_pause');
}

function onPositionChanged(index) {
    currentPage.verse = index;
    selectCurrentVerse(true);
}

function onIntroPositionChanged(duration, currenttime) {
    $('#media_time_control').html(secondsToTimeString(currenttime) + " / " + secondsToTimeString(duration));
}

function secondsToTimeString(input) {
    var seconds = Math.floor(input % 60);
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    var minutes = Math.floor(input / 60);
    return minutes + ":" + seconds;
}

function onStopped() {
    pause();
}

function onFinished() {
    if (currentPage.hasNextPage) {
        getNextPage(true);
    }
}