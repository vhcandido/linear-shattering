#include <stdlib.h>
#include <stdio.h>

enum {
	PROGNAME,
	N,
	H,
	NARGS
};

int main(int argc, char **argv) {
	int n, h, max;

	if(argc < NARGS) {
		fprintf(stderr, "usage: %s n h\n", argv[PROGNAME]);
		exit(EXIT_FAILURE);
	}

	n = (int) atoi(argv[N]);
	h = (int) atoi(argv[H]);

	if (n <= h) {
		fprintf(stderr, "n must be greater than h\n", argv[PROGNAME]);
		exit(EXIT_FAILURE);
	}

	if (h == 1) {
		for (int i = 0; i < n-1; ++i) {
			printf("%2d %2d\n", i, i+1);
		}
	} else if (h==2) {
		for (int i = 0; i < n; ++i) {
			printf("%2d %2d\n", i, (i+1)%n);
		}
	}

	return 0;
}
