# Goal

Try LLM detectors, and see if I can get any of them to work on the post ./structural_loyalty_compact.md.

I choose this post, because it seems fully AI-generated, and does not include any disclaimers about this fact.

# Research

## LLM Detectors results

1. ❌ [ZeroGPT](https://www.zerogpt.com/): Fail. Thinks it's human-written. 0% AI generated
2. ✅ [Copyleaks](https://copyleaks.com/ai-content-detector): 100% of content may be AI-generated. 64 typical AI phrases detected.
3. ❌ [BrandWell](https://brandwell.ai/ai-content-detector/): Passes as human. It does detect some sentence that "sound robotic"

- Note: does not accept markdown files. Had to convert to PDF

4. 🯄 [Undetectable AI](https://undetectable.ai/): Likely 86% AI

- Note: WOW this is a meta detector. It looks at GPTZero, OpenAI, Writer, QuillBot, Copyleaks, Sapling, Grammarly, ZeroGPT
- Note: I'm not sure I trust this one. It's says individual detectors like GPTZero think the content is AI generated, but when I try them myself they say it's human-written. Maybe this is a fake product to make people pay for their humanization service.
  - It even includes OpenAI detection, but apparently it does not even exist anymore

5. ❌ [GPTZero](https://www.gptzero.com/): We are highly confident this text is entirely human
6. ❌ [Writer](https://writer.com/ai-content-detector): 97% human-generated
7. ✅ [QuillBot](https://quillbot.com/ai-content-detector): 41% of text is likely AI. 59% of text is human-written.
8. ✅ [Sapling](https://sapling.ai/ai-content-detector): Fake 74.2%
9. ❌ [Grammarly](https://grammarly.com/ai-detector): 24% of this text appears to be AI-generated
10. ❌ [Monica](https://monica.im/tools/ai-content-detector): Human

- Note: Only an aggregator, and with only ZeroGPT, GPTZero, and Copyleaks.

11. ❌ [Originality](https://originality.ai/ai-checker): We are 99% confident that text is original
12. ✅ [Winston AI](https://gowinston.ai/): 21% human

- Note: Cool dashboard presenting the likelihood of being AI generated for each section, and a sample of sections driving the AI score.

13. ❌ [AI Detector](https://aidetector.com/): Overall result: 0% likely AI-generated

- They say they have a better model if you sign up, but can't try it without subcribing or buying credits. May be a scam.
