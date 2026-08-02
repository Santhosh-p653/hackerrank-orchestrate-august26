
# WhatsApp Message Routing & AI Orchestration Pipeline

## Overview

This project implements an AI-style message routing and prioritization system that analyzes WhatsApp-like messages and decides the best notification action:

* **`notify`** — Immediately alert the user.
* **`digest`** — Include the message in a summarized notification batch.
* **`mute`** — Suppress unnecessary or harmful notifications.

The system uses a context-aware orchestration architecture combining message analysis, user behavior, historical retrieval, and multiple specialized analyzers to produce explainable routing decisions.

---

## Architecture


```
Dataset Files
│
▼
Data Loader
│
▼
Context Builder
│
┌──────────────────┴──────────────────┐
│                                     │
▼                                     ▼
Retrieval System             User / Message Context
│                                     │
└──────────────────┬──────────────────┘
│
▼
Analyzer Pipeline
┌───────────────────┼───────────────────┐
│                   │                   │
▼                   ▼                   ▼
Safety              Priority         Personalization
Analyzer            Analyzer            Analyzer
│                   │                   │
▼                   ▼                   ▼
Business             Group               Media
Analyzer            Analyzer            Analyzer
│                   │                   │
▼                   ▼
Notification      Message Type
Analyzer            Analyzer
└───────────────────┬───────────────────┘
│
▼
Decision Engine
│
▼
Output Generator
│
▼
output.csv
```

---

## Project Structure

```text
code/
├── main.py
├── config.py
├── data_loader.py
├── context_builder.py
├── retriever.py
├── decision_engine.py
├── output_generator.py
├── models.py
├── analyzers/
│   ├── safety.py
│   ├── priority.py
│   ├── personalization.py
│   ├── notification_load.py
│   ├── message_type.py
│   ├── business.py
│   ├── group.py
│   └── media.py
├── requirements.txt
└── README.md

```
## Data Processing Pipeline
### 1. Data Loader
The data loader reads all required datasets:
 * Messages
 * Users
 * Groups
 * Business accounts
 * Message history
 * Message events
 * Images
 * Voice notes
 * Notification summaries
 * Historical examples
The loaded data is passed directly into the context layer.
### 2. Context Builder
The context builder creates a complete message context by combining:
 * Current message information
 * User behavior
 * Group information
 * Business relationship
 * Previous conversations
 * Message events
 * Media information
This avoids making decisions based solely on raw message text.
> **Example Workflow:**
>  * **Message:** *"Your payment failed"*
>  * **Additional Context:**
>    * User frequently interacts with this account
>    * Previous payment conversations exist
>    * User usually opens notifications quickly
>  * **Result:** Final routing decision becomes significantly more accurate.
> 
## Retrieval System
The retriever uses similarity matching to find historically similar examples.
 * **Technology:** RapidFuzz similarity matching
 * **Purpose:**
   * Provide evidence for decisions
   * Improve consistency with previous examples
   * Support system explainability
Retrieved examples are included in the final output under evidence_message_ids.
## Analyzer System
The system relies on multiple specialized analyzers working in tandem:
### Safety Analyzer
Detects potentially risky messages (e.g., scam indicators, suspicious keywords, fraud-like patterns).
 * **Influences:** notify, mute
### Priority Analyzer
Determines urgency based on intent and keywords.
 * **High priority:** *"urgent"*, *"immediately"*, *"payment"*, *"now"*
 * **Low priority:** Greetings, casual conversation
 * **Influences:** notify score
### Personalization Analyzer
Evaluates user behavior patterns (e.g., frequently opened/replied messages, notification dismissal history).
 * **Influences:** notify, digest decisions
### Notification Load Analyzer
Considers notification fatigue metrics (e.g., current alert volume, frequent dismissals).
 * **Influences:** digest decisions
### Business Analyzer
Checks user relationships with business accounts (e.g., past interactions, promotional preferences, activity history).
 * **Influences:** notify, mute, digest
### Group Analyzer
Analyzes group-related signals (e.g., family groups, frequently forwarded content, group relevance).
### Media Analyzer
Evaluates media context (e.g., presence of images or voice notes) to adjust importance scores.
## Decision Engine
The decision engine aggregates scores across all specialized analyzers:
### Notify Score
Calculated from priority, personal relevance, group importance, business relevance, media importance, notification behavior, and safety signals. High-urgency messages receive additional notification priority.
### Digest Score
Calculated for low-urgency or moderately important messages suitable for batching (e.g., greetings, casual forwarded messages).
### Mute Score
Applied to suspicious messages, low-value content, or unwanted interactions.
> **Rule:** The highest scoring action becomes the final prediction.
> 
## Explainability
Every prediction produces structured explanations containing:
 * Selected action
 * Message type
 * Detailed reasoning
 * Confidence score
 * Supporting evidence messages
```text
Decision=notify.
Safety: Suspicious keywords detected.
Priority: Urgent payment keywords detected.
User profile: User frequently interacts with this account.

```
## Output Format
 * **Generated File:** dataset/output.csv
 * **Schema:** message_id, action, message_type, reason, confidence, evidence_message_ids
### Example CSV Output
```csv
message_id,action,message_type,reason,confidence,evidence_message_ids
msg_023,notify,payment,"Decision=notify. Payment urgency detected",0.38,sample_msg_005;sample_msg_004

```
## Running the Project
### Prerequisites
 * **Python:** 3.12+
### Installation
```bash
pip install -r requirements.txt

```
### Generate Predictions
```bash
python main.py

```
Outputs to dataset/output.csv.
### Testing
Run the test suite with pytest:
```bash
pytest -q

```
The test suite validates:
 * Output file generation
 * Required CSV column presence
 * Action validity
 * Total prediction counts
## Design Philosophy
The system follows a modular orchestration approach:
 1. **Focused Responsibility:** Each analyzer handles a single domain metric.
 2. **Decoupled Architecture:** Context generation is strictly separated from decision logic.
 3. **Transparent Logic:** Decisions are fully explainable with trace evidence.
 4. **Extensibility:** New analyzers can be introduced without modifying core orchestration logic.
## Future Improvements
 * LLM-based reasoning layer
 * Advanced vector embeddings for semantic retrieval
 * User-specific adaptive learning models
 * Online feedback optimization
 * Multimodal message content understanding
```
