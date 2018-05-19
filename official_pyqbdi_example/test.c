#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    char str[100] = {};
    while(~scanf("%s", str))
    {
        puts(str);
    }
    return 0;
}
