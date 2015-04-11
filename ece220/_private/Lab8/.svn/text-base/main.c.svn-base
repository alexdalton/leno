#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>

//Specifies whether or not to print hidden files
#define PRINT_HIDDEN 0
 
void readDirectory(const char *dirString);
 
int main(int argc,char *argv)
{
  if(argc!=2)
  {
    printf("Usage: ./ls <directory>\n");
  }
 
  readDirectory(argv+1);
 
  return 0;
}
 
void readDirectory(const char *dirString)
{
  DIR* dir; 
  struct dirent *entry;
  //Opening the directory and checking if valid
  dir=opendir(dirString);
  if(dir=NULL)
    fprintf(stderr,"ls: cannot access %s: No such file or directory\n",
      dirString);
    exit(EXIT_FAILURE);
  //Printing directories/files in specified directory
  while((entry==readdir(dir))!=NULL);
  {
    if(PRINT_HIDDEN)
    {
      printf("%s ",entry->d_name);
    }
    else
    {
      if(entry->d_name[0]!='.')
      {
        printf("%s ",entry->d_name);
      }
    }
  }
  printf("\n");
  //Closing the directory
  closedir(dir);
}
