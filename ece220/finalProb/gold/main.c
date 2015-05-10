#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "database.h"

// FUNCTION DEFINITIONS
void readInPerson(char * line, person * thisPerson);
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

    char buffer[100];
    int i, personCount = 0;
    db database;

    // make sure input string is a valid file
    FILE * fp = fopen(fileName, "r");
    if (fp == NULL)
        return -1;

    // read the name of the database
    if (fgets(buffer, 100, fp) != NULL)
    {   
        database.name = (char *) malloc(sizeof(char) * (strlen(buffer) + 1)); 
        strcpy(database.name, buffer);
    }
    // count the number of people that appear
    while (fgets(buffer, 100, fp) != NULL)
        personCount++;

    // allocate space for array of people
    database.numPeople = personCount;
    database.people = (person *) malloc(sizeof(person) * personCount);
    
    // return to top of file and skip first line
    fseek(fp, 0, SEEK_SET);
    fgets(buffer, 100, fp);
   
    // read people into people array 
    for (i = 0; i < personCount; i++)
    {
        fgets(buffer, 100, fp);
        readInPerson(buffer, &database.people[i]);
    }
   
    // close file pointer 
    fclose(fp);

    // print database
    printDatabase(&database);

    // free each person's name and info
    for(i = 0; i < personCount; i++)
    {
        free(database.people[i].name);
        free(database.people[i].info);
    }
    // free the array of people
    free(database.name);
    free(database.people);
 
    return 0;
}

// given a line reads in the person information and sets
// a person struct pointed to by thisPerson
void readInPerson(char * line, person * thisPerson)
{
    if (line == NULL || line[0] == '\0')
        return;
    
    int index = 0;
    int infoStart = 0;
    while(line[index] != '\0')
    {
        if (line[index] == ' ')
        {
            line[index] = '\0';
            infoStart = index + 1;
            thisPerson->name = (char *) malloc(sizeof(char) * (index + 1));
            strcpy(thisPerson->name, line);
        }
        index++;
    }
    thisPerson->info = (char *) malloc(sizeof(char) * (index - infoStart + 1));
    strcpy(thisPerson->info, &line[infoStart]);
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
