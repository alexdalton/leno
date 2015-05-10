// defines the structure of a person
// name is a string containing the person's name 
// info is a string containing the person's info
typedef struct person_t {
    char * name;
    char * info; 
} person;

// defines the structure of a database
// name is a string containing the database's name
// numPeople is the number of people that appear in the database
// people is the array of persons
typedef struct db_t {
    char * name;
    int numPeople;
    person * people;
} db;
