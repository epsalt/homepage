(function () {
    var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
    window.requestAnimationFrame = requestAnimationFrame;
})();

function draw() {
    // Random walk canvas animation
    var canvas = document.getElementById("walker");
    if (canvas.getContext) {
        var ctx = canvas.getContext("2d"),
            nrows = 18,
            end = 20,
            n = 0,
            dims = {"nrows": nrows,
                    "ncols": Math.round(canvas.scrollHeight / canvas.scrollWidth * nrows),
                    "width": canvas.width / nrows,
                    "height": canvas.height / Math.round(canvas.scrollHeight / canvas.scrollWidth * nrows)},
            coords = [0, Math.round(dims.ncols / 2)], // start on the middle of the left side, walk right
            fpsInterval = 75 / 10,
            time = Date.now();
        
        ctx.fillStyle = "rgba(0, 0, 200, 0.25)";
        animate(coords, ctx, dims, time, fpsInterval, n, end);
    }
}

function animate(coords, ctx, dims, time, fpsInterval, n, end) {
    // if the walker goes out of bounds reset
    var elapsed = Date.now() - time;
    if(elapsed > fpsInterval) {
        time = Date.now();
        if (coords[0] >= dims.nrows ||
            coords[1] <= 0 ||
            coords[1] >= dims.ncols) {
            coords = [0, Math.round(Math.random() * dims.ncols)];
            n++;
         } else {
            // draw a rect then take a step        
            ctx.fillRect(coords[0] * dims.width, coords[1] * dims.height, dims.width, dims.height);        
            var step = Math.round((Math.random() * 2) - 1);
            coords = [coords[0] + 1, coords[1] + step];
         }
    }
    if(n < end) {
        requestAnimationFrame(function(){
            animate(coords, ctx, dims, time, fpsInterval, n, end);
        });
    }
}
