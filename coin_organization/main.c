#include <stdio.h>

const int max_name_length = 20;

typedef struct {
  char name[max_name_length];
  int bills;
  int tokens;
  long int units;
} Customer;

void merge_sort(Customer *customers, int len);

int main() {
  int num_customers;
  scanf("%d", &num_customers);

  Customer customers[num_customers];
  for (int idx = 0; idx < num_customers; idx++) {
    scanf("%s %d %d", customers[idx].name, &customers[idx].tokens,
          &customers[idx].bills);
  }

  int tokens, bills;
  scanf("%d %d", &tokens, &bills);

  // Calculate the number of units
  for (int idx = 0; idx < num_customers; idx++) {
    customers[idx].units = (long)customers[idx].tokens * bills +
                           (long)customers[idx].bills * tokens;
  }

  merge_sort(customers, num_customers);

  // Print in reverse order
  for (int idx = num_customers - 1; idx > -1; idx--) {
    printf("%s\n", customers[idx].name);
  }

  return 0;
}

void merge_sort(Customer *customers, int len) {
  // Base case
  if (len <= 1) {
    return;
  }
  int mid = len / 2;
  merge_sort(customers, mid);
  merge_sort(customers + mid, len - mid);
  // merge the array
  Customer temp[len];
  int fptr = 0;
  int bptr = mid;
  for (int i = 0; i < len; i++) {
    if (fptr < mid && bptr < len) {
      if (customers[fptr].units <
          customers[bptr].units) { // front has smaller element
        temp[i] = customers[fptr];
        fptr++;
      } else { // back has smaller (or equal) element
        temp[i] = customers[bptr];
        bptr++;
      }
    } else if (fptr < mid) { // front is non-empty, back is not
      temp[i] = customers[fptr];
      fptr++;
    } else { // back is non-empty, front is not
      temp[i] = customers[bptr];
      bptr++;
    }
  }
  for (int i = 0; i < len; i++)
    customers[i] = temp[i];
}
