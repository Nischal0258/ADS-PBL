import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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
    
    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
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
    
    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
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
    
    add_p(doc, "I express my heartfelt gratitude to my respected project guide, Mrs. K. Padmaja, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, continuous encouragement, and constructive feedback throughout the course of this Project-Based Learning (PBL) activity. Her insights into data structures and software engineering principles were pivotal in successfully designing and implementing this system.")
    
    add_p(doc, "I extend my sincere thanks to Dr. E. Ravindra, Professor and Head of the Department of Computer Science and Engineering, for his constant administrative support and for providing the modern computing and laboratory facilities necessary to complete this project.")
    
    add_p(doc, "Special thanks are also due to the laboratory instructors, faculty members, and my peers for their valuable discussions, cooperative assistance, and constructive suggestions during the testing phases.")
    
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
        ["3", "Implementation & Source Code", "9"],
        ["", "3.1 Algorithmic Design of Core Modules", "9"],
        ["", "3.2 Complete C Source Code", "10"],
        ["", "3.3 Sample Input and Output Test Runs", "16"],
        ["4", "Complexity & Performance Analysis", "18"],
        ["", "4.1 Time & Space Complexity Summary", "18"],
        ["", "4.2 Comparative Analysis: Arrays vs. Doubly Linked Lists", "19"],
        ["5", "Conclusion & Future Scope", "20"],
        ["6", "References", "21"]
    ]
    
    toc_table = doc.add_table(rows=1, cols=3)
    format_table(toc_table, [Inches(0.8), Inches(4.7), Inches(0.9)], ["S.No.", "Topic / Chapter", "Page No."], toc_data)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    add_styled_heading(doc, "1. INTRODUCTION", level=1)
    
    add_styled_heading(doc, "1.1 About the Project", level=2)
    add_p(doc, "The Music Playlist Management System is a streamlined console software application engineered in the C programming language. It is designed to demonstrate how fundamental data structures—specifically Doubly Linked Lists and Stacks—are applied to solve real-world music organization and playback challenges. Commercial audio streaming platforms such as Spotify and Apple Music manage vast music libraries, serving dynamic playlist modifications and playback histories. This project reproduces the internal mechanics of playlist management from first principles in C, using manual pointer operations and dynamic memory allocation.")
    
    add_styled_heading(doc, "1.2 Motivation & Real-World Problem Statement", level=2)
    add_p(doc, "In simple implementations, song collections are often placed in fixed or dynamic arrays. However, arrays present significant limitations for playlist applications:")
    add_bullet(doc, " Inserting a new song into an array requires shifting elements sequentially in memory, costing O(n) time.", "Expensive Insertions: ")
    add_bullet(doc, " Deleting a song from an array leaves gaps or requires shifting all subsequent elements.", "Costly Deletions: ")
    add_bullet(doc, " Singly linked lists only support forward movement; inspecting previous elements requires restarting traversal from the head.", "Single-Direction Limitation: ")
    add_p(doc, "By implementing a Doubly Linked List, songs can be added to the playlist dynamically in O(1) time and deleted cleanly without shifting remaining elements. Concurrently, a Linked Stack records playback history (LIFO), allowing users to track previously played songs effortlessly.")
    
    add_styled_heading(doc, "1.3 Project Objectives and Expected Outcomes", level=2)
    add_p(doc, "Objectives:")
    add_bullet(doc, " To design and develop a console-based music playlist system in C using dynamic memory allocation (malloc and free).")
    add_bullet(doc, " To implement a Doubly Linked List supporting dynamic additions, deletions by ID, and clean playlist display.")
    add_bullet(doc, " To provide direct song search and playback by Song Title or Artist name.")
    add_bullet(doc, " To incorporate a Last-In-First-Out (LIFO) Stack that automatically logs previously played songs.")
    add_bullet(doc, " To provide file persistence to automatically load and save songs across executions.")
    
    add_p(doc, "Expected Outcomes:")
    add_bullet(doc, " A clean, intuitive, and responsive console application with a concise player controls menu.")
    add_bullet(doc, " Immediate playback display without unnecessary delays or artificial progress bars.")
    add_bullet(doc, " Practical verification of O(1) insertion, deletion, and stack operations.")
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 2. SYSTEM DESIGN & ARCHITECTURE
    # -------------------------------------------------------------
    add_styled_heading(doc, "2. SYSTEM DESIGN & ARCHITECTURE", level=1)
    
    add_styled_heading(doc, "2.1 System Architecture", level=2)
    add_p(doc, "The system follows a three-tier modular architecture ensuring clean separation of user input, playback logic, and data storage:")
    
    add_code_block(doc, 
"+-----------------------------------------------------------------------------+\n"
"|                          1. USER INTERFACE LAYER                            |\n"
"|     - Streamlined Console Menu (1-6)    - Clean Song Table Display          |\n"
"|     - Direct Title/Artist Search Input  - Instant Now Playing Banner        |\n"
"+-----------------------------------------------------------------------------+\n"
"                                      |\n"
"                                      v\n"
"+-----------------------------------------------------------------------------+\n"
"|                            2. LOGIC CONTROLLER                              |\n"
"|     - Playback Engine (Instant Play by Title / Artist)                      |\n"
"|     - Dynamic History Stack Tracker (LIFO auto-push on playback change)     |\n"
"|     - Case-Insensitive String Matcher (Sub-string search)                   |\n"
"|     - Node Insertion & Safe Pointer Deletion Management                     |\n"
"+-----------------------------------------------------------------------------+\n"
"                                      |\n"
"                                      v\n"
"+-----------------------------------------------------------------------------+\n"
"|                       3. DATA STRUCTURE & STORAGE LAYER                     |\n"
"|  +-------------------------------------+  +-------------------------------+ |\n"
"|  |   Doubly Linked List (Playlist)     |  |    History Stack (LIFO)       | |\n"
"|  | (head, tail, currentSong pointers)  |  |   (tracks played songs)       | |\n"
"|  +-------------------------------------+  +-------------------------------+ |\n"
"|                                      |                                      |\n"
"|                       Persistent Disk Storage (playlist.txt)                |\n"
"+-----------------------------------------------------------------------------+"
    )
    
    add_styled_heading(doc, "2.2 Functional Modules Description", level=2)
    add_bullet(doc, " Displays the list of songs with ID, Title, Artist, Duration (MM:SS), and active playing status.", "1. Display Playlist Module: ")
    add_bullet(doc, " Appends a new song to the end of the Doubly Linked List in O(1) time.", "2. Add Song Module: ")
    add_bullet(doc, " Locates a song by ID and unlinks its node safely from the Doubly Linked List.", "3. Delete Song Module: ")
    add_bullet(doc, " Searches for a song by title or artist keyword, updates the current playing track, pushes the previous song to the history stack, and displays the Now Playing banner instantly.", "4. Play Song by Title / Artist: ")
    add_bullet(doc, " Displays the stack of previously played songs in reverse chronological order (LIFO).", "5. View History Module: ")
    add_bullet(doc, " Persists the entire playlist into 'playlist.txt' upon exit and reloads it on startup.", "6. Save & Exit Module: ")
    
    add_styled_heading(doc, "2.3 Data Structures Selection & Technical Rationale", level=2)
    add_p(doc, "Structure 1: Doubly Linked List (Playlist)")
    add_p(doc, "Each node represents a song and contains pointers to both the next and previous songs:")
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
    
    add_p(doc, "Structure 2: History Stack (Recently Played - LIFO)")
    add_p(doc, "Whenever a new song is played, a reference to the previously playing song is pushed onto the stack. Selecting 'View Recently Played History' traverses this stack from top to bottom:")
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
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 3. IMPLEMENTATION & SOURCE CODE
    # -------------------------------------------------------------
    add_styled_heading(doc, "3. IMPLEMENTATION & SOURCE CODE", level=1)
    
    add_styled_heading(doc, "3.1 Algorithmic Design of Core Modules", level=2)
    
    add_p(doc, "Algorithm: Play Song by Title or Artist Keyword", bold_prefix="")
    add_code_block(doc,
"Input: Query string (Title or Artist)\n"
"Output: Updated currentSong and playback confirmation\n\n"
"1. If head == NULL: Print 'Playlist is empty' and Return.\n"
"2. Read Query string from user and trim trailing spaces.\n"
"3. Traverse Doubly Linked List starting from head:\n"
"       Compare Query with node->title and node->artist (case-insensitive).\n"
"       If match found: Set match = node and break loop.\n"
"4. If match == NULL: Print 'No song found matching query' and Return.\n"
"5. If currentSong != NULL and currentSong != match:\n"
"       pushHistory(currentSong)  // Save to LIFO Stack\n"
"6. currentSong = match\n"
"7. Print Now Playing banner with title, artist, and formatted duration."
    )
    
    add_styled_heading(doc, "3.2 Complete C Source Code", level=2)
    add_p(doc, "Below is the complete, self-contained C source code for the Music Playlist Management System:")
    
    with open("music_player.c", "r") as f:
        c_code_content = f.read()
    
    add_code_block(doc, c_code_content)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 3.3 SAMPLE OUTPUT
    # -------------------------------------------------------------
    add_styled_heading(doc, "3.3 Sample Input and Output Test Runs", level=2)
    add_p(doc, "The following transcripts show execution of the compiled program (music_player.exe) in Windows Console:")
    
    add_p(doc, "Test Run 1: Launch and Display Playlist", bold_prefix="")
    add_code_block(doc,
"  ===============================================================\n"
"  *             MUSIC PLAYLIST MANAGEMENT SYSTEM                *\n"
"  *          Data Structures Project-Based Learning (PBL)       *\n"
"  ===============================================================\n\n"
"+----------------------- PLAYER CONTROLS -----------------------+\n"
"|  1. Display Playlist                                          |\n"
"|  2. Add Song                                                  |\n"
"|  3. Delete Song by ID                                         |\n"
"|  4. Play Song by Title / Artist                               |\n"
"|  5. View Recently Played History                              |\n"
"|  6. Save & Exit Program                                       |\n"
"+---------------------------------------------------------------+\n"
" Enter your choice (1-6): 1\n\n"
"========================================================================================\n"
"                                     MUSIC PLAYLIST                                     \n"
"========================================================================================\n"
" No.  | ID   | Song Title                 | Artist                 | Duration | Status      \n"
"----------------------------------------------------------------------------------------\n"
" 1    | 1    | Memories                   | Maroon 5               | 03:09    |             \n"
" 2    | 2    | Blinding Lights            | The Weeknd             | 03:20    |             \n"
" 3    | 3    | Smooth Criminal            | Michael Jackson        | 04:17    |             \n"
" 4    | 4    | Bohemian Rhapsody          | Queen                  | 05:54    |             \n"
" 5    | 5    | Shape of You               | Ed Sheeran             | 03:53    |             \n"
"========================================================================================\n"
" Total Songs: 5"
    )
    
    add_p(doc, "Test Run 2: Play Song by Title / Artist", bold_prefix="")
    add_code_block(doc,
" Enter your choice (1-6): 4\n"
"Enter Song Title or Artist to play: Queen\n\n"
"================================================================\n"
" [>] NOW PLAYING: \"Bohemian Rhapsody\" by Queen\n"
"     Duration: 05:54 | Status: Playing\n"
"================================================================\n\n"
" Enter your choice (1-6): 4\n"
"Enter Song Title or Artist to play: Memories\n\n"
"================================================================\n"
" [>] NOW PLAYING: \"Memories\" by Maroon 5\n"
"     Duration: 03:09 | Status: Playing\n"
"================================================================"
    )
    
    add_p(doc, "Test Run 3: View Recently Played History (LIFO Stack)", bold_prefix="")
    add_code_block(doc,
" Enter your choice (1-6): 5\n\n"
"================================================================\n"
"                  RECENTLY PLAYED HISTORY (LIFO STACK)          \n"
"================================================================\n"
" Pos  | ID   | Title                     | Artist               | Duration\n"
"----------------------------------------------------------------\n"
" #1   | 4    | Bohemian Rhapsody         | Queen                | 05:54   \n"
" Total songs in history: 1\n\n"
" Enter your choice (1-6): 6\n\n"
"================================================================\n"
"       Thank you for using Music Playlist Management System!     \n"
"================================================================"
    )
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 4. COMPLEXITY ANALYSIS
    # -------------------------------------------------------------
    add_styled_heading(doc, "4. COMPLEXITY & PERFORMANCE ANALYSIS", level=1)
    
    add_styled_heading(doc, "4.1 Time & Space Complexity Summary", level=2)
    
    comp_headers = ["Operation", "Data Structure", "Best / Avg Time", "Worst Time", "Space"]
    comp_data = [
        ["Add Song (End)", "Doubly Linked List (via tail)", "O(1)", "O(1)", "O(1)"],
        ["Delete Song (by ID)", "Doubly Linked List", "O(1) (head/tail)", "O(n)", "O(1)"],
        ["Display Playlist", "Doubly Linked List Traversal", "O(n)", "O(n)", "O(1)"],
        ["Play Song (by Title/Artist)", "Linear Node Search", "O(1) (first item)", "O(n)", "O(1)"],
        ["Push to History Stack", "Linked Stack (LIFO)", "O(1)", "O(1)", "O(1)"],
        ["Display History Stack", "Linked Stack Traversal", "O(k)", "O(k)", "O(1)"],
        ["Save / Load Playlist File", "Sequential Disk I/O", "O(n)", "O(n)", "O(n)"]
    ]
    
    comp_table = doc.add_table(rows=1, cols=5)
    format_table(comp_table, [Inches(1.8), Inches(1.8), Inches(1.1), Inches(1.0), Inches(0.8)], comp_headers, comp_data)
    
    add_styled_heading(doc, "4.2 Comparative Analysis: Arrays vs. Doubly Linked Lists", level=2)
    
    comp_headers2 = ["Performance Dimension", "Static / Dynamic Array", "Doubly Linked List (Our System)"]
    comp_data2 = [
        ["Insertion at Tail", "O(1) amortized (realloc copies memory)", "Guaranteed O(1) via tail pointer"],
        ["Arbitrary Node Deletion", "O(n) (requires shifting remaining items)", "O(1) pointer updates once node is located"],
        ["Bidirectional Navigation", "Index math (i++, i--), bounds sensitive", "Native pointer dereferencing (next, prev)"],
        ["Memory Allocation", "Contiguous block (risk of heap fragmentation)", "Dynamic node allocation on demand (malloc)"]
    ]
    
    comp_table2 = doc.add_table(rows=1, cols=3)
    format_table(comp_table2, [Inches(1.8), Inches(2.4), Inches(2.3)], comp_headers2, comp_data2)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 5. CONCLUSION & FUTURE SCOPE
    # -------------------------------------------------------------
    add_styled_heading(doc, "5. CONCLUSION & FUTURE SCOPE", level=1)
    
    add_styled_heading(doc, "5.1 Conclusion", level=2)
    add_p(doc, "The Music Playlist Management System provides a clean, practical demonstration of core data structures applied to music organization. By utilizing a Doubly Linked List for dynamic song storage and a Stack for tracking recently played history, the system eliminates the rigid memory constraints and element-shifting penalties of standard arrays. Operations such as adding tracks, deleting songs, and recording playback history are executed with optimal algorithmic efficiency. The project delivers hands-on mastery of dynamic memory management, pointer manipulation, and structured programming in C.")
    
    add_styled_heading(doc, "5.2 Future Scope & Enhancements", level=2)
    add_bullet(doc, " Implementing a prefix Trie structure to offer sub-millisecond autocomplete suggestions as the user types queries.", "Prefix Trie for Autocomplete: ")
    add_bullet(doc, " Connecting with audio libraries such as Windows mciSendString or SDL2 to directly play MP3 or WAV audio files.", "Audio Output Engine: ")
    add_bullet(doc, " Adding support for multiple user-defined playlists (e.g. Favorites, Study) using a list of linked lists.", "Multiple Playlists: ")
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # 6. REFERENCES
    # -------------------------------------------------------------
    add_styled_heading(doc, "6. REFERENCES", level=1)
    
    add_bullet(doc, " Reema Thareja, Data Structures Using C, Oxford University Press, 2nd Edition, 2014.")
    add_bullet(doc, " Ellis Horowitz, Sartaj Sahni, and Susan Anderson-Freed, Fundamentals of Data Structures in C, Silicon Press, 2nd Edition, 2008.")
    add_bullet(doc, " Mark Allen Weiss, Data Structures and Algorithm Analysis in C, Pearson Education, 4th Edition.")
    add_bullet(doc, " Brian W. Kernighan and Dennis M. Ritchie, The C Programming Language, Prentice Hall, 2nd Edition.")
    
    output_filename = "MUSIC_PLAYLIST_MANAGEMENT_SYSTEM_PBL_REPORT.docx"
    doc.save(output_filename)
    print(f"[v] Successfully generated Word Document: {output_filename}")

if __name__ == "__main__":
    build_pbl_report()
