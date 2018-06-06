G <- function(l, u) {	u - l + 1 }
F1 <- function(l, u, p) {
	if (p > 1 && l < u) {
		sum(sapply(l:u, function(i, u, p) F1(i+1, u+1, p-1), u=u, p=p))
	} else {
		G(l, u)
	}
}

F2 <- function(l, u, p) {
	if (p > 0 && l < u) {
		sum(sapply(l:u, function(i, u, p) F2(i+1, u+1, p-1), u=u, p=p))
	} else { 1 }
}

F3 <- function(n, p) {
	g <- expand.grid(rep(list(1:n), p))
	length(which(apply(g, 1, function(x) all(diff(x) > 0) )))
}


n = 10

p = 2
F1(1, n-(p-1), p) # paper's original one
F2(1, n-(p-1), p) # suggested on the paper (F1 slightly changed)
F3(n, p) # sum of a p-dimensional tensor's triangle
choose(n, p)

p = 3
F1(1, n-(p-1), p) # paper's original one
F2(1, n-(p-1), p) # suggested on the paper (F1 slightly changed)
F3(n, p) # sum of a p-dimensional tensor's triangle
choose(n, p)

p = 5
F1(1, n-(p-1), p) # paper's original one
F2(1, n-(p-1), p) # suggested on the paper (F1 slightly changed)
F3(n, p) # sum of a p-dimensional tensor's triangle
choose(n, p)
