#include <stdio.h>
#include <stdlib.h>
#include "maze.h"

int countSurroundingPath(maze_t * maze, int x, int y)
{
    int left = 0, right = 0, down = 0, up = 0;
    if ((x - 1) >= 0)
    {   
        left = (maze->cells[y][x - 1] == PATH) || (maze->cells[y][x - 1] == START) || (maze->cells[y][x - 1] == END);
    }   
    if ((x + 1) < maze->width)
    {   
        right = (maze->cells[y][x + 1] == PATH) || (maze->cells[y][x + 1] == START) || (maze->cells[y][x + 1] == END);
    }   
    if ((y - 1) >= 0)
    {   
        down = (maze->cells[y - 1][x] == PATH) || (maze->cells[y - 1][x] == START) || (maze->cells[y - 1][x] == END);
    }   
    if ((y + 1) < maze->height)
    {   
        up = (maze->cells[y + 1][x] == PATH) || (maze->cells[y + 1][x] == START) || (maze->cells[y + 1][x] == END);
    }   
    return left + right + down + up; 
}

int checkMaze(maze_t * maze)
{
    int i, j;
    for (i = 0; i < maze->height; i++)
    {   
        for (j = 0; j < maze->width; j++)
        {
            if (maze->cells[i][j] == START || maze->cells[i][j] == END) {
                if (countSurroundingPath(maze, j, i) != 1)
                    return 0;
            }
            if (maze->cells[i][j] == PATH) {
                if (countSurroundingPath(maze, j, i) != 2)
                    return 0;
            }
        }
    }   
    return 1;
}

maze_t * createMazeGold(char * fileName)
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

void destroyMazeGold(maze_t * maze)
{
    int i;
    for(i = 0; i < maze->height; i++)
    {   
        free(maze->cells[i]);
    }   
    free(maze->cells);
    free(maze);
}

void printMazeGold(maze_t * maze)
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

int manhattanGold(int col, int row, maze_t * maze)
{
    int xDist = col - maze->endColumn;
    int yDist = row - maze->endRow;
    if (xDist < 0) xDist *= -1;
    if (yDist < 0) yDist *= -1;
    return xDist + yDist;
}

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

    int leftDist = manhattanGold(col - 1, row, maze);
    int rightDist = manhattanGold(col + 1, row, maze);
    int upDist = manhattanGold(col, row - 1, maze);
    int downDist = manhattanGold(col, row + 1, maze);

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

int test0()
{           
    maze_t * their_maze0 = createMaze("test2.txt");
    maze_t * our_maze0 = createMazeGold("test2.txt");
    int total = 0;
    printf("Testing createMaze (20 pts total)\n");
    if (their_maze0->width == our_maze0->width &&
        their_maze0->height == our_maze0->height)
    {
        printf("    Correct width and height: +2\n");
        total += 2;
    }
    if (their_maze0->startColumn == our_maze0->startColumn &&
        their_maze0->startRow == our_maze0->startRow)
    {
        printf("    Correct start location: +4\n");
        total += 4; 
    }
            if (their_maze0->endColumn == our_maze0->endColumn &&
                their_maze0->endRow == our_maze0->endRow)
            {
                printf("    Correct end location: +4\n");
                total += 4;
            }
            correct = 1;
            for(i = 0; i < our_maze0->height; i++)
            {
                for(j = 0; j < our_maze0->width; j++)
                {
                    if(our_maze0->cells[i][j] != their_maze0->cells[i][j])
                        correct = 0;              
                }
            }
            if(correct)
            {
                printf("    Cells correctly set: +10\n");
                total += 10;
            }
            printf("createMaze score: %d\n", total);
            destroyMazeGold(our_maze0);
            destroyMazeGold(their_maze0);

}

int test1()
{
}

int test2()
{
}

int test3()
{
}
   
int main(int argc, char **argv)
{
    if(argc < 2)
        return 0;

    int testNum = atoi(argv[1]);
    int i, j, total, correct;

    switch(testNum)
    {
        case 0:
            break;
        case 1:
            maze_t * our_maze1 = createMazeGold("test2.txt");
            printf("Testing destroyMaze (10 pts total)\n");
            printf("destroyMaze score: 10 pts if no memory leaks/errors, else 0\n");
            destroyMaze(our_maze1);
            break;
        case 2:
            maze_t * our_maze2 = createMazeGold("test2.txt");
            printf("Testing printMaze (10 pts total)\n");
            printMaze(our_maze2);
            printf("printMaze score: 10 pts if correctly printed, else 0\n");
            destroyMazeGold(our_maze2);
            break;
        case 3:
            total = 0;
            maze_t * test_maze1 = createMazeGold("test1.txt");
            maze_t * test_maze2 = createMazeGold("test2.txt");
            maze_t * test_maze3 = createMazeGold("test3.txt");
            maze_t * original_maze3 = createMazeGold("test3.txt");

            printf("Testing solveMazeManhattan (50 pts total)\n");
            printf("Testing with maze from test1.txt (Simple maze)\n");
            int return1 = solveMazeManhattanDFS(test_maze1, test_maze1->startColumn, test_maze1->startRow);
            if (return1 == 1)
            {
                printf("Correct return value: +2\n"); 
                total += 2;
            }
            if(checkMaze(test_maze1))
            {
                printf("Solution to maze is valid: +10\n");
                total += 10;
            }
            printMazeGold(test_maze1);

            printf("Testing with maze from test2.txt (Complex maze)\n");
            int return2 = solveMazeManhattanDFS(test_maze2, test_maze1->startColumn, test_maze2->startRow);       
            if (return2 == 1)
            {
                printf("Correct return value: +2\n"); 
                total += 2;
            }
            if(checkMaze(test_maze2))
            {
                printf("Solution to maze is valid: +10\n");
                total += 10;
            }
            printMazeGold(test_maze2);
            printf("If solution searches paths following Manhattan heuristic: +14 to total score at end\n"); 


            printf("Testing with maze from test3.txt (Unsolvable maze)\n");
            int return3 = solveMazeManhattanDFS(test_maze3, test_maze1->startColumn, test_maze3->startRow);  
            if (return3 == 0)
            {
                printf("Correct return value: +2\n"); 
                total += 2;
            }
            correct = 1;
            for(i = 0; i < original_maze3->height; i++)
            {
                for(j = 0; j < original_maze3->width; j++)
                {
                    if(original_maze3->cells[i][j] == EMPTY && test_maze3->cells[i][j] != VISITED)
                        correct = 0;
                }
            }
            if(correct)
            {
                printf("All empty cells visisted during search: +10\n");
                total += 10;
            }
            printMazeGold(test_maze3);

            printf("solveMazeManhattanDFS score: %d + ?\n", total);
            
            destroyMazeGold(test_maze1);     
            destroyMazeGold(test_maze2);     
            destroyMazeGold(test_maze3);     
            destroyMazeGold(original_maze3);     
            break;
    } 

    return 0;
}
