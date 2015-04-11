CC=g++
CFLAGS=-g -Wall #-Werror

all: mp6 test gradetest

mp6: main.o lodepng.o imageData.o functions.o
	$(CC) $(CFLAGS) main.o lodepng.o imageData.o functions.o -o mp6

test: test.o lodepng.o imageData.o functions.o solution.o
	$(CC) $(CFLAGS) test.o lodepng.o imageData.o functions.o solution.o -o test

gradetest: gradetest.o lodepng.o imageData.o functions.o solution.o
	$(CC) $(CFLAGS) gradetest.o lodepng.o imageData.o functions.o solution.o -o gradetest

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

lodepng.o: lodepng.c
	$(CC) $(CFLAGS) -c lodepng.c

imageData.o: imageData.c
	$(CC) $(CFLAGS) -c imageData.c

functions.o: functions.c
	$(CC) $(CFLAGS) -c functions.c

test.o: test.c
	$(CC) $(CFLAGS) -c test.c

gradetest.o: gradetest.c
	$(CC) $(CFLAGS) -c gradetest.c

clean:
	rm -f *.o mp6 test gradetest
