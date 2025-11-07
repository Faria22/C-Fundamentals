#include <stdio.h>
#include <stdlib.h>

struct line { // Represents a row or a column
  int num_groups;
  int *groups_size;
};

typedef struct line line;

line *create_line(int num_groups);
int determinable_line(line *line, int max_num_items);
void fill_row(int **grid, int row_idx, line *row);
void fill_col(int **grid, int row_idx, line *row);
int **create_grid();
void destroy_grid(int **grid);
void destroy_line(line *line);
int solve_it(int **grid, int row, int col);
int is_valid(int **grid, int row, int col);
void print_grid(int **grid);

const int empty = -1;
const int red = 0;
const int black = 1;

int num_rows, num_cols;
line **rows, **cols;

int main() {
  scanf("%d %d", &num_rows, &num_cols);
  int **grid = create_grid();
  // print_grid(grid);
  // printf("\n");

  rows = calloc(num_rows, sizeof(line *));
  for (int row_idx = 0; row_idx < num_rows; row_idx++) {
    int num_groups;
    scanf("%d", &num_groups);
    rows[row_idx] = create_line(num_groups);
  }

  cols = calloc(num_cols, sizeof(line *));
  for (int col_idx = 0; col_idx < num_cols; col_idx++) {
    int num_groups;
    scanf("%d", &num_groups);
    cols[col_idx] = create_line(num_groups);
  }

  // Prefill any rows fully determined by their clues
  for (int row_idx = 0; row_idx < num_rows; row_idx++) {
    if (determinable_line(rows[row_idx], num_cols)) {
      fill_row(grid, row_idx, rows[row_idx]);
    }
  }
  // print_grid(grid);
  // printf("\n");
  // Prefill any columns fully determined by their clues
  for (int col_idx = 0; col_idx < num_cols; col_idx++) {
    if (determinable_line(cols[col_idx], num_rows)) {
      fill_col(grid, col_idx, cols[col_idx]);
    }
  }

  // print_grid(grid);
  // printf("\n");

  solve_it(grid, 0, 0);

  print_grid(grid);
  destroy_grid(grid);

  for (int row_idx = 0; row_idx < num_rows; row_idx++) {
    destroy_line(rows[row_idx]);
  }
  free(rows);

  // Do all cols that can be determine alone
  for (int col_idx = 0; col_idx < num_cols; col_idx++) {
    destroy_line(cols[col_idx]);
  }
  free(cols);

  return 0;
}

int solve_it(int **grid, int row, int col) {
  // Traverse the grid in row-major order, trying assignments on each cell
  if (col == num_cols) {
    row++;
    col = 0;
  }

  if (row == num_rows)
    return 1;

  if (grid[row][col] == empty) {
    for (int x = 1; x > -1; x--) { // try black before red to hit dense clues faster
      grid[row][col] = x;
      if (is_valid(grid, row, col)) {
        if (solve_it(grid, row, col + 1))
          return 1;
      }
    }
    grid[row][col] = empty;
  } else {
    return solve_it(grid, row, col + 1);
  }
  return 0;
}

int is_valid(int **grid, int row, int col) {
  // Validate target row by scanning left-to-right and enforcing clue lengths
  int group_idx = 0;
  int num_items_in_group = 0;
  int line_has_empty = 0;
  for (int col_idx = 0; col_idx < num_cols; col_idx++) {
    int cell = grid[row][col_idx];
    if (cell == empty) {
      line_has_empty = 1;
      break;
    }
    if (cell == red) {
      if (num_items_in_group > 0) {
        if (num_items_in_group != rows[row]->groups_size[group_idx - 1]) {
          return 0;
        }
        num_items_in_group = 0;
      }
      continue;
    }
    if (!num_items_in_group) { // starting a new black group
      group_idx++;
      if (group_idx > rows[row]->num_groups)
        return 0;
    }
    num_items_in_group++;
    if (num_items_in_group > rows[row]->groups_size[group_idx - 1]) {
      return 0;
    }
  }
  if (!line_has_empty && grid[row][num_cols - 1] == black &&
      num_items_in_group != rows[row]->groups_size[group_idx - 1]) {
    return 0;
  }
  if (!line_has_empty &&
      group_idx != rows[row]->num_groups) { // completed line but not all groups
    return 0;
  }

  // Validate target column using the same greedy check
  group_idx = 0;
  num_items_in_group = 0;
  line_has_empty = 0;
  for (int row_idx = 0; row_idx < num_rows; row_idx++) {
    int cell = grid[row_idx][col];
    if (cell == empty) {
      line_has_empty = 1;
      break;
    }
    if (cell == red) {
      if (num_items_in_group > 0) {
        if (num_items_in_group != cols[col]->groups_size[group_idx - 1]) {
          return 0;
        }
        num_items_in_group = 0;
      }
      continue;
    }
    if (!num_items_in_group) { // starting a new black group
      group_idx++;
      if (group_idx > cols[col]->num_groups)
        return 0;
    }
    num_items_in_group++;
    if (num_items_in_group > cols[col]->groups_size[group_idx - 1]) {
      return 0;
    }
  }
  if (!line_has_empty && grid[num_rows - 1][col] == black &&
      num_items_in_group != cols[col]->groups_size[group_idx - 1]) {
    return 0;
  }
  if (!line_has_empty &&
      group_idx != cols[col]->num_groups) { // completed line but not all groups
    return 0;
  }
  return 1;
}
void print_grid(int **grid) {
  for (int row = 0; row < num_rows; row++) {
    for (int col = 0; col < num_cols; col++) {
      char c;
      switch (grid[row][col]) {
        case empty:
          c = '.';
          break;
        case red:
          c = 'r';
          break;
        case black:
          c = 'B';
          break;
      }
      printf("%c", c);
    }
    printf("\n");
  }
}

void destroy_grid(int **grid) {
  for (int row_idx = 0; row_idx < num_rows; row_idx++) {
    free(grid[row_idx]);
  }
  free(grid);
}

void destroy_line(line *line) {
  free(line->groups_size);
  free(line);
}

int **create_grid() {
  int **grid = calloc(num_rows, sizeof(int *));
  for (int row_idx = 0; row_idx < num_rows; row_idx++) {
    grid[row_idx] = calloc(num_cols, sizeof(int));
    for (int col_idx = 0; col_idx < num_cols; col_idx++) {
      grid[row_idx][col_idx] = empty;
    }
  }
  return grid;
}

void fill_row(int **grid, int row_idx, line *row) {
  int col_idx = 0;
  int num_groups = row->num_groups;
  if (num_groups == 0) {
    for (int c = 0; c < num_cols; c++) {
      grid[row_idx][c] = red;
    }
    return;
  }
  // Lay down the exact run lengths, inserting a single separator red between runs
  for (int group_idx = 0; group_idx < num_groups; group_idx++) {
    for (int idx = 0; idx < row->groups_size[group_idx]; idx++) {
      grid[row_idx][col_idx] = black;
      col_idx++;
    }
    if (col_idx < num_cols) {
      grid[row_idx][col_idx] = red;
      col_idx++;
    }
  }
}

void fill_col(int **grid, int col_idx, line *col) {
  int row_idx = 0;
  int num_groups = col->num_groups;
  if (num_groups == 0) {
    for (int r = 0; r < num_rows; r++) {
      grid[r][col_idx] = red;
    }
    return;
  }
  // Same strategy as fill_row, but operate top-to-bottom
  for (int group_idx = 0; group_idx < num_groups; group_idx++) {
    for (int idx = 0; idx < col->groups_size[group_idx]; idx++) {
      grid[row_idx][col_idx] = black;
      row_idx++;
    }
    if (row_idx < num_rows) {
      grid[row_idx][col_idx] = red;
      row_idx++;
    }
  }
}

int determinable_line(line *line, int max_num_items) {
  int num_groups = line->num_groups;
  if (num_groups == 0)
    return 1;

  int total = num_groups;
  for (int idx = 0; idx < num_groups; idx++) {
    total += line->groups_size[idx];
  }
  // A line is forced when runs plus mandatory single reds fill the entire span
  return total - 1 == max_num_items;
}

line *create_line(int num_groups) {
  line *ret = calloc(1, sizeof(line));
  ret->num_groups = num_groups;
  ret->groups_size = calloc(num_groups, sizeof(int *));
  for (int group_idx = 0; group_idx < num_groups; group_idx++) {
    int group_size;
    scanf("%d", &group_size);
    ret->groups_size[group_idx] = group_size;
  }

  return ret;
}
