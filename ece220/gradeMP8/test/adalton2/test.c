#include <stdio.h>
#include <stdlib.h>
#include "maze.h"

void freeMaze(char ** maze, int height);
void myFindStart(char ** maze, int width, int height, int * x, int * y);
void myPrintMaze(char ** maze, int width, int height);
int myCheckMaze(char ** maze, int width, int height, int x, int y, int print); 
int mySolveMazeDFS(char ** maze, int width, int height, int xPos, int yPos);

int main(int argc, char **argv)
{
    int width, height;
    FILE *in;
    // attempt to open input file
    if (argc < 3)
    {
        printf("You need an input file and test to run.\n");
        return -1;
    }
    in = fopen(argv[1], "r");
    if (in == NULL)
    {
        printf("Could not open file: %s\n", argv[1]);
        return -1;
    }
    int mode = atoi(argv[2]);
    fscanf(in, "%d", &width);
    fscanf(in, "%d", &height);
    fgetc(in);
    // allocate memory for 2D array maze
    char ** maze1 = (char **) malloc(height * sizeof(char*));
    char ** maze2 = (char **) malloc(height * sizeof(char*));
    int i;
    for(i = 0; i < height; i++)
    {
        maze1[i] = (char *) malloc(width * sizeof(char));
        maze2[i] = (char *) malloc(width * sizeof(char));
    }
    // read contents of input file into maze
    char c;
    int x = 0, y = 0;
    while ((c = fgetc(in)) != EOF)
    {
        if (c == '\n')
        {
            y++;
            x = 0;
            continue;
        }
        else
        {
            maze1[y][x] = c;
            maze2[y][x] = c;
            x++;
        }
    }
    fclose(in);

    if (mode == 0)
    {
        printf("Test findStart on %s\n", argv[1]);
        int yStart1, xStart1, yStart2, xStart2;
        myFindStart(maze2, width, height, &xStart2, &yStart2);
        findStart(maze1, width, height, &xStart1, &yStart1);
        if ((yStart1 == yStart2) && (xStart1 == xStart2))
            printf("    Score: 5\n");
        else
            printf("    Score: 0\n");
    }
    else if (mode == 1)
    {
        printf("%d %d\n", width, height);
        printMaze(maze1, width, height);
    }
    else if (mode == 2)
    {
        printf("Test solveMazeDFS on %s\n", argv[1]);
        int yStart, xStart;
        int score = 50;
        myFindStart(maze1, width, height, &xStart, &yStart);
        int theirs = solveMazeDFS(maze1, width, height, xStart, yStart);
        int ours = mySolveMazeDFS(maze2, width, height, xStart, yStart);
        if (theirs != ours)
        {
            printf("    -10 points, return value does not match\n");
            score -= 10; 
        }
        if (ours)
            printf("    Score: %d\n", score - myCheckMaze(maze1, width, height, xStart, yStart, 1));
        else
            printf("    Score: %d\n", score);
    }
    else if (mode == 3)
    {
        printf("Test checkMaze on %s\n", argv[1]);
        int yStart, xStart;
        myFindStart(maze1, width, height, &xStart, &yStart);
        int theirs = checkMaze(maze1, width, height, xStart, yStart);
        int ours = myCheckMaze(maze1, width, height, xStart, yStart, 0);
        if ((theirs == 1 && ours == 0) || (theirs == 0 && ours > 0))
            printf("    Score: 5\n");
        else
            printf("    Score: 0\n");
    }
    else if (mode == 4)
    {
        printf("Test solveMazeBFS on %s\n", argv[1]);
        int yStart, xStart;
        int score = 20;
        myFindStart(maze1, width, height, &xStart, &yStart);
        int theirs = solveMazeBFS(maze1, width, height, xStart, yStart);
        int ours = mySolveMazeDFS(maze2, width, height, xStart, yStart);
        if (theirs != ours)
        {
            printf("    -10 points, return value does not match\n");
            score -= 10; 
        }
        if (ours)
            printf("    Score: %d\n", score - myCheckMaze(maze1, width, height, xStart, yStart, 1));
        else
            printf("    Score: %d\n", score);
    }
    freeMaze(maze1, height);
    freeMaze(maze2, height);
    return 0;
}

int mySolveMazeDFS(char ** maze, int width, int height, int xPos, int yPos)
{
    if (xPos < 0 || xPos >= width || yPos < 0 || yPos >= height)
        return 0;
    if (maze[yPos][xPos] == WALL || maze[yPos][xPos] == PATH || maze[yPos][xPos] == VISITED)
        return 0;
    if (maze[yPos][xPos] == END)
        return 1;

    int start = 0;
    if (maze[yPos][xPos] == START)
        start = 1;

    maze[yPos][xPos] = PATH;
    if (solveMazeDFS(maze, width, height, xPos + 1, yPos) ||
        solveMazeDFS(maze, width, height, xPos - 1, yPos) ||
        solveMazeDFS(maze, width, height, xPos, yPos + 1) ||
        solveMazeDFS(maze, width, height, xPos, yPos - 1))
    {
        if (start)
            maze[yPos][xPos] = START;
        return 1;
    }

    if (start)
        maze[yPos][xPos] = START;
    else
        maze[yPos][xPos] = VISITED;

    return 0;
}


void myFindStart(char ** maze, int width, int height, int * x, int * y)
{
    for(*y = 0; *y < height; (*y)++)
    {
        for(*x = 0; *x < width; (*x)++)
        {
            if(maze[*y][*x] == START)
                return;
        }
    }
    *y = -1;
    *x = -1;
}

void myPrintMaze(char ** maze, int width, int height)
{
    int i, j;
    for(i = 0; i < height; i++)
    {
        for(j = 0; j < width; j++)
        {
            printf("%c", maze[i][j]);
        }
        printf("\n");
    }
}

int myCheckMaze(char ** maze, int width, int height, int x, int y, int print)
{
    int startOverwritten = 0;
    int endOverwritten = 0;
    int pathDiverges = 0;
    int startDiverges = 0; 
    int endDiverges = 0;
    if (maze[y][x] != START)
    {
        if (print)
            printf("    -10, start position overwritten\n");
        startOverwritten = 10;
    }
    int i, j;
    int endFound = 0;
    for (i = 0; i < height; i++)
    {
        for(j = 0; j < width; j++)
        {
            if (maze[i][j] == WALL || maze[i][j] == EMPTY || maze[i][j] == VISITED)
                continue;
            else if (maze[i][j] == START)
            {
                int dotCount = 0;
                if (i + 1 < height && maze[i + 1][j] == PATH)
                    dotCount++;
                if (i - 1 > 0 && maze[i - 1][j] == PATH)
                    dotCount++;
                if (j + 1 < width && maze[i][j + 1] == PATH)
                    dotCount++;
                if (j - 1 > 0 && maze[i][j - 1] == PATH)
                    dotCount++;
                if (dotCount != 1)
                {
                    if (print)
                        printf("    -10, multiple or no paths found around start\n");
                    startDiverges = 10;
                }
            }
            else if (maze[i][j] == END)
            {
                int dotCount = 0;
                if (i + 1 < height && maze[i + 1][j] == PATH)
                    dotCount++;
                if (i - 1 > 0 && maze[i - 1][j] == PATH)
                    dotCount++;
                if (j + 1 < width && maze[i][j + 1] == PATH)
                    dotCount++;
                if (j - 1 > 0 && maze[i][j - 1] == PATH)
                    dotCount++;
                if (dotCount != 1)
                {
                    if (print)
                        printf("    -10, multiple or no paths found around end\n");
                    endDiverges = 10;
                }
                endFound = 1;
            }
            else if (maze[i][j] == PATH)
            {
                int dotCount = 0;
                if (i + 1 < height && (maze[i + 1][j] == PATH || maze[i + 1][j] == START || maze[i + 1][j] == END))
                    dotCount++;
                if (i - 1 > 0 && (maze[i - 1][j] == PATH || maze[i - 1][j] == START || maze[i - 1][j] == END))
                    dotCount++;
                if (j + 1 < width && (maze[i][j+1] == PATH || maze[i][j+1] == START || maze[i][j+1] == END))
                    dotCount++;
                if (j - 1 > 0 && (maze[i][j-1] == PATH || maze[i][j-1] == START || maze[i][j-1] == END))
                    dotCount++;
                if (dotCount != 2)
                {
                    if (print)
                        printf("    -50, path branches has a break or reaches a deadend\n");
                    pathDiverges = 50;
                }
            }
        }
    }
    if (endFound == 0)
    {
        if (print)
            printf("    -10, end is overwritten\n");
        endOverwritten = 10;
    }
    return startOverwritten + endOverwritten + startDiverges + endDiverges + pathDiverges;
}

// Frees the memory allocated for maze
void freeMaze(char ** maze, int height)
{
    int i;
    for(i = 0; i < height; i++)
    {
        free(maze[i]);
    }
    free(maze);
}
