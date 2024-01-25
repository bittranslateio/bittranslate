

def trim_prompt(input_tokens, max_prompt_len):

    prompt_token_len = len(input_tokens)

    if prompt_token_len > max_prompt_len:
        diff = prompt_token_len-max_prompt_len
        input_tokens = input_tokens[diff:]
    return input_tokens


