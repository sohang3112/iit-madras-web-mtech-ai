---
Author: Sohang
RollNo: DA25M622
CreationDate: 
ChangeDate: 
CurrentDate: 2026-08-06
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

<!-- NOTE: couldn't run Jmp software on linux. I registered for 1-month free trial, got download link in email after a while, it only had Windows and Mac so downloaded Windows exe and started it with `wine start path/to/exe` - but eventually it failed with some weird assert error with no way to fix. 

So TLDR: Can't use JMP
-->

**Author:** Sohang, **Roll No.:** DA25M622

## **CH5440W Assignment 2 Part 1** 

Individual Submissions; Submit a neat copy (handwritten or typed) 

## _a)_ _**Write the question number and subdivisions before the answer**_ 

- _b) Suggested to do numerical problems with Matlab/Excel/Python/JMP – Your_ 

   - _choice_ 

- _c)_ Mention all references used prominently in the answers 

- d) Deadline: 10[t] h August 2026 

**Question 1 [10+5+5]** 

We have learnt about PLS2 using NIPALS algorithm in the classes. 

- a) Discuss next on PLS1 algorithm using SIMPLS algorithm. 

- b) Bring out the difference between the two approaches 

- c) Explain where each approach is preferred/applied. 

## **Question 2 [4+2+2+2+2+2+3+3+3]** 

With reference to the NIPALS algorrithm dealt in class, answer the following questions in your own words 

- a) What is the difference between weights and loading? 

- b) Indicate how X and Y scores condense voluminous data involving multiple features 

- c) What is meant by deflation/reconstruction? 

- d) Explain the figure given below (reference to the diplomat thesis given in class) 

![](trimester3/CH5440W_MultiVariateAnalysis/assignments/Assignment2/CH5440W_Assignment2_Part1_images/CH5440W_Assignment2_Part1.pdf-0001-18.png)

e) To find weights **w** why do you use Y-scores **u** rather than **t** ? 

f) Why do you normalize the weights **w** using its norm? 

g) To find X scores, Why regress 𝐸' with 𝑤 𝑡' ? Should it not be 𝑝 𝑡' ? ℎ−1 ℎ ℎ ℎ ℎ 

- h) Explain the following steps in NIPALS PLS2 algorithm 

**Step 9:** Fit **t** h to the newly gained **p** h as 𝑡 = 𝑡 ‖𝑝 ‖ ℎ ℎ ℎ 

![](trimester3/CH5440W_MultiVariateAnalysis/assignments/Assignment2/CH5440W_Assignment2_Part1_images/CH5440W_Assignment2_Part1.pdf-0002-05.png)

- i) Why find by regression weights **w** for X residuals but loadings **q** for Y residuals? 

![](trimester3/CH5440W_MultiVariateAnalysis/assignments/Assignment2/CH5440W_Assignment2_Part1_images/CH5440W_Assignment2_Part1.pdf-0002-07.png)

**Question 3 [4+6+4]** 

- a) For facilitating your coding with Python and for a general understanding of the code’s workflow, neatly summarize the PLS2 algorithm step by step. 

- b) Solve the following problem without centering or scaling or standardizing 

- c) Report PRESS and root mean square PRESS 

- d) Compare and validate all your Matlab/Python answers with JMP ( **W,T,U,Q,P,Beta** , diagonal matrix **B,** Root Mean Square PRESS).  In JMP use “leave one out” option. 

- e) Show finally how the PLS2 led to predictions of the outcomes **Y** . 

**Note:** Use 3 factors 

![](trimester3/CH5440W_MultiVariateAnalysis/assignments/Assignment2/CH5440W_Assignment2_Part1_images/CH5440W_Assignment2_Part1.pdf-0003-00.png)

**Question 4 [10]** 

For the big data set (Gasoline.xls) carry out PLS2 analysis and find the model coefficients beta, **W,T,U,Q, P** and **B** .
