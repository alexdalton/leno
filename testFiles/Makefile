CC=gcc
CFLAGS=-Wall -Wextra

grader: grader.o maze.o
	$(CC) $(CFLAGS) grader.o maze.o -o grader

grader.o: grader.c
	$(CC) $(CFLAGS) -c grader.c

maze.o: maze.c
	$(CC) $(CFLAGS) -c maze.c

clean:
	rm -f maze.o grader.o grader
