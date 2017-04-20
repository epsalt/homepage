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
            nwalkers = 10,
            dims = {"nrows": nrows,
                    "ncols": Math.round(canvas.scrollHeight / canvas.scrollWidth * nrows),
                    "width": canvas.width / nrows,
                    "height": canvas.height / Math.round(canvas.scrollHeight / canvas.scrollWidth * nrows)},
            fpsInterval = 75 / 10,
            time = Date.now();

        var walkers = [];
        for (var i = 0; i < nwalkers; i++) {
            walkers.push(new Walker(ctx, dims));
        }

        ctx.fillStyle = "rgba(0, 0, 200, 0.25)";
        animate(walkers, time, fpsInterval, n, end);
    }
}

function animate(walkers, time, fpsInterval, n, end) {
    var elapsed = Date.now() - time;
    if (elapsed > fpsInterval) {
        time = Date.now();
        for (var i = 0; i < walkers.length; i++) {
            var w = walkers[i];
            if (w.rip == false) {
                w.step();
            } else {
                walkers[i] = new Walker(w.ctx, w.dims);
                n++;
            }
        }
    }

    if (n < end) {
        requestAnimationFrame(function(){
            animate(walkers, time, fpsInterval, n, end);
        });
    }
}

var Walker = class {
    constructor(ctx, dims) {
        this.ctx = ctx;
        this.dims = dims;
        this.x = 0;
        this.y = Math.round(Math.random() * dims.ncols);
        this.rip = false; // death is real
    }

    step() {
        if (this.x >= this.dims.nrows ||
            this.y <= 0 ||
            this.y >= this.dims.ncols) {
            this.rip = true;
        } else {
            this.draw();
            this.increment();
        }
    }

    draw() {
        this.ctx.fillRect(this.x * this.dims.width,
                          this.y * this.dims.height,
                          this.dims.width,
                          this.dims.height);
    }

    increment() {
        var y_step = Math.round((Math.random() * 2) - 1);
        this.x = this.x + 1;
        this.y = this.y + y_step;
    }
};
