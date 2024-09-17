# AIVE-Intro

This is the public development space to learn and work with the AIVE pipeline as part of the WEHI RCP internship program.

## Guidelines for working within the AIVE-Intro repo

Welcome to the AIVE project as part of the WEHI RCP internship!!

First of all, this repo is early in development and as such, there is minimal documentation available at this stage. The goal is for all students to contribute introduction materials so that new students can learn about AIVE and get up to date with the latest project developments.

All students are encouraged to ask yourself “What information was missing when I got here?” and feel free to write or update some documentation.  
This repo is specifically created to host your own code, documentation and development as an intern student on the AIVE project. There are several private repos that contain additional materials and draft code central to the AIVE project that you may reference. However, these materials should not be copied or reproduced within this repo itself. 

Keep in mind, this is a public space and your commits will be visible to other students on the project, but also to anyone in the world that visits this repo.
With that in mind, please double check any files that you plan to add to the repo. Ensure your commits are your own work and that any folders you include do not contain additional or unexpected files. Also take care to ensure you don’t accidentally include any sensitive personal information. 

This is a platform for learning - mistakes can happen and are expected! There is nothing that can’t be fixed, so when in doubt, just reach out.

## Branches
Each intake will have a dedicated branch to work on and contribute their code as a team. For many tasks, you might like to work together as a group to test your code in a local environment before uploading commits here. It is also expected that some code may be the result of collaborative efforts, inputs and verbal discussions. If this is the case, please allow all team members the ability to add final commits to the repo in an equitable manner.
Ideally, each student should end the semester with an individual commit history that they can use to demonstrate their contribution to the project.
At the conclusion of the intake, the branches will be merged onto the main branch via pull requests. These branches will not be deleted and will remain on the repo to allow new students to easily see the footprint of past teams.

## Commit standards
The AIVE project is a relatively new project and as such, there is no strict standard for commits. This is an area that you are welcome to contribute to as we develop this repo.
There are, however, a few key things to keep in mind when you do start contributing.

Commits help us track the progress of a project through development. They help identify what changes were made, when, and who contributed them. There are many varying standards when it comes to git commits. Exact standards will vary between projects, the users, and the nature of the work. Some projects have very strict regulations on submitting commits and pull requests. It is important to remember that many projects will have a different pattern and approach. 

### What makes a good commit?
In general, there are some good principles to follow in an open source collaboration. GitHub has some good guides and there are many blogs that discuss this elsewhere on the web. (If you find some good resources, feel free to update this section!)
To begin with, here are some ideas to consider when you add a commit to the AIVE project.

### Structure of a commit
When you submit a commit, you will have two components to add, in addition to your changes to the files themselves. These are the commit message, and the extended description. The commit message should be a brief phrase that describes the change. The description should also still be brief but should adequately summarise the nature of the commit. Depending on the change this may be one or two sentences. Some commits may be simple enough that just the commit message is enough information alone. If a new person read your commit message, would they know what to expect before they look at your code?
Granularity/singularity:
This principle refers to the size and specificity of a commit. Ideally, each commit is a small and specific workable step. This allows for easy tracking and merging of changes through the lifetime of the project. 
A single commit should be looked at independently. However, we don’t need a commit for every small change you make. For example, say you are updating the name of a variable that is referenced may times throughout your code. You can update all instances of the variable name in one go and submit it as single commit.

It can be tricky to find a good balance but an individual commit should include a single identifiable aim. For example: “Create a new function to process input A”, or “Correct an error in function B”.  
As a general rule, if you feel the need to add an “And” to your commit message, you may want to consider breaking it up. For example, instead of one commit that “Adds a new function A and fixes errors on line 127 of function B” you should split your changes into two separate commits. 

### Errors and corrections
As you are learning and working with =in the AIVE project you may find yourself testing and re-testing some code. Alternatively you may be working on some updates to the documentation. It can be tempting to only commit the final version of your work to the repo. Whilst we don't expect you to include all your tiny errors and corrections as you work, please consider submitting your commits before they are the "final" version. This helps you track your own progress and learning, and also allows others an insight into how a problem was solved. Perfect code is rare, but we can all learn by seeing how others approach an issue.

