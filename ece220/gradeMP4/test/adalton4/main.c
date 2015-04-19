#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv)
{
	double omega1, omega2, omegac, T, dt;
	int N, method;
	FILE *in;

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

	T = 3 * 2 * M_PI / omega1;
	N = 20 * T / (2 * M_PI / omega2);
	dt = T / N;

	if (method == 1) {
		int i;
		double Voutnew = 0, Voutcur = 0, Voutprev = 0;

		printf("%lf\n", Voutcur);
		for (i = 1; i < N-1; i++) {
			Voutprev = Voutcur;
			Voutcur = Voutnew;
			Voutnew = 1 / (sqrt(2) / (2 * dt*omegac) + 1 / (dt*dt*omegac*omegac))*(sin(omega1*i*dt)+.5*sin(omega2*i*dt) - Voutcur - sqrt(2)*(-Voutprev) / (2 * dt*omegac) - (-2 * Voutcur + Voutprev) / (dt*dt*omegac*omegac));
			printf("%lf\n", Voutcur);
		}
		printf("%lf\n", Voutnew);
	}
	else if (method == 2) {
		int i;
		double Vout1new = 0, Vout1 = 0, Vout2new = 0, Vout2 = 0;
		double k1, k2, k3, k4, m1, m2, m3, m4;

		for (i = 0; i < N-1; i++) {
			Vout1 = Vout1new;
			Vout2 = Vout2new;
			k1 = Vout2;
			k2 = Vout2 + k1*dt/2;
			k3 = Vout2 + k2*dt/2;
			k4 = Vout2 + k3*dt;
			Vout1new = Vout1 + dt/6*(k1+2*k2+2*k3+k4);
			m1 = omegac*omegac*(sin(omega1*i*dt)+.5*sin(omega2*i*dt)) - omegac*omegac*Vout1 - omegac*sqrt(2)*Vout2;
			m2 = m1*(1+dt/2);
			m3 = m1+m2*dt/2;
			m4 = m1+m3*dt;
			Vout2new = Vout2 + dt/6*(m1+2*m2+2*m3+m4);
			printf("%lf\n", Vout1);
		}
		printf("%lf\n", Vout1new);
	}
	else {
		printf("Incorrect method number.\n");
		return -1;
	}

	fclose(in);
	return 0;
}
