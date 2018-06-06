G <- function(l, u) {	u - l + 1 }
F1 <- function(l, u, p) {
	if (p > 1 && l < u) {
		sum(sapply(l:u, function(i, u, p) F1(i+1, u+1, p-1), u=u, p=p))
	} else {
		G(l, u)
	}
}

F2 <- function(l, u, p) {
	if (p > 0 && l <= u) {
		sum(sapply(l:u, function(i, u, p) F2(i+1, u+1, p-1), u=u, p=p))
	} else { 1 }
}

F3 <- function(n, p) {
	g <- expand.grid(rep(list(1:n), p))
	length(which(apply(g, 1, function(x) all(diff(x) > 0) )))
}

print.all <- function(n, p) {
	cat(' F1(1, n-p+1, p):', F1(1, n-(p-1), p), '\n') # paper's original one
	cat(' F2(1, n-p+1, p):', F2(1, n-(p-1), p), '\n') # suggested on the paper (F1 slightly changed)
	cat(' F2(0, n-p, p):', F2(0, n-p, p), '\n') # showing that u-l must be equal to n-p
	cat(' F3(n, p):', F3(n, p), '\n') # sum of a p-dimensional tensor's triangle
	cat(' choose(n, p):', choose(n, p), '\n\n')
}

n = 10
. <- sapply(0:5, function(i) { cat(' n=', n, '| p=', i, '\n'); print.all(n, i) })
