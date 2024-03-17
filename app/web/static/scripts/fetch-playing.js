const fetch_interval = 2500;
let start_time = 0;

let update_favicon = (icon) => {
    let link = document.querySelector("link[rel='icon']");

    if (!link) {
        link = document.createElement("link");
        link.setAttribute("rel", "icon");
        document.head.appendChild(link);
    }

    link.href = icon;
};

let fetch_playing = () => {
    fetch("/now-playing").then((response) => response.json()).then((json) => {
        NowPlaying.innerHTML = json.document;
        document.title = (
            json.state ?
            `${json.state.artist} - ${json.state.title} | Web Scrobbler RPC` :
            "Web Scrobbler RPC"
        );

        start_time = json.state.start_time ?? 0;
        update_elapsed();

        if(json.state && json.state.cover) {
            update_favicon(json.state.cover);
            Background.style.setProperty("--cover-image-url", `url("${json.state.cover}")`);
            Background.classList.add("has-cover");
        } else {
            Background.classList.remove("has-cover");
        }
    });
};

let update_elapsed = (timestamp) => {
    let seconds = Math.floor((Date.now() / 1000) - start_time);
    let minutes = Math.floor(seconds / 60);
    seconds = seconds % 60;

    Elapsed.innerHTML = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
};

(() => {
    fetch_playing();
    setInterval(fetch_playing, fetch_interval);
    setInterval(update_elapsed, 500);
})();
