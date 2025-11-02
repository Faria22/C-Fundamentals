#include <stdio.h>

int end_of_word(char c);

int main() {
  int num_lines;
  scanf("%d", &num_lines);

  char current_char, previous_char;
  scanf("%c", &current_char); // to consume the newline after the number input

  for (int line_idx = 1; line_idx <= num_lines; line_idx++) {
    current_char = ' ';
    previous_char = ' ';

    int cur_char_idx = 0;
    int last_added_char_idx = -1;
    while (current_char != '\n') {
      scanf("%c", &current_char);
      if (end_of_word(current_char)) {
        if (!end_of_word(previous_char) &&
            last_added_char_idx != cur_char_idx - 1) {
          printf("%c", previous_char);
          last_added_char_idx = cur_char_idx - 1;
        }
      } else {
        if (end_of_word(previous_char)) {
          printf("%c", current_char);
          last_added_char_idx = cur_char_idx;
        }
      }

      previous_char = current_char;
      cur_char_idx++;
    }
    printf("\n");
  }

  return 0;
}

int end_of_word(char c) { return c == ' ' || c == '\n'; }
