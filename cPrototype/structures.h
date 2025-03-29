#ifndef declarations
#define declarations

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct word
{
    char id;
    char cost;
    char name[100];
    char category;
} Tword;

extern Tword words[60];

#endif