/**
 * ============================================================================
 * Project: Music Playlist Management System
 * Course:  Data Structures (20CS21001) / ADS PBL
 * Platform: Windows Console (C Language)
 *
 * Core Data Structures Used:
 *  1. Doubly Linked List : Dynamic active playlist management (bidirectional navigation)
 *  2. Stack              : Recently played songs history (LIFO backtracking)
 *  3. Queue              : "Up Next" upcoming play queue (FIFO request processing)
 * ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <windows.h>

#define MAX_STR 100
#define FILE_NAME "playlist.txt"

/* ============================================================================
 * 1. DATA STRUCTURE DEFINITIONS
 * ============================================================================
 */

// Structure representing a single Song in the Doubly Linked List
typedef struct Song {
    int id;
    char title[MAX_STR];
    char artist[MAX_STR];
    int duration; // Duration in seconds
    struct Song *prev;
    struct Song *next;
} Song;

// Structure for Stack Node (Recently Played History)
typedef struct HistoryNode {
    Song *song;
    struct HistoryNode *next;
} HistoryNode;

// Stack container for playback history
typedef struct {
    HistoryNode *top;
    int count;
} HistoryStack;

// Structure for Queue Node ("Play Next" / Up Next queue)
typedef struct QueueNode {
    Song *song;
    struct QueueNode *next;
} QueueNode;

// Queue container for upcoming song queue
typedef struct {
    QueueNode *front;
    QueueNode *rear;
    int count;
} SongQueue;

/* ============================================================================
 * GLOBAL POINTERS & STATE
 * ============================================================================
 */
Song *head = NULL;
Song *tail = NULL;
Song *currentSong = NULL;
int songIdCounter = 1;
int isLoopMode = 0; // 0 = standard playback, 1 = repeat playlist

HistoryStack history = { NULL, 0 };
SongQueue upNextQueue = { NULL, NULL, 0 };

/* ============================================================================
 * UTILITY FUNCTIONS
 * ============================================================================
 */

// Format seconds into MM:SS string
void formatTime(int totalSeconds, char *buffer) {
    int minutes = totalSeconds / 60;
    int seconds = totalSeconds % 60;
    sprintf(buffer, "%02d:%02d", minutes, seconds);
}

// Case-insensitive string search helper
int strCaseContains(const char *haystack, const char *needle) {
    char h[MAX_STR], n[MAX_STR];
    int i;
    for (i = 0; haystack[i] && i < MAX_STR - 1; i++) h[i] = (char)tolower(haystack[i]);
    h[i] = '\0';
    for (i = 0; needle[i] && i < MAX_STR - 1; i++) n[i] = (char)tolower(needle[i]);
    n[i] = '\0';
    return (strstr(h, n) != NULL);
}

// Trim trailing newline and spaces
void trimNewline(char *str) {
    int len = (int)strlen(str);
    while (len > 0 && (str[len - 1] == '\n' || str[len - 1] == '\r' || str[len - 1] == ' ')) {
        str[len - 1] = '\0';
        len--;
    }
}

// Clear input buffer
void clearInputBuffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

/* ============================================================================
 * 2. STACK OPERATIONS (Recently Played History - LIFO)
 * ============================================================================
 */

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

/* ============================================================================
 * 3. QUEUE OPERATIONS ("Play Next" / Up Next - FIFO)
 * ============================================================================
 */

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

/* ============================================================================
 * 4. DOUBLY LINKED LIST (PLAYLIST) OPERATIONS
 * ============================================================================
 */

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

// Add song to the end of Doubly Linked List
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

// Search song by ID in the Doubly Linked List
Song *searchSongById(int id) {
    Song *temp = head;
    while (temp != NULL) {
        if (temp->id == id) return temp;
        temp = temp->next;
    }
    return NULL;
}

// Delete a song from the Doubly Linked List
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

    // If target is currently playing, advance or rewind currentSong
    if (currentSong == target) {
        if (target->next != NULL) {
            currentSong = target->next;
        } else if (target->prev != NULL) {
            currentSong = target->prev;
        } else {
            currentSong = NULL;
        }
    }

    // Unlink from Doubly Linked List
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

// Display complete playlist (traversal)
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

// Search songs by title or artist keyword
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

/* ============================================================================
 * 5. PLAYBACK CONTROLLER
 * ============================================================================
 */

// Simulated visual audio playback progress bar
void simulatePlaybackVisual(Song *s) {
    if (s == NULL) return;
    char totalTime[16];
    formatTime(s->duration, totalTime);

    printf("\n----------------------------------------------------------------\n");
    printf(" [>] NOW PLAYING: \"%s\" by %s\n", s->title, s->artist);
    printf("     Track Duration: %s | Audio Engine: Active\n", totalTime);
    printf("     Progress: [");

    // Quick visual progress simulation (10 blocks)
    for (int i = 0; i < 20; i++) {
        printf("#");
        fflush(stdout);
        Sleep(25); // 25ms delay for visual feedback
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

    // Step 1: Check if there is an item in the Up Next Queue (FIFO)
    if (upNextQueue.front != NULL) {
        if (currentSong != NULL) {
            pushHistory(currentSong); // Push current to history stack
        }
        currentSong = dequeueSong();
        printf("\n[Queue Triggered] Playing requested track from Up Next Queue!\n");
        simulatePlaybackVisual(currentSong);
        return;
    }

    // Step 2: Traverse to next node in Doubly Linked List
    if (currentSong == NULL) {
        currentSong = head;
    } else {
        pushHistory(currentSong); // Save to history
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

    // Step 1: Check history stack for backtracking (LIFO)
    Song *histSong = popHistory();
    if (histSong != NULL) {
        printf("\n[History Triggered] Rewinding to recently played track from History Stack!\n");
        currentSong = histSong;
        simulatePlaybackVisual(currentSong);
        return;
    }

    // Step 2: Fallback to Doubly Linked List prev pointer
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

/* ============================================================================
 * 6. FILE PERSISTENCE (LOAD / SAVE PLAYLIST)
 * ============================================================================
 */

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
        // If file doesn't exist, populate with initial default songs
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

/* ============================================================================
 * 7. INTERACTIVE CONSOLE MENU & MAIN
 * ============================================================================
 */

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
    // Enable ANSI console formatting support on Windows
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode = 0;
    GetConsoleMode(hOut, &dwMode);
    SetConsoleMode(hOut, dwMode | 0x0004);

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
                printf("Enter Duration in seconds (e.g., 210 for 3m 30s): ");
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
                    printf("[!] Invalid ID input.\n");
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
                printf("\n================================================================\n");
                printf("       Thank you for using Music Playlist Management System!     \n");
                printf("================================================================\n\n");
                exit(0);

            default:
                printf("\n[!] Invalid selection! Please enter an option between 1 and 12.\n");
        }
    }

    return 0;
}
