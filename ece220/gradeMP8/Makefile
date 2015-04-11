CC=gcc
CFLAGS= -g -Wall -Werror -Wextra

test: test.o maze.o
	$(CC) $(CFLAGS) test.o maze.o -o testMP8

mp8: main.o maze.o
	$(CC) $(CFLAGS) main.o maze.o -o mp8

test.o: test.c
	$(CC) $(CFLAGS) -c test.c

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

maze.o: maze.c
	$(CC) $(CLFAGS) -c maze.c

clean:
	rm -f *.o mp8 test
