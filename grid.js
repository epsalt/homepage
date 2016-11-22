
function draw(){
    var canvas = document.getElementById('walker');
    if (canvas.getContext){
        var ctx = canvas.getContext('2d');

        var nrows = 100;
        var ncols = Math.round(canvas.height / canvas.width * nrows);
        
        var cell_width = canvas.width / nrows;
        var cell_height = canvas.height / ncols;

        ctx.fillStyle = "rgba(0, 0, 200, 0.25)";

        var coords = [0, (ncols/2)];

        function animate(coords){
            if(coords[0] > nrows ||
               coords[1] < 1     ||
               coords[1] > ncols - 2) {
                setTimeout(animate, 750, [0, ncols/2]);
            } else {               
                var step = Math.round((Math.random() * 2) - 1);
                coords = [coords[0] + 1, coords[1] + step];          
                ctx.fillRect(coords[0]*cell_width, coords[1]*cell_height, cell_width, cell_height);
                setTimeout(animate, 200, coords);
            }
        }
        animate(coords);
    }
}
