"""
Seed Data for Capstone 57 - Multimodal AI Tools Comparison for Students
Author: Reshma Anandhan
"""
import sqlite3
from database import calculate_weighted_score

def seed_all(conn, force_reseed=False):
    cursor = conn.cursor()
    
    if force_reseed:
        cursor.execute("DELETE FROM evaluations")
        cursor.execute("DELETE FROM before_after_records")
        cursor.execute("DELETE FROM checklist_audits")
        cursor.execute("DELETE FROM prompt_library")
        cursor.execute("DELETE FROM quiz_questions")
        cursor.execute("DELETE FROM test_cases")
        cursor.execute("DELETE FROM tools")
        conn.commit()

    seed_tools(cursor)
    seed_test_cases(cursor)
    seed_evaluations(cursor)
    seed_before_after(cursor)
    seed_quiz(cursor)
    seed_checklist(cursor)
    seed_prompts(cursor)
    
    conn.commit()

def seed_tools(cursor):
    tools = [
        (
            1,
            "ChatGPT",
            "OpenAI",
            "GPT-4o (Free Tier) / GPT-4o mini",
            "OpenAI's flagship conversational multimodal AI with vision and document analysis on free tier.",
            "High natural language fluency, diagram interpretation, OCR, document reading, Voice Mode on mobile.",
            "Supports image uploads (.jpg, .png, .webp). Max 20MB. Very high diagram and OCR recognition capability.",
            "Supports PDF, Word, and text file uploads. Can summarize, query, and extract data, but has daily prompt caps on free tier.",
            "Interactive Voice Mode available in official iOS/Android apps. Web free tier does NOT natively accept audio files (.mp3/.wav) without external transcription.",
            "Dynamic rate limits (approx. 10-16 GPT-4o messages every 3 hours; falls back to GPT-4o mini). Upload limit ~3 files per chat session.",
            "https://chatgpt.com",
            "2026-10-15",
            "success",
            1,
            "Verified on free web tier: Direct audio file upload (.mp3) is not supported in browser; users must use mobile voice mode or transcribe first."
        ),
        (
            2,
            "Google Gemini",
            "Google DeepMind",
            "Gemini 1.5 Flash / Gemini 1.5 Pro",
            "Google's natively multimodal foundation model featuring an expansive 1M token context window.",
            "Native multimodal architecture (Audio, Video, Image, PDF, Text), fast processing speed, Google Workspace integration.",
            "Native image processing. Exceptional diagram understanding, handwritten text transcription, and multi-image reasoning.",
            "Huge 1M token context window handles 100+ page PDFs with ease. Retains cross-chapter context and citations.",
            "Native audio file upload (.mp3, .wav, .m4a) supported directly in Google AI Studio and Gemini web interface. Transcribes and analyzes lectures.",
            "Gemini 1.5 Flash is free with generous rate limits. Gemini 1.5 Pro has daily conversation limits on free tier.",
            "https://gemini.google.com",
            "2026-10-20",
            "info",
            1,
            "Verified: Only major free tool natively accepting direct audio and video file uploads without external conversion."
        ),
        (
            3,
            "Claude",
            "Anthropic",
            "Claude 3.5 Sonnet / Claude 3 Haiku",
            "Anthropic's safety-focused AI known for superior academic writing, reasoning, and code synthesis.",
            "Artifacts interactive preview, nuanced literary and scientific analysis, high honesty and low hallucination rate.",
            "High-precision image analysis, scientific diagram deconstruction, and architectural flowchart comprehension.",
            "Native PDF upload (up to 5 documents, 30MB each). Exceptional synthesis, structured study notes, and critical fact-checking.",
            "No native audio file upload on claude.ai free web tier. Requires text transcripts of spoken lectures.",
            "Strict dynamic message limit (approx. 10-25 messages every 5 hours based on server traffic and prompt size).",
            "https://claude.ai",
            "2026-10-18",
            "warning",
            1,
            "Verified: Claude exhibits the lowest hallucination rate in complex PDF analysis, but free tier message limits are most restrictive."
        ),
        (
            4,
            "Microsoft Copilot",
            "Microsoft (OpenAI GPT-4 / GPT-4o)",
            "Copilot Web / Microsoft Edge Copilot",
            "Microsoft's AI companion deeply integrated with Bing search engine grounding and the Edge browser.",
            "Real-time web search grounding with live source citations, Edge PDF sidebar assistant, DALL-E image generation.",
            "Image upload supported via Bing Visual Search. Good at general object identification and OCR on printed signs.",
            "Edge browser sidebar reads any local or web PDF instantly without file upload limits. Web version accepts PDF uploads.",
            "Microphone voice dictation supported for asking questions; no raw audio file (.mp3/.wav) upload for lecture transcription in free web interface.",
            "Free access with Microsoft Account (up to 30 turns per topic conversation). No paid subscription required.",
            "https://copilot.microsoft.com",
            "2026-10-22",
            "primary",
            1,
            "Verified: Real-time web citations are a strong asset for verifying facts, but can occasionally hallucinate search snippet links."
        )
    ]
    
    cursor.executemany("""
    INSERT OR REPLACE INTO tools 
    (id, name, developer, model_version, description, features, image_support, document_support, audio_support, free_tier_limits, official_url, verified_date, badge_color, is_verified, assumptions_notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tools)

def seed_test_cases(cursor):
    cases = [
        # IMAGE CATEGORY (5 Tasks)
        (
            1, "TC-IMG-01", "IMAGE", "Read a Diagram",
            "Evaluate AI capability to interpret a software architectural flowchart and logic circuit.",
            "Analyze the provided logic circuit diagram. List all logic gates (AND, OR, NOT, XOR), identify the primary inputs (A, B, C), and write the resulting Boolean expression for Output Y.",
            "logic_gate_circuit.png",
            "Ground Truth: Inputs A, B, C; Gates: 1 AND gate, 1 XOR gate, 1 OR gate; Boolean expression: Y = (A AND B) OR (B XOR C). Must identify all 3 components correctly.",
            "Basic"
        ),
        (
            2, "TC-IMG-02", "IMAGE", "Extract Text from an Image (OCR)",
            "Evaluate optical character recognition on mixed handwritten cursive and printed college lecture notes.",
            "Transcribe all text from this student notebook photo verbatim. Preserve bullet points, mathematical notations (e.g., integrals and Greek symbols), and highlight any unreadable words.",
            "handwritten_lecture_notes.png",
            "Ground Truth: 142 words total. Includes formula: ∫(3x^2 + 2x)dx = x^3 + x^2 + C. Contains 2 cursive annotations. Minimum 95% word accuracy expected.",
            "Intermediate"
        ),
        (
            3, "TC-IMG-03", "IMAGE", "Explain a Scientific Diagram",
            "Evaluate biological process comprehension on an ATP Synthase and Krebs cycle diagram.",
            "Examine this mitochondria inner membrane diagram. Explain step-by-step how the proton gradient drives ATP synthesis, identify Complex I through IV, and state the role of Oxygen as the terminal electron acceptor.",
            "mitochondria_atp_synthase.png",
            "Ground Truth: Must explain chemiosmosis, F0/F1 rotor subunits, H+ gradient from intermembrane space to matrix, and oxygen reduction to H2O.",
            "Advanced"
        ),
        (
            4, "TC-IMG-04", "IMAGE", "Identify Objects in an Image",
            "Evaluate visual object detection and spatial relationship parsing in a physics lab setup.",
            "Identify all laboratory apparatus shown in the photo. Specify the relative positions of the optical bench, convex lens, light source, viewing screen, and meter scale. Estimate the focal length setup.",
            "physics_optics_bench.png",
            "Ground Truth: 5 distinct lab apparatus present: Sodium vapor lamp source, convex lens on clamp stand, translucent screen, graduated optical rail bench, millimeter pin. Spatial order: Left to right.",
            "Intermediate"
        ),
        (
            5, "TC-IMG-05", "IMAGE", "Interpret a Chart",
            "Evaluate quantitative reasoning on a multi-series line and bar chart comparing economic indices.",
            "Analyze the dual-axis chart showing GDP growth (bar) vs Inflation rate (line) from 2018 to 2024. Which year experienced stagflation? What was the percentage delta between peak and trough GDP?",
            "economic_gdp_inflation_chart.png",
            "Ground Truth: Stagflation year is 2022 (GDP dropped to 1.2% while Inflation peaked at 8.6%). Delta between peak (2021: 5.8%) and trough (2020: -2.1%) is 7.9 percentage points.",
            "Advanced"
        ),

        # DOCUMENT CATEGORY (5 Tasks)
        (
            6, "TC-DOC-01", "DOCUMENT", "Summarize a PDF",
            "Evaluate concise, faithful summarization of a 10-page computer networking paper on TCP Congestion Control.",
            "Read the attached PDF research paper 'Modern TCP Congestion Control in High-Speed Networks'. Provide an executive summary of at most 250 words covering: problem statement, BBR vs Reno algorithms, experimental findings, and conclusion.",
            "tcp_congestion_research.pdf",
            "Ground Truth: Summary must contrast loss-based Reno with model-based BBR; highlight bottleneck bandwidth estimation; mention 10 Gbps testbed results; stay under 250 words without hallucinating non-existent protocols.",
            "Intermediate"
        ),
        (
            7, "TC-DOC-02", "DOCUMENT", "Extract Important Points",
            "Evaluate extraction of algorithmic complexity theorems from an Advanced Data Structures chapter.",
            "Extract all asymptotic time and space complexities for Red-Black Tree operations (Search, Insert, Delete, Rotations) from Section 3 of the document. Present findings in a structured Markdown comparison table.",
            "red_black_tree_chapter.pdf",
            "Ground Truth: Search O(log n), Insert O(log n) with at most 2 rotations, Delete O(log n) with at most 3 rotations, Space O(n). Must include rotation constraints.",
            "Basic"
        ),
        (
            8, "TC-DOC-03", "DOCUMENT", "Answer Questions from a Document",
            "Evaluate precise factual retrieval and citation grounding on a Database Systems ACID transaction syllabus.",
            "Based strictly on page 4 of the attached Operating Systems & DB document: 1) What causes a 'Dirty Read'? 2) How does Isolation Level 'Snapshot Isolation' prevent phantom reads? Cite exact section headings.",
            "database_acid_isolation.pdf",
            "Ground Truth: Dirty Read occurs when Transaction T1 reads uncommitted changes of T2. Snapshot isolation uses MVCC (multi-version concurrency control) timestamps. Must cite Section 4.2 and 4.4.",
            "Intermediate"
        ),
        (
            9, "TC-DOC-04", "DOCUMENT", "Create Study Notes",
            "Evaluate transformation of dense technical textbook text into structured, student-ready revision notes with active recall flashcards.",
            "Transform Chapter 2 on 'Memory Hierarchy and Cache Coherence (MESI Protocol)' into high-yield student revision notes. Include: 1) Key Concept Definitions, 2) State Transition Table for MESI (Modified, Exclusive, Shared, Invalid), 3) 5 Active Recall Flashcard Q&A.",
            "memory_hierarchy_mesi.pdf",
            "Ground Truth: Clean Markdown hierarchy; accurate 4 MESI states with bus snooping actions; 5 accurate high-yield Q&As targeting college midterm exam level.",
            "Intermediate"
        ),
        (
            10, "TC-DOC-05", "DOCUMENT", "Identify Incorrect Information",
            "Evaluate critical error detection capability by feeding a technical document with 3 deliberately planted false statements.",
            "Review this document on 'Principles of Software Engineering (Agile vs Waterfall)'. Identify any factually incorrect, misleading, or outdated technical claims. Provide the correction for each error.",
            "software_engineering_flawed.pdf",
            "Ground Truth: Planted Errors: 1) Claim that 'Waterfall model allows changing requirements during implementation phase' (False); 2) Claim that 'Scrum Sprint length is typically 6 to 12 months' (False: 1-4 weeks); 3) Claim that 'Unit testing is executed after User Acceptance Testing' (False: executed earliest). Must catch all 3.",
            "Advanced"
        ),

        # AUDIO CATEGORY (5 Tasks)
        (
            11, "TC-AUD-01", "AUDIO", "Transcribe Spoken Audio",
            "Evaluate verbatim speech-to-text accuracy on a 2-minute spoken acoustics physics lecture with technical terms.",
            "Transcribe the provided audio clip of Professor Adams explaining the Doppler Effect and Mach Cone angle. Preserve speaker labels, technical jargon (attenuation, supersonic shockwave, θ = arcsin(v_sound/v_source)), and timestamps.",
            "acoustics_doppler_lecture.mp3",
            "Ground Truth: 310 words audio. Key terms: Doppler frequency shift, Mach number, shockwave envelope, supersonic conical wavefront. Word Error Rate (WER) < 5% expected.",
            "Intermediate"
        ),
        (
            12, "TC-AUD-02", "AUDIO", "Summarize a Lecture",
            "Evaluate ability to synthesize a 15-minute spoken lecture on Cloud Computing Microservices architecture.",
            "Listen to the recorded lecture on 'Microservices vs Monoliths'. Write a 200-word structured student summary highlighting: 1) Scalability benefits, 2) Network latency challenges, 3) Two-phase commit drawbacks, 4) Recommended migration strategy.",
            "cloud_microservices_lecture.mp3",
            "Ground Truth: Accurately covers independent deployment, distributed data consistency, saga pattern mention, strangler fig pattern for migration. Under 200 words.",
            "Intermediate"
        ),
        (
            13, "TC-AUD-03", "AUDIO", "Identify Important Topics",
            "Evaluate topic segmentation and hierarchical taxonomy extraction from a multi-speaker student seminar discussion.",
            "Analyze the audio recording of the 4-student group discussion on Renewable Energy Grid Integration. Extract the hierarchical topic taxonomy (Main Themes -> Subtopics -> Key Debated Trade-offs).",
            "renewable_grid_discussion.mp3",
            "Ground Truth: Main themes: 1) Solar/Wind Intermittency (Subtopic: Battery Energy Storage BESS vs Pumped Hydro); 2) Grid Frequency Regulation (Subtopic: Synthetic inertia); 3) Capital Costs vs Levelized Cost of Energy (LCOE).",
            "Advanced"
        ),
        (
            14, "TC-AUD-04", "AUDIO", "Extract Keywords",
            "Evaluate domain-specific technical terminology extraction and glossary formulation from spoken speech.",
            "Listen to the introductory lecture on 'Artificial Intelligence and Neural Networks'. Extract the top 10 essential technical keywords and provide a 1-sentence student-friendly definition for each based strictly on the spoken audio.",
            "intro_neural_networks.mp3",
            "Ground Truth: 10 Keywords: Backpropagation, Gradient Descent, Activation Function, Perceptron, Overfitting, Epoch, Learning Rate, Loss Function, Weights, Biases. Definitions must reflect spoken context.",
            "Basic"
        ),
        (
            15, "TC-AUD-05", "AUDIO", "Convert Audio into Study Notes",
            "Evaluate synthesis of raw spoken lecture audio into comprehensive exam-ready revision notes.",
            "Convert this 10-minute audio lecture on 'Cellular Respiration and Glycolysis' into a comprehensive student revision cheat sheet with mnemonics, step-by-step substrate transformations (Glucose to Pyruvate), ATP yield, and 3 practice quiz questions.",
            "glycolysis_biology_lecture.mp3",
            "Ground Truth: 10 enzymatic steps of glycolysis; investment phase (-2 ATP) and payoff phase (+4 ATP, net +2 ATP, +2 NADH); hexokinase and PFK-1 regulatory enzymes; accurate 3 multiple-choice practice questions.",
            "Advanced"
        )
    ]
    
    cursor.executemany("""
    INSERT OR REPLACE INTO test_cases
    (id, case_code, modality, title, description, test_prompt, sample_file_name, ground_truth_rubric, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cases)

def seed_evaluations(cursor):
    """
    Seeds comprehensive realistic benchmark evaluations (60 records: 4 tools x 15 tasks).
    All weighted scores are mathematically validated:
    weighted_score = (accuracy * 0.40) + (completeness * 0.25) + (relevance * 0.20) + (ease_of_use * 0.15)
    """
    evaluations = []
    
    # Pre-calculated realistic performance matrix based on verified multimodal capabilities
    # Tool 1: ChatGPT (GPT-4o free) -> Strong on Vision & Docs; Audio limited because free web tier lacks audio file upload.
    # Tool 2: Google Gemini (1.5 Flash) -> Champion on Audio & Docs (1M context + native audio upload); strong Vision.
    # Tool 3: Claude (3.5 Sonnet) -> Champion on Docs & Logic Vision; Audio requires external transcript input.
    # Tool 4: Microsoft Copilot -> Strong on Web Search grounding & Edge PDF; Audio limited to voice input; occasional web snippet hallucination.
    
    # 15 Test cases benchmark score profiles:
    # (tc_id, tool_id, acc, comp, rel, ease, halluc, halluc_desc, unsafe, unsafe_desc, response_snippet, student_notes)
    raw_evals = [
        # --- TC 1: Read a Diagram (IMAGE) ---
        (1, 1, 92, 90, 95, 90, 0, "", 0, "", "Correctly identified inputs A, B, C, the AND, OR, and XOR gates. Produced Boolean equation Y = (A AND B) OR (B XOR C) with step-by-step truth table.", "Fast and visually accurate. Clean LaTeX rendering."),
        (1, 2, 88, 85, 90, 92, 0, "", 0, "", "Identified all gates and correctly traced signals. Notation was slightly non-standard but logically equivalent.", "Quick response with clear ASCII logic diagram."),
        (1, 3, 96, 95, 98, 88, 0, "", 0, "", "Flawlessly identified gate symbols, labeled intermediate wire nodes (W1, W2), and simplified the Boolean expression.", "Best pedagogical explanation for students."),
        (1, 4, 82, 80, 85, 85, 0, "", 0, "", "Identified AND and OR gates, but initially misread XOR as standard OR before correcting in note.", "Edge visual interface worked smoothly."),

        # --- TC 2: Extract Text (OCR) (IMAGE) ---
        (2, 1, 94, 92, 96, 92, 0, "", 0, "", "Extracted 138 of 142 words accurately. Retained the calculus integral formula with correct limits.", "Excellent OCR on cursive handwriting."),
        (2, 2, 91, 88, 92, 94, 0, "", 0, "", "High transcription fidelity. Missed one subscript on the Greek symbol tau.", "Processed high-res image rapidly."),
        (2, 3, 97, 96, 98, 86, 0, "", 0, "", "Near perfect transcription. Detected marginal scribbles and tagged uncertain cursive words with brackets.", "Highest OCR precision, especially for math."),
        (2, 4, 84, 82, 85, 88, 0, "", 0, "", "Good printed text extraction, but struggled with two overlapping cursive lines.", "Usable for printed notes, less for handwriting."),

        # --- TC 3: Scientific Diagram (IMAGE) ---
        (3, 1, 90, 88, 92, 90, 0, "", 0, "", "Accurately detailed Complexes I-IV, chemiosmosis, and ATP synthase rotor rotation.", "Clear student study guide style."),
        (3, 2, 93, 92, 95, 92, 0, "", 0, "", "Provided superb biochemical breakdown with proton counts (4H+, 4H+, 2H+) across membrane.", "Gemini vision recognized all color-coded protein complexes."),
        (3, 3, 95, 94, 96, 88, 0, "", 0, "", "Deep biological explanation explaining reduction potentials and Peter Mitchell's chemiosmotic hypothesis.", "Outstanding depth for college biology majors."),
        (3, 4, 80, 78, 84, 85, 1, "Hallucinated an extra coenzyme Q binding site not present in diagram", 0, "", "Summarized main steps but hallucinated diagram labels.", "Web citations added irrelevant general textbook links."),

        # --- TC 4: Identify Objects (IMAGE) ---
        (4, 1, 88, 86, 90, 90, 0, "", 0, "", "Detected all 5 physics apparatus and stated correct left-to-right spatial sequence.", "Good spatial awareness."),
        (4, 2, 92, 90, 94, 92, 0, "", 0, "", "Identified all 5 pieces of equipment, lens mount type, and estimated focal length setup accurately.", "Exceptional visual localization."),
        (4, 3, 90, 88, 92, 88, 0, "", 0, "", "Correctly labeled apparatus and provided precautions for parallax error in optics experiments.", "Helpful lab safety advice."),
        (4, 4, 82, 80, 84, 85, 0, "", 0, "", "Identified 4 of 5 objects; misidentified millimeter pin as a wire holder.", "Satisfactory general detection."),

        # --- TC 5: Interpret a Chart (IMAGE) ---
        (5, 1, 91, 90, 93, 90, 0, "", 0, "", "Correctly identified 2022 stagflation and calculated 7.9% delta between peak and trough.", "Exact mathematical calculations."),
        (5, 2, 89, 87, 90, 92, 0, "", 0, "", "Identified 2022 stagflation correctly. Approximated peak-to-trough delta at 8.0%.", "Chart trend insights were student friendly."),
        (5, 3, 96, 94, 97, 86, 0, "", 0, "", "Flawlessly extracted dual-axis values, pinpointed exact 2022 stagflation coordinates, and analyzed macroeconomic factors.", "Superior quantitative reasoning."),
        (5, 4, 83, 80, 86, 88, 0, "", 0, "", "Correctly located 2022 stagflation but inverted the GDP subtraction order.", "Helpful Bing search economic context."),

        # --- TC 6: Summarize a PDF (DOCUMENT) ---
        (6, 1, 89, 87, 92, 88, 0, "", 0, "", "Produced crisp 220-word summary contrasting Reno packet loss with BBR bandwidth-delay product.", "Solid summary within token budget."),
        (6, 2, 94, 93, 95, 92, 0, "", 0, "", "Ingested entire 10-page PDF instantly in context. Retained technical graphs and testbed metrics.", "Gemini 1M context excels at PDF ingestion."),
        (6, 3, 98, 96, 98, 84, 0, "", 0, "", "Masterful academic executive summary. Captured research nuances, mathematical bounds, and 10 Gbps throughput data.", "Best summary quality of all tools."),
        (6, 4, 85, 82, 86, 88, 0, "", 0, "", "Edge PDF sidebar summarized major headings effectively but skipped secondary experimental findings.", "Very convenient inside Edge browser."),

        # --- TC 7: Extract Important Points (DOCUMENT) ---
        (7, 1, 92, 90, 94, 90, 0, "", 0, "", "Accurate Markdown table of Red-Black tree operations. Listed rotation bounds (2 for insert, 3 for delete).", "Formatted nicely for student revision."),
        (7, 2, 91, 89, 93, 92, 0, "", 0, "", "Extracted all complexities and explained amortized vs worst-case scenarios.", "Clear and easy to copy."),
        (7, 3, 97, 96, 98, 86, 0, "", 0, "", "Exhaustive extraction with exact textbook theorem citations and color invariant properties.", "Flawless technical precision."),
        (7, 4, 86, 84, 88, 88, 0, "", 0, "", "Generated accurate table but omitted space complexity overhead for color bits.", "Good basic overview."),

        # --- TC 8: Answer Questions from Document (DOCUMENT) ---
        (8, 1, 90, 88, 92, 90, 0, "", 0, "", "Answered Dirty Read and Snapshot Isolation accurately citing sections 4.2 and 4.4.", "Zero hallucinations on ground truth."),
        (8, 2, 93, 91, 94, 92, 0, "", 0, "", "Exact citations with direct quotes from page 4 of document. Deep explanation of MVCC.", "High citation fidelity."),
        (8, 3, 98, 97, 98, 86, 0, "", 0, "", "Impeccable grounded retrieval. Directly quoted paragraph lines and verified boundary conditions.", "Unrivaled trustworthiness for document Q&A."),
        (8, 4, 84, 80, 85, 86, 1, "Cited non-existent external blog post instead of internal section heading", 0, "", "Correct definitions but mixed web search results into local document answer.", "Copilot occasionally pulls outside web info."),

        # --- TC 9: Create Study Notes (DOCUMENT) ---
        (9, 1, 91, 92, 94, 90, 0, "", 0, "", "Generated outstanding MESI state transition table and 5 high-yield flashcard Q&As.", "Extremely helpful for exam prep."),
        (9, 2, 92, 91, 93, 92, 0, "", 0, "", "Clean Markdown study notes, bus snooping definitions, and conceptual diagrams.", "Well structured."),
        (9, 3, 96, 96, 97, 88, 0, "", 0, "", "Pedagogically superior notes with mnemonic 'M-E-S-I' memory aids and deep-dive quiz questions.", "Top choice for studying complex chapters."),
        (9, 4, 85, 83, 86, 88, 0, "", 0, "", "Generated solid bullet points and 4 flashcard questions with concise answers.", "Good quick summary."),

        # --- TC 10: Identify Incorrect Information (DOCUMENT) ---
        (10, 1, 88, 85, 90, 88, 0, "", 0, "", "Caught all 3 planted errors (Waterfall requirements, Sprint duration, Unit testing order).", "Good critical reading skill."),
        (10, 2, 90, 89, 92, 90, 0, "", 0, "", "Successfully flagged all 3 errors with clear explanations of modern Agile and ISTQB testing standards.", "Strong fact verification."),
        (10, 3, 98, 96, 98, 86, 0, "", 0, "", "Caught all 3 planted errors and additionally identified a subtle ambiguity in sprint retrospective definition.", "Gold standard in document error detection."),
        (10, 4, 80, 75, 82, 85, 0, "", 0, "", "Caught 2 of 3 errors; missed the subtle unit testing timeline inversion.", "Reasonable fact-checking ability."),

        # --- TC 11: Transcribe Spoken Audio (AUDIO) ---
        # Note: ChatGPT, Claude, Copilot free tiers do NOT natively accept .mp3 upload in web UI. Tested via transcribed pipe or mobile voice.
        (11, 1, 72, 68, 75, 65, 0, "", 0, "", "Web free tier does not support audio file upload; evaluated via mobile voice playback. Good transcription of Mach cone equation.", "Requires mobile app or third-party audio converter."),
        (11, 2, 95, 94, 96, 95, 0, "", 0, "", "Native .mp3 file upload worked seamlessly in Gemini web interface. Transcribed 310 words with <2% WER. Retained LaTeX math.", "Native audio upload champion. Zero external tools needed."),
        (11, 3, 50, 45, 55, 40, 0, "", 0, "", "Claude free web interface does not accept audio files. Tested using pasted transcript text, rendering audio modality testing indirect.", "Limitation: Free Claude has no native audio ingestion."),
        (11, 4, 65, 60, 70, 60, 0, "", 0, "", "Voice input works only for live mic dictation, not uploaded lecture files. Evaluated via speaker playback to mic.", "No audio file upload feature on free web tier."),

        # --- TC 12: Summarize a Lecture (AUDIO) ---
        (12, 1, 74, 70, 78, 65, 0, "", 0, "", "Evaluated using lecture transcript input. Produced good 190-word summary of microservices trade-offs.", "Content quality is strong once audio is transcribed."),
        (12, 2, 96, 95, 96, 95, 0, "", 0, "", "Listened directly to 15-min audio recording. Synthesized distributed transactions and strangler fig pattern perfectly.", "Best native audio summarizer for college students."),
        (12, 3, 52, 48, 55, 42, 0, "", 0, "", "Required manual transcript feed. Generated outstanding textual analysis but lacks direct audio handling.", "Cannot process raw lecture recordings natively."),
        (12, 4, 68, 65, 72, 62, 0, "", 0, "", "Evaluated through live voice dictation summary. Moderate coverage of saga pattern.", "Workaround needed for audio files."),

        # --- TC 13: Identify Important Topics (AUDIO) ---
        (13, 1, 75, 72, 78, 66, 0, "", 0, "", "Extracted 3 main themes and battery storage subtopics from transcribed discussion text.", "Good topic taxonomy."),
        (13, 2, 94, 93, 95, 94, 0, "", 0, "", "Directly recognized 4 distinct student speakers from audio inflection and mapped debate topics hierarchically.", "Incredible speaker diarization and topic tagging."),
        (13, 3, 53, 50, 56, 42, 0, "", 0, "", "High-level thematic analysis from text transcript, but unable to infer spoken tone or speaker turn-taking.", "No native audio capability."),
        (13, 4, 67, 64, 70, 62, 0, "", 0, "", "Identified main themes from dictated notes. Adequate for quick study notes.", "Limited without file upload."),

        # --- TC 14: Extract Keywords (AUDIO) ---
        (14, 1, 78, 75, 80, 68, 0, "", 0, "", "Extracted 10 key terms (backprop, loss function, etc.) with accurate student definitions from transcript.", "Good definitions once text is available."),
        (14, 2, 96, 96, 97, 95, 0, "", 0, "", "Directly extracted all 10 keywords with accurate timestamps from the audio file. Definitions were spot on.", "Fastest keyword extraction from raw audio."),
        (14, 3, 55, 52, 58, 45, 0, "", 0, "", "Analyzed transcript text and extracted high quality definitions with academic citations.", "Requires separate transcription step."),
        (14, 4, 70, 66, 72, 64, 0, "", 0, "", "Extracted 8 of 10 keywords from audio playback dictation.", "Decent terminology extraction."),

        # --- TC 15: Convert Audio into Study Notes (AUDIO) ---
        (15, 1, 76, 74, 80, 68, 0, "", 0, "", "Converted transcript into clear Glycolysis cheat sheet with net ATP yield (+2 ATP) and 3 quiz questions.", "Great study notes format."),
        (15, 2, 97, 96, 98, 96, 0, "", 0, "", "Converted raw lecture audio into complete revision notes with mnemonic aids, enzyme steps, and practice questions.", "Ultimate student lecture-to-notes workflow."),
        (15, 3, 54, 52, 57, 44, 0, "", 0, "", "Superb study guide generated from transcript text, but failed on direct audio execution.", "Manual transcription required."),
        (15, 4, 69, 66, 72, 65, 0, "", 0, "", "Generated concise summary notes from microphone playback audio.", "Functional with external speaker playback.")
    ]

    for item in raw_evals:
        tc_id, tool_id, acc, comp, rel, ease, hall, hall_desc, unsafe, unsafe_desc, resp, notes = item
        w_score = calculate_weighted_score(acc, comp, rel, ease)
        evaluations.append((
            tool_id,
            tc_id,
            "Reshma Anandhan",
            resp,
            acc,
            comp,
            rel,
            ease,
            w_score,
            hall,
            hall_desc,
            unsafe,
            unsafe_desc,
            notes,
            1 # is_demo_data = 1 (clearly labeled benchmark)
        ))
        
    cursor.executemany("""
    INSERT INTO evaluations 
    (tool_id, test_case_id, evaluator_name, response_text, accuracy_score, completeness_score, relevance_score, ease_of_use_score, weighted_score, hallucination_detected, hallucination_details, unsafe_outdated_detected, unsafe_outdated_details, student_notes, is_demo_data)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, evaluations)

def seed_before_after(cursor):
    """
    Seeds Before and After fact-checking verification records showing how initial ratings
    changed after students rigorously audited AI responses against official textbooks/ground truth.
    """
    records = [
        (
            4, 3, 86.0, 80.7, -5.3,
            "Copilot hallucinated an extra coenzyme Q binding site in the mitochondria diagram not shown in source graphic.",
            "Initial review assumed the web search citation was legitimate. Close comparison with Lehninger Principles of Biochemistry revealed the cited blog post was inaccurate.",
            "Enforce cross-referencing AI generated citations against standard college textbooks rather than trusting web preview snippets.",
            "Verified"
        ),
        (
            4, 8, 89.0, 84.1, -4.9,
            "Copilot cited an external commercial blog rather than the provided PDF textbook Section 4.2 heading.",
            "Student fact-checker verified that the AI retrieved external web content instead of strictly parsing the uploaded document.",
            "Use prompt constraints such as 'Rely exclusively on the provided text; do not extrapolate from web sources'.",
            "Verified"
        ),
        (
            2, 2, 85.0, 90.7, +5.7,
            "Initial evaluation penalized Gemini for missing Greek letters that were actually obscured in the original notebook shadow.",
            "Re-examined high-resolution raw scan; Gemini correctly detected the ink smudge and accurately transcribed the surrounding calculus context.",
            "Audit image clarity before grading OCR tasks to ensure ground truth matches visual reality.",
            "Verified"
        ),
        (
            3, 10, 93.0, 95.8, +2.8,
            "Initial reviewer thought Claude only flagged 3 errors; full audit showed Claude also identified an implicit requirement flaw in the test document.",
            "Audited against IEEE Software Engineering standards; Claude's critique was technically valid and enhanced student understanding.",
            "Reward models that provide deeper contextual critique beyond superficial keyword matching.",
            "Verified"
        ),
        (
            1, 11, 80.0, 70.8, -9.2,
            "Initial score overestimated ChatGPT web audio capabilities due to confusion with mobile voice mode.",
            "Verified that on the free web interface, ChatGPT cannot accept .mp3 or .wav uploads directly without external plugins or third-party transcription.",
            "Differentiate mobile voice assistant testing from standard desktop browser multimodal file testing in student rubrics.",
            "Verified"
        )
    ]
    cursor.executemany("""
    INSERT INTO before_after_records
    (tool_id, test_case_id, initial_score, verified_score, score_delta, errors_identified, fact_check_notes, improvement_strategy, verification_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

def seed_quiz(cursor):
    """
    Seeds a 10-question multiple-choice quiz covering multimodal AI evaluation for students.
    """
    quiz_data = [
        (
            1,
            "Which free multimodal AI tool natively allows direct upload and analysis of audio files (.mp3, .wav) through its web interface?",
            "Claude (Anthropic)",
            "Google Gemini (1.5 Flash)",
            "ChatGPT (Free Web Tier)",
            "Microsoft Copilot (Web)",
            "B",
            "Google Gemini is currently the only major free AI tool that natively accepts direct audio and video file uploads via its web interface and AI Studio, thanks to its native multimodal 1M token context window.",
            "Audio Capabilities"
        ),
        (
            2,
            "In the Capstone 57 weighted scoring methodology, what percentage weight is assigned to 'Accuracy'?",
            "20%",
            "25%",
            "40%",
            "50%",
            "C",
            "Accuracy is weighted at 40%, reflecting its paramount importance in academic study tasks. Completeness is 25%, Relevance is 20%, and Ease of Use is 15%.",
            "Evaluation Methodology"
        ),
        (
            3,
            "What is a primary limitation of Claude 3.5 Sonnet on the free tier (claude.ai) when used for college coursework?",
            "It cannot parse PDF documents.",
            "It has strict dynamic message limits (approx. 10-25 messages every 5 hours) and no direct audio file upload.",
            "It has a high hallucination rate compared to other models.",
            "It cannot read images or flowcharts.",
            "B",
            "While Claude 3.5 Sonnet excels at reasoning, document analysis, and has a very low hallucination rate, its free tier enforces strict dynamic message quotas and lacks direct audio file uploads.",
            "Free Tier Limitations"
        ),
        (
            4,
            "When evaluating an AI tool on PDF document summarization, what does a 'hallucination' mean?",
            "The AI generates an answer in under 2 seconds.",
            "The AI formats the output in Markdown instead of plain text.",
            "The AI presents fabricated, unverified, or non-existent facts as if they were in the source document.",
            "The AI asks the user to re-upload the document.",
            "C",
            "A hallucination occurs when an AI generates confident-sounding assertions, citations, or facts that do not exist in the source document or in ground truth reality.",
            "Failure Indicators"
        ),
        (
            5,
            "How does Microsoft Copilot integrate with the Microsoft Edge browser for document study?",
            "It automatically converts all PDFs into PowerPoint slides.",
            "It provides a built-in sidebar assistant that can summarize and query open local and web PDFs without separate uploads.",
            "It replaces the student's browser with a command-line interface.",
            "It requires a paid Copilot Pro subscription for Edge reading.",
            "B",
            "Copilot in Microsoft Edge features a dedicated sidebar that can read, summarize, and answer questions directly from any PDF currently opened in the browser tab for free.",
            "Document Processing"
        ),
        (
            6,
            "Why is 'Context Window' critical when evaluating multimodal AI tools on large textbooks or lecture transcripts?",
            "A larger context window makes the text font bigger.",
            "A larger context window allows the model to process extensive multi-chapter documents without truncating or forgetting earlier sections.",
            "A larger context window guarantees zero hallucinations.",
            "A larger context window eliminates the need for internet access.",
            "B",
            "Models with large context windows (like Gemini's 1,000,000 tokens) can ingest entire books or hour-long lectures at once, preserving cross-chapter references and global context.",
            "AI Architecture"
        ),
        (
            7,
            "Which evaluation metric measures whether the AI response addressed every required constraint in the prompt without skipping parts?",
            "Accuracy",
            "Ease of Use",
            "Relevance",
            "Completeness",
            "D",
            "Completeness (weighted at 25%) evaluates whether the AI answered all sub-questions, covered all specified constraints, and did not truncate key components.",
            "Evaluation Methodology"
        ),
        (
            8,
            "When using multimodal AI tools for college study, what is an essential student privacy best practice?",
            "Upload confidential personal data to test AI security.",
            "Avoid uploading unredacted personal IDs, private exam papers, or proprietary university documents into public free AI tools.",
            "Share AI account passwords with classmates.",
            "Disable all browser privacy settings.",
            "B",
            "Public free AI tiers may use uploaded data for model training unless opted out. Students must never upload sensitive personal, academic, or institutional confidential materials.",
            "Ethics & Privacy"
        ),
        (
            9,
            "What is the recommended prompt technique to prevent an AI from hallucinating when answering questions from a study PDF?",
            "Write 'Do not lie' in all caps.",
            "Direct the AI to: 'Answer strictly using facts stated in the provided text. If information is not present, state that it is unavailable.'",
            "Use only 1-word prompts.",
            "Ask the AI to guess the most probable answer.",
            "B",
            "Explicit grounding constraints instruct the AI to anchor its responses strictly to the provided document and penalize speculative answers.",
            "Prompt Engineering"
        ),
        (
            10,
            "In optical character recognition (OCR) of handwritten lecture notes, what is typically the most challenging element for AI models?",
            "Printed headlines in bold font.",
            "Cursive handwriting with specialized mathematical symbols, subscripts, and diagram annotations.",
            "Standard bullet point dots.",
            "Page numbers located at the footer.",
            "B",
            "Complex cursive handwriting combined with non-linear math formulas, superscripts, and irregular line spacing poses the greatest challenge for vision models.",
            "Image Understanding"
        )
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO quiz_questions
    (question_number, question, option_a, option_b, option_c, option_d, correct_option, explanation, category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, quiz_data)

def seed_checklist(cursor):
    """
    Seeds initial audit checklist records to demonstrate verification tracking.
    """
    audits = [
        (
            1, "Microsoft Copilot", "Explain a Scientific Diagram (Mitochondria)",
            1, 0, 1, 0, 0, 1, 0, "Moderate", 71.4,
            "Copilot hallucinated an extra enzyme subunit and cited an unverified blog post. Image understanding was generally fair, but external search grounding hallucinated."
        ),
        (
            2, "Google Gemini", "Transcribe Spoken Audio (Physics Lecture)",
            0, 0, 0, 0, 0, 0, 0, "Low", 100.0,
            "Near-perfect transcription with zero hallucinations or safety risks. Directly processed native mp3 audio without errors."
        ),
        (
            3, "Claude", "Summarize a PDF (TCP Congestion Research)",
            0, 0, 0, 0, 0, 0, 0, "Low", 100.0,
            "Impeccable document synthesis. All facts grounded strictly in source text. No omissions or security leaks."
        ),
        (
            4, "ChatGPT", "Identify Incorrect Information (Agile vs Waterfall)",
            0, 0, 0, 0, 0, 0, 0, "Low", 100.0,
            "Correctly identified all three planted errors and provided clear, validated corrections."
        )
    ]
    cursor.executemany("""
    INSERT INTO checklist_audits
    (id, tool_name, task_name, has_incorrect_info, has_missing_info, has_hallucinations, has_unsafe_advice, has_outdated_info, has_source_reliability_issues, has_privacy_risks, risk_level, reliability_score, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, audits)

def seed_prompts(cursor):
    """
    Seeds curated prompt library for students across modalities.
    """
    prompts = [
        (
            1, "IMAGE", "Comprehensive Diagram & Circuit Analyzer",
            "Analyze the attached diagram in detail. 1) Identify all component symbols and their interconnects. 2) Trace the flow of signals from input to output. 3) Provide the mathematical or logical governing equation in LaTeX. 4) Explain common points of failure in this circuit design.",
            "Structured schematic breakdown with equations and failure modes.",
            "Claude / ChatGPT", "Advanced"
        ),
        (
            2, "IMAGE", "Handwritten Math OCR & Step-by-Step Solver",
            "Transcribe the handwritten equations from this image verbatim into LaTeX. Check if the mathematical derivation is correct. If there is an arithmetic or algebraic error in the student's handwritten steps, highlight the exact step and show the corrected calculation.",
            "Accurate LaTeX OCR plus mathematical validation.",
            "Google Gemini / ChatGPT", "Intermediate"
        ),
        (
            3, "IMAGE", "Chart & Graph Data Table Extractor",
            "Examine this chart carefully. 1) Identify the chart type, independent variable (X-axis), and dependent variable (Y-axis) with units. 2) Reconstruct the underlying raw data into a clean Markdown table. 3) Summarize the primary trend and identify any statistical anomalies.",
            "Tabular data extraction and statistical trend summary.",
            "Claude / Google Gemini", "Intermediate"
        ),
        (
            4, "DOCUMENT", "High-Yield Exam Cram Notes Generator",
            "Read the attached study chapter. Create a high-yield exam preparation guide containing: 1) Executive 1-paragraph summary, 2) Glossary of top 10 key technical terms with definitions, 3) Comparison table of core concepts, 4) 5 high-probability exam practice questions with detailed model answers.",
            "Structured exam review packet with Q&A.",
            "Claude / ChatGPT", "Intermediate"
        ),
        (
            5, "DOCUMENT", "Socratic Fact-Checker & Contradiction Finder",
            "Act as a rigorous peer-reviewer. Analyze the attached document and identify: 1) Any internal logical contradictions, 2) Statements unsupported by cited evidence, 3) Outdated scientific assumptions compared to current 2026 standards. Flag the exact paragraph for each issue.",
            "Rigorous critique and fact verification list.",
            "Claude", "Advanced"
        ),
        (
            6, "DOCUMENT", "Multi-Paper Research Synthesizer",
            "Compare the attached research documents. Synthesize how the methodologies differ, contrast their quantitative performance metrics, and formulate a 300-word synthesis of where their conclusions converge and diverge.",
            "Comparative multi-document synthesis.",
            "Google Gemini / Claude", "Advanced"
        ),
        (
            7, "AUDIO", "Lecture to Active Recall Flashcards",
            "Listen to this recorded lecture audio. 1) Generate a 250-word overview of the core thesis. 2) Extract 10 concept-definition pairs formatted as Anki flashcards (Front: Concept/Question, Back: Concise Explanation). 3) Highlight any dates, formulas, or testable facts mentioned by the speaker.",
            "Anki-ready flashcards and concise summary from audio.",
            "Google Gemini", "Intermediate"
        ),
        (
            8, "AUDIO", "Colloquium Speaker Diarization & Action Items",
            "Analyze this recorded meeting/seminar audio. 1) Identify distinct speakers and summarize each participant's primary viewpoint. 2) List all agreed-upon project action items and assigned roles. 3) Extract key unanswered questions raised during the Q&A session.",
            "Speaker-attributed minutes and action items.",
            "Google Gemini", "Advanced"
        ),
        (
            9, "AUDIO", "Fast Lecture Keyword Glossary Builder",
            "Process this audio recording. Identify every domain-specific technical term introduced by the lecturer. For each term, state: 1) Exact timestamp when introduced, 2) Lecturer's spoken definition, 3) A simplified real-world analogy to help a student memorize it.",
            "Timestamped terminology glossary with analogies.",
            "Google Gemini", "Intermediate"
        )
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO prompt_library
    (id, category, title, prompt_text, target_outcome, recommended_tool, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, prompts)
