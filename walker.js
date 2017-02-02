(function () {
    var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
    window.requestAnimationFrame = requestAnimationFrame;
})();

function draw() {
    // Random walk canvas animation
    var canvas = document.getElementById("walker");
    if (canvas.getContext) {
        var ctx = canvas.getContext("2d");
        var nrows = 80;
        var dims = {"nrows": nrows,
                    "ncols": Math.round(canvas.scrollHeight / canvas.scrollWidth * nrows),
                    "width": canvas.width / nrows,
                    "height": canvas.height / Math.round(canvas.scrollHeight / canvas.scrollWidth * nrows)};
        ctx.fillStyle = "rgba(0, 0, 200, 0.25)";
        var coords = [0, Math.round(dims.ncols / 2)]; // start on the middle of the left side, walk right
        animate(coords, ctx, dims);
    }
}

function animate(coords, ctx, dims) {
    // if the walker goes out of bounds reset
    if (coords[0] >= dims.nrows ||
        coords[1] <= 0 ||
        coords[1] >= dims.ncols) {
        requestAnimationFrame(function(){
            animate([0, Math.round(dims.ncols / 2)], ctx, dims);
        });
    } else {
        // draw a rect then take a step        
        ctx.fillRect(coords[0] * dims.width, coords[1] * dims.height, dims.width, dims.height);        
        var step = Math.round((Math.random() * 2) - 1);
        coords = [coords[0] + 1, coords[1] + step];
        requestAnimationFrame(function(){
            animate(coords, ctx, dims);
        });
    }
}
