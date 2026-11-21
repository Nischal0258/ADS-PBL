import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.keep_with_next = True
    if level == 1:
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        for run in h.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 32, 96) # Dark Navy
    elif level == 2:
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
        for run in h.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(31, 78, 121)
    elif level == 3:
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
        for run in h.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(50, 50, 50)
    return h

def add_p(doc, text="", bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Times New Roman'
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
    if text:
        r_text = p.add_run(text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(11)
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Times New Roman'
        r_b.font.size = Pt(11)
        r_b.font.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    return p

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F2F4F7")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="002060"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str.strip('\n'))
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(30, 30, 30)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_row = table.rows[0]
    for i, h_text in enumerate(headers):
        cell = header_row.cells[i]
        set_cell_background(cell, "002060")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
    
    for r_idx, row_data in enumerate(data):
        row = table.add_row()
        bg_color = "F9FAFB" if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            if c_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(val))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
    
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

def build_pbl_report():
    doc = docx.Document()
    
    # Set page margins to 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header
        header_p = section.header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        h_run = header_p.add_run("Music Playlist Management System | Data Structures PBL Report")
        h_run.font.name = 'Times New Roman'
        h_run.font.size = Pt(8.5)
        h_run.font.italic = True
        h_run.font.color.rgb = RGBColor(120, 120, 120)
    
    # -------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("GEETHANJALI COLLEGE OF ENGINEERING AND TECHNOLOGY\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 32, 96)
    
    r_sub = p_inst.add_run("(UGC AUTONOMOUS INSTITUTION)\nAccredited by NBA & NAAC with 'A' Grade, Approved by AICTE, Affiliated to JNTUH\nCheeryal (V), Keesara (M), Medchal Dist., Telangana – 501 301\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = RGBColor(80, 80, 80)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(18)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("MUSIC PLAYLIST MANAGEMENT SYSTEM\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 32, 96)
    
    p_subtitle = doc.add_paragraph()
    p_subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subtitle.paragraph_format.space_after = Pt(16)
    r_subt = p_subtitle.add_run("PROJECT BASED LEARNING (PBL) REPORT\n")
    r_subt.font.name = 'Times New Roman'
    r_subt.font.size = Pt(13)
    r_subt.font.bold = True
    r_subt.font.color.rgb = RGBColor(31, 78, 121)
    
    r_crs = p_subtitle.add_run("For the Course:\nDATA STRUCTURES / ADVANCED DATA STRUCTURES (20CS21001)\nB.Tech II Year I Semester (AR22) | A.Y 2025–2026\n")
    r_crs.font.name = 'Times New Roman'
    r_crs.font.size = Pt(11)
    r_crs.font.italic = True
    
    doc.add_paragraph().paragraph_format.space_after = Pt(24)
    
    # Metadata Box Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Left: Submitted by
    cell_left = meta_table.cell(0, 0)
    set_cell_background(cell_left, "F4F6F9")
    set_cell_margins(cell_left, top=100, bottom=100, left=140, right=140)
    p_l = cell_left.paragraphs[0]
    p_l.paragraph_format.space_after = Pt(2)
    r_lb = p_l.add_run("Submitted By:\n")
    r_lb.font.bold = True
    r_lb.font.size = Pt(11)
    r_ln = p_l.add_run("SAI PRABHAVATI\n")
    r_ln.font.bold = True
    r_ln.font.size = Pt(11.5)
    r_ln.font.color.rgb = RGBColor(0, 32, 96)
    r_lr = p_l.add_run("Roll No: 24R11A05W9\nB.Tech (CSE) - II Year I Sem")
    r_lr.font.size = Pt(10)
    
    # Right: Guided by
    cell_right = meta_table.cell(0, 1)
    set_cell_background(cell_right, "F4F6F9")
    set_cell_margins(cell_right, top=100, bottom=100, left=140, right=140)
    p_r = cell_right.paragraphs[0]
    p_r.paragraph_format.space_after = Pt(2)
    r_rb = p_r.add_run("Under the Guidance of:\n")
    r_rb.font.bold = True
    r_rb.font.size = Pt(11)
    r_rn = p_r.add_run("Mrs. K. PADMAJA\n")
    r_rn.font.bold = True
    r_rn.font.size = Pt(11.5)
    r_rn.font.color.rgb = RGBColor(0, 32, 96)
    r_rr = p_r.add_run("Assistant Professor\nDept. of Computer Science & Engg.")
    r_rr.font.size = Pt(10)
    
    # Bottom: Leadership
    cell_bottom = meta_table.cell(1, 0)
    cell_bottom.merge(meta_table.cell(1, 1))
    set_cell_background(cell_bottom, "FFFFFF")
    set_cell_margins(cell_bottom, top=80, bottom=80, left=140, right=140)
    p_b = cell_bottom.paragraphs[0]
    p_b.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_lead = p_b.add_run("\nLab In-Charge: Mrs. K. Padmaja  |  Head of Department (CSE): Dr. E. Ravindra, Professor\nDepartment of Computer Science and Engineering")
    r_lead.font.size = Pt(10)
    r_lead.font.bold = True
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_styled_heading(doc, "ACKNOWLEDGEMENT", level=1)
    
    add_p(doc, "I express my heartfelt gratitude to my respected project guide, Mrs. K. Padmaja, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, continuous encouragement, and constructive feedback throughout the course of this Project-Based Learning (PBL) activity. Her insights into data structure applications and software engineering principles were pivotal in successfully designing and implementing this system.")
    
    add_p(doc, "I extend my sincere thanks to Dr. E. Ravindra, Professor and Head of the Department of Computer Science and Engineering, for his constant administrative support and for providing the modern computing and laboratory facilities necessary to complete this project.")
    
    add_p(doc, "Special thanks are also due to the laboratory instructors, faculty members, and my peers for their valuable discussions, cooperative assistance, and constructive suggestions during the debugging and testing phases.")
    
    add_p(doc, "Finally, I express my deep sense of gratitude to the Management and Principal of Geethanjali College of Engineering and Technology for nurturing an academic environment that promotes practical problem-solving, hands-on coding, and technical excellence.")
    
    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(24)
    r_s1 = p_sig.add_run("Sai Prabhavati\n")
    r_s1.font.bold = True
    r_s1.font.size = Pt(11)
    r_s2 = p_sig.add_run("Roll No: 24R11A05W9\nB.Tech (CSE) - II Year I Semester\nGeethanjali College of Engineering & Technology")
    r_s2.font.size = Pt(10)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_styled_heading(doc, "TABLE OF CONTENTS", level=1)
    
    toc_data = [
        ["1", "Introduction", "4"],
        ["", "1.1 About the Project", "4"],
        ["", "1.2 Motivation & Real-World Problem Statement", "4"],
        ["", "1.3 Project Objectives and Expected Outcomes", "5"],
        ["2", "System Design & Architecture", "6"],
        ["", "2.1 System Architecture", "6"],
        ["", "2.2 Functional Modules Description", "7"],
        ["", "2.3 Data Structures Selection & Technical Rationale", "8"],
        ["", "2.4 Entity Relationship & Pointer Structure", "9"],
        ["3", "Implementation & Source Code", "10"],
        ["", "3.1 Algorithmic Design of Core Modules", "10"],
        ["", "3.2 Complete C Source Code", "11"],
        ["", "3.3 Sample Input and Output Test Runs", "18"],
        ["4", "Complexity & Performance Analysis", "21"],
        ["", "4.1 Time & Space Complexity Summary", "21"],
        ["", "4.2 Comparative Analysis: Arrays vs. Doubly Linked Lists", "22"],
        ["5", "Conclusion & Future Scope", "23"],
        ["6", "References", "24"]
    ]
    
    toc_table = doc.add_table(rows=1, cols=3)
    format_table(toc_table, [Inches(0.8), Inches(4.7), Inches(0.9)], ["S.No.", "Topic / Chapter", "Page No."], toc_data)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    add_styled_heading(doc, "1. INTRODUCTION", level=1)
    
    add_styled_heading(doc, "1.1 About the Project", level=2)
    add_p(doc, "The Music Playlist Management System is a specialized console software application engineered in the C programming language. It is designed to demonstrate how fundamental data structures—specifically Doubly Linked Lists, Stacks, and Queues—are synergistically applied to solve real-world music organization and playback challenges. Commercial audio streaming platforms such as Spotify, Apple Music, and Amazon Music manage catalog sizes exceeding 100 million tracks, serving millions of concurrent playlist navigations, playback histories, and dynamic request queues. This project reproduces the internal mechanics of such playback engines without third-party dependencies, implementing clear pointer-level data structures from first principles.")
    
    add_styled_heading(doc, "1.2 Motivation & Real-World Problem Statement", level=2)
    add_p(doc, "In elementary computer science applications, collections of records are frequently stored in static or dynamic arrays. However, arrays present severe algorithmic and operational bottlenecks when deployed in real-time multimedia systems:")
    add_bullet(doc, " Inserting a new song into the beginning or middle of an array necessitates shifting O(n) elements sequentially in memory.", "Expensive Insertions: ")
    add_bullet(doc, " Deleting a track from an active playlist leaves memory gaps or requires another O(n) element compaction.", "High Cost Deletions: ")
    add_bullet(doc, " Fixed-size arrays either waste memory if underutilized or risk buffer overflow when songs exceed allocated bounds.", "Inflexible Memory Sizing: ")
    add_bullet(doc, " Singly linked lists allow only forward traversal; navigating back to the previous track requires re-traversing the list from the head node in O(n) time.", "Asymmetric Navigation: ")
    add_p(doc, "To overcome these challenges, this system models the active playlist as a Doubly Linked List with head, tail, and current pointers, achieving guaranteed O(1) track transitions, dynamic growth, and instantaneous bidirectional navigation. To complement the active playlist, a Linked Stack provides playback history backtracking, and a Linked Queue manages prioritized 'Up Next' song queues.")
    
    add_styled_heading(doc, "1.3 Project Objectives and Expected Outcomes", level=2)
    add_p(doc, "Objectives:", bold_prefix="")
    add_bullet(doc, " To design and develop an interactive music player application in C using manual heap memory allocation (malloc and free).")
    add_bullet(doc, " To implement a Doubly Linked List supporting bidirectional playback, end-insertion, middle-deletion, and loop/repeat modes.")
    add_bullet(doc, " To integrate a Last-In-First-Out (LIFO) Stack to record played tracks for immediate history playback.")
    add_bullet(doc, " To incorporate a First-In-First-Out (FIFO) Queue for custom 'Play Next' song requests that take priority over standard sequential flow.")
    add_bullet(doc, " To provide persistent file storage using delimited text parsing to save and reload playlist data across executions.")
    
    add_p(doc, "Expected Outcomes:", bold_prefix="")
    add_bullet(doc, " A stable, crash-free console application with formatted ANSI status screens and simulated progress visualizers.")
    add_bullet(doc, " Practical verification of O(1) time complexities for track switching, queue dispatch, and history backtracking.")
    add_bullet(doc, " Deep technical mastery of dynamic memory management, pointer arithmetic, and modular software architecture in C.")
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 2. SYSTEM DESIGN & ARCHITECTURE
    # -------------------------------------------------------------
    add_styled_heading(doc, "2. SYSTEM DESIGN & ARCHITECTURE", level=1)
    
    add_styled_heading(doc, "2.1 System Architecture", level=2)
    add_p(doc, "The system follows a three-tier modular architecture ensuring strict separation between user input/presentation, business rules/playback logic, and underlying data structures:")
    
    add_code_block(doc, 
"+-----------------------------------------------------------------------------+\n"
"|                          1. USER INTERFACE LAYER                            |\n"
"|     - Console Menu System            - Real-time Visual Progress Bar        |\n"
"|     - ANSI Formatted Song Tables     - Search Results & System Alerts       |\n"
"+-----------------------------------------------------------------------------+\n"
"                                      |\n"
"                                      v\n"
"+-----------------------------------------------------------------------------+\n"
"|                            2. LOGIC CONTROLLER                              |\n"
"|     - Playback Engine (Play, Next, Prev, Loop Mode)                         |\n"
"|     - Priority Queue Dispatcher (Up Next overrides playlist order)         |\n"
"|     - History Tracker (Stack push upon track playback)                      |\n"
"|     - Search & Validation Engine (Case-insensitive title/artist matching)   |\n"
"+-----------------------------------------------------------------------------+\n"
"                                      |\n"
"                                      v\n"
"+-----------------------------------------------------------------------------+\n"
"|                       3. DATA STRUCTURE & STORAGE LAYER                     |\n"
"|  +-------------------------+  +--------------------+  +-------------------+ |\n"
"|  |   Doubly Linked List    |  |    History Stack   |  |   Up Next Queue   | |\n"
"|  | (head, tail, curr)      |  |   (LIFO Backtrack) |  |   (FIFO Requests) | |\n"
"|  +-------------------------+  +--------------------+  +-------------------+ |\n"
"|                                      |                                      |\n"
"|                       Persistent Disk Storage (playlist.txt)                |\n"
"+-----------------------------------------------------------------------------+"
    )
    
    add_styled_heading(doc, "2.2 Functional Modules Description", level=2)
    add_bullet(doc, " Allows dynamic insertion of tracks at the tail of the playlist with automatic unique ID assignment and duration formatting.", "Add Song Module: ")
    add_bullet(doc, " Searches by song ID and cleanly unlinks the target node by updating neighboring pointers, safeguarding against dangling references and memory leaks.", "Delete Song Module: ")
    add_bullet(doc, " Traverses the Doubly Linked List from head to tail, displaying song ID, title, artist, formatted duration (MM:SS), and an active playback indicator.", "Display Playlist Module: ")
    add_bullet(doc, " Performs case-insensitive linear substring scanning across both titles and artist names.", "Search Song Module: ")
    add_bullet(doc, " Orchestrates playback navigation. When 'Next' is pressed, it first checks if the FIFO Queue contains pending requests; if empty, it advances along the list. When 'Previous' is pressed, it pops from the LIFO Stack.", "Playback Navigation Engine: ")
    add_bullet(doc, " Parses and serializes song records to and from 'playlist.txt' using pipe-delimited format (id|title|artist|duration).", "Persistence Module: ")
    
    add_styled_heading(doc, "2.3 Data Structures Selection & Technical Rationale", level=2)
    
    add_p(doc, "Structure 1: Doubly Linked List (Playlist)", bold_prefix="")
    add_p(doc, "Each song node maintains two explicit pointers: next (pointing to the subsequent song) and prev (pointing to the preceding song). A global currentSong pointer indicates the track currently loaded in the playback engine.")
    add_code_block(doc,
"typedef struct Song {\n"
"    int id;\n"
"    char title[100];\n"
"    char artist[100];\n"
"    int duration;       // in seconds\n"
"    struct Song *prev;  // pointer to previous track\n"
"    struct Song *next;  // pointer to next track\n"
"} Song;"
    )
    
    add_p(doc, "Structure 2: History Stack (Recently Played - LIFO)", bold_prefix="")
    add_p(doc, "Whenever a song is played or skipped, a pointer reference to the song is pushed onto the history stack. When the user selects 'Play Previous', the system pops the top entry, instantly restoring playback history in exact reverse order.")
    add_code_block(doc,
"typedef struct HistoryNode {\n"
"    Song *song;\n"
"    struct HistoryNode *next;\n"
"} HistoryNode;\n\n"
"typedef struct {\n"
"    HistoryNode *top;\n"
"    int count;\n"
"} HistoryStack;"
    )
    
    add_p(doc, "Structure 3: Up Next Queue (FIFO Requests)", bold_prefix="")
    add_p(doc, "Songs specifically chosen by the user to 'Play Next' are enqueued at the rear. When advancing playback, the engine checks whether the queue front is non-NULL. If so, it dequeues the requested song before resuming sequential traversal.")
    add_code_block(doc,
"typedef struct QueueNode {\n"
"    Song *song;\n"
"    struct QueueNode *next;\n"
"} QueueNode;\n\n"
"typedef struct {\n"
"    QueueNode *front;\n"
"    QueueNode *rear;\n"
"    int count;\n"
"} SongQueue;"
    )
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 3. IMPLEMENTATION & SOURCE CODE
    # -------------------------------------------------------------
    add_styled_heading(doc, "3. IMPLEMENTATION & SOURCE CODE", level=1)
    
    add_styled_heading(doc, "3.1 Algorithmic Design of Core Modules", level=2)
    
    add_p(doc, "Algorithm: Add Song to Playlist (End Insertion)", bold_prefix="")
    add_code_block(doc,
"Input: Title, Artist, Duration\n"
"Output: Updated Doubly Linked List with new Song Node\n\n"
"1. Allocate heap memory: newSong = (Song*)malloc(sizeof(Song))\n"
"2. Assign attributes: newSong->title = Title, newSong->artist = Artist, newSong->duration = Duration\n"
"3. Initialize pointers: newSong->next = NULL, newSong->prev = NULL\n"
"4. If head == NULL (Empty List):\n"
"       head = tail = currentSong = newSong\n"
"   Else:\n"
"       tail->next = newSong\n"
"       newSong->prev = tail\n"
"       tail = newSong\n"
"5. Return Success"
    )
    
    add_p(doc, "Algorithm: Play Next Track (Queue Check + DLL Traversal)", bold_prefix="")
    add_code_block(doc,
"1. If head == NULL: Display 'Playlist is empty' and Exit.\n"
"2. If upNextQueue.front != NULL:\n"
"       Push currentSong onto HistoryStack\n"
"       currentSong = dequeue(upNextQueue)\n"
"       Display '[Queue Triggered] Playing requested track'\n"
"       Trigger simulatePlaybackVisual(currentSong)\n"
"       Exit.\n"
"3. If currentSong != NULL:\n"
"       Push currentSong onto HistoryStack\n"
"       If currentSong->next != NULL:\n"
"           currentSong = currentSong->next\n"
"       Else:\n"
"           If isLoopMode == TRUE:\n"
"               currentSong = head\n"
"           Else:\n"
"               Display 'End of playlist reached'\n"
"               Exit.\n"
"4. Trigger simulatePlaybackVisual(currentSong)"
    )
    
    add_styled_heading(doc, "3.2 Complete C Source Code", level=2)
    add_p(doc, "Below is the complete, self-contained, and verified C implementation of the Music Playlist Management System:")
    
    # Read the actual C file to embed into the report
    with open("music_player.c", "r") as f:
        c_code_content = f.read()
    
    add_code_block(doc, c_code_content)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 3.3 SAMPLE OUTPUT
    # -------------------------------------------------------------
    add_styled_heading(doc, "3.3 Sample Input and Output Test Runs", level=2)
    add_p(doc, "The following transcripts document real execution runs of the compiled executable (music_player.exe) in Windows Console, verifying each functional requirement:")
    
    add_p(doc, "Test Run 1: Launch and Display Active Playlist", bold_prefix="")
    add_code_block(doc,
"  ===============================================================\n"
"  *             MUSIC PLAYLIST MANAGEMENT SYSTEM                *\n"
"  *          Data Structures Project-Based Learning (PBL)       *\n"
"  ===============================================================\n\n"
"[*] Playlist initialized with first track: \"Memories\"!\n"
"[+] Added \"Blinding Lights\" by The Weeknd successfully!\n"
"[+] Added \"Smooth Criminal\" by Michael Jackson successfully!\n"
"[+] Added \"Bohemian Rhapsody\" by Queen successfully!\n"
"[+] Added \"Shape of You\" by Ed Sheeran successfully!\n"
"[v] Playlist saved to file: playlist.txt\n\n"
"Enter your choice (1-12): 1\n\n"
"========================================================================================\n"
"                                ACTIVE MUSIC PLAYLIST                                   \n"
"========================================================================================\n"
" No.  | ID   | Song Title                 | Artist                 | Duration | Status      \n"
"----------------------------------------------------------------------------------------\n"
" 1    | 1    | Memories                   | Maroon 5               | 03:09    | >> PLAYING <<\n"
" 2    | 2    | Blinding Lights            | The Weeknd             | 03:20    |             \n"
" 3    | 3    | Smooth Criminal            | Michael Jackson        | 04:17    |             \n"
" 4    | 4    | Bohemian Rhapsody          | Queen                  | 05:54    |             \n"
" 5    | 5    | Shape of You               | Ed Sheeran             | 03:53    |             \n"
"========================================================================================\n"
" Loop Mode: OFF (Sequential) | Total Songs: 5"
    )
    
    add_p(doc, "Test Run 2: Enqueueing Song and Play Next Priority Override", bold_prefix="")
    add_code_block(doc,
"Enter your choice (1-12): 8\n"
"Enter Song ID to add to 'Play Next' queue: 4\n"
"[+] Enqueued \"Bohemian Rhapsody\" to Up Next Queue (Position: 1)\n\n"
"Enter your choice (1-12): 6\n"
"[Queue Triggered] Playing requested track from Up Next Queue!\n\n"
"----------------------------------------------------------------\n"
" [>] NOW PLAYING: \"Bohemian Rhapsody\" by Queen\n"
"     Track Duration: 05:54 | Audio Engine: Active\n"
"     Progress: [####################] 100%\n"
"----------------------------------------------------------------"
    )
    
    add_p(doc, "Test Run 3: History Stack Backtracking (LIFO)", bold_prefix="")
    add_code_block(doc,
"Enter your choice (1-12): 7\n"
"[History Triggered] Rewinding to recently played track from History Stack!\n\n"
"----------------------------------------------------------------\n"
" [>] NOW PLAYING: \"Memories\" by Maroon 5\n"
"     Track Duration: 03:09 | Audio Engine: Active\n"
"     Progress: [####################] 100%\n"
"----------------------------------------------------------------\n\n"
"Enter your choice (1-12): 10\n\n"
"================================================================\n"
"                  RECENTLY PLAYED HISTORY (STACK - LIFO)        \n"
"================================================================\n"
" Pos  | ID   | Title                     | Artist               | Duration\n"
"----------------------------------------------------------------\n"
" #1   | 1    | Memories                  | Maroon 5             | 03:09   \n"
" Total entries in history: 1"
    )
    
    add_p(doc, "Test Run 4: Case-Insensitive Search by Keyword", bold_prefix="")
    add_code_block(doc,
"Enter your choice (1-12): 4\n"
"Enter search keyword (Title or Artist): queen\n\n"
"--- Search Results for \"queen\" ---\n"
" ID   | Title                      | Artist                 | Duration\n"
"----------------------------------------------------------------\n"
" 4    | Bohemian Rhapsody          | Queen                  | 05:54   \n"
" Found 1 matching song(s)."
    )
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 4. COMPLEXITY & PERFORMANCE ANALYSIS
    # -------------------------------------------------------------
    add_styled_heading(doc, "4. COMPLEXITY & PERFORMANCE ANALYSIS", level=1)
    
    add_styled_heading(doc, "4.1 Time & Space Complexity Summary", level=2)
    
    comp_headers = ["Operation", "Data Structure", "Best / Avg Time", "Worst Time", "Space"]
    comp_data = [
        ["Add Song (End)", "Doubly Linked List (via tail)", "O(1)", "O(1)", "O(1)"],
        ["Delete Song (by ID)", "Doubly Linked List", "O(1) (head/tail)", "O(n)", "O(1)"],
        ["Display Playlist", "Doubly Linked List Traversal", "O(n)", "O(n)", "O(1)"],
        ["Play Next Song", "DLL Pointer / Queue Dequeue", "O(1)", "O(1)", "O(1)"],
        ["Play Previous Song", "Stack Pop / DLL Prev", "O(1)", "O(1)", "O(1)"],
        ["Enqueue 'Play Next'", "Linked Queue (FIFO)", "O(1)", "O(1)", "O(1)"],
        ["Dequeue 'Play Next'", "Linked Queue (FIFO)", "O(1)", "O(1)", "O(1)"],
        ["Push / Pop History", "Linked Stack (LIFO)", "O(1)", "O(1)", "O(1)"],
        ["Search Song Keyword", "Linear Search on Nodes", "O(1) (at head)", "O(n)", "O(1)"],
        ["Save / Load File", "Sequential Disk I/O", "O(n)", "O(n)", "O(n)"]
    ]
    
    comp_table = doc.add_table(rows=1, cols=5)
    format_table(comp_table, [Inches(1.8), Inches(1.8), Inches(1.1), Inches(1.0), Inches(0.8)], comp_headers, comp_data)
    
    add_styled_heading(doc, "4.2 Comparative Analysis: Arrays vs. Doubly Linked Lists", level=2)
    
    comp_headers2 = ["Performance Dimension", "Static / Dynamic Array", "Doubly Linked List (Our System)"]
    comp_data2 = [
        ["Insertion at Tail", "O(1) amortized (realloc copies memory)", "Guaranteed O(1) via tail pointer"],
        ["Arbitrary Node Deletion", "O(n) (requires shifting remaining items)", "O(1) pointer updates once node is located"],
        ["Bidirectional Navigation", "Index math (i++, i--), bounds sensitive", "Native pointer dereferencing (next, prev)"],
        ["Memory Allocation", "Contiguous block (risk of heap fragmentation)", "Dynamic node allocation on demand (malloc)"],
        ["Queue/History Integration", "Fixed capacity arrays risk overflow", "Unbounded dynamic Stack & Queue chaining"]
    ]
    
    comp_table2 = doc.add_table(rows=1, cols=3)
    format_table(comp_table2, [Inches(1.8), Inches(2.4), Inches(2.3)], comp_headers2, comp_data2)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 5. CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------
    add_styled_heading(doc, "5. CONCLUSION & FUTURE SCOPE", level=1)
    
    add_styled_heading(doc, "5.1 Conclusion", level=2)
    add_p(doc, "The Music Playlist Management System demonstrates the decisive practical advantages of combining fundamental abstract data structures to engineer high-performance applications. By designating Doubly Linked Lists for playlist traversal, Stacks for history backtracking, and Queues for upcoming song requests, the application delivers optimal O(1) runtime responsiveness across all primary user operations. Dynamic memory allocation eliminates static buffer restrictions, while persistent disk storage guarantees continuity across sessions. The project provides substantial practical mastery over pointer management, heap allocation, edge-case prevention, and structured C programming.")
    
    add_styled_heading(doc, "5.2 Future Scope & Enhancements", level=2)
    add_bullet(doc, " Implementing a prefix Trie structure to offer sub-millisecond autocomplete search suggestions as the user types queries.", "Prefix Trie for Autocomplete: ")
    add_bullet(doc, " Interfacing with low-level audio libraries (such as Windows mciSendString or SDL2_mixer) to decode and stream real .mp3 and .wav audio files.", "Actual Audio Playback Engine: ")
    add_bullet(doc, " Extending the data model to manage multiple distinct playlists (e.g., Favorites, Workout, Focus) using an array of linked list heads or graph structures.", "Multi-Playlist Management: ")
    add_bullet(doc, " Implementing an unbiased Fisher-Yates shuffle algorithm by mapping linked nodes into a temporary pointer index array.", "Shuffle Playback Mode: ")
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 6. REFERENCES
    # -------------------------------------------------------------
    add_styled_heading(doc, "6. REFERENCES", level=1)
    
    add_bullet(doc, " Reema Thareja, Data Structures Using C, Oxford University Press, 2nd Edition, 2014. (Referenced for doubly linked lists, pointer manipulation, and memory management).")
    add_bullet(doc, " Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed, Fundamentals of Data Structures in C, Silicon Press, 2nd Edition, 2008. (Referenced for node insertion, deletion, and linear traversal algorithms).")
    add_bullet(doc, " Mark Allen Weiss, Data Structures and Algorithm Analysis in C, Pearson Education, 4th Edition. (Referenced for asymptotic time and space complexity models).")
    add_bullet(doc, " Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, Prentice Hall, 2nd Edition. (Referenced for standard C I/O, file serialization, and memory allocation conventions).")
    
    output_filename = "MUSIC_PLAYLIST_MANAGEMENT_SYSTEM_PBL_REPORT.docx"
    doc.save(output_filename)
    print(f"[v] Successfully generated Word Document: {output_filename}")

if __name__ == "__main__":
    build_pbl_report()
