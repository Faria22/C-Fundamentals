#include <stdio.h>

void guess(int number);
static inline int max(int a, int b);
static inline int min(int a, int b);

int main() {
  int n;
  scanf("%d", &n);
  char line[10];
  fgets(line, 10, stdin); // remove the new line character

  int low = 1, high = n;
  int prev_guess = 0;
  while (low <= high) {
    int mid = (low + high) / 2;
    mid = mid == prev_guess ? max((mid + high) / 2, mid + 1)
                            : mid; // Avoid repeating the same guess
    guess(mid);

    scanf("%s", line);
    if (line[0] == 'Y') // Correct guess
      return 0;
    if (line[0] == 'G') // Too many guesses or guess was out of bounds
      return 0;

    if (!prev_guess) { // First guess case
      // Guess upper half
      prev_guess = mid;
      mid = (mid + high) / 2;
      guess(mid);
      scanf("%s", line);
    }

    int new_edge = (mid + prev_guess) / 2;

    scanf("%s", line); // Get's the warmer/colder response
    switch (line[0]) {
      case 'N': // No change
        // Correct number is exactly between prev_guess and mid
        low = new_edge;
        if (mid % 2 != prev_guess % 2) // Adjust for integer division
          low += 1;
        high = low;
        break;
      case 'W': // Warmer
        if (mid < prev_guess) {
          high = min(high - 1, new_edge);
        } else {
          low = max(low + 1, new_edge);
        }
        break;
      case 'C': // Colder
        if (mid < prev_guess) {
          low = max(low + 1, new_edge);
        } else {
          high = min(high - 1, new_edge);
        }
        break;
      default:
        return 0; // Invalid response
    }

    prev_guess = mid;
  }

  return 0;
}

void guess(int number) {
  printf("%d\n", number);
  fflush(stdout);
}

static inline int max(int a, int b) { return a > b ? a : b; }

static inline int min(int a, int b) { return a < b ? a : b; }
