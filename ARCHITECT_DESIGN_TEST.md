```markdown
# Technical Design Document: Notification System

## 1. Overview

This document outlines the design for a robust notification system integrated into the Codex IA platform. The system will allow sending notifications to users via Email and SMS, based on their configured preferences. It will support high-volume notification delivery through queueing and maintain a history of sent notifications for auditing and analysis.  The system will be designed to integrate seamlessly with the existing Codex IA architecture.

## 2. System Architecture

### 2.1. Architecture Diagram (Mermaid)

```mermaid
graph LR
    subgraph Codex IA
        A[CodexAgent] --> B(Notification Service API);
        C[EvolutionAgent] --> B;
        D[VisionaryAgent] --> B;
        E[ArchitectAgent] --> B;
    end

    subgraph Notification Service
        B --> F[Notification Queue (Redis)];
        F --> G[Notification Worker(s)];
        G --> H{User Preferences};
        H --> I{Email Provider (e.g., SendGrid, AWS SES)};
        H --> J{SMS Provider (e.g., Twilio, AWS SNS)};
        G --> K[Notification History (PostgreSQL)];
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#f9f,stroke:#333,stroke-width:2px
```

### 2.2. Components

*   **Notification Service API:** Exposes endpoints for other Codex IA components (Agents) to trigger notifications.  This will be a REST API.
*   **Notification Queue (Redis):**  A message queue to handle high-volume notification requests asynchronously.  Redis is chosen for its speed and suitability for queueing.
*   **Notification Worker(s):**  Background worker processes that consume messages from the notification queue, determine the user's preferred notification method, and send the notification via the appropriate provider.  These workers will be scalable to handle varying load.
*   **User Preferences:**  Stores user-specific notification preferences (Email, SMS, Both, None).  This will likely be stored in the existing database used by Codex IA (assumed to be PostgreSQL or similar).
*   **Email Provider (e.g., SendGrid, AWS SES):**  A third-party service for sending emails.
*   **SMS Provider (e.g., Twilio, AWS SNS):**  A third-party service for sending SMS messages.
*   **Notification History (PostgreSQL):**  Stores a record of all sent notifications, including recipient, message content, delivery status, and timestamps.  This will be a new table in the existing Codex IA database.

### 2.3. Data Flow

1.  A Codex IA Agent (e.g., `CodexAgent`, `EvolutionAgent`) needs to send a notification.
2.  The Agent calls the Notification Service API, providing the recipient user ID, notification type, and message content.
3.  The Notification Service API publishes a message to the Notification Queue (Redis).
4.  A Notification Worker picks up the message from the queue.
5.  The worker retrieves the user's notification preferences from the database.
6.  Based on the preferences, the worker sends the notification via the Email Provider and/or SMS Provider.
7.  The worker records the notification details (recipient, message, status, timestamp) in the Notification History database.

## 3. Data Model

### 3.1. User Preferences (Database Table - Assuming PostgreSQL)

This table will likely already exist or can be easily added to the existing user profile table.  If a separate table is needed:

```sql
CREATE TABLE user_notification_preferences (
    user_id UUID PRIMARY KEY, -- Assuming UUID for user IDs
    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    sms_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

### 3.2. Notification History (Database Table - PostgreSQL)

```sql
CREATE TABLE notification_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    notification_type VARCHAR(255) NOT NULL, -- e.g., "code_review_request", "optimization_complete"
    message_content TEXT NOT NULL,
    email_sent BOOLEAN NOT NULL DEFAULT FALSE,
    sms_sent BOOLEAN NOT NULL DEFAULT FALSE,
    email_delivery_status VARCHAR(255), -- e.g., "sent", "delivered", "bounced"
    sms_delivery_status VARCHAR(255),   -- e.g., "sent", "delivered", "failed"
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user_notification_preferences(user_id) -- Or the appropriate user table
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- If not already enabled
```

### 3.3. Notification Queue Message (JSON)

```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "notification_type": "code_review_request",
  "message_content": "A code review is requested for your latest commit.",
  "metadata": {
    "code_review_id": "f1g2h3i4-j5k6-l7m8-n9o0-p1q2r3s4t5u6"
  }
}
```

## 4. API Design

### 4.1. Endpoint: `/notifications` (POST)

*   **Description:**  Triggers a notification to be sent to a user.
*   **Method:** POST
*   **Request Body (JSON):**

```json
{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "notification_type": "code_review_request",
  "message_content": "A code review is requested for your latest commit.",
  "metadata": {
    "code_review_id": "f1g2h3i4-j5k6-l7m8-n9o0-p1q2r3s4t5u6"
  }
}
```

*   **Response Codes:**
    *   202 Accepted:  Notification request successfully queued.
    *   400 Bad Request:  Invalid request body.
    *   500 Internal Server Error:  Error queuing the notification.
*   **Example Response (202 Accepted):**

```json
{
  "message": "Notification request accepted for processing."
}
```

### 4.2. Authentication

The Notification Service API will need to be authenticated to prevent unauthorized access.  This can be achieved using API keys or JWT tokens, consistent with the existing Codex IA authentication mechanism.

## 5. Implementation Plan

1.  **Database Setup:**
    *   Create the `notification_history` table in the existing Codex IA database.
    *   Ensure the `user_notification_preferences` table exists (or add columns to the existing user table).
    *   Enable UUID generation if not already enabled.
2.  **Notification Service API Development:**
    *   Implement the `/notifications` endpoint.
    *   Implement authentication for the API.
    *   Integrate with the Notification Queue (Redis).
3.  **Notification Queue Setup:**
    *   Deploy and configure a Redis instance.
4.  **Notification Worker Development:**
    *   Implement the worker process to consume messages from the queue.
    *   Implement logic to retrieve user preferences.
    *   Integrate with Email and SMS providers (e.g., Twilio, SendGrid).  Consider using environment variables for API keys.
    *   Implement error handling and retry mechanisms.
    *   Implement logging for debugging and monitoring.
    *   Implement logic to record notification history in the database.
5.  **Integration with Codex IA Agents:**
    *   Modify the relevant Codex IA Agents (e.g., `CodexAgent`, `EvolutionAgent`, `VisionaryAgent`, `ArchitectAgent`) to call the Notification Service API when necessary.
6.  **Testing:**
    *   Unit tests for the Notification Service API and workers.
    *   Integration tests to ensure end-to-end functionality.
    *   Load testing to ensure the system can handle high volumes of notifications.
7.  **Deployment:**
    *   Deploy the Notification Service API and workers to the production environment.
    *   Configure monitoring and alerting.

## 6.  Integration with Existing Codex IA Context

*   **Context Manager (`codex_ia/core/context.py`):**  The `ContextManager` might need to be updated to include information about the Notification Service API endpoint, allowing agents to discover and use it.  This could be a configuration setting loaded by the `ContextManager`.
*   **LLM Client (`codex_ia/core/llm_client.py`):**  The `LLMClient` could be used to generate notification messages based on context.  For example, it could be used to create a summary of code changes for a code review notification.
*   **Knowledge Base (`codex_ia/core/knowledge_base.py`):**  The `KnowledgeBase` could store templates for common notification messages, allowing for consistent and personalized notifications.

## 7. Future Considerations

*   **Notification Templates:** Implement a system for managing notification templates, allowing for easy customization of notification messages.
*   **User Interface:**  Develop a user interface for managing notification preferences.
*   **Analytics:**  Implement analytics to track notification delivery rates and user engagement.
*   **Webhooks:**  Allow users to subscribe to notifications via webhooks.
*   **Support for additional notification channels:**  Consider adding support for other notification channels, such as Slack or Microsoft Teams.
```