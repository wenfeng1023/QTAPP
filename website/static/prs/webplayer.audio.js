var audioList = null;
var currentIndex = null;
var onPositionChangedCallback = null;
var onFinishedCallback = null;
var onStoppedCallback = null;
var ignoreTimerUpdates = false;

var lastPlayingAnalyticEventTime = 0; //track the last time we sent a playing notification - we send analytics every minute of play
var AnalyticsPlayingEventLabel = ""; //the label for the playing event - could be either the Book Chapter or Playlist: [name of playlist] - sent for every minute of play

var audioCheckTimer;
var errorCount = 0;
var duration = 0;
var offset = 0;
var introBook = -1;
var introAudio = false;

$(document).ready(function () {
    $('#jquery_jplayer_1').jPlayer({
        errorAlerts: true,
        warningAlerts: true,
        ready: function () {
            $(this).jPlayer('setMedia', {
                m4a: 'https://www.jplayer.org/audio/m4a/Miaow-07-Bubble.m4a'
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.progress, function (event) {
                //doPlayerEventProgress(event.jPlayer.status.seekPercent);
                console.log("Player downloading audio.");
                errorCount = 0;
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.play, function (event) {
                //doPlayerEventPlay(event.jPlayer.status.currentTime);
                spinMediaButton(false);
                console.log("Player playing.");
                errorCount = 0;
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.pause, function (event) {
                //doPlayerEventPause(event.jPlayer.status.currentTime);
                spinMediaButton(false);
                console.log("Player paused.");
                errorCount = 0;
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.loadstart, function (event) {
                console.log("player loadstart:" + event.jPlayer.status.src);
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.loadeddata, function (event) {
                console.log("player loadeddata:" + event.jPlayer.status.src);
                duration = event.jPlayer.status.duration;
                errorCount = 0;
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.error, function (event) {
                console.log("player error code: " + event.jPlayer.error.type);
                console.log("player error context: " + event.jPlayer.error.context);
                console.log("player error message: " + event.jPlayer.error.message);
                console.log("player error hint: " + event.jPlayer.error.hint);
                if (event.jPlayer.error.type == $.jPlayer.error.URL) {
                    errorCount++;
                    if (errorCount < 5) {
                        playAudio(audioList, currentIndex, onPositionChangedCallback);
                    } else {
                        errorCount = 0;
                        spinMediaButton(false);
                    }
                }
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.warning, function (event) {
                console.log("player warning context:" + event.jPlayer.warning.context);
                console.log("player warning message:" + event.jPlayer.warning.message);
                console.log("player warning hint:" + event.jPlayer.warning.hint);
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.suspend, function (event) {
                console.log("Player suspend event.");
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.abort, function (event) {
                console.log("Player abort event.");
                errorCount = 0;
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.stalled, function (event) {
                console.log("Player stalled event.");
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.waiting, function (event) {
                spinMediaButton(false);
                console.log("Player waiting.");
            });

            $('#jquery_jplayer_1').bind($.jPlayer.event.ended, function (event) {
                errorCount = 0;
                if (currentIndex < audioList.length - 1) {
                    if (onPositionChangedCallback) {
                        onPositionChangedCallback(currentIndex + 1);
                    }

                    let audioItem = audioList[currentIndex];
                    if (audioItem.Pause) {
                        stopAudio();
                        onStoppedCallback();
                        ignoreTimerUpdates = true;
                    } else {
                        playAudio(audioList, currentIndex + 1, onPositionChangedCallback);
                    }
                } else {
                    if (onStoppedCallback) {
                        onStoppedCallback();
                    }
                    if (onFinishedCallback) {
                        onFinishedCallback();
                    }
                }
            });
        },
        cssSelectorAncestor: '#jp_container_1',
        swfPath: '/js',
        supplied: 'm4a, mp3',
        useStateClassSkin: true,
        autoBlur: false,
        smoothPlayBar: true,
        keyEnabled: true,
        remainingDuration: true,
        toggleDuration: true
    });
});

function onAudioTimer() {
    if (isPlaying() && !introAudio && audioList && !ignoreTimerUpdates) {
        let time = $("#jquery_jplayer_1").data("jPlayer").htmlElement.audio.currentTime;
        let src = $("#jquery_jplayer_1").data("jPlayer").status.src;
        let audioItem = audioList[currentIndex];

        //update the playing analytics for each minute of play
        if (lastPlayingAnalyticEventTime > time) {
            lastPlayingAnalyticEventTime = time; //reset after a pause
        }

        if (time - lastPlayingAnalyticEventTime >= 60) {
            lastPlayingAnalyticEventTime = time;
            analytics.logEvent("bible_player", {
                screen_name: "web player",
                action: "playing",
                label: AnalyticsPlayingEventLabel,
                value: "1",
                bible_translation: bible.Translation,
                bible_id: bible.BibleID,
                bible_name: bible.Name,
                bible_language: bible.Language
            })
        }

        if (audioItem && audioItem.AudioEnd != -1 && time > audioItem.AudioEnd) {
            updateTiming(currentIndex, time);

            currentIndex += 1;

            if (currentIndex >= audioList.length) {
                stopAudio();
                if (onStoppedCallback) {
                    onStoppedCallback();
                }
                if (onFinishedCallback) {
                    onFinishedCallback();
                }
            } else {
                if (onPositionChangedCallback) {
                    onPositionChangedCallback(currentIndex);
                }

                if (audioItem.Pause) {
                    stopAudio();
                    onStoppedCallback();
                    ignoreTimerUpdates = true;
                } else {
                    let nextItem = audioList[currentIndex];

                    if (!nextItem.HasAudio) {
                        if (onStoppedCallback) {
                            onStoppedCallback();
                        }
                    } else {
                        if (/*!src.endsWith('getaudio?book=' + nextItem.Book + '&chapter=' + nextItem.Chapter) ||*/ nextItem.AudioStart != audioItem.AudioEnd) {
                            $("#jquery_jplayer_1").jPlayer('pause');
                            playAudio(audioList, currentIndex, onPositionChangedCallback);
                        }
                    }

                    updateTiming(currentIndex, time);
                }
            }
        } else {
            updateTiming(currentIndex, time);
        }
    } else if (isPlaying() && introAudio && !ignoreTimerUpdates) {
        if (onPositionChangedCallback) {
            let time = $("#jquery_jplayer_1").data("jPlayer").htmlElement.audio.currentTime;
            //let duration = $("#jquery_jplayer_1").data("jPlayer").htmlElement.audio.duration;
            onPositionChangedCallback(duration, time);
        }
    }
}

function updateTiming(index, time) {
    if (currentPage.showTimingMarks) {
        $("#ct_" + index).html(time);
    }    
}

function resetOffset() {
    offset = 0;
}

function playIntroAudio(book, onIntroPositionChanged, stoppedCallback, finishedCallback) {
    introAudio = true;
    if (introBook != book) {
        resetOffset();
    }
    introBook = book;
    onFinishedCallback = finishedCallback;
    onStoppedCallback = stoppedCallback;
    onPositionChangedCallback = onIntroPositionChanged;

    AnalyticsPlayingEventLabel = getBook(book).Name + " Introduction";

    $.ajax({
        type: 'GET',
        url: baseUrl + 'getintroaudiolink?book=' + book,
        dataType: 'json',
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else {
                if (audioCheckTimer == null) {
                    audioCheckTimer = setInterval(onAudioTimer, 10);
                }

                spinMediaButton(true);
                $('#jquery_jplayer_1').jPlayer('setMedia',
                    data
                ).jPlayer('play', offset);
                ignoreTimerUpdates = false;
            }
        },
        error: function (err) {
            alert(err.status);
        }
    });
}

function playAudio(list, index, positionChangedCallback, stoppedCallback, finishedCallback) {
    introAudio = false;
    introBook = -1;
    audioList = list;
    currentIndex = index;
    onPositionChangedCallback = positionChangedCallback;
    onFinishedCallback = finishedCallback;
    onStoppedCallback = stoppedCallback;

    var book = audioList[currentIndex].Book;
    var chapter = audioList[currentIndex].Chapter;
    offset = audioList[currentIndex].AudioStart;
    if (currentPage.playlist) {
        AnalyticsPlayingEventLabel = "playlist: " + $('#source_name').html();
    } else {
        AnalyticsPlayingEventLabel = getBook(book - 1).Name + " " + chapter;
    }

    $.ajax({
        type: 'GET',
        url: "https://bible.prsi.org/ko/Player/getaudiomedia?book=9&chapter=1",
        dataType: 'json',
        success: function (data) {
            if (data.AjaxFailed) {
                location = data.Redirect;
            } else if (data.NotAuthorized) {
                stopAudio(false);
                pause();
               // alert(data.Message);
                showPurchaseNotice(data.Message, data.PurchaseLink, data.LinkText);
            } else {
                if (audioCheckTimer == null) {
                    audioCheckTimer = setInterval(onAudioTimer, 10);
                }
                spinMediaButton(true);
                $('#jquery_jplayer_1').jPlayer('setMedia',
                    data
                ).jPlayer('play', offset);
                ignoreTimerUpdates = false;
            }
        },
        error: function (err) {
            alert(err.status);
        }
    });
}

function stopAudio(keepPosition) {
    if (isPlaying()) {
        $("#jquery_jplayer_1").jPlayer('pause');
        if (keepPosition) {
            offset = $("#jquery_jplayer_1").data("jPlayer").htmlElement.audio.currentTime;
        } 
        clearInterval(audioCheckTimer);
        audioCheckTimer = null;        
    }
}

function isPlaying() {
    var data = $("#jquery_jplayer_1").data("jPlayer");

    return data && data.status.paused == false;
}