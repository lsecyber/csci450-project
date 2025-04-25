# csci450-project
This repository houses our CSCI450 group project: the STEM Summer Camp Registration Tracking System. It combines a C++ backend for efficient data processing and business logic with a Vue.js frontend to deliver an intuitive, fast-to-build user interface (languages/frameworks chosen to align with our team’s expertise and minimize development time).
[View Project Proposal](https://docs.google.com/document/d/1cg5LX8voT3fD8cpvl5Lv9KpxlI0-Bvyw6eWG5MOu3UE/edit?tab=t.0 "Project Proposal - Google Docs")

## Database Schema
### families
| Field        | Type          | Attributes                                  |
| ------------ | ------------- | ------------------------------------------- |
| `id`         | INT           | PRIMARY KEY, AUTO_INCREMENT                 |
| `name`       | VARCHAR(100)  | NOT NULL                                    |
| `email`      | VARCHAR(255)  | NOT NULL, UNIQUE                            |
| `phone`      | VARCHAR(20)   | NULL                                        |
| `created_at` | DATETIME      | NOT NULL, DEFAULT CURRENT_TIMESTAMP         |
| `updated_at` | DATETIME      | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### camp_sessions
| Field        | Type         | Attributes                                  |
| ------------ | ------------ | ------------------------------------------- |
| `id`         | INT          | PRIMARY KEY, AUTO_INCREMENT                 |
| `name`       | VARCHAR(100) | NOT NULL                                    |
| `start_date` | DATE         | NOT NULL                                    |
| `end_date`   | DATE         | NOT NULL                                    |
| `capacity`   | INT          | NOT NULL                                    |
| `created_at` | DATETIME     | NOT NULL, DEFAULT CURRENT_TIMESTAMP         |
| `updated_at` | DATETIME     | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### campers
| Field       | Type                     | Attributes                                |
| ----------- | ------------------------ | ----------------------------------------- |
| `id`        | INT                      | PRIMARY KEY, AUTO_INCREMENT               |
| `family_id` | INT                      | NOT NULL, FOREIGN KEY → `families(id)`    |
| `first_name`| VARCHAR(50)              | NOT NULL                                  |
| `last_name` | VARCHAR(50)              | NOT NULL                                  |
| `dob`       | DATE                     | NULL                                      |
| `gender`    | ENUM('M','F','Other')    | NULL                                      |
| `created_at`| DATETIME                 | NOT NULL, DEFAULT CURRENT_TIMESTAMP       |
| `updated_at`| DATETIME                 | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### registrations
| Field              | Type                                | Attributes                                              |
| ------------------ | ----------------------------------- | ------------------------------------------------------- |
| `id`               | INT                                 | PRIMARY KEY, AUTO_INCREMENT                             |
| `camper_id`        | INT                                 | NOT NULL, FOREIGN KEY → `campers(id)`                   |
| `session_id`       | INT                                 | NOT NULL, FOREIGN KEY → `camp_sessions(id)`             |
| `status`           | ENUM('registered','waitlisted')     | NOT NULL                                                |
| `waitlist_position`| INT                                 | NULL (only for waitlisted)                              |
| `registered_at`    | DATETIME                            | NOT NULL, DEFAULT CURRENT_TIMESTAMP                     |
| `updated_at`       | DATETIME                            | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

> **Index:** `UNIQUE(camper_id, session_id)` to prevent duplicate sign-ups.

### notifications
| Field             | Type                                                    | Attributes                                           |
| ----------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| `id`              | INT                                                     | PRIMARY KEY, AUTO_INCREMENT                          |
| `registration_id` | INT                                                     | NOT NULL, FOREIGN KEY → `registrations(id)`          |
| `type`            | ENUM('confirmation','waitlist','availability')          | NOT NULL                                             |
| `to_email`        | VARCHAR(255)                                            | NOT NULL                                             |
| `subject`         | VARCHAR(255)                                            | NOT NULL                                             |
| `html_content`    | TEXT                                                    | NOT NULL                                             |
| `sent_at`         | DATETIME                                                | NOT NULL, DEFAULT CURRENT_TIMESTAMP                  |

---

#### Reporting
Generate summary and trend reports by querying `registrations` joined with `camp_sessions` (e.g. counts per session, wait-list lengths). All timestamps support audit and performance monitoring.
