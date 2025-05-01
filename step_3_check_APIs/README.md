# Step 3: Check the APIs

I'm building a script analyze_posts.py that will analyze posts using the APIs of the AI detectors identified in step 2.

## Notes on APIs

### Sapling

Sapling works great. Rafe is pretty happy about the result. Next step is running with more posts, if the rate limit allows it.

Good points:
- Last update in January 2025.
- Uses perplexity metric

Issues:
- API often gets limited. I had to put quite aggressive exponential backoff to use it.

### Undetectable

Had trouble getting the API to work. They have a weird API, where you send documents and pull to check if they are finished processing. It seems to be taking very long to process.

### QuillBot

Does not provide an API currently https://help.quillbot.com/hc/en-us/articles/4541472549527-Does-QuillBot-Offer-an-API

There's a [GitHub project](https://github.com/Luen/quillbot-api) that uses puppeteer to scrape the website and extract the data, but that sounds very flaky.

# Results

Run the visualize_results.py script to see the results.