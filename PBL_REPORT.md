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

I express my heartfelt gratitude to my respected project guide, **Mrs. K. Padmaja**, Assistant Professor, Department of Computer Science and Engineering, for her valuable guidance, continuous encouragement, and constructive feedback throughout the course of this Project-Based Learning (PBL) activity. Her insights into data structures and software engineering principles were pivotal in successfully designing and implementing this system.

I extend my sincere thanks to **Dr. E. Ravindra**, Professor and Head of the Department of Computer Science and Engineering, for his constant administrative support and for providing the modern computing and laboratory facilities necessary to complete this project.

Special thanks to my faculty members, lab instructors, and peers for their continuous cooperation, constructive discussions, and assistance during the course of this activity.

Finally, I express my profound gratitude to the Management and Principal of **Geethanjali College of Engineering and Technology** for providing an environment conducive to learning, technical innovation, and hands-on software development.

— **Sai Prabhavati** (`24R11A05W9`)

---

## TABLE OF CONTENTS

| S.No. | Contents | Page No. |
| :---: | :--- | :---: |
| **1** | **Introduction** | **4** |
| | 1.1 About the Project | 4 |
| | 1.2 Motivation & Real-World Problem Statement | 4 |
| | 1.3 Project Objectives and Expected Outcomes | 5 |
| **2** | **System Design & Architecture** | **6** |
| | 2.1 System Architecture | 6 |
| | 2.2 Functional Modules Description | 7 |
| | 2.3 Data Structures Selection & Technical Rationale | 8 |
| **3** | **Implementation & Source Code** | **9** |
| | 3.1 Algorithmic Design of Core Modules | 9 |
| | 3.2 Complete C Source Code | 10 |
| | 3.3 Sample Input and Output Test Runs | 16 |
| **4** | **Complexity & Performance Analysis** | **18** |
| | 4.1 Time & Space Complexity Summary | 18 |
| | 4.2 Comparative Analysis: Arrays vs. Doubly Linked Lists | 19 |
| **5** | **Conclusion & Future Scope** | **20** |
| **6** | **References** | **21** |

---

## 1. INTRODUCTION

### 1.1 About the Project
The **Music Playlist Management System** is a streamlined console software application engineered in the C programming language. It demonstrates how fundamental data structures—specifically Doubly Linked Lists and Stacks—are practically applied to solve real-world music organization and playback challenges. Commercial audio streaming platforms such as Spotify and Apple Music manage large song libraries, dynamic playlist modifications, and playback histories. This project reproduces the internal mechanics of playlist management from first principles in C, using manual pointer operations and dynamic memory allocation.

### 1.2 Motivation & Real-World Problem Statement
In simple implementations, song collections are often placed in fixed or dynamic arrays. However, arrays present significant limitations for playlist applications:
- **Expensive Insertions:** Inserting a new song into an array requires shifting elements sequentially in memory, costing $\mathcal{O}(n)$ time.
- **Costly Deletions:** Deleting a song from an array leaves gaps or requires shifting all subsequent elements.
- **Single-Direction Limitation:** Singly linked lists only support forward movement; inspecting previous elements requires restarting traversal from the head.

By implementing a **Doubly Linked List**, songs can be added to the playlist dynamically in $\mathcal{O}(1)$ time and deleted cleanly without shifting remaining elements. Concurrently, a **Linked Stack** records playback history (LIFO), allowing users to track previously played songs effortlessly.

### 1.3 Project Objectives and Expected Outcomes
#### Objectives:
- To design and develop a console-based music playlist system in C using dynamic memory allocation (`malloc` and `free`).
- To implement a Doubly Linked List supporting dynamic additions, deletions by ID, and clean playlist display.
- To provide direct song search and playback by Song Title or Artist name.
- To incorporate a Last-In-First-Out (LIFO) Stack that automatically logs previously played songs.
- To provide file persistence to automatically load and save songs across executions.

#### Expected Outcomes:
- A clean, intuitive, and responsive console application with a concise player controls menu.
- Immediate playback display without unnecessary delays or artificial progress bars.
- Practical verification of $\mathcal{O}(1)$ insertion, deletion, and stack operations.

---

## 2. SYSTEM DESIGN & ARCHITECTURE

### 2.1 System Architecture
The system follows a three-tier modular architecture ensuring clean separation of user input, playback logic, and data storage:

```
+-----------------------------------------------------------------------------+
|                          1. USER INTERFACE LAYER                            |
|     - Streamlined Console Menu (1-6)    - Clean Song Table Display          |
|     - Direct Title/Artist Search Input  - Instant Now Playing Banner        |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
|                            2. LOGIC CONTROLLER                              |
|     - Playback Engine (Instant Play by Title / Artist)                      |
|     - Dynamic History Stack Tracker (LIFO auto-push on playback change)     |
|     - Case-Insensitive String Matcher (Substring search)                    |
|     - Node Insertion & Safe Pointer Deletion Management                     |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
|                       3. DATA STRUCTURE & STORAGE LAYER                     |
|  +-------------------------------------+  +-------------------------------+ |
|  |   Doubly Linked List (Playlist)     |  |    History Stack (LIFO)       | |
|  | (head, tail, currentSong pointers)  |  |   (tracks played songs)       | |
|  +-------------------------------------+  +-------------------------------+ |
|                                      |                                      |
|                       Persistent Disk Storage (playlist.txt)                |
+-----------------------------------------------------------------------------+
```

### 2.2 Functional Modules Description
1. **Display Playlist Module:** Displays the list of songs with ID, Title, Artist, Duration (MM:SS), and active playing status.
2. **Add Song Module:** Appends a new song to the end of the Doubly Linked List in $\mathcal{O}(1)$ time.
3. **Delete Song Module:** Locates a song by ID and unlinks its node safely from the Doubly Linked List.
4. **Play Song by Title / Artist:** Searches for a song by title or artist keyword, updates the current playing track, pushes the previous song to the history stack, and displays the Now Playing banner instantly.
5. **View History Module:** Displays the stack of previously played songs in reverse chronological order (LIFO).
6. **Save & Exit Module:** Persists the entire playlist into `playlist.txt` upon exit and reloads it on startup.

### 2.3 Data Structures Selection & Technical Rationale

#### Structure 1: Doubly Linked List (Playlist)
Each node represents a song and contains pointers to both the next and previous songs:
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

#### Structure 2: History Stack (Recently Played - LIFO)
Whenever a new song is played, a reference to the previously playing song is pushed onto the stack:
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

---

## 3. IMPLEMENTATION & SOURCE CODE

### 3.1 Algorithmic Design of Core Modules

#### Algorithm: Play Song by Title or Artist Keyword
```
Input: Query string (Title or Artist)
Output: Updated currentSong and playback confirmation

1. If head == NULL: Print 'Playlist is empty' and Return.
2. Read Query string from user and trim trailing spaces.
3. Traverse Doubly Linked List starting from head:
       Compare Query with node->title and node->artist (case-insensitive).
       If match found: Set match = node and break loop.
4. If match == NULL: Print 'No song found matching query' and Return.
5. If currentSong != NULL and currentSong != match:
       pushHistory(currentSong)  // Save to LIFO Stack
6. currentSong = match
7. Print Now Playing banner with title, artist, and formatted duration.
```

### 3.2 Complete C Source Code
*(See complete source code in `music_player.c`)*

---

### 3.3 Sample Input and Output Test Runs

#### Test Run 1: Launch and Display Playlist
```text
  ===============================================================
  *             MUSIC PLAYLIST MANAGEMENT SYSTEM                *
  *          Data Structures Project-Based Learning (PBL)       *
  ===============================================================

+----------------------- PLAYER CONTROLS -----------------------+
|  1. Display Playlist                                          |
|  2. Add Song                                                  |
|  3. Delete Song by ID                                         |
|  4. Play Song by Title / Artist                               |
|  5. View Recently Played History                              |
|  6. Save & Exit Program                                       |
+---------------------------------------------------------------+
 Enter your choice (1-6): 1

========================================================================================
                                     MUSIC PLAYLIST                                     
========================================================================================
 No.  | ID   | Song Title                 | Artist                 | Duration | Status      
----------------------------------------------------------------------------------------
 1    | 1    | Memories                   | Maroon 5               | 03:09    |             
 2    | 2    | Blinding Lights            | The Weeknd             | 03:20    |             
 3    | 3    | Smooth Criminal            | Michael Jackson        | 04:17    |             
 4    | 4    | Bohemian Rhapsody          | Queen                  | 05:54    |             
 5    | 5    | Shape of You               | Ed Sheeran             | 03:53    |             
========================================================================================
 Total Songs: 5
```

#### Test Run 2: Play Song by Title / Artist
```text
 Enter your choice (1-6): 4
Enter Song Title or Artist to play: Queen

================================================================
 [>] NOW PLAYING: "Bohemian Rhapsody" by Queen
     Duration: 05:54 | Status: Playing
================================================================

 Enter your choice (1-6): 4
Enter Song Title or Artist to play: Memories

================================================================
 [>] NOW PLAYING: "Memories" by Maroon 5
     Duration: 03:09 | Status: Playing
================================================================
```

#### Test Run 3: View Recently Played History (LIFO Stack)
```text
 Enter your choice (1-6): 5

================================================================
                  RECENTLY PLAYED HISTORY (LIFO STACK)          
================================================================
 Pos  | ID   | Title                     | Artist               | Duration
----------------------------------------------------------------
 #1   | 4    | Bohemian Rhapsody         | Queen                | 05:54   
 Total songs in history: 1

 Enter your choice (1-6): 6

================================================================
       Thank you for using Music Playlist Management System!     
================================================================
```

---

## 4. COMPLEXITY & PERFORMANCE ANALYSIS

### 4.1 Time & Space Complexity Summary

| Functional Operation | Primary Data Structure | Time Complexity (Best / Avg) | Time Complexity (Worst) | Space Complexity |
| :--- | :--- | :---: | :---: | :---: |
| **Add Song (End)** | Doubly Linked List (via `tail`) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Delete Song (by ID)** | Doubly Linked List | $\mathcal{O}(1)$ (head/tail) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |
| **Display Playlist** | Doubly Linked List Traversal | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |
| **Play Song (by Title/Artist)** | Linear Search on Nodes | $\mathcal{O}(1)$ (first item) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |
| **Push to History Stack** | Linked Stack (LIFO) | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Display History Stack** | Linked Stack Traversal | $\mathcal{O}(k)$ | $\mathcal{O}(k)$ | $\mathcal{O}(1)$ |
| **Save / Load File** | Sequential Disk I/O | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |

### 4.2 Comparative Analysis: Arrays vs. Doubly Linked Lists
| Performance Dimension | Static / Dynamic Array | Doubly Linked List (Our System) |
| :--- | :--- | :--- |
| **Insertion at Tail** | $\mathcal{O}(1)$ amortized (requires reallocation) | $\mathcal{O}(1)$ guaranteed using `tail` pointer |
| **Arbitrary Node Deletion** | $\mathcal{O}(n)$ (elements must be shifted) | $\mathcal{O}(1)$ pointer updates once node is located |
| **Bidirectional Navigation** | Index math (`i++`, `i--`), bounds sensitive | Native pointer dereferencing (`next`, `prev`) |
| **Memory Allocation** | Contiguous chunk (risk of fragmentation) | Dynamic heap allocation per node |

---

## 5. CONCLUSION & FUTURE SCOPE

### 5.1 Conclusion
The **Music Playlist Management System** provides a clean, practical demonstration of core data structures applied to music organization. By utilizing a Doubly Linked List for dynamic song storage and a Stack for tracking recently played history, the system eliminates the rigid memory constraints and element-shifting penalties of standard arrays. Operations such as adding tracks, deleting songs, and recording playback history are executed with optimal algorithmic efficiency. The project delivers hands-on mastery of dynamic memory management, pointer manipulation, and structured programming in C.

### 5.2 Future Scope & Enhancements
1. **Prefix Trie for Autocomplete:** Implementing a prefix Trie structure to offer sub-millisecond autocomplete suggestions as the user types queries.
2. **Audio Output Engine:** Connecting with audio libraries such as Windows `mciSendString` or `SDL2` to directly play MP3 or WAV audio files.
3. **Multiple Playlists:** Adding support for multiple user-defined playlists (e.g. Favorites, Study) using a list of linked lists.

---

## 6. REFERENCES

1. **Reema Thareja**, *Data Structures Using C*, Oxford University Press, 2nd Edition, 2014.
2. **Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed**, *Fundamentals of Data Structures in C*, Silicon Press, 2nd Edition, 2008.
3. **Mark Allen Weiss**, *Data Structures and Algorithm Analysis in C*, Pearson Education, 4th Edition.
4. **Brian W. Kernighan and Dennis M. Ritchie**, *The C Programming Language*, Prentice Hall, 2nd Edition.
