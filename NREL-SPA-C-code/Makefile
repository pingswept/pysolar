
SHELL = /bin/sh

# V=0 quiet, V=1 verbose.  other values don't work.
V = 0
Q1 = $(V:1=)
Q = $(Q1:0=@)
ECHO1 = $(V:1=@:)
all: spa solpos
spa: spa_tester.c spa.c
	gcc -o spa_tester spa_tester.c spa.c -I.

solpos: stest00.c solpos.c
	gcc -o stest00 stest00.c solpos.c -I.
