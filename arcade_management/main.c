#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LENGTH 21 // Including null terminator

typedef struct Node Node;
typedef struct Stack Stack;

struct Node {
  char name[MAX_NAME_LENGTH];
  int money;
  Node *next;
};

struct Stack {
  Node *head;
};

Stack *create_stack();
void add_player_to_stack(Stack *stack, char name[MAX_NAME_LENGTH], int money);
Node *top(Stack *stack);
void pop(Stack *stack);
void destroy_stack(Stack *stack);

int main() {
  Stack *stack = create_stack();

  int ans;
  do {
    scanf("%d", &ans);
    if (ans == 1) {
      char name[MAX_NAME_LENGTH];
      int money;
      scanf("%d %s", &money, name);

      Node *most_valuable_player = top(stack);
      int max_money;
      if (!most_valuable_player) { // Case if stack is empty
        max_money = 0;
      } else {
        max_money = most_valuable_player->money;
      }

      if (money >= max_money) {
        add_player_to_stack(stack, name, money);
      } else {
        add_player_to_stack(stack, most_valuable_player->name, max_money);
      }
    } else if (ans == 2) {
      pop(stack);
    } else if (ans == 3) {
      printf("%s\n", top(stack)->name);
    }
  } while (ans);

  destroy_stack(stack);

  return 0;
}

Stack *create_stack() {
  Stack *stack = calloc(1, sizeof(Stack));
  stack->head = NULL;
  return stack;
}
void add_player_to_stack(Stack *stack, char name[MAX_NAME_LENGTH], int money) {
  Node *player = calloc(1, sizeof(Node));
  strcpy(player->name, name);
  player->money = money;
  player->next = top(stack);
  stack->head = player;
}

Node *top(Stack *stack) { return stack->head; }
void pop(Stack *stack) {
  Node *head = stack->head;
  if (head) {
    stack->head = head->next;
    free(head);
  }
}
void destroy_stack(Stack *stack) {
  while (stack->head) {
    pop(stack);
  }
  free(stack);
}
