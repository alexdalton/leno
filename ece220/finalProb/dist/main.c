#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "database.h"

// FUNCTION DEFINITIONS
void printDatabase(db * db);


int main(int argc, char ** argv)
{
    // check number of arguments
    if (argc < 2)
    {
        printf("Must provide text file as argument\n");
        return -1;
    }

    // fileName is a string containing the input file name
    const char * fileName = argv[1];

    // INSERT YOUR CODE HERE
    return 0;
}


// Given a pointer to a database prints the contents
// DO NOT CHANGE, what you print to console will be used for grading
void printDatabase(db * db)
{
    int i;
    printf("name: %s", db->name);
    printf("numPeople: %d\n", db->numPeople);
    for (i = 0; i < db->numPeople; i++)
    {
        printf("person %d:\n", i);
        printf("    name: %s\n    info: %s",
               db->people[i].name, db->people[i].info);
    }
}
