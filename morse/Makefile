.PHONY: default lib clean
CC = gcc

LD = $(CC)

SOURCE = $(wildcard *.c)
SOURCE_FOR = $(wildcard forces/*.c)
OBJECTS = $(patsubst %.c, %.o, $(SOURCE))
OBJECTS_FOR = $(patsubst %.c, %.o, $(SOURCE_FOR))
LIBRARIES = $(patsubst %.c, %.so, $(SOURCE))

FLAGS = -O$(O) -lm -std=gnu99

default: forces.so

lib: $(LIBRARIES)

%.o: %.c
	$(CC) $(FLAGS) -c -fPIC $^ -o $@

forces.so: $(OBJECTS_FOR)
	$(CC) -shared $^ -o forces.so

%.so: %.o
	$(LD) -shared $^ -o $@

clean:
	rm -rfv $(OBJECTS) $(OBJECTS_FOR) $(LIBRARIES) forces.so
