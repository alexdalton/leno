#include <stdio.h>
#include <stdlib.h>

 
int findLargest(int ** pyramid, int height, int curDepth, int x, int y);


int main(int argc, char **argv)
{
    FILE *in;
    int height;
    // Try to open file from command line argument
    if (argc < 2)
    {
        printf("You need an input file\n");
        return -1;
    }
    in = fopen(argv[1], "r");
    if (in == NULL)
    {
        printf("Could not open file: %s\n", argv[1]);
        return -1;
    }
    // Read the height of the pyramid into the variable named height
    fscanf(in, "%d", &height);
    // Allocate memory for the 2D array representing the pyramid
    int ** pyramid = (int **) malloc(height * sizeof(int*));
    int i;
    for (i = 0; i < height; i++)
    {
        pyramid[i] = (int *) malloc((i + 1) * sizeof(int));
    }

    int row = 0;
    int col = 0;
    int value; 
    // Fill pyramid in with values from input file
    while (fscanf(in, "%d", &value) != EOF)
    {
        pyramid[row][col++] = value;
        if (col > row)
        {
            col = 0;
            row++;
        }
    }
    fclose(in);

    // pyramid = the 2D array for the pyramid
    // height  = the height of the pyramid
    printf("%d\n", findLargest(pyramid, height, 1, 0, 0));

    // free the memory allocated for the pyramid
    for (i = 0; i < height; i ++)
    {
        free(pyramid[i]);
    }
    free(pyramid);
    return 0;
}


int findLargest(int ** pyramid, int height, int curDepth, int x, int y)
{
    if (curDepth == height)
        return pyramid[y][x];

    int below = findLargest(pyramid, height, curDepth + 1, x, y + 1);
    int belowRight = findLargest(pyramid, height, curDepth + 1, x + 1, y + 1); 
    if (below > belowRight)
        return below + pyramid[y][x];
    else
        return belowRight + pyramid[y][x];
}
