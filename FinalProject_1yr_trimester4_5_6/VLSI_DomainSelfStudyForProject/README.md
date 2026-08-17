**VLSI for 1D-CNN Timing Prediction: To-Do Study List**

**Phase 1: Basic Digital Logic (2-3 Hours)**

* [ ] **Watch:** [CrashCourse Computer Science (Episodes 3 & 4)](https://robohub.org/crash-course-computer-science-video-series/)
* *Goal:* Understand basic logic gates, transistors, and registers.


* [ ] **Watch:** [Neso Academy Digital Electronics Playlist](https://play.google.com/store/apps/details?id=org.nesoacademy&hl=en_IN) (also discussed on [Reddit](https://www.reddit.com/r/computerscience/comments/9s23e8/lets_post_all_the_free_courses_and_content_about/))
* *Goal:* Focus specifically on Combinational (MUX, Decoders) and Sequential circuits (Flip-Flops, Latches).



**Phase 2: Static Timing Analysis & Flow (Weekend)**

* [ ] **Complete:** [Static Timing Analysis I & II by VSD](https://www.udemy.com/course/vlsi-academy-sta-checks/) on Udemy
* *Goal:* Master Setup/Hold time, Slack, and Data Arrival Paths.


* [ ] **Watch:** [ASIC Digital Design Flow / RTL-to-GDSII by VSD](https://www.instagram.com/reel/DZfGUJ9h2Di/)
* *Goal:* Understand how code turns into placed gates on a 2D layout.



**Phase 3: Data & Feature Extraction (1-2 Hours)**

* [ ] **Watch:** OpenLane / OpenROAD Tutorials by Google Open Source / Matt Venn on YouTube
* *Goal:* See how netlists, $(x, y)$ gate coordinates, and Manhattan wire lengths are extracted for your CNN dataset.



**Core Mental Model to Keep in Mind:**
Treat every hardware timing path as a 1D sequence for your CNN:
`[Flip-Flop A] ➔ [Wire 1] ➔ [NAND Gate] ➔ [Wire 2] ➔ [Buffer] ➔ [Flip-Flop B]`