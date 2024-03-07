const fetch_interval = 2500;

let fetch_playing = () => {
    fetch("/now-playing").then((response) => response.json()).then((json) => {
        NowPlaying.innerHTML = json.document;

        if(json.state.cover) {
            Background.style.setProperty("--cover-image-url", `url("${json.state.cover}")`);
            Background.classList.add("has-cover");
        } else {
            Background.classList.remove("has-cover");
        }
    });
};

(() => {
    fetch_playing();
    setInterval(fetch_playing, fetch_interval);
})();