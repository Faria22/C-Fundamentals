#include <stdio.h>
#include <stdlib.h>

typedef struct Node Node;

struct Node {
  int is_table;
  int val; // table number or skill value
  Node *left, *right;
};

int added = 0; // keeps track if a player was added or not

Node *add_table(Node *head, int val);
Node *add_player(Node *head, int val);
Node *create_node(int val);
long int calculate_excitement(Node *head);
void destroy_node(Node *head);
int max(int a, int b);
int abs(int a);

int main() {
  int num_players;
  scanf("%d", &num_players);

  int tables[num_players - 1];
  for (int idx = 0; idx < num_players - 1; idx++) {
    scanf("%d", &tables[idx]);
  }

  Node *head = NULL;
  for (int idx = num_players - 2; idx > -1; idx--) {
    head = add_table(head, tables[idx]);
  }

  int player_skill;
  for (int idx = 0; idx < num_players; idx++) {
    scanf("%d", &player_skill);
    head = add_player(head, player_skill);
    added = 0;
  }

  printf("%ld\n", calculate_excitement(head));

  destroy_node(head);

  return 0;
}

Node *add_table(Node *head, int val) {
  if (!head) {
    head = create_node(val);
    head->is_table = 1;
    return head;
  }

  if (val < head->val) {
    head->left = add_table(head->left, val);
  } else {
    head->right = add_table(head->right, val);
  }

  return head;
}

Node *add_player(Node *head, int skill) {
  if (added) {
    return head;
  }

  if (!head) {
    head = create_node(skill);
    added = 1;
    return head;
  }

  if (head->is_table) {
    head->left = add_player(head->left, skill);
    head->right = add_player(head->right, skill);
  }

  return head;
}

Node *create_node(int val) {
  Node *node = calloc(1, sizeof(Node));
  node->val = val;
  return node;
}

long int calculate_excitement(Node *head) {
  if (!head->is_table)
    return 0;

  long int excitement = 0;
  excitement += calculate_excitement(head->left);
  excitement += calculate_excitement(head->right);

  head->is_table = 0;
  head->val = max(head->right->val, head->left->val);

  return excitement + abs(head->right->val - head->left->val);
}

int abs(int a) { return a > 0 ? a : -a; };

void destroy_node(Node *head) {
  if (!head)
    return;

  destroy_node(head->left);
  destroy_node(head->right);

  free(head);
}

int max(int a, int b) { return a > b ? a : b; };
