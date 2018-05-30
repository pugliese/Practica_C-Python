.PHONY: default lib clean
CC = gcc

LD = $(CC)

SOURCE = $(wildcard *.c)
OBJECTS = $(patsubst %.c, %.o, $(SOURCE))
LIBRARIES = $(patsubst %.c, %.so, $(SOURCE))


FLAGS = -O$(O) -lm

default: lib

lib: $(LIBRARIES)

%.o: %.c
	$(CC) $(FLAGS) -c -fPIC $^

%.so: %.o
	$(LD) -shared $^ -o $@

clean:
	rm -rfv $(OBJECTS) $(LIBRARIES)
