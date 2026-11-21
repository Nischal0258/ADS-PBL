/**
 * ============================================================================
 * Project: Music Playlist Management System
 * Course:  Data Structures (20CS21001) / ADS PBL
 * Student: Sai Prabhavati
 * Platform: Windows Console (C Language)
 *
 * Core Data Structures Used:
 *  1. Doubly Linked List : Dynamic playlist management (bidirectional links)
 *  2. Stack              : Recently played history (LIFO backtracking)
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

/* ============================================================================
 * GLOBAL STATE
 * ============================================================================
 */
Song *head = NULL;
Song *tail = NULL;
Song *currentSong = NULL;
int songIdCounter = 1;

HistoryStack history = { NULL, 0 };

/* ============================================================================
 * UTILITY FUNCTIONS
 * ============================================================================
 */

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

void displayHistory(void) {
    printf("\n================================================================\n");
    printf("                  RECENTLY PLAYED HISTORY (LIFO STACK)          \n");
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
    printf(" Total songs in history: %d\n", history.count);
}

/* ============================================================================
 * 3. DOUBLY LINKED LIST (PLAYLIST) OPERATIONS
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

void insertSong(const char *title, const char *artist, int duration) {
    Song *newSong = createSongNode(0, title, artist, duration);
    if (!newSong) return;

    if (head == NULL) {
        head = tail = newSong;
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
        currentSong = NULL;
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
    printf("                                     MUSIC PLAYLIST                                     \n");
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
    printf(" Total Songs: %d\n", index - 1);
}

/* ============================================================================
 * 4. PLAYBACK CONTROLLER
 * ============================================================================
 */

void displayNowPlaying(Song *s) {
    if (s == NULL) return;
    char timeStr[16];
    formatTime(s->duration, timeStr);

    printf("\n================================================================\n");
    printf(" [>] NOW PLAYING: \"%s\" by %s\n", s->title, s->artist);
    printf("     Duration: %s | Status: Playing\n", timeStr);
    printf("================================================================\n");
}

void playByTitleOrArtist(void) {
    if (head == NULL) {
        printf("\n[!] Playlist is empty. Add songs first.\n");
        return;
    }

    char query[MAX_STR];
    printf("\nEnter Song Title or Artist to play: ");
    scanf(" %[^\n]", query);
    trimNewline(query);

    Song *temp = head;
    Song *match = NULL;

    while (temp != NULL) {
        if (strCaseContains(temp->title, query) || strCaseContains(temp->artist, query)) {
            match = temp;
            break;
        }
        temp = temp->next;
    }

    if (match == NULL) {
        printf("\n[!] No song found matching \"%s\". Please check the spelling or view playlist.\n", query);
        return;
    }

    // Save previous playing song to history stack
    if (currentSong != NULL && currentSong != match) {
        pushHistory(currentSong);
    }

    currentSong = match;
    displayNowPlaying(currentSong);
}

/* ============================================================================
 * 5. FILE PERSISTENCE
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
}

void loadPlaylistFromFile(void) {
    FILE *fp = fopen(FILE_NAME, "r");
    if (!fp) {
        insertSong("Memories", "Maroon 5", 189);
        insertSong("Blinding Lights", "The Weeknd", 200);
        insertSong("Smooth Criminal", "Michael Jackson", 257);
        insertSong("Bohemian Rhapsody", "Queen", 354);
        insertSong("Shape of You", "Ed Sheeran", 233);
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
}

/* ============================================================================
 * 6. INTERACTIVE MENU & MAIN
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
    printf("|  1. Display Playlist                                          |\n");
    printf("|  2. Add Song                                                  |\n");
    printf("|  3. Delete Song by ID                                         |\n");
    printf("|  4. Play Song by Title / Artist                               |\n");
    printf("|  5. View Recently Played History                              |\n");
    printf("|  6. Save & Exit Program                                       |\n");
    printf("+---------------------------------------------------------------+\n");
    printf(" Enter your choice (1-6): ");
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
            printf("\n[!] Invalid input! Please enter a valid number (1-6).\n");
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
                printf("Enter Duration in seconds (e.g. 210 for 3m 30s): ");
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
                playByTitleOrArtist();
                break;

            case 5:
                displayHistory();
                break;

            case 6:
                savePlaylistToFile();
                printf("\n================================================================\n");
                printf("       Thank you for using Music Playlist Management System!     \n");
                printf("================================================================\n\n");
                exit(0);

            default:
                printf("\n[!] Invalid selection! Please enter an option between 1 and 6.\n");
        }
    }

    return 0;
}
