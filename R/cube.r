require(rgl)
require(magrittr)

#shade3d( translate3d( cube3d(col = "green"), 3, 0, 0) , alpha=.1)

draw.poly <- function(poly.col = NULL) {
	if(is.null(poly.col)) poly.col <- 'black'
	
	# Coordinates according to the drawing of points
	#           1 2 3 4 5 6 7 8
	i = 0 # perturbation
	poly.x <- c(1+i,0,0-i,1,1,0-i,0,1+i)
	poly.y <- c(1+i,1,1+i,1,0,0-i,0,0-i)
	poly.z <- c(1+i,1,0-i,0,1,1+i,0,0-i)
	poly <- cbind(poly.x, poly.y, poly.z)
	#poly <- as.matrix(expand.grid(0:1, 0:1, 0:1))
	
	# Edges connecting each vertex
	edges <- c(1,2, 1,4, 1,5,
						 3,7, 3,2, 3,4,
						 8,4, 8,7, 8,5,
						 6,2, 6,5, 6,7)
	
	open3d()
	plot3d(poly, col=poly.col, box=FALSE, type="s", radius=0.05,
				 xlim=c(-1,2), ylim=c(-1,2), zlim=c(-1,2))
	text3d(poly + .07, texts=0:7, col=poly.col, cex=1.5)
	segments3d(poly[edges,])
}

bin.to.redblue <- function(x) {
	x <- strsplit(x, '') %>% unlist %>% as.numeric
	ifelse(x, 'blue', 'red')
}

poly.col <- '11010001'
draw.poly(poly.col = bin.to.redblue(poly.col))
