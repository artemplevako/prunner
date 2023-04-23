#include <stdio.h>
#include <time.h>

int main()
{
    double duration = 5 * 60;
    time_t start = time(NULL);
    while (difftime(time(NULL), start) < duration);
    puts("Process has finished execution");
    return 0;
}
