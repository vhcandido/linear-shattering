require(rgl)
require(magrittr)

#shade3d( translate3d( cube3d(col = "green"), 3, 0, 0) , alpha=.1)

draw.poly <- function(poly.col = NULL) {
	if(is.null(poly.col)) poly.col <- 'black'
	
	# Coordinates according to the drawing of points
	#           1 2 3 4 5 6 7 8
	poly.x <- c(1,0,0,1)
	poly.y <- c(1,1,0,0)
	poly.z <- c(1,0,1,0)
	poly.x <- c(poly.x, c(1,0,0,-.3)-.8)
	poly.y <- c(poly.y, c(0,0,1,-.3)-.8)
	poly.z <- c(poly.z, c(0,1,0,-.3)-.8)
	poly <- cbind(poly.x, poly.y, poly.z)
	#poly <- as.matrix(expand.grid(0:1, 0:1, 0:1))
	
	# Edges connecting each vertex
	edges <- c(1,2, 1,3, 1,4,
						 2,3, 2,4,
						 3,4,
						 8,5, 8,7, 8,6,
						 7,6, 7,5,
						 6,5,
						 2,7, 3,6, 4,5)
	
	open3d()
	plot3d(poly, col=poly.col, box=FALSE, type="s", radius=0.05,
				 xlim=c(-2,2), ylim=c(-2,2), zlim=c(-2,2))
	text3d(poly + .07, texts=1:8, col=poly.col, cex=1.5)
	segments3d(poly[edges,])
	return(poly)
}

bin.to.redblue <- function(x) {
	x <- strsplit(x, '') %>% unlist %>% as.numeric
	ifelse(x, 'blue', 'red')
}

#poly.col <- NULL
#draw.poly(poly.col = bin.to.redblue(poly.col))
draw.poly()
