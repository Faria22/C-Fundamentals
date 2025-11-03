#include <stdbool.h>
#include <stdio.h>
#include <string.h>

static void consume_line(void) {
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF) {
        continue;
    }
}

static bool read_response(char *buffer, size_t size) {
    while (fgets(buffer, (int)size, stdin) != NULL) {
        size_t len = strlen(buffer);
        while (len > 0 && (buffer[len - 1] == '\n' || buffer[len - 1] == '\r')) {
            buffer[--len] = '\0';
        }
        if (len == 0) {
            continue;
        }
        return true;
    }
    return false;
}

static void submit_guess(long long guess) {
    printf("%lld\n", guess);
    fflush(stdout);
}

static long long choose_next_guess(long long lo, long long hi, long long prev_guess, long long max_value) {
    if (lo == hi) {
        return lo;
    }
    long long guess;
    if (prev_guess <= lo) {
        guess = hi;
    } else if (prev_guess >= hi) {
        guess = lo;
    } else {
        long long left_span = prev_guess - lo;
        long long right_span = hi - prev_guess;
        guess = (right_span >= left_span) ? hi : lo;
    }

    if (guess == prev_guess) {
        if (guess < hi) {
            guess += 1;
        } else if (guess > lo) {
            guess -= 1;
        }
    }

    if (guess < 1) {
        guess = 1;
    }
    if (guess > max_value) {
        guess = max_value;
    }
    return guess;
}

int main(void) {
    long long max_value;
    if (scanf("%lld", &max_value) != 1) {
        return 0;
    }
    consume_line();

    long long lo = 1;
    long long hi = max_value;
    long long prev_guess = -1;
    char response[128];

    while (true) {
        long long guess = (prev_guess == -1) ? lo : choose_next_guess(lo, hi, prev_guess, max_value);
        submit_guess(guess);

        if (!read_response(response, sizeof response)) {
            return 0;
        }
        if (response[0] == 'Y' || response[0] == 'G') {
            return 0;
        }

        if (prev_guess == -1) {
            prev_guess = guess;
            continue;
        }

        bool warmer = strstr(response, "Warmer.") != NULL;
        bool colder = strstr(response, "Colder.") != NULL;
        bool same = strstr(response, "No change.") != NULL;

        long long sum = prev_guess + guess;
        long long half = sum / 2;

        if (same) {
            lo = hi = half;
        } else if (warmer) {
            if (prev_guess < guess) {
                long long candidate = half + 1;
                if (candidate > lo) {
                    lo = candidate;
                }
            } else if (prev_guess > guess) {
                long long candidate = (sum - 1) / 2;
                if (candidate < hi) {
                    hi = candidate;
                }
            }
        } else if (colder) {
            if (prev_guess < guess) {
                if (half < hi) {
                    hi = half;
                }
            } else if (prev_guess > guess) {
                long long candidate = half + 1;
                if (candidate > lo) {
                    lo = candidate;
                }
            }
        }

        if (lo < 1) {
            lo = 1;
        }
        if (hi > max_value) {
            hi = max_value;
        }
        if (lo > hi) {
            lo = hi = guess;
        }

        prev_guess = guess;
    }
}
