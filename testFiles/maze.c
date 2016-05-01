#include <stdio.h>
#include <stdlib.h>
#include "maze.h"


maze_t * createMaze(char * fileName)
{
    FILE * in = fopen(fileName, "r");
    int i, x = 0, y =0;
    char c;

    maze_t * maze = (maze_t *) malloc(sizeof(maze_t));
    fscanf(in, "%d %d\n", &(maze->width), &(maze->height));
    maze->startColumn = 0;
    maze->startRow = 0;
    maze->endColumn = maze->width;
    maze->endRow = maze->height;

    maze->cells = (char **) malloc(maze->height * sizeof(char *));
    for(i = 0; i < maze->height; i++)
    {
        maze->cells[i] = (char *) malloc(maze->width * sizeof(char));
    }

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
            maze->cells[y][x] = c;
            if(c == START)
            {
                maze->startColumn = x;
                maze->startRow = y;
            }
            else if(c == END)
            {
                maze->endColumn = x;
                maze->endRow = y;
            }
            x++;
        }
    }
    fclose(in);

    return maze;
}

void destroyMaze(maze_t * maze)
{
    int i;
    for(i = 0; i < maze->height; i++)
    {
        free(maze->cells[i]);
    }
    free(maze->cells);
    free(maze);
}


/*
 * printMaze -- prints out the maze in a human readable format (should look like examples)
 * INPUTS:      maze -- pointer to maze structure that contains all necessary information 
 *              width -- width of the maze
 *              height -- height of the maze
 * OUTPUTS:     none
 * RETURN:      none
 * SIDE EFFECTS: prints the maze to the console
 */
void printMaze(maze_t * maze)
{
    int i, j;
    for(i = 0; i < maze->height; i++)
    {
        for(j = 0; j < maze->width; j++)
        {
            printf("%c", maze->cells[i][j]);
        }
        printf("\n");
    }
}

int manhattan(int col, int row, maze_t * maze)
{
    int xDist = col - maze->endColumn;
    int yDist = row - maze->endRow;
    if (xDist < 0) xDist *= -1;
    if (yDist < 0) yDist *= -1;
    return xDist + yDist;
}

/*
 * solveMazeManhattanDFS -- recursively solves the maze using depth first search and a manhattan distance heuristic
 * INPUTS:               maze -- pointer to maze structure with all necessary maze information
 *                       col -- the column of the cell currently beinging visited within the maze
 *                       row -- the row of the cell currently being visited within the maze
 * OUTPUTS:              updates maze with the solution path ('.') and visited nodes ('~')
 * RETURNS:              0 if the maze is unsolvable, 1 if it is solved
 * SIDE EFFECTS:         none
 */ 
int solveMazeManhattanDFS(maze_t * maze, int col, int row)
{
    if (col < 0 || col >= maze->width || row < 0 || row >= maze->height)
        return 0;
    if (maze->cells[row][col] == WALL || maze->cells[row][col] == PATH || maze->cells[row][col] == VISITED)
        return 0;
    if (maze->cells[row][col] == END)
        return 1;
 
    int start = 0;
    if (maze->cells[row][col] == START)
        start = 1;
 
    maze->cells[row][col] = PATH;

    int leftDist = manhattan(col - 1, row, maze);
    int rightDist = manhattan(col + 1, row, maze);
    int upDist = manhattan(col, row - 1, maze);
    int downDist = manhattan(col, row + 1, maze);

    int i;
    for(i = 0; i < 4; i++) 
    {
        if (leftDist <= rightDist && leftDist <= upDist && leftDist <= downDist) 
        {
            if (solveMazeManhattanDFS(maze, col - 1, row))
            {
                if (start)
                    maze->cells[row][col] = START;
                return 1;    
            }
            leftDist = 1000000;
        }
        if (downDist <= upDist && downDist <= leftDist && downDist <= rightDist)
        {
            if (solveMazeManhattanDFS(maze, col, row + 1))
            {
                if (start)
                    maze->cells[row][col] = START;
                return 1;    
            }
            downDist = 1000000;
        }
        if (rightDist <= leftDist && rightDist <= upDist && rightDist <= downDist)
        {            
            if (solveMazeManhattanDFS(maze, col + 1, row))
            {
                if (start)
                    maze->cells[row][col] = START;
                return 1;    
            }
            rightDist = 1000000;
        }
        if (upDist <= leftDist && upDist <= rightDist && upDist <= downDist)
        {
            if (solveMazeManhattanDFS(maze, col, row - 1))
            {
                if (start)
                    maze->cells[row][col] = START;
                return 1;    
            }
            upDist = 1000000;
        }
    }
 
    if (start)
        maze->cells[row][col] = START;
    else
        maze->cells[row][col] = VISITED;
 
    return 0;
}
