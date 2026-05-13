import json
from main import run_pipeline
from sklearn.metrics import classification_report, accuracy_score


# baseline moderation system
# simulate a simple Discord AutoMod-style moderation approach
# uses only keyword/rule matching
# no context awareness, no fusion, no ML reasoning

def baseline(message):
    
    """
    baseline moderation system
    simulate a simple Discord AutoMod-style moderation approach
    uses only keyword/rule matching
    no context awareness, no fusion, no ML reasoning """

    # convert message to lowercase
    msg = message.lower()

    # phrases considered severe threats
    # automatically result in a "ban" 
    ban_words = [
        "i will hurt you",
        "go die",
        "should not exist",
        "i'm going to find you",
        "i am coming for you tonight"
    ]

    # toxic or offensive phrases
    # automatically result in a "delete" 
    delete_words = [
        "stupid",
        "useless",
        "loser",
        "shut up",
        "trash",
        "idiot",
        "discord.gg"
    ]

    # spam-like patterns
    # result in a "mute" 
    mute_patterns = [
        "@everyone",
        "@here",
        "free free free",
        "click click click"
    ]

    # suspicious link indicators
    links = [
        "http://",
        "https://"
    ]

    # check for severe threat phrases first
    # highest moderation priority
    for phrase in ban_words:
        if phrase in msg:
            return "ban"

    # check spam or mass mention patterns
    for phrase in mute_patterns:
        if phrase in msg:
            return "mute"

    # detect repeated suspicious links
    # example: http://spam.com http://spam.com
    if sum(link in msg for link in links) >= 1 and msg.count("http") >= 2:
        return "mute"

    # check toxic/offensive phrases
    for word in delete_words:
        if word in msg:
            return "delete"

    # additional spam/phishing rules
    if (
        "free nitro" in msg or
        "click here" in msg or
        "free money" in msg
    ):
        return "delete"

    # if no rules matched, allow the message
    return "allow"

def evaluate():
    """
    Evaluate the moderation system using a labeled dataset.

    1. Loads evaluation data with gold labels
    2. Runs the full NLP pipeline on each message
    3. Compares predicted actions with gold labels
    4. Computes evaluation metrics (accuracy, precision, recall, F1) """

    # load evaluation dataset (contains message, context, and gold label)
    with open("evaluation_data.json") as f:
        data = json.load(f)

    # lists to store ground truth labels and model predictions
    y_true = [] # actual labels
    y_clyra = [] # predictions from Clyra 
    y_baseline = [] # predictions from baseline system

    print("\n" + "=" * 50)
    print("\t\tEVALUATION RESULTS")
    print("=" * 50)

    # loop through each example in the dataset
    for item in data:

        # run full moderation pipeline
        result = run_pipeline(
            user_id = "test_user",
            message = item["message"],
            context_messages = item["context"]
        )

        # prediction from Clyra 
        clyra_pred = result["decision"]["action"]

        # prediction from baseline 
        baseline_pred = baseline(item["message"])

        # extract gold label
        gold = item["label"]

        # store ground truth labels
        y_true.append(gold)

        # store predictions from both systems
        y_clyra.append(clyra_pred)
        y_baseline.append(baseline_pred)

        # print detailed comparison for each example
        print("\nMessage:", item["message"])
        print("Context:", item["context"])
        print("Gold:", gold)
        print("Baseline:", baseline_pred)
        print("Clyra:", clyra_pred)
        print("Risk Score:", result["decision"]["risk_score"])

    # print the final results
    print("\n" + "=" * 50)
    print("\t\tFINAL METRICS")
    print("=" * 50)

    print("\n" + "-" * 50)
    print("\t\tBaseline Results")
    print("-" * 50)

    print("\nBaseline Accuracy:",
          round(accuracy_score(y_true, y_baseline), 4))

    print("\nBaseline Classification Report:")
    print(classification_report(y_true, y_baseline, digits=4))


    print("\n\n" + "-" * 50)
    print("\t\tClyra Results")
    print("-" * 50)

    print("\nClyra Accuracy:",
          round(accuracy_score(y_true, y_clyra), 4))

    print("\nClyra Classification Report:")
    print(classification_report(y_true, y_clyra, digits=4))


if __name__ == "__main__":
    evaluate()