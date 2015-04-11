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
pgmimage * newImage(int c, int r, int m);

void printImage(int *im, int cols, int rows, int maxval, FILE * fd);
void drawHexagon(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow, int color);
void sierpinski(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow);
void hexaflake(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow);


void square_tri(int *img, int rows, int cols, int height, int width, int centercol, int centerrow, int depth);
void drawTriangle(int *img, int rows, int cols, int height, int colCenter, int rowCenter, int color);
void drawSquare(int *img, int rows, int cols, int height, int width, int colCenter, int rowCenter, int color);


int main(int argc, char **argv){

  pgmimage *image = NULL;
  FILE* fptr = fopen("result.pgm","w");
  int rows,cols,max,method,n;
  method = atoi(argv[1]);
  n = atoi(argv[2]);
  max = 255;
  int height;
  int width;

  if(method == 1){
      height = pow(3,n)*102;
      width = pow(3,n)*128;
      cols = width;
      rows = height;
      image = newImage(cols, rows, max);
      sierpinski(image->par,rows,cols,height,width,width/4,0);
  }
  else if(method == 2){
      height = pow(3,n)*102;
      width = pow(3,n)*128;
      cols = width;
      rows = height;
      image = newImage(cols, rows, max);
      hexaflake(image->par,rows,cols,height,width,width/4,0);
  }
  else if(method == 3){
      height = pow(2,n)*56;
      width = pow(2,n)*64;
      cols = width;
      rows = height;
      image = newImage(cols, rows, max);
      square_tri(image->par,rows,cols,height,width,width/2,height/2,0);
  }
  else
      printf("Invalid input for method.\n");
  printImage(image->par,image->cols, image->rows, image->maxval, fptr);

  return 0;

}

/* sierpinski function                        
 *    input: img - int array that holds value for each pixel of the image
 *              rows - the height of entire image
 *                        cols - the width of entie image
 *                                  height - the height of the current hexagon
 *                                            width - the width of the current hexagon
 *                                                      toplcol, toplrow - col # and row # of the top left corner of the current hexagon*/

void sierpinski(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow){

  if(height==102){

    drawHexagon(img,rows,cols,height,width,toplcol,toplrow,0);

  }else{

    int newHeight = height/3;
    int newWidth = width/3;

    sierpinski(img,rows,cols,newHeight,newWidth, toplcol,toplrow);

    sierpinski(img,rows,cols,newHeight,newWidth, toplcol+width/2-newWidth/2,toplrow);

    sierpinski(img,rows,cols,newHeight,newWidth, toplcol-newWidth/2,toplrow+newHeight);
    
    sierpinski(img,rows,cols,newHeight,newWidth, toplcol+width/2,toplrow+newHeight);
    
    sierpinski(img,rows,cols,newHeight,newWidth, toplcol,toplrow+height-newHeight);
    
    sierpinski(img,rows,cols,newHeight,newWidth, toplcol+width/2-newWidth/2,toplrow+height-newHeight);

  }
}

/* drawHexagon function\
 *    input: img - int array that holds value for each pixel of the image
 *              rows - the height of entire image
 *                        cols - the width of entie image
 *                                  height - the height of the current hexagon
 *                                            width - the width of the current hexagon
 *                                                      toplcol, toplrow - col # and row # of the top left corner of the current hexagon
 *                                                                color - the value that you want to draw each pixel*/
void drawHexagon(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow, int color){

  int i,col, row, w, counter;

    for(row = 0, col = 0, w = width/2, counter = 1; row < (height)/2; row++, counter++){
      for(i = 0; i<w;i++){
          img[(toplrow+row)*cols+(toplcol+col+i)] = color;
      }
      if(counter%3==0){
        w+=4;
        col-=2;
      }
    }

    for(w = width, col = col+2, counter = 1; row < height; row++, counter++){
      for(i = 0; i<w;i++){
          img[(toplrow+row)*cols+(toplcol+col+i)] = color;
      }
      if(counter%3==0){
        w-=4;
        col+=2;
      }
    }
}


 /* printImage function
 *     inputs: im - the int array that holds image pixel value
 *                 cols - the number of total cols
 *                             rows - the number of total rows
 *                                         maxval - the max value of each pixel
 *                                                     fd - file pointer*/
void printImage(int *im, int cols, int rows, int maxval, FILE * fd)
{
  int i;

  /* Print header */
  fprintf(fd, "P2\n%d %d\n%d\n", cols, rows, maxval);
  int size = rows * cols;
  /* Print pixels */
  for(i = 0; i < size;i++){
    fprintf(fd, " %d ", im[i]);
  }
  fprintf(fd, "\n");
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
 *    input: img - int array that holds value for each pixel of the image
 *              rows - the height of entire image
 *                        cols - the width of entie image
 *                                  height - the height of the current hexagon
 *                                            width - the width of the current hexagon
 *                                                      toplcol, toplrow - col # and row # of the top left corner of the current hexagon*/
void hexaflake(int *img, int rows, int cols, int height, int width, int toplcol, int toplrow){

  if(height==102){

    drawHexagon(img,rows,cols,height,width,toplcol,toplrow,0);

  }else{

    int newHeight = height/3;
    int newWidth = width/3;

    hexaflake(img,rows,cols,newHeight,newWidth, toplcol,toplrow);

    hexaflake(img,rows,cols,newHeight,newWidth, toplcol+width/2-newWidth/2,toplrow);

    hexaflake(img,rows,cols,newHeight,newWidth, toplcol-newWidth/2,toplrow+newHeight);
    
    hexaflake(img,rows,cols,newHeight,newWidth,toplcol+newWidth/2,toplrow+newHeight);
    
    hexaflake(img,rows,cols,newHeight,newWidth, toplcol+width/2,toplrow+newHeight);
    
    hexaflake(img,rows,cols,newHeight,newWidth, toplcol,toplrow+height-newHeight);
    
    hexaflake(img,rows,cols,newHeight,newWidth, toplcol+width/2-newWidth/2,toplrow+height-newHeight);
  }
}

void square_tri(int *img, int rows, int cols, int height, int width, int centercol, int centerrow, int depth){
    if (height == 56 && (depth%2))
    drawTriangle(img, rows, cols, height, centercol, centerrow, 255);
    else{
    if(depth%2)
    {
        drawTriangle(img, rows, cols, height, centercol, centerrow, 255);
        square_tri(img, rows, cols, height/2, width/2, centercol, centerrow+height/4, depth+1);
    }
    else
    {
        drawSquare(img, rows, cols, height, width, centercol, centerrow, 0);
        square_tri(img, rows, cols, height, width, centercol, centerrow, depth+1);
    }
    }
}

void drawTriangle(int *img, int rows, int cols, int height, int colCenter, int rowCenter, int color){
  int i,col, row, width, counter;

    for(row = -height/2, col = -4, width = 8, counter = 1; row < height/2; row++, counter++){
      for(i = 0; i<width;i++){
          img[(rowCenter+row)*cols+(colCenter+col+i)] = color;
      }
      if(counter%7==0){
        width+=8;
        col-=4;
      }
    }
}

void drawSquare(int *img, int rows, int cols, int height, int width, int colCenter, int rowCenter, int color){
  int col, row;
    for(row = -height/2; row < height/2; row++){
      for(col = -width/2; col<width/2;col++){
          img[(rowCenter+row)*cols+(colCenter+col)] = color;
      }
    }
}

