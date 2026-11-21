# Music Playlist Management System (ADS PBL)

A console-based Music Playlist Management System implemented in **C** for the **Data Structures (20CS21001)** / **Advanced Data Structures (ADS)** Project-Based Learning curriculum.

---

## 🎵 Key Features & Data Structures Mapping

| Feature | Data Structure | Why This Data Structure? | Time Complexity |
| :--- | :--- | :--- | :---: |
| **Playlist Management** | **Doubly Linked List** | Enables instant forward (`next`) and backward (`prev`) track traversal, with $O(1)$ node insertion/deletion. | $\mathcal{O}(1)$ |
| **Playback History** | **Linked Stack (LIFO)** | Automatically records completed tracks for instantaneous rewind and history inspection. | $\mathcal{O}(1)$ |
| **"Up Next" Play Queue** | **Linked Queue (FIFO)** | Gives priority to user-requested tracks before resuming sequential playlist order. | $\mathcal{O}(1)$ |
| **Persistent Storage** | **File I/O (`playlist.txt`)** | Automatically loads songs on boot and saves updates when exiting. | $\mathcal{O}(n)$ |
| **Case-Insensitive Search**| **Linear Traversal** | Fast keyword search across titles and artist names. | $\mathcal{O}(n)$ |

---

## 📂 Project Directory Structure

```text
ADS-PBL/
├── music_player.c                                  # Full C source code with Doubly Linked List, Stack, and Queue
├── music_player.exe                                # Compiled Windows executable binary
├── playlist.txt                                    # Persistent storage file containing song data
├── MUSIC_PLAYLIST_MANAGEMENT_SYSTEM_PBL_REPORT.docx # Official Microsoft Word PBL Report (Sai Prabhavati)
├── PBL_REPORT.md                                   # Markdown version of the academic PBL report
├── generate_docx.py                                # Python script used to build the DOCX report
└── README.md                                       # Instructions and documentation
```

---

## 🛠️ How to Compile and Run

### 1. Requirements
- Windows 10/11
- GCC compiler (MinGW / MinGW-w64 or Clang)

### 2. Compilation
Open Command Prompt or PowerShell in the project directory and run:

```bash
gcc -Wall -Wextra -std=c99 music_player.c -o music_player.exe
```

### 3. Execution
```bash
.\music_player.exe
```

---

## 🎮 Interactive Menu Options

```text
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
| 11. Toggle Loop / Repeat Mode [ON/OFF]                        |
| 12. Save & Exit Program                                       |
+---------------------------------------------------------------+
```

---

## 📄 Academic PBL Report
The complete report following the exact format of **Geethanjali College of Engineering and Technology** is located in [PBL_REPORT.md](file:///c:/Users/Dell/Desktop/All-Projects/ADS-PBL/PBL_REPORT.md). You can open it in any Markdown viewer, copy it directly into Microsoft Word, or convert it to PDF.
