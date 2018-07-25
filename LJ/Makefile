.PHONY: default lib clean
CC = gcc

LD = $(CC)

SOURCE = $(wildcard *.c)
OBJECTS = $(patsubst %.c, %.o, $(SOURCE))

FLAGS = -O$(O) -lm -std=gnu99

default: forces.so

%.o: %.c
	$(CC) $(FLAGS) -c -fPIC $^

forces.so: $(OBJECTS)
	$(CC) -shared $^ -o forces.so

clean:
	rm -rfv $(OBJECTS) forces.so
