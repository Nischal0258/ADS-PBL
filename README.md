# Music Playlist Management System (ADS PBL)

A console-based Music Playlist Management System implemented in **C** for the **Data Structures (20CS21001)** / **Advanced Data Structures (ADS)** Project-Based Learning curriculum.

---

## 🎵 Key Features & Data Structures Mapping

| Feature | Data Structure | Why This Data Structure? | Time Complexity |
| :--- | :--- | :--- | :---: |
| **Playlist Management** | **Doubly Linked List** | Bidirectional node connections (`next`, `prev`) with dynamic heap allocation and $O(1)$ end insertion. | $\mathcal{O}(1)$ |
| **Play by Title / Artist** | **Linear Traversal** | Instant search and immediate playback without artificial progress delays. | $\mathcal{O}(n)$ |
| **Playback History** | **Linked Stack (LIFO)** | Automatically records played tracks in reverse chronological order. | $\mathcal{O}(1)$ |
| **Persistent Storage** | **File I/O (`playlist.txt`)** | Loads songs on boot and saves updates on exit. | $\mathcal{O}(n)$ |

---

## 📂 Project Directory Structure

```text
ADS-PBL/
├── music_player.c                                  # Clean C source code with Doubly Linked List and Stack
├── music_player.exe                                # Compiled Windows executable binary
├── playlist.txt                                    # Persistent storage file containing song data
├── MUSIC_PLAYLIST_MANAGEMENT_SYSTEM_PBL_REPORT.docx # Official Microsoft Word PBL Report (Sai Prabhavati)
├── PBL_REPORT.md                                   # Markdown version of the academic PBL report
├── generate_docx.py                                # Python script used to build the Word report
└── README.md                                       # Instructions and documentation
```

---

## 🛠️ How to Compile and Run

### 1. Requirements
- Windows 10/11
- GCC compiler (MinGW or Clang)

### 2. Compilation
```bash
gcc -Wall -Wextra -std=c99 music_player.c -o music_player.exe
```

### 3. Execution
```bash
.\music_player.exe
```

---

## 🎮 Streamlined Menu Options

```text
+----------------------- PLAYER CONTROLS -----------------------+
|  1. Display Playlist                                          |
|  2. Add Song                                                  |
|  3. Delete Song by ID                                         |
|  4. Play Song by Title / Artist                               |
|  5. View Recently Played History                              |
|  6. Save & Exit Program                                       |
+---------------------------------------------------------------+
```

---

## 📄 Academic PBL Report
The complete report following the exact format of **Geethanjali College of Engineering and Technology** is located in:
- **`MUSIC_PLAYLIST_MANAGEMENT_SYSTEM_PBL_REPORT.docx`** (Microsoft Word)
- **`PBL_REPORT.md`** (Markdown)
