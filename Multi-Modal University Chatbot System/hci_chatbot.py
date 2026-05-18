# =========================================
# HCI Assignment #5
# Multi-Modal University Chatbot System
# =========================================

import speech_recognition as sr
import pyttsx3


def speak_text(text):
    """
    Converts text into speech output.
    """

    engine = pyttsx3.init()

    engine.say(text)

    engine.runAndWait()


def recognize_speech():
    """
    Converts speech into text using microphone.

    Returns:
        recognized text (str)
    """

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print(f"\nRecognized Text: {text}")

        return text

    except sr.UnknownValueError:

        print("\nCould not understand audio.")

        return ""

    except sr.RequestError:

        print("\nSpeech recognition service error.")

        return ""


def detect_spam(user_input):
    """
    Detects whether the user query is spam or not.

    Returns:
        True  -> if spam detected
        False -> if not spam
    """

    spam_keywords = [

        # General spam
        "win money",
        "free bitcoin",
        "click here",
        "earn dollars",
        "lottery",
        "casino",
        "buy followers",
        "investment scheme",
        "free gift",
        "get rich quick",
        "promo code",

        # University specific spam
        "fake admission",
        "buy degree",
        "cheap certificate",
        "exam leak",
        "paid promotion",
        "fake scholarship",
        "sell assignment",
        "buy project",
        "proxy exam"
    ]

    user_input = user_input.lower()

    for keyword in spam_keywords:

        if keyword in user_input:
            return True

    return False


def identify_intent(user_input):
    """
    Identifies user intent based on keywords.

    Returns:
        intent (str)
        confidence_score (float)
        matched_keywords (list)
    """

    intents = {

        "Admission": [
            "admission",
            "apply",
            "application",
            "enroll",
            "enrollment",
            "eligibility",
            "requirements",
            "admission process",
            "how to apply",
            "merit list",
            "criteria"
        ],

        "Fee": [
            "fee",
            "fees",
            "charges",
            "semester cost",
            "tuition",
            "payment",
            "pay",
            "scholarship",
            "financial aid",
            "dues",
            "expense"
        ],

        "Courses": [
            "course",
            "courses",
            "subject",
            "subjects",
            "program",
            "degree",
            "curriculum",
            "syllabus",
            "credit hours",
            "field",
            "ai",
            "software engineering",
            "bsse",
            "data science"
        ],

        "Schedule": [
            "schedule",
            "timing",
            "class time",
            "date sheet",
            "exam schedule",
            "timetable",
            "routine",
            "calendar",
            "exam date",
            "lecture timing"
        ]
    }

    user_input = user_input.lower()

    best_intent = None
    best_score = 0
    matched_words = []

    for intent, keywords in intents.items():

        score = 0
        current_matches = []

        for keyword in keywords:

            if keyword in user_input:

                score += 1

                current_matches.append(keyword)

        if score > best_score:

            best_score = score

            best_intent = intent

            matched_words = current_matches

    confidence_score = best_score / 11

    return best_intent, confidence_score, matched_words


def get_static_response(intent):
    """
    Returns predefined static responses
    for each detected intent.
    """

    static_responses = {

        "Admission": (
            "ITU admissions open twice a year. "
            "You can apply online through the admission portal."
        ),

        "Fee": (
            "Fee structure depends on the selected program. "
            "Visit the university website for updated fee details."
        ),

        "Courses": (
            "The university offers BS, MS, and PhD programs "
            "in multiple disciplines."
        ),

        "Schedule": (
            "Class schedules and exam dates are available "
            "on the student portal."
        )
    }

    return static_responses.get(intent, None)


def get_dynamic_response(intent, user_input):
    """
    Returns dynamic responses based on
    keywords inside the user query.
    """

    query = user_input.lower()

    # ==========================
    # FEE RESPONSES
    # ==========================

    if intent == "Fee":

        if "bs" in query or "bachelors" in query:

            return (
                "The BS program fee is approximately "
                "PKR 40,000 per semester."
            )

        elif "ms" in query or "masters" in query:

            return (
                "The MS program fee is approximately "
                "PKR 50,000 per semester."
            )

        elif "scholarship" in query:

            return (
                "The university offers merit-based "
                "and need-based scholarships."
            )

    # ==========================
    # COURSES RESPONSES
    # ==========================

    elif intent == "Courses":

        if "bsse" in query or "software engineering" in query:

            return (
                "BS Software Engineering includes "
                "AI, HCI, Web Development, and DBMS courses."
            )

        elif "ai" in query:

            return (
                "AI courses include Machine Learning, "
                "Deep Learning, and NLP."
            )

        elif "data science" in query:

            return (
                "Data Science includes Statistics, "
                "Python, and Big Data Analytics."
            )

    # ==========================
    # ADMISSION RESPONSES
    # ==========================

    elif intent == "Admission":

        if "eligibility" in query or "criteria" in query:

            return (
                "Minimum 60 percent marks are required "
                "for admission eligibility."
            )

        elif "deadline" in query:

            return (
                "Admission deadlines are announced "
                "on the university website every semester."
            )

    # ==========================
    # SCHEDULE RESPONSES
    # ==========================

    elif intent == "Schedule":

        if "exam" in query or "date sheet" in query:

            return (
                "Exam schedules are uploaded "
                "before final examinations."
            )

        elif "class" in query or "timing" in query:

            return (
                "Class timings are available "
                "on the student portal."
            )

    # Fallback
    return get_static_response(intent)


def handle_unknown_query():
    """
    Returns error message for unknown queries.
    """

    return (
        "Sorry, I could not understand your request. "
        "Please ask about Admission, Fee, Courses, or Schedule."
    )


def process_query(user_input):
    """
    Processes user query through:

    1. Spam Detection
    2. Intent Identification
    3. Response Generation
    """

    # ==========================
    # MODULE 1 -> SPAM DETECTION
    # ==========================

    is_spam = detect_spam(user_input)

    if is_spam:

        response = "This query is classified as spam."

        print(f"\n{response}")

        speak_text(response)

        return

    else:

        print("\nNot Spam")

    # ==========================
    # MODULE 2 -> INTENT DETECTION
    # ==========================

    intent, confidence, matched = identify_intent(user_input)

    if intent and confidence > 0:

        print(f"\nDetected Intent  : {intent}")

        print(f"Confidence Score : {confidence:.2f}")

        print(f"Matched Keywords : {matched}")

        # ==========================
        # MODULE 3 -> RESPONSE
        # ==========================

        response = get_dynamic_response(intent, user_input)

        if not response:

            response = get_static_response(intent)

        print(f"\nChatbot Response : {response}")

        # Voice Output
        speak_text(response)

    else:

        response = handle_unknown_query()

        print(f"\nChatbot Response : {response}")

        speak_text(response)

    print("\n---------------------------------")


def text_mode():
    """
    Handles text input mode.
    Type ESC to return to main menu.
    """

    print("\nTEXT MODE ACTIVATED")
    print("Type ESC anytime to return to main menu.")

    while True:

        user_input = input("\nEnter your query: ")

        if user_input.strip().upper() == "ESC":

            print("\nReturning to Main Menu...")

            break

        process_query(user_input)


def voice_mode():
    """
    Handles voice interaction mode.
    Say EXIT, STOP, or CLOSE to return.
    """

    print("\nVOICE MODE ACTIVATED")

    while True:

        user_input = recognize_speech()

        if user_input == "":

            continue

        exit_commands = ["exit", "stop", "close"]

        if user_input.lower() in exit_commands:

            print("\nReturning to Main Menu...")

            speak_text("Returning to main menu")

            break

        process_query(user_input)


def hybrid_mode():
    """
    Handles both text and voice interaction.
    """

    print("\nHYBRID MODE ACTIVATED")

    while True:

        print("\n1. Text Input")
        print("2. Voice Input")
        print("3. Return to Main Menu")

        choice = input("\nChoose option: ")

        if choice.strip().upper() == "ESC":

            break

        if choice == "1":

            user_input = input("\nEnter your query: ")

            if user_input.strip().upper() == "ESC":

                continue

            process_query(user_input)

        elif choice == "2":

            user_input = recognize_speech()

            if user_input == "":

                continue

            process_query(user_input)

        elif choice == "3":

            print("\nReturning to Main Menu...")

            break

        else:

            print("\nInvalid option.")


def chatbot():
    """
    Main menu-driven chatbot system.
    """

    while True:

        print("\n=================================")
        print(" UNIVERSITY CHATBOT SYSTEM ")
        print("=================================")

        print("\nSelect Input Mode")

        print("1. Text Mode")
        print("2. Voice Mode")
        print("3. Hybrid Mode")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice.strip().upper() == "ESC":

            print("\nChatbot Closed.")

            break

        if choice == "1":

            text_mode()

        elif choice == "2":

            voice_mode()

        elif choice == "3":

            hybrid_mode()

        elif choice == "4":

            print("\nChatbot Closed.")

            break

        else:

            print("\nInvalid choice. Please try again.")


# =========================================
# Program Starts Here
# =========================================

chatbot()