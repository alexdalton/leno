#include <stdio.h>
#include <stdlib.h>

 
int findLargest(int ** pyramid, int height, int curDepth, int x, int y);
void printTriangle(int ** pyramid, int height);

int main(int argc, char **argv)
{
    FILE *in;
    int height;
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
    fscanf(in, "%d", &height);
    int ** pyramid = (int **) malloc(height * sizeof(int*));
    int i;
    for (i = 0; i < height; i++)
    {
        pyramid[i] = (int *) malloc((i + 1) * sizeof(int));
    }

    int row = 0;
    int col = 0;
    int value; 
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

    printf("%d\n", findLargest(pyramid, height, 1, 0, 0));

    for (i = 0; i < height; i ++)
    {
        free(pyramid[i]);
    }
    free(pyramid);
    return 0;
}

void printTriangle(int ** pyramid, int height)
{
    int i, j;
    for (i = 0; i < height; i++)
    {
        for(j = 0; j < i + 1; j++)
        {
            printf("%d ", pyramid[i][j]);
        }
        printf("\n");
    }
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
