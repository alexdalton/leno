#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "imageData.h"
#include "functions.h"
#include "solution.h"
 
#define IMAGE_WIDTH 480
#define IMAGE_HEIGHT 320
 
Image *initializeInput();
int checkRadius(int stud,int sol);
int checkGausFilter(double *stud,double *sol,int size);
int checkImage(Image *stud,Image *sol);
double imageError(Image *stud,Image *sol);
 
int main()
{
  Image *inputImage=initializeInput();
  Image *studImage=generateOutput(inputImage);
  Image *solImage=generateOutput(inputImage);
 
  double sigma=2;
  int radius=getRadiusSol(sigma);
  const double gMonoMult[3]={.299,.587,.114};
   
  printf("Testing getRadius:\n");
  if(!checkRadius(getRadius(sigma),radius))
  {
    printf("getRadius correct\n");
  }
  else
  {
    printf("getRadius incorrect\n");
  }
 
  int size=(2*radius+1)*(2*radius+1);
  double *gausFilter=(double*)malloc(sizeof(double)*size);
  double *gausFilterSol=(double*)malloc(sizeof(double)*size);
  printf("\nTesting calculateGausFilter:\n");
  calculateGausFilter(gausFilter,sigma);
  calculateGausFilterSol(gausFilterSol,sigma);
  if(!checkGausFilter(gausFilter,gausFilterSol,size))
  {
    printf("calculateGausFilter correct\n");
  }
  else 
  {
    printf("calculateGausFilter incorrect\n");
  }
 
  uint8_t *inRed=inputImage->redChannel;
  uint8_t *inGreen=inputImage->greenChannel;
  uint8_t *inBlue=inputImage->blueChannel;
  uint8_t *inAlpha=inputImage->alphaChannel;
  uint8_t *studRed=studImage->redChannel;
  uint8_t *studGreen=studImage->greenChannel;
  uint8_t *studBlue=studImage->blueChannel;
  uint8_t *studAlpha=studImage->alphaChannel;
  uint8_t *solRed=solImage->redChannel;
  uint8_t *solGreen=solImage->greenChannel;
  uint8_t *solBlue=solImage->blueChannel;
  uint8_t *solAlpha=solImage->alphaChannel;
  printf("\nTesting convolveImage:\n");
  convolveImage(inRed,inGreen,inBlue,inAlpha,studRed,studGreen,studBlue,
                studAlpha,gausFilterSol,radius,IMAGE_WIDTH,IMAGE_HEIGHT);
  convolveImageSol(inRed,inGreen,inBlue,inAlpha,solRed,solGreen,solBlue,
                   solAlpha,gausFilterSol,radius,IMAGE_WIDTH,IMAGE_HEIGHT);
  double convolveError = 0.00005;
  if(imageError(studImage,solImage)<convolveError)
  {
    printf("convolveImage correct with error %lf < %lf\n",imageError(studImage,solImage),convolveError);
  }
  else
  {
    printf("convolveImage incorrect with error %lf > %lf\n",imageError(studImage,solImage),convolveError);
  }
 
  printf("\nTesting Nearest Pixel\n");
  int x,y,xSolOut,ySolOut,xStuOut,yStuOut;
  x=100;
  y=120;
  double transformnp[2][3]={{0.8,0.2,-22},{0.1,0.3,-32}};
  double transformnpstu[2][3]={{0.8,0.2,-22},{0.1,0.3,-32}};
  nearestPixel(y, x, transformnpstu,
              &yStuOut, &xStuOut, IMAGE_WIDTH, IMAGE_HEIGHT);
  nearestPixelSol(y, x, transformnp,
              &ySolOut, &xSolOut, IMAGE_WIDTH, IMAGE_HEIGHT);
  if(abs(ySolOut-yStuOut)<2){
    printf("nearestPixel Y value correct\n");
  }else{
    printf("nearestPixel Y value incorrect\n");
  }
  if(abs(xSolOut-xStuOut)<2){
        printf("nearestPixel X value correct\n");
  }else{
    printf("nearestPixel X value incorrect\n");
  }
 
printf("\nTesting transformImage\n");
  /*test cases for transform*/
  double acceptableError = 0.03;
  /*shift*/
  double computedError;
  double transform1[2][3]={{1,0,50},{0,1,50}};
  double transform1stu[2][3]={{1,0,50},{0,1,50}};
  transformImage(inRed,inGreen,inBlue,inAlpha,
              studRed,studGreen,studBlue,
              studAlpha,transform1stu,IMAGE_WIDTH,IMAGE_HEIGHT);
  transformImageSol(inRed,inGreen,inBlue,inAlpha,
              solRed,solGreen,solBlue,
              solAlpha,transform1,IMAGE_WIDTH,IMAGE_HEIGHT);
  computedError = imageError(studImage,solImage);
  if(computedError<acceptableError)
  {
    printf("transformImage with shift transform correct with error: %lf < %lf\n",computedError,acceptableError);
  }
  else
  { 
    printf("transformImage with shift transform incorrect with error: %lf > %lf\n",computedError,acceptableError); 
  }
  /*scale*/
  double transform2[2][3]={{0.5,0,0},{0,0.5,0}};
  double transform2stu[2][3]={{0.5,0,0},{0,0.5,0}};
  transformImage(inRed,inGreen,inBlue,inAlpha,
              studRed,studGreen,studBlue,
              studAlpha,transform2stu,IMAGE_WIDTH,IMAGE_HEIGHT);
  transformImageSol(inRed,inGreen,inBlue,inAlpha,
              solRed,solGreen,solBlue,
              solAlpha,transform2,IMAGE_WIDTH,IMAGE_HEIGHT);
  computedError = imageError(studImage,solImage);
  if(computedError<acceptableError)
  {
    printf("transformImage with scale transform correct with error: %lf < %lf\n",computedError,acceptableError);
  }
  else
  { 
    printf("transformImage with scale transform incorrect with error: %lf > %lf\n",computedError,acceptableError); 
  }
  /*rotate*/
  double transform3[2][3]={{cos(35),-sin(35),0},{sin(35),cos(35),0}};
  double transform3stu[2][3]={{cos(35),-sin(35),0},{sin(35),cos(35),0}};
  transformImage(inRed,inGreen,inBlue,inAlpha,
              studRed,studGreen,studBlue,
              studAlpha,transform3stu,IMAGE_WIDTH,IMAGE_HEIGHT);
  transformImageSol(inRed,inGreen,inBlue,inAlpha,
              solRed,solGreen,solBlue,
              solAlpha,transform3,IMAGE_WIDTH,IMAGE_HEIGHT);
  computedError = imageError(studImage,solImage);
  if(computedError<acceptableError)
  {
    printf("transformImage with rotation transform correct with error: %lf < %lf\n",computedError,acceptableError);
  }
  else
  { 
    printf("transformImage with rotation transform incorrect with error: %lf > %lf\n",computedError,acceptableError); 
  }
  /*skew, scale and shift*/
  double transform4[2][3]={{0.8,0.2,-20},{0.1,0.3,-30}};
  double transform4stu[2][3]={{0.8,0.2,-20},{0.1,0.3,-30}};
  transformImage(inRed,inGreen,inBlue,inAlpha,
              studRed,studGreen,studBlue,
              studAlpha,transform4stu,IMAGE_WIDTH,IMAGE_HEIGHT);
  transformImageSol(inRed,inGreen,inBlue,inAlpha,
              solRed,solGreen,solBlue,
              solAlpha,transform4,IMAGE_WIDTH,IMAGE_HEIGHT);
  computedError = imageError(studImage,solImage);
  if(computedError<acceptableError)
  {
    printf("transformImage with general transform correct with error: %lf < %lf\n",computedError,acceptableError);
  }
  else
  { 
    printf("transformImage with general transform incorrect with error: %lf > %lf\n",computedError,acceptableError);
  }
 
 
  printf("\nTesting convertToGray\n");
  convertToGray(inRed,inGreen,inBlue,inAlpha,studRed,studGreen,studBlue,
                studAlpha,gMonoMult,IMAGE_WIDTH,IMAGE_HEIGHT);
  convertToGraySol(inRed,inGreen,inBlue,inAlpha,solRed,solGreen,solBlue,
                   solAlpha,gMonoMult,IMAGE_WIDTH,IMAGE_HEIGHT);
  if(!checkImage(studImage,solImage))
  {
    printf("convertToGray correct\n");
  }
  else
  {
    printf("convertToGray incorrect\n");
  }
 
  printf("\nTesting invertImage:\n");
  invertImage(inRed,inGreen,inBlue,inAlpha,studRed,studGreen,studBlue,
              studAlpha,IMAGE_WIDTH,IMAGE_HEIGHT);
  invertImageSol(inRed,inGreen,inBlue,inAlpha,solRed,solGreen,solBlue,
                 solAlpha,IMAGE_WIDTH,IMAGE_HEIGHT);
  if(!checkImage(studImage,solImage))
  {
    printf("invertImage correct\n");
  }
  else
  {
    printf("invertImage incorrect\n");
  }
 
 
  printf("\nTesting pixelate:\n");
  pixelate(inRed,inGreen,inBlue,inAlpha,studRed,studGreen,studBlue,studAlpha,
           8,8,IMAGE_WIDTH,IMAGE_HEIGHT);
  pixelateSol(inRed,inGreen,inBlue,inAlpha,solRed,solGreen,solBlue,solAlpha,
              8,8,IMAGE_WIDTH,IMAGE_HEIGHT);
  if(!checkImage(studImage,solImage))
  {
    printf("pixelate correct\n");
  }
  else
  {
    printf("pixelate incorrect\n");
  }
 
  printf("\nTesting colorDodge:\n");
  colorDodge(inRed,inGreen,inBlue,inAlpha,inRed,inGreen,inBlue,inAlpha,
             studRed,studGreen,studBlue,studAlpha,IMAGE_WIDTH,IMAGE_HEIGHT);
  colorDodgeSol(inRed,inGreen,inBlue,inAlpha,inRed,inGreen,inBlue,inAlpha,
             solRed,solGreen,solBlue,solAlpha,IMAGE_WIDTH,IMAGE_HEIGHT);
  if(!checkImage(studImage,solImage))
  {
    printf("colorDodge correct\n");
  }
  else
  {
    printf("colorDodge incorrect\n");
  }
 
  printf("\nTesting pencilSketch:\n");
  Image *sImage=generateOutput(inputImage);
  Image *tImage=generateOutput(inputImage);
  uint8_t *sRed=sImage->redChannel;
  uint8_t *sGreen=sImage->greenChannel;
  uint8_t *sBlue=sImage->blueChannel;
  uint8_t *sAlpha=sImage->alphaChannel;
  uint8_t *tRed=tImage->redChannel;
  uint8_t *tGreen=tImage->greenChannel;
  uint8_t *tBlue=tImage->blueChannel;
  uint8_t *tAlpha=tImage->alphaChannel;
  pencilSketch(inRed,inGreen,inBlue,inAlpha,tRed,tGreen,tBlue,tAlpha,
               sRed,sGreen,sBlue,sAlpha,studRed,studGreen,studBlue,
               studAlpha,gausFilterSol,radius,IMAGE_WIDTH,IMAGE_HEIGHT,
               gMonoMult);
  pencilSketchSol(inRed,inGreen,inBlue,inAlpha,tRed,tGreen,tBlue,tAlpha,
                  sRed,sGreen,sBlue,sAlpha,solRed,solGreen,solBlue,solAlpha,
                  gausFilterSol,radius,IMAGE_WIDTH,IMAGE_HEIGHT,gMonoMult);
  if(!checkImage(studImage,solImage))
  {
    printf("pencilSketch correct\n");
  }
  else
  {
    printf("pencilSketch incorrect\n");
  }
 
  free(gausFilter);
  free(gausFilterSol);
  freeImage(inputImage);
  freeImage(studImage);
  freeImage(solImage);
  freeImage(sImage);
  freeImage(tImage);
  return 0;
}
 
int checkRadius(int stud,int sol)
{
  if(stud!=sol)
    return -1;
  return 0;
}
 
int checkGausFilter(double *stud,double *sol,int size)
{
  int i;
  for(i=0;i<size;i++)
    if(fabs(sol[i]-stud[i])>.002)
      return -1;
  return 0;
}
 
int checkImage(Image *stud,Image *sol)
{
  uint8_t *studRed=stud->redChannel;
  uint8_t *studGreen=stud->greenChannel;
  uint8_t *studBlue=stud->blueChannel;
  uint8_t *studAlpha=stud->alphaChannel;
  uint8_t *solRed=sol->redChannel;
  uint8_t *solGreen=sol->greenChannel;
  uint8_t *solBlue=sol->blueChannel;
  uint8_t *solAlpha=sol->alphaChannel;
 
  int loc,row,col;
  for(row=0;row<IMAGE_HEIGHT;row++)
    for(col=0;col<IMAGE_WIDTH;col++)
    {
      loc=row*IMAGE_WIDTH+col;
      if(studRed[loc]!=solRed[loc])
        return -1;
      if(studGreen[loc]!=solGreen[loc])
        return -1;
      if(studBlue[loc]!=solBlue[loc])
        return -1;
      if(studAlpha[loc]!=solAlpha[loc])
        return -1;
    }
 
  return 0;
}
 
Image *initializeInput()
{
  int row,col;
  Image *newImage=(Image*)malloc(sizeof(Image));
  newImage->redChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
  newImage->greenChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
  newImage->blueChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
  newImage->alphaChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
 
  for(row=0;row<IMAGE_HEIGHT;row++)
    for(col=0;col<IMAGE_WIDTH;col++)
    {
      newImage->redChannel[row*IMAGE_WIDTH+col]=rand()%256;
      newImage->greenChannel[row*IMAGE_WIDTH+col]=rand()%256;
      newImage->blueChannel[row*IMAGE_WIDTH+col]=rand()%256;
      newImage->alphaChannel[row*IMAGE_WIDTH+col]=255;
    }
  newImage->width=IMAGE_WIDTH;
  newImage->height=IMAGE_HEIGHT;
  double sigma=0.995;
  int radius=getRadiusSol(sigma);
  int size=(2*radius+1)*(2*radius+1);
  double *gausFilterSol=(double*)malloc(sizeof(double)*size);
  calculateGausFilterSol(gausFilterSol,sigma);
 
  Image *newImageOut=(Image*)malloc(sizeof(Image));
  newImageOut->redChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
  newImageOut->greenChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
  newImageOut->blueChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
  newImageOut->alphaChannel=(uint8_t*)malloc(sizeof(uint8_t)*IMAGE_HEIGHT*IMAGE_WIDTH);
 
  uint8_t *inRed=newImage->redChannel;
  uint8_t *inGreen=newImage->greenChannel;
  uint8_t *inBlue=newImage->blueChannel;
  uint8_t *inAlpha=newImage->alphaChannel;
  uint8_t *outRed=newImageOut->redChannel;
  uint8_t *outGreen=newImageOut->greenChannel;
  uint8_t *outBlue=newImageOut->blueChannel;
  uint8_t *outAlpha=newImageOut->alphaChannel;
  newImageOut->width=IMAGE_WIDTH;
  newImageOut->height=IMAGE_HEIGHT;
   
convolveImageSol(inRed,inGreen,inBlue,inAlpha,outRed,outGreen,outBlue,
                   outAlpha,gausFilterSol,radius,IMAGE_WIDTH,IMAGE_HEIGHT);
  freeImage(newImage);
  return newImageOut;
}
 
double imageError(Image *stud,Image *sol)
{
  uint8_t *studRed=stud->redChannel;
  uint8_t *studGreen=stud->greenChannel;
  uint8_t *studBlue=stud->blueChannel;
  uint8_t *solRed=sol->redChannel;
  uint8_t *solGreen=sol->greenChannel;
  uint8_t *solBlue=sol->blueChannel;
   
  double power = 0;/*solution image power*/
  double error = 0;/*error power*/
  int loc,row,col;
  double npix = IMAGE_HEIGHT*IMAGE_WIDTH;
  for(row=0;row<IMAGE_HEIGHT;row++){
    for(col=0;col<IMAGE_WIDTH;col++)
    {
      loc=row*IMAGE_WIDTH+col;
      power = power + (1.0/npix)*(pow((double)solRed[loc],2.0) + pow((double)solGreen[loc],2.0) + pow((double)solBlue[loc],2.0));
      error = error + (1.0/npix)*(pow((double)solRed[loc]-(double)studRed[loc],2.0)+pow((double)solGreen[loc]-(double)studGreen[loc],2.0)+pow((double)solBlue[loc]-(double)studBlue[loc],2.0));
    }
   }
  return error/power;/*return error to signal ratio, want less than 1%*/
}
