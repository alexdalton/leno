#include <stdio.h>
#include <stdlib.h>
#include <math.h>
struct pgmimage{
  char type[4];
  int rows,cols;
  int maxval;
  int *par;
};

typedef struct pgmimage pgmimage;
//Allocate memory space for image struct
pgmimage * newImage(int c, int r, int m);

//Implement these functions for MP7
void printImage(int *im, int cols, int rows, int maxval, FILE * fd);
void drawHexagon(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow, int color);
void sierpinski(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow);
void hexaflake(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow);


//Implement this function for challenges
//declare more helper function if needed
void square_tri(int *img, int rows, int cols, int height, int width, int centercol, int centerrow, int depth);




int main(int argc, char **argv){

  pgmimage *image = NULL;
  //create a file pointer
  FILE* fptr = fopen("result.pgm","w");
  int rows,cols,max,method,n;
  //get arugment 1 and argument 2 from the commandline
  method = atoi(argv[1]);
  n = atoi(argv[2]);
  max = 255;
  int height;
  int width;

  //call sierpinski function with calculated height and width using n
  if(method == 1){
      height = pow(3,n)*102;
      width = pow(3,n)*128;
      cols = width;
      rows = height;
      image = newImage(cols, rows, max);
      sierpinski(image->par,rows,cols,height,width,width/4,0);
  }
  //call hexaflake function with calculated height and width using n
  else if(method == 2){
      height = pow(3,n)*102;
      width = pow(3,n)*128;
      cols = width;
      rows = height;
      image = newImage(cols, rows, max);
      hexaflake(image->par,rows,cols,height,width,width/4,0);
  }
  //call square_tri function with calculated height and width using n
  else if(method == 3){
      height = pow(2,n)*56;
      width = pow(2,n)*64;
      cols = width;
      rows = height;
      image = newImage(cols, rows, max);
      //modify the following call if you changed the signature of square_tri function
      square_tri(image->par,rows,cols,height,width,width/2,height/2,0);
  }
  else
      printf("Invalid input for method.\n");
  //print the image file
  printImage(image->par,image->cols, image->rows, image->maxval, fptr);

  return 0;

}

/* sierpinski function                        
   input: img - int array that holds value for each pixel of the image
          rows - the height of entire image
          cols - the width of entie image
          height - the height of the current hexagon
          width - the width of the current hexagon
          toplcol, toplrow - col # and row # of the top left corner of the current hexagon*/

void sierpinski(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow){
  //your code goes here
}

/* drawHexagon function\
   input: img - int array that holds value for each pixel of the image
          rows - the height of entire image
          cols - the width of entie image
          height - the height of the current hexagon
          width - the width of the current hexagon
          toplcol, toplrow - col # and row # of the top left corner of the current hexagon
          color - the value that you want to draw each pixel*/
void drawHexagon(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow, int color){
  //your code goes here
}


 /* printImage function
    inputs: im - the int array that holds image pixel value
            cols - the number of total cols
            rows - the number of total rows
            maxval - the max value of each pixel
            fd - file pointer*/
void printImage(int *im, int cols, int rows, int maxval, FILE * fd)
{
//your code goes here
}


pgmimage* newImage(int c, int r, int m)
{
  pgmimage* im;
  im = (pgmimage *)malloc(sizeof(pgmimage));
  if (im!=NULL) {
    im ->type[0] = 'P';
    im ->type[1] = 'G';
    im ->type[2] = 'M';
    im ->type[3] = '\0';
    im ->rows = r; // *im.rows = r;
    im ->cols = c;
    im ->maxval = m;
    im ->par = (int *)malloc(c*r*sizeof(int));
    if (im->par==NULL)
      exit(-1);
  }
   int i;
  
  for(i=0;i<c*r;i++)
    im->par[i]=m;

 return im;
}


/* hexaflake function                        
   input: img - int array that holds value for each pixel of the image
          rows - the height of entire image
          cols - the width of entie image
          height - the height of the current hexagon
          width - the width of the current hexagon
          toplcol, toplrow - col # and row # of the top left corner of the current hexagon*/
void hexaflake(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow){
//your code goes here
}

void square_tri(int *img, int rows, int cols, int height, int width, int centercol, int centerrow, int depth){
//your code goes here
}

