# IIT Madras Web MTech (Industrial AI) 2025

Notes during my Web MTech (AI) at IIT Madras.  Web MTech is an Executive course to be done along with job.
Company MoU (Memorandum of Understanding) or LoS (Letter of Support) is mandatory, otherwise learners can exit with PG Diploma.

Instead of GATE exam scores that are required for admission to regular MTech, 
for web MTech an internal entrance exam of IIT Madras is conducted.

**NOTE**: most files are text, but some are videos. GIT LFS is used to track these, so make sure to install it before cloning repo (eg. `sudo dnf install git-lfs` on Fedora linux).

### TODO

NOTE: There's a minor rendering bug in Markdown Convert extension - it renders $\hat{y}$ (`\hat{y}`) with the "hat" too low over y so that it's overlapping and hard to read.
Seems to affect only this, so workaround is to just use some other notation like $y_{predict}$.

Scrape from course portals - module lecture slides PDFs (currently downloading them manually).

Automate (pre-made solution or else program myself) digitally doing Linear Algebra assignments:
* PDF -> markdown with OCR (images -> text eg. where question text in image), math expressions correctly rendered using MathJAX, and deleting any unicode (invisible?) characters
* ChatGPT output has math in latex expressions, convert to MathJAX inside Markdown 
  (eg. `(`, `)`, --> `$`, `[`, `]` --> `$$`, `\` (when followed by newline) --> `\\`)
* GenAI automate (maybe via new MCP server in VS Code?) (NOTE OpenAI doesn't have free tier for API calling but Gemini does - try it at https://aistudio.google.com/) :
    * verify my (question, answer)(s)
    * cheat (hopefully rarely!): get solutions for all questions

NOTE: when just putting multiple questions to solve to ChatGPT in single prompt, it always misses out on some questions, probably due to its context length (TODO: check how much?).
But I have tried same with Gemini - it's much better, doesn't forget any question (probably has bigger context length). So shouldn't be an issue.

But Gemini has its own major problem -- you can't copy its math expressions!! 
Unlike Chatgpt, which generates Latex that can be copied easily, Gemini instead generates some code to actually render the math, with result being it's useless when you need to actually copy its output (obviously all my math questions have math expressions!!).

I observed that when I tell it explicitly NOT to render answer but instead generate my answer as markdown code having embedded mathjax - 
ChatGPT follows instructions, Gemini completely ignores it.
 
## TODO: General Brush Up (Topics I don't really understand, need to impl from scratch)

* RNN (Recurrent Neural Network) [it also has an attention mechanism]
* Transformer

## Main Course Material

Table of all courses (core & elective) with credits info for all trimesters is available at https://code.iitm.ac.in/artificial-intelligence in *Course Curriculum* tab.

- [Trimester 1: September - December 2025](trimester1/)
- [Trimester 2: January - April 2026](trimester2/)

### Course Grades

Grade Code | Grade Points | Remarks
---------- | ------------ | ---------
S          | 10           | _
A          |  9           | _
B          |  8           | _
C          |  7           | _
D          |  6           | _
E          |  4           | _
U          |  0           | _
P          |  0           | Pass
F          |  0           | Fail
I          |  0           | Course incomplete / with hold

**Grades 'S' to 'E' indicate successful completion of course.**

Total CGPA of a semester is calculated as average of course grade points $GP_i$, weighted by course credits $C_i$:

$$CGPA = \frac{\sum (C_i \times GP_i)}{\sum C_i}$$

## IITM Links

For any help / queries, send email at webmtech@code.iitm.ac.in .

* Example roll number: DA25M518 - here 25 stands for year 2025, M stands for MTech (other option being P for students who opted for PG Diploma).
* Smail (student email id) example: da25m518@smail.iitm.ac.in -- i.e. ROLL_NUMBER@smail.iitm.ac.in

### Public IITM Links (any logins are with personal email)
* AI Course Structure, Entrance Exam, etc.: https://code.iitm.ac.in/artificial-intelligence/
* Apply at: https://code.iitm.ac.in/webmtech/
* Fill personal details in form (after clearing entrance exam and being nominated by company): https://forms.study.iitm.ac.in/
* [Term 1 Registration & Fees Guide 2025](https://docs.google.com/document/d/10lF62VJSPmCi2U7WuYcMctIIrS_WTwc55nXv6H1DuZg/edit?usp=drive_link)
* [Student Handbook (Google Doc)](https://docs.google.com/document/d/e/2PACX-1vSC8Bh--zcS5pZ_qgUbjBq029vGzvHVbeqENMIiVp0n-WsvdIdKb8pwse1jXLZsxdkCwb7SJVavx5HT/pub)

### IITM Login via Student LDAP Credentials (with IITM smail)
* Student Dashboard (overall): https://wmtech.code.iitm.ac.in/student_dashboard/
    * Midsem score (only total marks, no details) is shown (in small font!) in respective course cards at https://wmtech.code.iitm.ac.in/student_dashboard/current_courses
    * Above dashboard's courses page has links to each course site, url of the form: https://seek.onlinedegree.iitm.ac.in/courses/{COURSE_ID}/
    * *Cannot login to* https://app.onlinedegree.iitm.ac.in/auth/login (linked to as dashboard in seek course site) - not a big issue as main dashboard link above is working (wmtech).
* To upload all documents and get student ID card issued: [SSP (Student/Staff Services Portal)](https://ssp.iitm.ac.in/)
    * Email &lt;sspsupport@smail.iitm.ac.in&gt; if any issue in SSP Portal, eg. an uploaded document needs to be corrected after submision.
* ~~Fee portal (except first trimester): https://fees.iitm.ac.in/~~ - seems applicable for regular BTech students, not us Web MTech ones
    * Web MTech specific: After first trimester, login with smail Google account & do course registration + fee payment at https://wmtech.code.iitm.ac.in/student_dashboard/wmtech_course_registration
* Apply for Hostel (us web MTech students have to choose "Others Login" to apply for temporary stay): [IKollege](https://ikollege.iitm.ac.in/iitmhostel/)
* Office of Hostel Management: [CCW](https://ccw.iitm.ac.in/)
* Exams (mid-terms only, end-term is seperately held at exam centres): https://exams.study.iitm.ac.in/
* Complaints platform: https://cc.iitm.ac.in/
* Discussion by students & faculty: https://discourse.iitm.ac.in/
* IITM Student Support: https://study-supportdesk.freshdesk.com/support/login -- NOT SURE IF APPLICABLE TO Web MTech students
* Buy merchandise (cloths, stationary etc.) having IIT Madras logo at [Gift Shop](https://giftshop.iitm.ac.in/).
* IITM WiFi site (intranet only in campus): https://netaccess.iitm.ac.in/
* **IITM AI Research Lab**: https://ai4bharat.iitm.ac.in/ - work on LLMs (eg. specialized train on Indian languages) and other tech.


## General Misc Resources
* Subreddit [r/iitmadras](https://www.reddit.com/r/iitmadras/)
- Past Papers (various subjects, levels, years): https://acegrade.in/prev_papers -- math, stats, python, deep learning, etc.
- https://iitmdatascience.com/notes.html has some notes (no question papers) on math, python, ML etc. (though not sure of quality as haven't tried)
