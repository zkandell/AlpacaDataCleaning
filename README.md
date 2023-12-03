# AlpacaDataCleaning

This is a series of scripts designed to help with cleaning up the Alpaca data set and repurpose it to train a Large Language Model to be an instructional model, with a focus on helping with writing tasks. The intended target of this is to train a custom module with NovelAI's models, but it can be applied to any language models or adapted for any other instruct datasets. I have included the final results of running the code, but cannot guarantee that it is functional in its current state. 

The key ideas:
- The data is turned into three lists of queries: Keep, Maybe, and Remove. Keep queries will always be included in the training data, Remove queries will never be included in the training data, and queries will be pulled from the Maybe list if the Yes list alone does not fill up the character count. 
- The data is only programmatically cleaned, not manually. The lists can be recreated simply by running the script. 
- Queries are categorized by keywords. This is a broad, imperfect method, but it is also simple and quick, like using a chainsaw instead of a scalpel. 
- To improve the categorization, each keyword can have several connected keywords that exclude it. For example, while the focus of this model is on writing, a request that starts with "write" could be something like "Write a function that(...)". Since coding is not part of the scope of this, words like "function" and "code" can be added to "write", meaning that any command that includes the words "write" and ("code" or "function") are added to the Remove list instead of the Keep list. 

These scripts support the main work for cleaning the dataset, which is looking through keywords and items that are in the Maybe list to determine which requests should be in or out, and how to make that determination based on just the keywords. For this purpose, finditemswithword.py can be run to create a file with just requests that have a specific keyword, making that kind of analysis much easier. 

I did ultimately use the results of these scripts, in the final.txt file, to use to train a module for NovelAI's Euterpe module. However, with the release of their official (experimental) instruct module, moving further with this became a much lower priority. 
