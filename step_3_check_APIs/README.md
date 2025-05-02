# Step 3: Check the APIs

I'm building a script analyze_posts.py that will analyze posts using the APIs of the AI detectors identified in step 2.

## Notes on APIs

### Sapling

Sapling works great. Rafe is pretty happy about the result. Next step is running with more posts, if the rate limit allows it.

Good points:

- Last update in January 2025.
- Uses perplexity metric instead of "does this look like an LLM" vibe test
- Gives detailed analysis with sentence by sentence breakdown of AI generated probability

Issues:

- ~~API often gets limited. I had to put quite aggressive exponential backoff to use it.~~
  - Update: I was actually sending gigantic posts like Zvi's AI posts. I cut up the posts to 10000 characters and that fixed the issue.

### Undetectable

Had trouble getting the API to work. They have a weird API, where you send documents and pull to check if they are finished processing. It seems to be taking very long to process.

TODO: Try again and look at the output of the queries to find what's going on.

### QuillBot

Does not provide an API currently https://help.quillbot.com/hc/en-us/articles/4541472549527-Does-QuillBot-Offer-an-API

There's a [GitHub project](https://github.com/Luen/quillbot-api) that uses puppeteer to scrape the website and extract the data, but that sounds very flaky.

## Copyleaks

They have a great SDK and API documentation. I especially like the sandbox mode to get back fake data and test the integration without spending credits.

Issues:

- Only recurring subscriptions with fixed number of credits are available. No pay-as-you-go option.

# Results

Run the visualize_results.py script to see the results.
