#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
 
 
double fx_val(double a, double b, double c, double d, double e, double x)
{
    return (a*pow(x,4) + b*pow(x,3) + c*pow(x, 2) + d*x + e);
}
 
double fx_dval(double a, double b, double c, double d, double e, double x)
{
    return (4*a*pow(x,3) + 3*b*pow(x,2) + 2*c*x + d);
    
}
double newrfind(double a, double b, double c, double d, double e, double x)
{
    double xn, xc; 
    int n = 1;
    xn = x;
    xc = x;
    do
    {   xc = xn;
        xn = (xc - (fx_val(a, b, c, d, e, xc)/fx_dval(a, b, c, d, e, xc)));
        n++;
    }while((abs(xn-xc) > 0.0000001)||(n<10000));
     
     
    return xn;
}
 
int rootbound(double a, double b, double c, double d, double e, double r, double l)
{
    double ar, br, cr, dr, er, al, bl, cl, dl, el;
    int n = 0, vr = 0, vl = 0;
    ar = a;
    br = 4*a*r + b;
    cr = 6*a*pow(r,2) + 3*b*r + c;
    dr = 4*a*pow(r,3) + 3*b*pow(r,2) + 2*c*r + d;
    er = a*pow(r,4) + b*pow(r,3) + c*pow(r, 2) + d*r + e;
    al = a;
    bl = 4*a*l + b;
    cl = 6*a*pow(l,2) + 3*b*l + c;
    dl = 4*a*pow(l,3) + 3*b*pow(l,2) + 2*c*l + d;
    el = a*pow(l,4) + b*pow(l,3) + c*pow(l, 2) + d*l + e;
     
    if(ar*br < 0)
        vr++;
    if(br*cr < 0)
        vr++;
    if(cr*dr < 0)
        vr++;
    if(dr*er < 0)
        vr++;
     
    if(al*bl < 0)
        vl++;
    if(bl*cl < 0)
        vl++;
    if(cl*dl < 0)
        vl++;
    if(dl*el < 0)
        vl++;
         
    n = abs(vl-vr);
     
    return n;
}
 
int main(int argc, char **argv)
{
    double a, b, c, d, e, l, r;
    FILE *in;
 
    if (argv[1] == NULL) {
        printf("You need an input file.\n");
        return -1;
    }
    in = fopen(argv[1], "r");
    if (in == NULL)
        return -1;
    fscanf(in, "%lf", &a);
    fscanf(in, "%lf", &b);
    fscanf(in, "%lf", &c);
    fscanf(in, "%lf", &d);
    fscanf(in, "%lf", &e);
    fscanf(in, "%lf", &l);
    fscanf(in, "%lf", &r);
     
    int n;
    double i, root; 
    n = rootbound(a, b, c, d, e, r, l);
    if(n == 0)
    {   
        printf("The polynomial has no roots in the given interval.\n");
    }
    else
    {
        for (i = l; i <= r; i = i + 0.5)
        {
        root = newrfind(a, b, c, d, e, i);
        if(root == DBL_MAX)
        {
            printf("No roots found.\n");
        }
        else
        { 
            printf("Root found: %f\n", root);
 
        }
         
    }
         
     
    }
     
     
    fclose(in);
     
    return 0;
}
