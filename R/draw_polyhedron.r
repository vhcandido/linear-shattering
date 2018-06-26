read.v <- function(file='../draw/vertices.dat') { as.matrix(read.table(file)) }
read.e <- function(file='../draw/edges.dat') { as.matrix(read.table(file)) }

draw.poly <- function(v, e, v.col=NULL, e.col=NULL) {
	if (is.null(v.col)) v.col <- 'black'
	if (is.null(e.col)) e.col <- 'black'

	rgl::open3d()
	rgl::plot3d(v, col=v.col, box=FALSE, type='s', radius=0.05,
				xlim=c(-2,2), ylim=c(-2,2), zlim=c(-2,2))
	rgl::text3d(v + .1, texts=0:(nrow(v)-1), col=v.col)

	#apply(e+1, 1, function(pair) rgl::segments3d(v[unlist(pair),]))
	if (length(e.col) == 1) {
		edges <- as.numeric(t(e)) + 1
		rgl::segments3d(v[edges,], col=e.col)
	} else {
		for (i in 1:nrow(e)) {
			rgl::segments3d(v[unlist(e[i,])+1,], col=e.col[i])
		}
	}
}

# Returns a list with a color for each vertex/edge according to the vertices in the positive class
# - 'blue' for the graph induced by v.pos
# - 'black' for the graph induce by v\v.pos
# - 'yellow' for the edges not included in the aforementioned graphs ("removed")
gen.colors <- function(v, e, v.pos) {
	v.col <- rep('black', nrow(v))
	v.col[v.pos+1] = 'blue'

	e.col <- rep('black', nrow(e))

	# For each edge, ask: is there any vertex from v.pos in this edge?
	idx <- apply(e, 1, function(edge) {
		any(!is.na(match(v.pos, edge)))
	})
    e.col[which(idx)] = 'yellow'

	idx <- apply(e, 1, function(edge) {
		any(apply(combn(v.pos, 2), 2, function(pair) {
			all(edge == pair)
		}))
	})
	e.col[which(idx)] = 'blue'

    return(list(v = v.col, e = e.col))
}

# Expectance of edges cut by a hyperplane passing through the origin
# https://math.stackexchange.com/questions/1509007/separating-points-on-the-n-sphere
cuts.origin <- function(v, e) {
	dot <- apply(e+1, 1, function(i) {
		v[i[1],] %*% v[i[2],]
	})
	sum(acos(dot)/pi)
}
