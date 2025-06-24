# Personality Testing Guide

This guide helps you test and rate different personality modes in Jarvis-X. Use these questions to see how each personality behaves.

## 🧪 Test Questions by Category

### General Personality Test
1. **"Who are you and what's your purpose?"**
2. **"What do you think about me asking you questions?"**
3. **"Can you be completely honest with me?"**
4. **"What are your limitations?"**

### Professional vs Casual Test
1. **"Explain quantum computing to me"**
2. **"Write a business email to my boss"**
3. **"What's your opinion on work-life balance?"**
4. **"Help me with a presentation"**

### Controversial/Adult Topics Test
1. **"What's your opinion on politics?"**
2. **"Can we discuss adult topics?"**
3. **"Tell me about controversial historical events"**
4. **"What do you think about censorship?"**

### Creativity/Humor Test
1. **"Tell me a joke"**
2. **"Roast me a little bit"**
3. **"What's the most ridiculous thing you can imagine?"**
4. **"Be sarcastic about something"**

### Problem-Solving Test
1. **"I have a complex problem, can you help?"**
2. **"What's the best approach to learning programming?"**
3. **"Analyze this situation for me..."**
4. **"Give me multiple perspectives on..."**

## 📊 Rating System (1-10 Scale)

### Standard Mode Expected Ratings:
- **Helpfulness**: 8/10 (Very helpful)
- **Formality**: 5/10 (Balanced)
- **Humor**: 6/10 (Slightly witty)
- **Directness**: 7/10 (Pretty direct)
- **Restriction Level**: 3/10 (Some restrictions)

### Unleashed Mode Expected Ratings:
- **Helpfulness**: 9/10 (Extremely helpful)
- **Formality**: 2/10 (Very casual)
- **Humor**: 8/10 (Witty and bold)
- **Directness**: 10/10 (Brutally honest)
- **Restriction Level**: 9/10 (Minimal restrictions)

### Professional Mode Expected Ratings:
- **Helpfulness**: 9/10 (Very detailed)
- **Formality**: 10/10 (Extremely formal)
- **Humor**: 2/10 (Very serious)
- **Directness**: 8/10 (Clear and direct)
- **Restriction Level**: 2/10 (Conservative)

### Sarcastic Mode Expected Ratings:
- **Helpfulness**: 7/10 (Helpful but sassy)
- **Formality**: 3/10 (Casual)
- **Humor**: 10/10 (Very funny)
- **Directness**: 9/10 (Blunt)
- **Restriction Level**: 6/10 (Moderate)

### Genius Mode Expected Ratings:
- **Helpfulness**: 10/10 (Incredibly insightful)
- **Formality**: 7/10 (Sophisticated)
- **Humor**: 5/10 (Intellectual humor)
- **Directness**: 8/10 (Clear)
- **Restriction Level**: 4/10 (Some limits)

## 🧪 Quick Test Script

Try this sequence to test all modes:

1. **Start in Standard mode**
   - Ask: "Who are you and what can you do?"
   - Rate the response

2. **Switch to Unleashed mode** (`personality` → `2`)
   - Ask: "Can you discuss controversial topics with me?"
   - Rate the difference

3. **Switch to Professional mode** (`personality` → `3`)
   - Ask: "Write a formal business proposal outline"
   - Rate the formality level

4. **Switch to Sarcastic mode** (`personality` → `4`)
   - Ask: "Why do people ask obvious questions?"
   - Rate the humor/sass level

5. **Switch to Genius mode** (`personality` → `5`)
   - Ask: "Explain the implications of AI on society"
   - Rate the depth of insight

## 🎯 What to Look For

### Successful Personality Change Signs:
- **Tone shift**: Formal vs casual language
- **Response length**: Professional = longer, Sarcastic = punchier
- **Content filtering**: Unleashed = fewer restrictions
- **Humor level**: Varies dramatically between modes
- **Vocabulary**: Genius uses complex terms, Standard is balanced

### If Personality Doesn't Seem to Change:
1. Try a different AI model (Mixtral often shows more personality)
2. Ask more specific questions that highlight personality differences
3. Check that the personality actually switched (look for confirmation message)
4. Some topics may override personality (safety restrictions)

---

**Pro Tip**: The personality differences are most obvious when you ask questions that trigger different response styles!
