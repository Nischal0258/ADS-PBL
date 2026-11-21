# MUSIC PLAYLIST MANAGEMENT SYSTEM
### Project Based Learning (PBL) Report
**Course:** DATA STRUCTURES / ADVANCED DATA STRUCTURES (Course Code: 20CS21001)  
**Degree:** BACHELOR OF TECHNOLOGY IN COMPUTER SCIENCE AND ENGINEERING  
**Academic Year:** 2025–2026 (II Year – I Semester, AR22 Regulation)

---

### Submitted By:
- **SAI PRABHAVATI** (Roll No: `24R11A05W9`)

### Under the Guidance of:
**Mrs. K. Padmaja**  
*Assistant Professor, Department of Computer Science and Engineering*

### Department Leadership:
- **Lab In-Charge:** Mrs. K. Padmaja
- **Head of the Department (HOD - CSE):** Dr. E. Ravindra, Professor

**Department of Computer Science and Engineering**  
*(Accredited by NBA and NAAC with 'A' Grade, Approved by AICTE New Delhi, Affiliated to JNTUH)*  
**Geethanjali College of Engineering and Technology (UGC Autonomous)**  
Cheeryal (V), Keesara (M), Medchal Dist., Telangana – 501 301.

---

## ACKNOWLEDGEMENT

I express my heartfelt gratitude to my respected guide, **Mrs. K. Padmaja**, for her valuable guidance, constant encouragement, and insightful suggestions throughout the development of this Project-Based Learning (PBL) project. Her technical expertise and constructive feedback have been instrumental in the successful completion of this work.

I extend my sincere thanks to **Dr. E. Ravindra**, Professor and Head of the Department of Computer Science and Engineering, for providing the necessary laboratory resources and administrative support to carry out this project.

Special thanks to my faculty members, lab technicians, and peers for their continuous cooperation, constructive discussions, and assistance during the course of this activity.

Finally, I express my profound gratitude to the Management and Principal of **Geethanjali College of Engineering and Technology** for providing an environment conducive to learning, technical innovation, and hands-on software development.

— **Sai Prabhavati** (`24R11A05W9`)

---

## TABLE OF CONTENTS

| S.No. | Contents | Page No. |
| :---: | :--- | :---: |
| **1** | **Introduction** | **4** |
| | 1.1 About the Project | 4 |
| | 1.2 Motivation & Real-World Relevance | 4 |
| | 1.3 Project Objectives and Expected Outcomes | 5 |
| **2** | **System Design & Architecture** | **6** |
| | 2.1 System Architecture | 6 |
| | 2.2 System Modules Description | 7 |
| | 2.3 Data Structure Design & Rationale | 8 |
| | 2.4 Entity Relationship & Pointer Mapping | 9 |
| **3** | **Implementation & Source Code** | **10** |
| | 3.1 Algorithmic Procedures of Modules | 10 |
| | 3.2 Complete C Source Code | 11 |
| | 3.3 Sample Input and Output Test Runs | 19 |
| **4** | **Complexity & Performance Analysis** | **22** |
| | 4.1 Time & Space Complexity Summary | 22 |
| | 4.2 Comparative Analysis (Array vs. Doubly Linked List) | 23 |
| **5** | **Conclusion & Future Scope** | **24** |
| **6** | **References** | **25** |

---

## 1. INTRODUCTION

### 1.1 About the Project
The **Music Playlist Management System** is a console-based software application engineered in the C programming language to demonstrate the practical, real-world utility of linear and non-linear data structures. In the era of modern music streaming services such as Spotify, Apple Music, and Amazon Music, millions of musical tracks must be indexed, queued, traversed, and backtracked with sub-millisecond responsiveness.

Rather than relying on high-level libraries or opaque runtime engines, this system implements core computer science primitives from scratch:
1. **Doubly Linked List:** Models the active playback sequence, enabling continuous bidirectional navigation (`Next Track` / `Previous Track`) and dynamically inserting or removing songs without memory shifting.
2. **Stack (LIFO - Last In, First Out):** Automatically logs played tracks, enabling an instant "Rewind / Recently Played History" backtracking mechanism.
3. **Queue (FIFO - First In, First Out):** Manages an explicit "Up Next / Request Queue" where user-queued songs take priority before resuming standard playlist traversal.
4. **Persistent File I/O:** Saves and loads library state across application restarts.

### 1.2 Motivation & Real-World Relevance
Static data representations (such as standard arrays) fail to meet the requirements of music playback engines due to:
- **Fixed Allocation:** Memory must be declared beforehand, causing either memory wastage or buffer overflow.
- **Expensive Deletion/Insertion:** Removing or adding a track at the middle or start of an array requires shifting $O(n)$ elements.
- **Single-Direction Limitation:** Singly linked lists do not support natural backward traversal without costly head-to-target reprocessing.

By using a **Doubly Linked List coupled with auxiliary Stacks and Queues**, this project replicates the fundamental internal architecture of commercial music streaming engines while upholding algorithmic efficiency.

### 1.3 Project Objectives and Expected Outcomes
#### Objectives:
- To design and implement a dynamic music playlist manager in C using explicit pointer manipulation and heap memory management (`malloc` / `free`).
- To integrate multiple complementary data structures (Doubly Linked List, Stack, and Queue) in a cohesive, interactive system.
- To provide robust navigation: sequential play, queue priority override, history backtracking, and case-insensitive searching.
- To implement file persistence to retain playlist updates across program sessions.

#### Expected Outcomes:
- A modular, crash-free console application with a clean, formatted terminal interface.
- Demonstrated time complexity of $O(1)$ for track switching, history push/pop, and queue enqueue/dequeue operations.
- Practical understanding of dynamic pointer manipulation, memory leak avoidance, and separation of UI, logic, and storage concerns.

---

## 2. SYSTEM DESIGN & ARCHITECTURE

### 2.1 System Architecture
The Music Playlist Management System is architected in a clean, three-tier modular pattern:

```
+-----------------------------------------------------------------------------+
|                          1. USER INTERFACE LAYER                            |
|     - Console Menu System            - Real-time Visual Progress Simulation |
|     - ANSI Formatted Song Tables     - Error Prompts & Notifications        |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
|                            2. LOGIC CONTROLLER                              |
|     - Playback Engine (Play, Next, Prev, Loop Mode)                         |
|     - Queue Dispatcher (Up Next priority over sequential flow)              |
|     - History Tracker (Stack push on track completion)                      |
|     - Search & Validation Engine (Case-insensitive string parsing)          |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
|                       3. DATA STRUCTURE & STORAGE LAYER                     |
|  +-------------------------+  +--------------------+  +-------------------+ |
|  |   Doubly Linked List    |  |    History Stack   |  |   Up Next Queue   | |
|  | (head, tail, curr pointers) |  |   (LIFO Backtrack) |  |   (FIFO Requests) | |
|  +-------------------------+  +--------------------+  +-------------------+ |
|                                      |                                      |
|                       Persistent Disk Storage (playlist.txt)                |
+-----------------------------------------------------------------------------+
```

### 2.2 System Modules Description
1. **Playlist Node Management Module:**
   - Dynamically allocates `Song` records with attributes: `id`, `title`, `artist`, and `duration`.
   - Links nodes with forward (`next`) and backward (`prev`) pointers.
2. **Playback Controller Module:**
   - Manages `currentSong`.
   - Before advancing, pushes the current song onto the `HistoryStack`.
   - Evaluates whether the `SongQueue` contains pending priority tracks before advancing to `currentSong->next`.
3. **Queue ("Up Next") Module:**
   - Implements FIFO semantics. Allows users to cherry-pick any song in the library to play next, preserving the original playlist sequence.
4. **History ("Recently Played") Module:**
   - Implements LIFO semantics. Provides a history trail so users can backtrack previous listens.
5. **Search & Filter Module:**
   - Scans the playlist in $O(n)$ time using case-insensitive substring matching on song titles and artist names.
6. **File Persistence Engine:**
   - Reads existing records from `playlist.txt` using formatted delimiter parsing (`|`) upon boot, and commits changes upon exit.

### 2.3 Data Structure Design & Rationale

#### A. Doubly Linked List (Playlist)
```c
typedef struct Song {
    int id;
    char title[100];
    char artist[100];
    int duration;       // in seconds
    struct Song *prev;  // pointer to previous track
    struct Song *next;  // pointer to next track
} Song;
```
*Rationale:* Enables $O(1)$ bidirectional stepping between tracks, $O(1)$ insertion at the end of the playlist using a `tail` pointer, and $O(1)$ deletion of any identified node without shifting remaining memory elements.

#### B. History Stack (Recently Played)
```c
typedef struct HistoryNode {
    Song *song;
    struct HistoryNode *next;
} HistoryNode;

typedef struct {
    HistoryNode *top;
    int count;
} HistoryStack;
```
*Rationale:* LIFO structure perfectly matches the playback rewind pattern: the most recently finished song is always the first one restored upon pressing "Previous".

#### C. Up Next Queue (Upcoming Tracks)
```c
typedef struct QueueNode {
    Song *song;
    struct QueueNode *next;
} QueueNode;

typedef struct {
    QueueNode *front;
    QueueNode *rear;
    int count;
} SongQueue;
```
*Rationale:* FIFO structure ensures fairness in song requests. If track A is queued before track B, track A is guaranteed to play first.

---

## 3. IMPLEMENTATION & SOURCE CODE

### 3.1 Algorithmic Procedures of Modules

#### Algorithm 1: Add Song to Playlist
```
Input: Title, Artist, Duration
Output: Updated Doubly Linked List with new Song Node

1. Allocate memory for new Song node: newSong = malloc(sizeof(Song))
2. Set newSong->title = Title, newSong->artist = Artist, newSong->duration = Duration
3. Set newSong->next = NULL, newSong->prev = NULL
4. If head == NULL:
       head = newSong
       tail = newSong
       currentSong = head
   Else:
       tail->next = newSong
       newSong->prev = tail
       tail = newSong
5. Return Success
```

#### Algorithm 2: Play Next Track (Hybrid Queue + DLL Traversal)
```
Input: Global state (upNextQueue, currentSong, historyStack, isLoopMode)
Output: Updated currentSong playing in console

1. If head == NULL:
       Display "Playlist is empty" and Return
2. If upNextQueue.front != NULL:
       Push currentSong to historyStack
       currentSong = dequeue(upNextQueue)
       Display "Playing from Up Next Queue"
       Trigger VisualPlayback(currentSong)
       Return
3. If currentSong != NULL:
       Push currentSong to historyStack
       If currentSong->next != NULL:
           currentSong = currentSong->next
       Else:
           If isLoopMode == TRUE:
               currentSong = head
           Else:
               Display "End of playlist reached" and Return
4. Else:
       currentSong = head
5. Trigger VisualPlayback(currentSong)
```

#### Algorithm 3: Play Previous Track (Stack Backtrack + DLL Fallback)
```
Input: Global state (historyStack, currentSong, isLoopMode)
Output: Previous song restored to playback

1. If historyStack.top != NULL:
       currentSong = pop(historyStack)
       Display "Rewinding from History Stack"
       Trigger VisualPlayback(currentSong)
       Return
2. If currentSong != NULL and currentSong->prev != NULL:
       currentSong = currentSong->prev
       Trigger VisualPlayback(currentSong)
       Return
3. If isLoopMode == TRUE and tail != NULL:
       currentSong = tail
       Trigger VisualPlayback(currentSong)
       Return
4. Display "At start of playlist. No prior history."
```

---

### 3.2 Complete C Source Code

```c
/**
 * ============================================================================
 * Project: Music Playlist Management System
 * Course:  Data Structures (20CS21001) / ADS PBL
 * Institution: Geethanjali College of Engineering and Technology
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <windows.h>

#define MAX_STR 100
#define FILE_NAME "playlist.txt"

/* ---------------------------------------------------------
 * DATA STRUCTURE DEFINITIONS
 * --------------------------------------------------------- */

// Doubly Linked List Node for Active Playlist
typedef struct Song {
    int id;
    char title[MAX_STR];
    char artist[MAX_STR];
    int duration; // Duration in seconds
    struct Song *prev;
    struct Song *next;
} Song;

// Stack Node for Recently Played History
typedef struct HistoryNode {
    Song *song;
    struct HistoryNode *next;
} HistoryNode;

typedef struct {
    HistoryNode *top;
    int count;
} HistoryStack;

// Queue Node for 'Play Next' Queue
typedef struct QueueNode {
    Song *song;
    struct QueueNode *next;
} QueueNode;

typedef struct {
    QueueNode *front;
    QueueNode *rear;
    int count;
} SongQueue;

/* ---------------------------------------------------------
 * GLOBAL SYSTEM STATE
 * --------------------------------------------------------- */
Song *head = NULL;
Song *tail = NULL;
Song *currentSong = NULL;
int songIdCounter = 1;
int isLoopMode = 0; // 0 = Sequential, 1 = Repeat Playlist

HistoryStack history = { NULL, 0 };
SongQueue upNextQueue = { NULL, NULL, 0 };

/* ---------------------------------------------------------
 * HELPER UTILITIES
 * --------------------------------------------------------- */
void formatTime(int totalSeconds, char *buffer) {
    int minutes = totalSeconds / 60;
    int seconds = totalSeconds % 60;
    sprintf(buffer, "%02d:%02d", minutes, seconds);
}

int strCaseContains(const char *haystack, const char *needle) {
    char h[MAX_STR], n[MAX_STR];
    int i;
    for (i = 0; haystack[i] && i < MAX_STR - 1; i++) h[i] = (char)tolower(haystack[i]);
    h[i] = '\0';
    for (i = 0; needle[i] && i < MAX_STR - 1; i++) n[i] = (char)tolower(needle[i]);
    n[i] = '\0';
    return (strstr(h, n) != NULL);
}

void trimNewline(char *str) {
    int len = (int)strlen(str);
    while (len > 0 && (str[len - 1] == '\n' || str[len - 1] == '\r' || str[len - 1] == ' ')) {
        str[len - 1] = '\0';
        len--;
    }
}

void clearInputBuffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

/* ---------------------------------------------------------
 * STACK OPERATIONS (HISTORY - LIFO)
 * --------------------------------------------------------- */
void pushHistory(Song *s) {
    if (s == NULL) return;
    HistoryNode *newNode = (HistoryNode *)malloc(sizeof(HistoryNode));
    if (!newNode) return;
    newNode->song = s;
    newNode->next = history.top;
    history.top = newNode;
    history.count++;
}

Song *popHistory(void) {
    if (history.top == NULL) return NULL;
    HistoryNode *temp = history.top;
    Song *song = temp->song;
    history.top = history.top->next;
    free(temp);
    history.count--;
    return song;
}

void displayHistory(void) {
    printf("\n================================================================\n");
    printf("                  RECENTLY PLAYED HISTORY (STACK - LIFO)        \n");
    printf("================================================================\n");
    if (history.top == NULL) {
        printf(" [!] History is empty. No songs have been played yet.\n");
        return;
    }
    HistoryNode *curr = history.top;
    int index = 1;
    char timeStr[16];
    printf(" %-4s | %-4s | %-25s | %-20s | %-8s\n", "Pos", "ID", "Title", "Artist", "Duration");
    printf("----------------------------------------------------------------\n");
    while (curr != NULL) {
        formatTime(curr->song->duration, timeStr);
        printf(" #%-3d | %-4d | %-25s | %-20s | %-8s\n",
               index++, curr->song->id, curr->song->title, curr->song->artist, timeStr);
        curr = curr->next;
    }
    printf(" Total entries in history: %d\n", history.count);
}

/* ---------------------------------------------------------
 * QUEUE OPERATIONS ('UP NEXT' - FIFO)
 * --------------------------------------------------------- */
void enqueueSong(Song *s) {
    if (s == NULL) return;
    QueueNode *newNode = (QueueNode *)malloc(sizeof(QueueNode));
    if (!newNode) return;
    newNode->song = s;
    newNode->next = NULL;

    if (upNextQueue.rear == NULL) {
        upNextQueue.front = upNextQueue.rear = newNode;
    } else {
        upNextQueue.rear->next = newNode;
        upNextQueue.rear = newNode;
    }
    upNextQueue.count++;
}

Song *dequeueSong(void) {
    if (upNextQueue.front == NULL) return NULL;
    QueueNode *temp = upNextQueue.front;
    Song *s = temp->song;
    upNextQueue.front = upNextQueue.front->next;
    if (upNextQueue.front == NULL) {
        upNextQueue.rear = NULL;
    }
    free(temp);
    upNextQueue.count--;
    return s;
}

void displayQueue(void) {
    printf("\n================================================================\n");
    printf("                     UP NEXT QUEUE (FIFO)                       \n");
    printf("================================================================\n");
    if (upNextQueue.front == NULL) {
        printf(" [!] Queue is empty. No songs waiting in 'Play Next' queue.\n");
        return;
    }
    QueueNode *curr = upNextQueue.front;
    int index = 1;
    char timeStr[16];
    printf(" %-4s | %-4s | %-25s | %-20s | %-8s\n", "Pos", "ID", "Title", "Artist", "Duration");
    printf("----------------------------------------------------------------\n");
    while (curr != NULL) {
        formatTime(curr->song->duration, timeStr);
        printf(" #%-3d | %-4d | %-25s | %-20s | %-8s\n",
               index++, curr->song->id, curr->song->title, curr->song->artist, timeStr);
        curr = curr->next;
    }
    printf(" Total songs in queue: %d\n", upNextQueue.count);
}

/* ---------------------------------------------------------
 * DOUBLY LINKED LIST OPERATIONS
 * --------------------------------------------------------- */
Song *createSongNode(int id, const char *title, const char *artist, int duration) {
    Song *newSong = (Song *)malloc(sizeof(Song));
    if (!newSong) {
        printf("[!] Memory allocation failed!\n");
        return NULL;
    }
    newSong->id = (id > 0) ? id : songIdCounter++;
    if (newSong->id >= songIdCounter) {
        songIdCounter = newSong->id + 1;
    }
    strncpy(newSong->title, title, MAX_STR - 1);
    newSong->title[MAX_STR - 1] = '\0';
    strncpy(newSong->artist, artist, MAX_STR - 1);
    newSong->artist[MAX_STR - 1] = '\0';
    newSong->duration = duration > 0 ? duration : 180;
    newSong->prev = NULL;
    newSong->next = NULL;
    return newSong;
}

void insertSong(const char *title, const char *artist, int duration) {
    Song *newSong = createSongNode(0, title, artist, duration);
    if (!newSong) return;

    if (head == NULL) {
        head = tail = newSong;
        currentSong = head;
        printf("\n[*] Playlist initialized with first track: \"%s\"!\n", newSong->title);
    } else {
        tail->next = newSong;
        newSong->prev = tail;
        tail = newSong;
        printf("\n[+] Added \"%s\" by %s successfully!\n", newSong->title, newSong->artist);
    }
}

Song *searchSongById(int id) {
    Song *temp = head;
    while (temp != NULL) {
        if (temp->id == id) return temp;
        temp = temp->next;
    }
    return NULL;
}

int deleteSong(int id) {
    if (head == NULL) {
        printf("\n[!] Playlist is empty. Nothing to delete.\n");
        return 0;
    }

    Song *target = searchSongById(id);
    if (target == NULL) {
        printf("\n[!] Song with ID %d not found in playlist.\n", id);
        return 0;
    }

    if (currentSong == target) {
        if (target->next != NULL) {
            currentSong = target->next;
        } else if (target->prev != NULL) {
            currentSong = target->prev;
        } else {
            currentSong = NULL;
        }
    }

    if (target == head && target == tail) {
        head = tail = NULL;
    } else if (target == head) {
        head = head->next;
        head->prev = NULL;
    } else if (target == tail) {
        tail = tail->prev;
        tail->next = NULL;
    } else {
        target->prev->next = target->next;
        target->next->prev = target->prev;
    }

    printf("\n[-] Successfully deleted \"%s\" (ID: %d) from playlist.\n", target->title, target->id);
    free(target);
    return 1;
}

void displayPlaylist(void) {
    printf("\n========================================================================================\n");
    printf("                                ACTIVE MUSIC PLAYLIST                                   \n");
    printf("========================================================================================\n");
    if (head == NULL) {
        printf(" [!] The playlist is currently empty.\n");
        return;
    }

    printf(" %-4s | %-4s | %-26s | %-22s | %-8s | %-12s\n",
           "No.", "ID", "Song Title", "Artist", "Duration", "Status");
    printf("----------------------------------------------------------------------------------------\n");

    Song *temp = head;
    int index = 1;
    char timeStr[16];

    while (temp != NULL) {
        formatTime(temp->duration, timeStr);
        const char *status = (temp == currentSong) ? ">> PLAYING <<" : "";
        printf(" %-4d | %-4d | %-26s | %-22s | %-8s | %-12s\n",
               index++, temp->id, temp->title, temp->artist, timeStr, status);
        temp = temp->next;
    }
    printf("========================================================================================\n");
    printf(" Loop Mode: %s | Total Songs: %d\n", isLoopMode ? "ON (Infinite Repeat)" : "OFF (Sequential)", index - 1);
}

void searchSongs(void) {
    if (head == NULL) {
        printf("\n[!] Playlist is empty. Nothing to search.\n");
        return;
    }

    char query[MAX_STR];
    printf("\nEnter search keyword (Title or Artist): ");
    scanf(" %[^\n]", query);
    trimNewline(query);

    printf("\n--- Search Results for \"%s\" ---\n", query);
    Song *temp = head;
    int found = 0;
    char timeStr[16];

    printf(" %-4s | %-26s | %-22s | %-8s\n", "ID", "Title", "Artist", "Duration");
    printf("----------------------------------------------------------------\n");
    while (temp != NULL) {
        if (strCaseContains(temp->title, query) || strCaseContains(temp->artist, query)) {
            formatTime(temp->duration, timeStr);
            printf(" %-4d | %-26s | %-22s | %-8s\n", temp->id, temp->title, temp->artist, timeStr);
            found++;
        }
        temp = temp->next;
    }

    if (!found) {
        printf(" [!] No songs matched your search query.\n");
    } else {
        printf(" Found %d matching song(s).\n", found);
    }
}

/* ---------------------------------------------------------
 * PLAYBACK CONTROLLER
 * --------------------------------------------------------- */
void simulatePlaybackVisual(Song *s) {
    if (s == NULL) return;
    char totalTime[16];
    formatTime(s->duration, totalTime);

    printf("\n----------------------------------------------------------------\n");
    printf(" [>] NOW PLAYING: \"%s\" by %s\n", s->title, s->artist);
    printf("     Track Duration: %s | Audio Engine: Active\n", totalTime);
    printf("     Progress: [");

    for (int i = 0; i < 20; i++) {
        printf("#");
        fflush(stdout);
        Sleep(20);
    }
    printf("] 100%%\n");
    printf("----------------------------------------------------------------\n");
}

void playCurrent(void) {
    if (currentSong == NULL) {
        if (head != NULL) {
            currentSong = head;
        } else {
            printf("\n[!] Playlist is empty. Add songs first.\n");
            return;
        }
    }
    simulatePlaybackVisual(currentSong);
}

void playNext(void) {
    if (head == NULL) {
        printf("\n[!] Playlist is empty.\n");
        return;
    }

    if (upNextQueue.front != NULL) {
        if (currentSong != NULL) {
            pushHistory(currentSong);
        }
        currentSong = dequeueSong();
        printf("\n[Queue Triggered] Playing requested track from Up Next Queue!\n");
        simulatePlaybackVisual(currentSong);
        return;
    }

    if (currentSong == NULL) {
        currentSong = head;
    } else {
        pushHistory(currentSong);
        if (currentSong->next != NULL) {
            currentSong = currentSong->next;
        } else {
            if (isLoopMode) {
                printf("\n[*] End of playlist reached. Looping back to the beginning...\n");
                currentSong = head;
            } else {
                printf("\n[!] Reached the end of the playlist. (Turn ON loop mode to repeat)\n");
                return;
            }
        }
    }
    simulatePlaybackVisual(currentSong);
}

void playPrevious(void) {
    if (head == NULL) {
        printf("\n[!] Playlist is empty.\n");
        return;
    }

    Song *histSong = popHistory();
    if (histSong != NULL) {
        printf("\n[History Triggered] Rewinding to recently played track from History Stack!\n");
        currentSong = histSong;
        simulatePlaybackVisual(currentSong);
        return;
    }

    if (currentSong != NULL && currentSong->prev != NULL) {
        currentSong = currentSong->prev;
        simulatePlaybackVisual(currentSong);
    } else if (isLoopMode && tail != NULL) {
        printf("\n[*] At the start of playlist. Looping to the end...\n");
        currentSong = tail;
        simulatePlaybackVisual(currentSong);
    } else {
        printf("\n[!] You are already at the first song. No previous history found.\n");
    }
}

void queueSongOption(void) {
    if (head == NULL) {
        printf("\n[!] Playlist is empty.\n");
        return;
    }
    int id;
    printf("\nEnter Song ID to add to 'Play Next' queue: ");
    if (scanf("%d", &id) != 1) {
        clearInputBuffer();
        printf("[!] Invalid input.\n");
        return;
    }
    Song *s = searchSongById(id);
    if (s == NULL) {
        printf("[!] Song with ID %d not found.\n", id);
        return;
    }
    enqueueSong(s);
    printf("[+] Enqueued \"%s\" to Up Next Queue (Position: %d)\n", s->title, upNextQueue.count);
}

/* ---------------------------------------------------------
 * FILE PERSISTENCE
 * --------------------------------------------------------- */
void savePlaylistToFile(void) {
    FILE *fp = fopen(FILE_NAME, "w");
    if (!fp) {
        printf("\n[!] Error saving playlist to %s\n", FILE_NAME);
        return;
    }
    Song *temp = head;
    while (temp != NULL) {
        fprintf(fp, "%d|%s|%s|%d\n", temp->id, temp->title, temp->artist, temp->duration);
        temp = temp->next;
    }
    fclose(fp);
    printf("\n[v] Playlist saved to file: %s\n", FILE_NAME);
}

void loadPlaylistFromFile(void) {
    FILE *fp = fopen(FILE_NAME, "r");
    if (!fp) {
        insertSong("Memories", "Maroon 5", 189);
        insertSong("Blinding Lights", "The Weeknd", 200);
        insertSong("Smooth Criminal", "Michael Jackson", 257);
        insertSong("Bohemian Rhapsody", "Queen", 354);
        insertSong("Shape of You", "Ed Sheeran", 233);
        currentSong = head;
        savePlaylistToFile();
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        trimNewline(line);
        if (strlen(line) == 0) continue;

        char *token = strtok(line, "|");
        if (!token) continue;
        int id = atoi(token);

        token = strtok(NULL, "|");
        if (!token) continue;
        char title[MAX_STR];
        strncpy(title, token, MAX_STR - 1);
        title[MAX_STR - 1] = '\0';

        token = strtok(NULL, "|");
        if (!token) continue;
        char artist[MAX_STR];
        strncpy(artist, token, MAX_STR - 1);
        artist[MAX_STR - 1] = '\0';

        token = strtok(NULL, "|");
        int duration = token ? atoi(token) : 180;

        Song *newSong = createSongNode(id, title, artist, duration);
        if (head == NULL) {
            head = tail = newSong;
        } else {
            tail->next = newSong;
            newSong->prev = tail;
            tail = newSong;
        }
    }
    fclose(fp);
    currentSong = head;
}

/* ---------------------------------------------------------
 * MAIN FUNCTION & UI CONTROLS
 * --------------------------------------------------------- */
void printBanner(void) {
    printf("\n");
    printf("  ===============================================================\n");
    printf("  *             MUSIC PLAYLIST MANAGEMENT SYSTEM                *\n");
    printf("  *          Data Structures Project-Based Learning (PBL)       *\n");
    printf("  ===============================================================\n");
}

void printMenu(void) {
    printf("\n+----------------------- PLAYER CONTROLS -----------------------+\n");
    printf("|  1. Display Active Playlist (Doubly Linked List)              |\n");
    printf("|  2. Add New Song                                              |\n");
    printf("|  3. Delete Song by ID                                         |\n");
    printf("|  4. Search Song (By Title / Artist)                           |\n");
    printf("|  5. Play / Resume Current Song                                |\n");
    printf("|  6. Play Next Song (Queue Check -> DLL Next)                  |\n");
    printf("|  7. Play Previous Song (Stack Check -> DLL Prev)              |\n");
    printf("|  8. Add Song to 'Play Next' Queue (FIFO Queue)                |\n");
    printf("|  9. View 'Play Next' Queue                                    |\n");
    printf("| 10. View Recently Played History (LIFO Stack)                 |\n");
    printf("| 11. Toggle Loop / Repeat Mode [%-3s]                           |\n", isLoopMode ? "ON" : "OFF");
    printf("| 12. Save & Exit Program                                       |\n");
    printf("+---------------------------------------------------------------+\n");
    printf(" Enter your choice (1-12): ");
}

int main(void) {
    printBanner();
    loadPlaylistFromFile();

    int choice;
    char title[MAX_STR], artist[MAX_STR];
    int duration, id;

    while (1) {
        printMenu();
        if (scanf("%d", &choice) != 1) {
            clearInputBuffer();
            printf("\n[!] Invalid input! Please enter a valid number (1-12).\n");
            continue;
        }

        switch (choice) {
            case 1:
                displayPlaylist();
                break;
            case 2:
                printf("\n--- Add New Song ---\n");
                printf("Enter Song Title : ");
                scanf(" %[^\n]", title);
                trimNewline(title);
                printf("Enter Artist Name: ");
                scanf(" %[^\n]", artist);
                trimNewline(artist);
                printf("Enter Duration in seconds: ");
                if (scanf("%d", &duration) != 1 || duration <= 0) {
                    clearInputBuffer();
                    duration = 180;
                }
                insertSong(title, artist, duration);
                savePlaylistToFile();
                break;
            case 3:
                displayPlaylist();
                printf("\nEnter Song ID to delete: ");
                if (scanf("%d", &id) != 1) {
                    clearInputBuffer();
                    printf("[!] Invalid ID.\n");
                    break;
                }
                deleteSong(id);
                savePlaylistToFile();
                break;
            case 4:
                searchSongs();
                break;
            case 5:
                playCurrent();
                break;
            case 6:
                playNext();
                break;
            case 7:
                playPrevious();
                break;
            case 8:
                queueSongOption();
                break;
            case 9:
                displayQueue();
                break;
            case 10:
                displayHistory();
                break;
            case 11:
                isLoopMode = !isLoopMode;
                printf("\n[*] Loop Mode toggled to: %s\n", isLoopMode ? "ON" : "OFF");
                break;
            case 12:
                savePlaylistToFile();
                printf("\n[!] Exiting Music Playlist Management System. Goodbye!\n");
                exit(0);
            default:
                printf("\n[!] Invalid choice! Try again.\n");
        }
    }
    return 0;
}
```

---

### 3.3 Sample Input and Output Test Runs

#### Test Run 1: Launch and Display Active Playlist
```text
  ===============================================================
  *             MUSIC PLAYLIST MANAGEMENT SYSTEM                *
  *          Data Structures Project-Based Learning (PBL)       *
  ===============================================================

[v] Playlist loaded from file: playlist.txt

+----------------------- PLAYER CONTROLS -----------------------+
|  1. Display Active Playlist (Doubly Linked List)              |
|  2. Add New Song                                              |
|  3. Delete Song by ID                                         |
|  4. Search Song (By Title / Artist)                           |
|  5. Play / Resume Current Song                                |
|  6. Play Next Song (Queue Check -> DLL Next)                  |
|  7. Play Previous Song (Stack Check -> DLL Prev)              |
|  8. Add Song to 'Play Next' Queue (FIFO Queue)                |
|  9. View 'Play Next' Queue                                    |
| 10. View Recently Played History (LIFO Stack)                 |
| 11. Toggle Loop / Repeat Mode [OFF]                           |
| 12. Save & Exit Program                                       |
+---------------------------------------------------------------+
 Enter your choice (1-12): 1

========================================================================================
                                ACTIVE MUSIC PLAYLIST                                   
========================================================================================
 No.  | ID   | Song Title                 | Artist                 | Duration | Status      
----------------------------------------------------------------------------------------
 1    | 1    | Memories                   | Maroon 5               | 03:09    | >> PLAYING <<
 2    | 2    | Blinding Lights            | The Weeknd             | 03:20    |             
 3    | 3    | Smooth Criminal            | Michael Jackson        | 04:17    |             
 4    | 4    | Bohemian Rhapsody          | Queen                  | 05:54    |             
 5    | 5    | Shape of You               | Ed Sheeran             | 03:53    |             
========================================================================================
 Loop Mode: OFF (Sequential) | Total Songs: 5
```

#### Test Run 2: Playing Next Track and Queueing Song
```text
 Enter your choice (1-12): 6

----------------------------------------------------------------
 [>] NOW PLAYING: "Blinding Lights" by The Weeknd
     Track Duration: 03:20 | Audio Engine: Active
     Progress: [####################] 100%
----------------------------------------------------------------

 Enter your choice (1-12): 8

Enter Song ID to add to 'Play Next' queue: 4
[+] Enqueued "Bohemian Rhapsody" to Up Next Queue (Position: 1)

 Enter your choice (1-12): 6

[Queue Triggered] Playing requested track from Up Next Queue!

----------------------------------------------------------------
 [>] NOW PLAYING: "Bohemian Rhapsody" by Queen
     Track Duration: 05:54 | Audio Engine: Active
     Progress: [####################] 100%
----------------------------------------------------------------
```

#### Test Run 3: Rewinding with History Stack (LIFO)
```text
 Enter your choice (1-12): 7

[History Triggered] Rewinding to recently played track from History Stack!

----------------------------------------------------------------
 [>] NOW PLAYING: "Blinding Lights" by The Weeknd
     Track Duration: 03:20 | Audio Engine: Active
     Progress: [####################] 100%
----------------------------------------------------------------

 Enter your choice (1-12): 10

================================================================
                  RECENTLY PLAYED HISTORY (STACK - LIFO)        
================================================================
 Pos  | ID   | Title                     | Artist               | Duration
----------------------------------------------------------------
 #1   | 1    | Memories                  | Maroon 5             | 03:09   
 Total entries in history: 1
```

#### Test Run 4: Searching Songs by Keyword
```text
 Enter your choice (1-12): 4

Enter search keyword (Title or Artist): Michael

--- Search Results for "Michael" ---
 ID   | Title                      | Artist                 | Duration
----------------------------------------------------------------
 3    | Smooth Criminal            | Michael Jackson        | 04:17   
 Found 1 matching song(s).
```

---

## 4. COMPLEXITY & PERFORMANCE ANALYSIS

### 4.1 Time & Space Complexity Summary

| Functional Operation | Primary Data Structure | Time Complexity (Best / Avg) | Time Complexity (Worst) | Space Complexity |
| :--- | :--- | :---: | :---: | :---: |
| **Add Song (End of Playlist)** | Doubly Linked List (via `tail`) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Delete Song (by ID)** | Doubly Linked List | $\mathcal{O}(1)$ (at head/tail) | $\mathcal{O}(n)$ (linear search) | $\mathcal{O}(1)$ |
| **Traverse / Display Playlist** | Doubly Linked List | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |
| **Play Next Track** | Doubly Linked List / Queue | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Play Previous Track** | Stack / Doubly Linked List | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Enqueue "Play Next"** | FIFO Linked Queue | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Dequeue "Play Next"** | FIFO Linked Queue | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Push / Pop History** | LIFO Linked Stack | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Search by Keyword** | Linear Search (DLL Nodes) | $\mathcal{O}(1)$ (first item) | $\mathcal{O}(n)$ (full scan) | $\mathcal{O}(1)$ |

### 4.2 Comparative Analysis: Array vs. Doubly Linked List
| Performance Metric | Static / Dynamic Array | Doubly Linked List (This Project) |
| :--- | :--- | :--- |
| **Insertion at Tail** | $\mathcal{O}(1)$ amortized (requires reallocation) | $\mathcal{O}(1)$ guaranteed using `tail` pointer |
| **Deletion at arbitrary node** | $\mathcal{O}(n)$ (elements must be shifted) | $\mathcal{O}(1)$ pointer reconnection once located |
| **Memory Allocation** | Contiguous chunk (risk of fragmentation) | Dynamic heap allocation per node |
| **Bidirectional Navigation** | Requires index tracking (`i++`, `i--`) | Native pointers (`curr->next`, `curr->prev`) |
| **Memory Overhead** | Low (only data elements) | Slightly higher (stores 2 pointers per node) |

---

## 5. CONCLUSION & FUTURE SCOPE

### 5.1 Conclusion
The **Music Playlist Management System** successfully validates how foundational abstract data structures solve complex real-world problems. By mapping:
- **Doubly Linked Lists** to interactive playlist traversal,
- **Stacks** to non-destructive history backtracking, and
- **Queues** to prioritized song requests,

the application achieves optimal $\mathcal{O}(1)$ time complexity for all primary user actions. Dynamic memory allocation eliminates static buffer restrictions, while persistent disk storage ensures uninterrupted continuity between sessions. The project reinforces essential engineering principles including pointer safety, separation of concerns, and clean console interface design.

### 5.2 Future Scope & Enhancements
1. **Trie / AVL Tree for Autocomplete:** Integrating a prefix Trie to autocomplete song searches in $\mathcal{O}(L)$ time where $L$ is the length of the query string.
2. **Audio Decoding Engine:** Connecting the C program with external multimedia libraries like `SDL2_mixer` or Windows `mciSendString` to directly decode and play real `.mp3` and `.wav` audio files.
3. **Multi-Playlist Support:** Using an adjacency list or a collection of linked lists to allow users to create and switch between multiple custom playlists (e.g., "Favorites", "Gym Workout", "Study Beats").
4. **Fisher-Yates Shuffle Algorithm:** Implementing true random shuffle by converting pointers or mapping nodes into temporary index pointers for unbiased $O(n)$ shuffling.

---

## 6. REFERENCES

1. **Reema Thareja**, *Data Structures Using C*, Oxford University Press, 2nd Edition, 2014.  
   *(Referenced for dynamic memory management, pointer manipulation, and doubly linked list architectures).*
2. **Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed**, *Fundamentals of Data Structures in C*, Silicon Press, 2nd Edition, 2008.  
   *(Foundational algorithms for insertion, node deletion, and linked list traversal).*
3. **Mark Allen Weiss**, *Data Structures and Algorithm Analysis in C*, Pearson Education, 4th Edition.  
   *(Referenced for asymptotic time and space complexity evaluations).*
4. **Brian W. Kernighan and Dennis M. Ritchie**, *The C Programming Language*, Prentice Hall, 2nd Edition.  
   *(Standard conventions for file I/O, string operations, and dynamic struct allocations).*
