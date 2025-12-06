from ai_engine import generate_clinical_answer, text_to_pdf, text_to_speech

def chat_diagnosis_module():
    """
    Main interaction module for clinical diagnosis.
    - Accepts user query
    - Generates clinical answer
    - Optionally converts answer to PDF or speech
    """
    print("Welcome to HealthChecker 360\n")
    user_query = input("Enter your medical query: ").strip()

    if not user_query:
        print("⚠️ Please enter a valid query!")
        return

    # -------------------------
    # Generate clinical answer
    # -------------------------
    answer = generate_clinical_answer(user_query)

    # -------------------------
    # Display answer
    # -------------------------
    print("\n--- Clinical Answer ---\n")
    print(answer)

    # -------------------------
    # Optional: Save PDF
    # -------------------------
    save_pdf = input("\nDo you want to save this answer as PDF? (y/n): ").lower()
    if save_pdf == "y":
        pdf_file = text_to_pdf(answer)
        print(f"✅ PDF saved as: {pdf_file}")

    # -------------------------
    # Optional: Convert to Speech
    # -------------------------
    save_speech = input("\nDo you want to convert this answer to audio? (y/n): ").lower()
    if save_speech == "y":
        audio_file = text_to_speech(answer)
        print(f"✅ Audio saved as: {audio_file}")
