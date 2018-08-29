read.v <- function(file='../draw/vertices.dat') { as.matrix(read.table(file)) }
read.e <- function(file='../draw/edges.dat') { as.matrix(read.table(file)) }
read.f <- function(file='../draw/faces.dat') { as.matrix(read.table(file)) }

draw.poly <- function(V, E, v.col=NULL, e.col=NULL) {
	if (is.null(v.col)) v.col <- 'black'
	if (is.null(e.col)) e.col <- 'black'

	rgl::open3d()
	rgl::plot3d(V, col=v.col, box=FALSE, type='s', radius=0.05,
				xlim=c(-2,2), ylim=c(-2,2), zlim=c(-2,2))
	rgl::text3d(V + .1, texts=0:(nrow(V)-1), col=v.col)

	#apply(e+1, 1, function(pair) rgl::segments3d(v[unlist(pair),]))
	if (length(e.col) == 1) {
		edges <- as.numeric(t(E)) + 1
		rgl::segments3d(V[edges,], col=e.col)
	} else {
		for (i in 1:nrow(E)) {
			rgl::segments3d(V[unlist(E[i,])+1,], col=e.col[i])
		}
	}
}

# Returns a list with a color for each vertex/edge according to the vertices in the positive class
# - 'blue' for the graph induced by v.pos
# - 'black' for the graph induce by v\v.pos
# - 'yellow' for the edges not included in the aforementioned graphs ("removed")
#
# cube examples:
# c(0,1,4,5)
# c(0,1,5)
# c(0,1,3,5)
gen.colors <- function(V, E, v.pos) {
	v.col <- rep('black', nrow(V))
	v.col[v.pos+1] = 'blue'

	e.col <- rep('black', nrow(E))

	# For each edge, ask: is there any vertex from v.pos in this edge?
	idx <- apply(E, 1, function(edge) {
		any(!is.na(match(v.pos, edge)))
	})
    e.col[which(idx)] = 'yellow'

	if(length(v.pos) > 1) {
		idx <- apply(E, 1, function(edge) {
			any(apply(combn(v.pos, 2), 2, function(pair) {
				all(edge == pair)
			}))
		})
		e.col[which(idx)] = 'blue'
	}

    return(list(v = v.col, e = e.col))
}

# Expectance of edges cut by a hyperplane passing through the origin
# https://math.stackexchange.com/questions/1509007/separating-points-on-the-n-sphere
expected.cuts <- function(v, e) {
	dot <- apply(e+1, 1, function(i) {
		v[i[1],] %*% v[i[2],]
	})
	sum(acos(dot)/pi)
}

# add offset somehow
# default is 0
draw.surface <- function(p, b=0) {
	n <- 100
	x <- y <- seq(-1.5, 1.5, len=n)
	z <- outer(x, y, function(x,y) {
		z_ <- -(p[1]*x + p[2]*y + b)/p[3]
		z_[which(z_ < -1.5 | z_ > 1.5)] <- NA
		z_
	})
	surface3d(x, y, z, back='lines', front='lines', col='blue', lwd=1.5, alpha=.5)
}

draw.sphere <- function(V, alpha=.4) {
	rgl.spheres(0, 0, 0, radius=sqrt(V[1,] %*% V[1,]), alpha=alpha)
}

load.poly <- function(dir='../draw') {
	foo <- function(x) as.matrix(read.table(x))
	V <- foo(file.path(dir, 'vertices.dat'))
	E <- foo(file.path(dir, 'edges.dat'))
	F. <- foo(file.path(dir, 'faces.dat'))
	return(list(V=V, E=E, F=F.))
}

load.hyp <- function(suf='gi30', dir='../draw') {
	fname <- sprintf('v_%s.dat', suf)
	as.matrix(read.table(file.path(dir, fname)))
}

count.cuts <- function(V, E, H) {
	cuts <- apply(H, 1, function(h) {
		dot <- V %*% h
		apply(E+1, 1, function(e) {
			a <- dot[e[1]]
			b <- dot[e[2]]

			if (a == 0 || b == 0) {
				return(NA)
			} else {
				return(xor(a < 0, b < 0))
			}
		})
	})
	return(apply(cuts, 2, sum))
}

all.binaries <- function(n) {
	# create all n-bits binaries and concatenate each one into a string
	bin <- expand.grid(replicate(n, 0:1, simplify=FALSE))[,n:1]
	return(apply(bin, 1, paste0, collapse=''))
}

neighbourhood <- function(v, E) {
	idx <- which(apply(E == v, 1, any))
	unique(c(E[idx,]))
}

count.ways <- function(v, hyp, k=10) {
	n <- nrow(v)
	cuts <- apply(hyp, 1, function(h) {
		dot <- v %*% h
		h.norm <- sqrt(c(h %*% h))
		# dislocate the hyperplane generating k perturbations
		sapply(seq(-h.norm, h.norm, len=k), function(b) {
			net <- dot + b
			if (any(net == 0)) NA * net else as.numeric(net > 0)
		})
	})
	cuts <- matrix(cuts, nrow=n)

	# count how many of each pattern occurs
	ways <- table(apply(cuts, 2, paste0, collapse=''))
	names(ways)[length(ways)] <- 'NA'
	
	# initialize (with 0) a hash table for each binary and 'NA'
	count <- setNames(rep(0, 2**n + 1), c(all.binaries(n), 'NA'))
	#store the pattern occurences in ways
	count[names(ways)] = as.numeric(ways)
	
	return(list(way=names(count), count=as.numeric(count)))
}

count.ways <- function(V, E, k=10) {
	n <- nrow(V)
	
	# VERTICES
	cuts.v <- apply(V, 1, function(h) {
		dot <- V %*% h
		h.norm <- sqrt(c(h %*% h))
		# dislocate the hyperplane generating k perturbations
		sapply(seq(-h.norm, h.norm, len=k), function(b) {
			net <- dot + b
			if (any(net == 0)) NA * net else as.numeric(net > 0)
		})
	})
	cuts.v <- matrix(cuts.v, nrow=n)
	
	# EDGES
	E.mid <- apply(E+1, 1, function(e) colMeans(cube$V[e,]))
	cuts.e <- apply(E.mid, 1, function(h) {
		dot <- V %*% h
		h.norm <- sqrt(c(h %*% h))
		# dislocate the hyperplane generating k perturbations
		sapply(seq(-h.norm, h.norm, len=k), function(b) {
			net <- dot + b
			if (any(net == 0)) NA * net else as.numeric(net > 0)
		})
	})
	cuts.e <- matrix(cuts.e, nrow=n)
	
	# PAREI AQUI, TENHO QUE ENCONTRAR UMA FORMA DE DETERMINAR AS FACES PELOS EDGES
	# OU JÁ BAIXAR ESSAS FACES DO DMCCOOEY
	# FACES
	ajd.list <- lapply(1:nrow(V), function(v) {
		c(E[which(E[,2]+1 == v),1],
			E[which(E[,1]+1 == v),2]) + 1
	})
	visited <- rep(0, nrow(E))
	
	F_ <- apply()
	F.mid <- apply(F_, 1, function(f) colMeans(cube$V[f,]))
	cuts.f <- apply(F.mid, 1, function(h) {
		dot <- V %*% h
		h.norm <- sqrt(c(h %*% h))
		# dislocate the hyperplane generating k perturbations
		sapply(seq(-h.norm, h.norm, len=k), function(b) {
			net <- dot + b
			if (any(net == 0)) NA * net else as.numeric(net > 0)
		})
	})
	cuts.f <- matrix(cuts.f, nrow=n)
	
	# count how many of each pattern occurs
	ways <- table(apply(cuts, 2, paste0, collapse=''))
	names(ways)[length(ways)] <- 'NA'
	
	# initialize (with 0) a hash table for each binary and 'NA'
	count <- setNames(rep(0, 2**n + 1), c(all.binaries(n), 'NA'))
	#store the pattern occurences in ways
	count[names(ways)] = as.numeric(ways)
	
	return(list(way=names(count), count=as.numeric(count)))
}