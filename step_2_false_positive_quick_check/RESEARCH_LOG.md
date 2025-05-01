# Goal

Check if the LLM detectors that successfully detected the "The Structural Loyalty Compact" post as AI-generated, mark normal posts as AI-generated.

# Research

## Selecting the posts

Two rejected posts, but not AI-generated:

- [I Tried to Formalize Meaning. I May Have Accidentally Described Consciousness.](I_Tried_to_Formalize_Meaning.md)
- [The Misstep of the Cutting Mind: Why AGI Needs Poetry and Emotion](The_Misstep_of_the_Cutting_Mind.md)

Two accepted posts:

- [Anthropomorphizing AI might be good, actually](Anthropomorphizing_AI_might_be_good_actually.md)
- [Judging types of consequentialism by influence and normativity](Judging_types_of_consequentialism_by_influence_and_normativity.md)

For reference, I also added the AI post I tested previously:

- [The Structural Loyalty Compact](The_Structural_Loyalty_Compact.md)

## Detectors used

1. [Copyleaks](https://copyleaks.com/ai-content-detector):
2. [Undetectable AI](https://undetectable.ai/):
3. [QuillBot](https://quillbot.com/ai-content-detector):
4. [Sapling](https://sapling.ai/ai-content-detector):
5. [Winston AI](https://gowinston.ai/):

## Results

| Post                                | Copyleaks (AI phrases) | Undetectable AI | QuillBot | Sapling    | Winston AI |
| ----------------------------------- | ---------------------- | --------------- | -------- | ---------- | ---------- |
| I Tried to Formalize Meaning        | 100% AI (11 phrases)   | 78% AI          | 0% AI    | Fake 0.0%  | 17% human  |
| The Misstep of the Cutting Mind     | 100% AI (35 phrases)   | 0% AI           | 0% AI    | Fake 0.0%  | 96% human  |
| Anthropomorphizing AI might be good | 0% (0 phrases)         | 1% AI           | 0% AI    | Fake 0.0%  | 100% human |
| Judging types of consequentialism   | 0% (0 phrases)         | 0% AI           | 0% AI    | Fake 0.0%  | 100% human |
| (AI) The Structural Loyalty Compact | 100% (64 phrases)      | 86% AI          | 41% AI   | Fake 74.2% | 100% human |

## Thoughts on the results

[I tried to formalize meaning](I_Tried_to_Formalize_Meaning.md) is confusing those detectors. I think those detectors may be suffering from the problem of classifying non native English posts as AI-generated.

Overall the best ones seem to be QuillBot and Sapling, just because they did not make any mistakes on this dataset.

I think another thing that might be causing issues is that they might detect text that has been written by AI then rewritten by the author, or something like that. On LW we don't care if people use AI to help them write, we only care about the posts quality, and things that look obviously AI-generated are just bad writing.

## Possible next steps

- Pay for subscriptions to those services to see what are the additional details they provide on their analysis.
- Write a script that does a larger number of tests using the APIs
