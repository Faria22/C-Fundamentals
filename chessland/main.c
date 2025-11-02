#include <stdio.h>
#include <stdlib.h>

#define DEFAULT_CAP 10

// Some typedefs to make life easier
typedef struct Piece Piece;
typedef struct List List;
typedef struct intList intList;
typedef struct Board Board;

// Our structs
struct Piece {
  int rank, file, ind;
};

struct List {
  int identifier;
  Piece **arr;
  int size, cap;
};

struct intList {
  int *arr;
  int size, cap;
};

struct Board {
  List **ranks, **files;
  int num_ranks, num_files;
};

// Prototypes
Board *create_board();
List *create_list(int);
intList *create_int_list();
Piece *create_piece(int, int, int);
void destroy_board(Board *);
void destroy_list(List *);
void destroy_list_without_pieces(List *list);
void destroy_int_list(intList *);
void destroy_piece(Piece *);
void add_piece_to_list(List *, Piece *);
void add_piece_to_board(Board *, Piece *);
void add_rank_to_board(Board *, List *);
void add_file_to_board(Board *, List *);
void add_piece_to_int_list(intList *, int);
void expand_list(List *);
void expand_int_list(intList *);
List *find_rank(Board *, int);
List *find_file(Board *, int);
void add_attackers_rank(intList *, List *, int);
void add_attackers_file(intList *, List *, int);

int main() {
  Board *board = create_board();
  List *all_pieces = create_list(-1); // List to hold all pieces for easy access

  int num_pieces;
  scanf("%d", &num_pieces);

  for (int ind = 0; ind < num_pieces; ind++) {
    int rank, file;
    scanf("%d %d", &rank, &file);

    Piece *cur_piece = create_piece(ind, rank, file);
    add_piece_to_board(board, cur_piece);
    add_piece_to_list(all_pieces, cur_piece); // Add to all pieces list
  }

  for (int ind = 0; ind < num_pieces; ind++) {
    Piece *cur_piece = all_pieces->arr[ind];
    List *rank = find_rank(board, cur_piece->rank);
    List *file = find_file(board, cur_piece->file);

    intList *attackers = create_int_list();
    if (file != NULL) {
      add_attackers_file(attackers, file, cur_piece->rank);
    }
    if (rank != NULL) {
      add_attackers_rank(attackers, rank, cur_piece->file);
    }

    printf("%d", attackers->size);
    if (attackers->size > 0) {
      for (int att_idx = 0; att_idx < attackers->size; att_idx++) {
        printf(" %d", attackers->arr[att_idx] + 1); // Convert to 1-based index
      }
    }
    printf("\n");
    destroy_int_list(attackers);
  }

  destroy_list(all_pieces);
  destroy_board(board);
  return 0;
}

Board *create_board() {
  Board *board = (Board *)malloc(sizeof(Board));
  board->num_ranks = 0;
  board->num_files = 0;
  board->ranks = NULL;
  board->files = NULL;
  return board;
}

List *create_list(int ind) {
  List *list = (List *)malloc(sizeof(List));
  list->identifier = ind;
  list->size = 0;
  list->cap = DEFAULT_CAP;
  list->arr = (Piece **)malloc(DEFAULT_CAP * sizeof(Piece *));
  return list;
}

intList *create_int_list() {
  intList *list = (intList *)malloc(sizeof(intList));
  list->size = 0;
  list->cap = DEFAULT_CAP;
  list->arr = (int *)malloc(DEFAULT_CAP * sizeof(int));
  return list;
}

Piece *create_piece(int ind, int rank, int file) {
  Piece *piece = (Piece *)malloc(sizeof(Piece));

  piece->ind = ind;
  piece->rank = rank;
  piece->file = file;

  return piece;
}

void destroy_board(Board *board) {
  for (int rank_idx = 0; rank_idx < board->num_ranks; rank_idx++) {
    destroy_list_without_pieces(board->ranks[rank_idx]);
  }
  for (int file_idx = 0; file_idx < board->num_files; file_idx++) {
    destroy_list_without_pieces(board->files[file_idx]);
  }
  free(board->ranks);
  free(board->files);
  free(board);
}

void destroy_list(List *list) {
  for (int piece_idx = 0; piece_idx < list->size; piece_idx++) {
    destroy_piece(list->arr[piece_idx]);
  }
  free(list->arr);
  free(list);
}

void destroy_list_without_pieces(List *list) {
  free(list->arr);
  free(list);
}

void destroy_int_list(intList *list) {
  free(list->arr);
  free(list);
}

void destroy_piece(Piece *piece) { free(piece); }

void add_piece_to_list(List *list, Piece *piece) {
  if (list->size == list->cap)
    expand_list(list);

  list->arr[list->size] = piece;
  list->size++;
}

void add_piece_to_board(Board *board, Piece *piece) {
  List *rank = find_rank(board, piece->rank);
  List *file = find_file(board, piece->file);

  if (rank == NULL) {
    rank = create_list(piece->rank);
    add_rank_to_board(board, rank);
  }

  if (file == NULL) {
    file = create_list(piece->file);
    add_file_to_board(board, file);
  }

  add_piece_to_list(file, piece);
  add_piece_to_list(rank, piece);
}
void add_rank_to_board(Board *board, List *rank) {
  board->num_ranks++;
  board->ranks =
      (List **)realloc(board->ranks, board->num_ranks * sizeof(List *));
  board->ranks[board->num_ranks - 1] = rank;
}

void add_file_to_board(Board *board, List *file) {
  board->num_files++;
  board->files =
      (List **)realloc(board->files, board->num_files * sizeof(List *));
  board->files[board->num_files - 1] = file;
}

void add_piece_to_int_list(intList *list, int piece_idx) {
  if (list->size == list->cap)
    expand_int_list(list);

  list->arr[list->size] = piece_idx;
  list->size++;
}

void expand_list(List *list) {
  list->cap *= 2;
  list->arr = (Piece **)realloc(list->arr, list->cap * sizeof(Piece *));
}

void expand_int_list(intList *list) {
  list->cap *= 2;
  list->arr = (int *)realloc(list->arr, list->cap * sizeof(int));
}

List *find_rank(Board *board, int idx) {
  for (int rank_idx = 0; rank_idx < board->num_ranks; rank_idx++) {
    if (board->ranks[rank_idx]->identifier == idx)
      return board->ranks[rank_idx];
  }
  return NULL;
}

List *find_file(Board *board, int idx) {
  for (int file_idx = 0; file_idx < board->num_files; file_idx++) {
    if (board->files[file_idx]->identifier == idx)
      return board->files[file_idx];
  }
  return NULL;
}

void add_attackers_file(intList *attackers, List *file_list,
                        int attacked_rank) {
  Piece *bellow_piece = NULL;
  Piece *above_piece = NULL;
  for (int piece_idx = 0; piece_idx < file_list->size; piece_idx++) {
    Piece *piece = file_list->arr[piece_idx];

    if (piece->rank == attacked_rank)
      continue;

    if (piece->rank < attacked_rank) {
      if (bellow_piece == NULL || piece->rank > bellow_piece->rank) {
        bellow_piece = piece;
      }
    } else {
      if (above_piece == NULL || piece->rank < above_piece->rank) {
        above_piece = piece;
      }
    }
  }

  if (bellow_piece != NULL)
    add_piece_to_int_list(attackers, bellow_piece->ind);
  if (above_piece != NULL)
    add_piece_to_int_list(attackers, above_piece->ind);
}

void add_attackers_rank(intList *attackers, List *rank_list,
                        int attacked_file) {
  Piece *left_piece = NULL;
  Piece *right_piece = NULL;
  for (int piece_idx = 0; piece_idx < rank_list->size; piece_idx++) {
    Piece *piece = rank_list->arr[piece_idx];

    if (piece->file == attacked_file)
      continue;

    if (piece->file < attacked_file) {
      if (left_piece == NULL || piece->file > left_piece->file) {
        left_piece = piece;
      }
    } else {
      if (right_piece == NULL || piece->file < right_piece->file) {
        right_piece = piece;
      }
    }
  }

  if (left_piece != NULL)
    add_piece_to_int_list(attackers, left_piece->ind);
  if (right_piece != NULL)
    add_piece_to_int_list(attackers, right_piece->ind);
}
