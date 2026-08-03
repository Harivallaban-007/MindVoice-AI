def get_quick_tips(text):

    text = text.lower()

    tips = []

    if "hate" in text:
        tips.append("Avoid harsh words.")

    if "always" in text:
        tips.append("Avoid generalizations like 'always'.")

    if "never" in text:
        tips.append("Avoid absolute words like 'never'.")

    if "angry" in text:
        tips.append("Explain why you feel angry.")

    if "sorry" in text:
        tips.append("Appreciate the apology sincerely.")

    if "thank" in text:
        tips.append("Express gratitude naturally.")

    return tips