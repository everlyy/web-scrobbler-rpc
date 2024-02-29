const fetch_interval = 2500;

let fetch_playing = () => {
    fetch("/now-playing").then((response) => response.text()).then((text) => {
        NowPlaying.innerHTML = text;
    });
};

(() => {
    fetch_playing();
    setInterval(fetch_playing, fetch_interval);
})();