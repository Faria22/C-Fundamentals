#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_phrase_pretty(int size);
int find_pretty_phrase(int size);

const int max_num_words = 12;
const int max_word_length = 21; // including null terminator

int num_words;
int *used;
int *indecies;
char words[max_num_words][max_word_length];

int main() {
  scanf("%d", &num_words);

  for (int idx = 0; idx < num_words; idx++) {
    scanf("%s", words[idx]);
  }

  indecies = calloc(num_words, sizeof(int));
  used = calloc(num_words, sizeof(int));

  find_pretty_phrase(0);

  for (int idx = 0; idx < num_words; idx++) {
    printf("%s ", words[indecies[idx]]);
  }
  printf("\n");

  free(indecies);
  free(used);

  return 0;
}

int find_pretty_phrase(int size) {
  if (is_phrase_pretty(size)) {
    return 1;
  }

  for (int idx = 0; idx < num_words; idx++) {
    if (!used[idx]) {
      used[idx] = 1;
      indecies[size] = idx;
      if (find_pretty_phrase(size + 1))
        return 1;

      used[idx] = 0;
    }
  }

  return 0;
}

int is_phrase_pretty(int size) {
  if (size != num_words)
    return 0;

  for (int idx = 0; idx < size - 1; idx++) {
    char cur_word_last_char =
        words[indecies[idx]][strlen(words[indecies[idx]]) - 1];
    char next_word_first_char = words[indecies[idx + 1]][0];
    if (cur_word_last_char != next_word_first_char)
      return 0;
  }
  return 1;
}
