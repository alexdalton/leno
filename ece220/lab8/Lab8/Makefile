C=g++
CFLAGS=-c -g -w

all: ls

ls: main.o
	$(CC) main.o -o ls

main.o: main.c
	$(CC) $(CFLAGS) main.c

clean:
	rm main.o ls

