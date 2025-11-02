
#include <stdio.h>
#include <stdlib.h>

#define MAX     1000000000
#define MIN     -1000000000

int main(int argc, char ** argv) {
    int maxValue, lastGuess, numGuesses, target;

    // Try to read in a setup from the arguements
    if (argc > 2) {
        sscanf(argv[1], "%d", &maxValue);
        sscanf(argv[2], "%d", &target);
        if (target > maxValue) {
            target = maxValue;
        }
        if (target < 1) {
            target = 1;
        }
    } else {
        maxValue = 20;
        target = 13;
    }

    // Compute the number of guesses
    numGuesses = 0;
    while ((1<<numGuesses) < maxValue)
        numGuesses++;
    numGuesses = 1 + (numGuesses * 2);

    // Print maximum possible value
    printf("%d\n", maxValue);
    fflush(stdout);

    // Read in the number
    scanf("%d", &lastGuess);

    // Check the bounds on the guess
    if (lastGuess < MIN) {
        printf("Game Over.\n");
        fflush(stdout);
        fprintf(stderr, "Game Over.\n");
        fflush(stderr);
        return 0;
    }
    if (lastGuess > MAX) {
        printf("Game Over.\n");
        fflush(stdout);
        fprintf(stderr, "Game Over.\n");
        fflush(stderr);
        return 0;
    }

    // Check if the first guess was wrong
    if (lastGuess != target) {
        numGuesses--;
        printf("No.\n");
        fprintf(stderr, "No.\n");
        fflush(stdout);
        fflush(stderr);
    } else {
        printf("Yes!!!\n");
        fprintf(stderr, "Yes!!!\n");
        fflush(stdout);
        fflush(stderr);
    }

    // Loop until the guess is correct
    while (lastGuess != target) {
        numGuesses--;

        // Check if they are out of guesses
        if (numGuesses < 0) { 
            printf("Game Over.\n");
            fprintf(stderr, "Game Over.\n");
            fflush(stdout);
            fflush(stderr);
            return 0;
        }    
        
        // read in the current guess
        int curGuess;
        scanf("%d", &curGuess);

        // Check if the guess is correct
        if (curGuess == target) {
            fprintf(stderr, "Yes!!!\n");
            fflush(stderr);
            printf("Yes!!!\n");
            fflush(stdout);
            break;
        }

        // Get the delta
        int lastDelta = target - lastGuess;
        int curDelta = target - curGuess;

        // Do the absolute value
        if (lastDelta < 0) lastDelta = -lastDelta;
        if (curDelta < 0) curDelta = -curDelta;

        // Check which delta is closer
        if (lastDelta < curDelta) {
            fprintf(stderr, "No. Colder.\n");
            fflush(stderr);
            printf("No. Colder.\n");
            fflush(stdout);
        } else if (curDelta < lastDelta) {
            fprintf(stderr, "No. Warmer.\n");
            fflush(stderr);
            printf("No. Warmer.\n");
            fflush(stdout);
        } else {
            fprintf(stderr, "No. No change.\n");
            fflush(stderr);
            printf("No. No change.\n");
            fflush(stdout);
        }

        // Update the guess
        lastGuess = curGuess;
    }

    // Exit the program
    return 0;
}
