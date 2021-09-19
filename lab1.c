#include <stdio.h>
#include <string.h> 
#include <stdbool.h>
#include <stdlib.h>

#define MAX_STRING_SIZE 100

/*
 * Prints tokens
 */
void print_tokens(char** tokens, int num_tokens){
    for(int i = 0; i < num_tokens; ++i){
        printf("\nToken %d: %s", i, tokens[i]);
    }
    printf("\n");
}

/*
 * Returns char** with all the tokens in input string
 */
char** get_tokens(char* str, int num_tokens){
    char** tokens = (char**)malloc(num_tokens * sizeof(char*));
    for(int i = 0; i < num_tokens; ++i){
        tokens[i] = (char*)malloc(MAX_STRING_SIZE * sizeof(char));
    }

    int word_index = 0;
    int letter_index = 0;

    for(int i = 0; i < strlen(str); ++i){
        bool is_delimiter = _is_delimiter(str[i]);

        if(!is_delimiter){
            tokens[word_index][letter_index] = str[i];
            ++letter_index;

            if(_is_delimiter(str[i + 1])){
                tokens[word_index][letter_index + 1] = '\0';
                ++word_index;
                letter_index = 0;
            }
        }     
    }

    return tokens;
}

/*
 * Tells us if the character we saw is considered a delimiter
 */
bool _is_delimiter(char c){
    return c == ' ' || c == '\t' || c == '\0' || c == '\n';
}

/*
 * Returns how many tokens there are in the input string
 */
int count_tokens(char* str){
    bool saw_delimiter = _is_delimiter(str[0]);
    int word_count = saw_delimiter ? 0 : 1;

    for(int i = 0; i < strlen(str) - 1; ++i){ 
        if(saw_delimiter){
            if(!_is_delimiter(str[i])){
                word_count++;
            }
        }
        saw_delimiter = _is_delimiter(str[i]);
    }
    return word_count;
}

/*
 * Orchestrates the tokenization
 *
 * First count number of tokens
 * Next create pointers
 * Then just print them and return them
 */
char** tokenize(char* str){
    int num_tokens = count_tokens(str);
    char** tokens = get_tokens(str, num_tokens);
    print_tokens(tokens, num_tokens);
    return tokens;
}

/*
 * Use main class to get the input string
 */
int main(){
    char input[MAX_STRING_SIZE];
    printf("Please enter the input string: ");
    fgets(input, MAX_STRING_SIZE, stdin);

    if(strlen(input) > 1) tokenize(input);
    return(0);
}
  