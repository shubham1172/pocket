#include <stdio.h>
#include <stdlib.h>
#define MEGABYTE 1 << 20

int main(int argc, char* argv[]) 
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <num_mega_bytes>\n", argv[0]);
        return -1;
    }

    int num_mega_bytes = atoi(argv[1]);
    void *memory = malloc(num_mega_bytes);

    if (memory == NULL)
    {
        fprintf(stderr, "Error allocating %d MB of memory", num_mega_bytes);
        return -1;
    }

    printf("Allocated %d MB of memory\n", num_mega_bytes);

    return 0;
}