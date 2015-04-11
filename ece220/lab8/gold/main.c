#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
 
#define PRINT_HIDDEN 0
 
void readDirectory(const char *dirString);
 
int main(int argc,char **argv)
{
  if(argc!=2)
  {
    printf("Usage: ./ls <directory>\n");
  }
 
  readDirectory(argv[1]);
 
  return 0;
}
 
void readDirectory(const char *dirString)
{
  DIR* dir; 
  struct dirent *entry;
  dir=opendir(dirString);
  if(dir==NULL)
  {
    fprintf(stderr,"ls: cannot access %s: No such file or directory\n",
      dirString);
    exit(EXIT_FAILURE);
  }
 
  while((entry=readdir(dir))!=NULL)
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
 
  closedir(dir);
}
