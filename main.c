#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int random_index(float * cum_p, unsigned int len) {
	float rand_value = ((float) rand()) / ((float) RAND_MAX);
	for (unsigned int i = 0; i < len; i++) {
		if (rand_value < cum_p[i]) {
			return i;
		}
	}
	return -1;
}

struct markov_cell {
	char * text;
	float * chances;
};

#include "markov.h"

int main(int argc, char ** argv) {
	srand(time(NULL));
	unsigned int samples = 1024;
	unsigned int * sample = malloc(sizeof(unsigned int) * samples);
	for(int i = 0; i < samples; i ++) {
		if(i == 0) {
			sample[i] = (rand() % num_tokens);
			continue;
		}
		int x = random_index(markov_table[sample[i-1]].chances, num_tokens);
		if(x == -1) {
			i -= 2;
			continue;
		}
		sample[i] = x;
	}
	for(int i = 0; i < samples; i ++) {
		printf("%s", markov_table[sample[i]].text);
	}
	return 0;
}



