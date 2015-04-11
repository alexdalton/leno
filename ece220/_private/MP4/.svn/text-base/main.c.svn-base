#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Do not modify anything. Write your code under the two if statements indicated below.
int main(int argc, char **argv)
{
	double omega1, omega2, omegac, T, dt;
	int N, method;
	FILE *in;

	// Open the file and scan the input variables.
	if (argv[1] == NULL) {
		printf("You need an input file.\n");
		return -1;
	}
	in = fopen(argv[1], "r");
	if (in == NULL)
		return -1;
	fscanf(in, "%lf", &omega1);
	fscanf(in, "%lf", &omega2);
	fscanf(in, "%lf", &omegac);
	fscanf(in, "%d", &method);

	T = 3 * 2 * M_PI / omega1; 		// Total time
	N = 20 * T / (2 * M_PI / omega2); 	// Total number of time steps
	dt = T / N;				// Time step ("delta t")

	// Method number 1 corresponds to the finite difference method.
	if (method == 1) {
		int i;
		double Voutnew = 0, Voutcur = 0, Voutprev = 0;

		// Write your code here!
	}

	// Method number 2 corresponds to the Runge-Kutta method (only for challenge).
	else if (method == 2) {
		// Write your code here for the challenge problem.
	}

	else {
		// Print error message.
		printf("Incorrect method number.\n");
		return -1;
	}

	fclose(in);
	return 0;
}
