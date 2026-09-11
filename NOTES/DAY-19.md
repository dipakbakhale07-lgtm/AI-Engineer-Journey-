# DAY 19 — Build the Drafting Pipeline

## Goal

Generate different post styles from the same real facts using a Python script.

## What I Learned

### 1. Drafting Pipeline

A drafting pipeline takes structured content inputs and turns them into a social media post draft.

The basic flow is:

Content Input
↓
Prompt Template
↓
AI Draft
↓
Different Post Versions
↓
Factual Checking
↓
Human Review

### 2. Prompt Template

A prompt template gives the AI a fixed structure for generating content.

The required output should contain:

- Hook
- 5–8 line body
- Lesson
- Optional Call to Action
- Hashtags

### 3. Simple English

The generated posts should use simple English so that the content is easy to understand.

### 4. Three Versions

The same real information should be converted into three different styles:

1. Technical
2. Beginner-friendly
3. Short

The facts should remain the same in all three versions.

### 5. Factual Consistency

Every factual claim must be checked against my notes and actual project work.

The AI should not add:

- Invented experiences
- Unsupported facts
- Exaggerated achievements
- Claims that I did not actually make

### 6. Human Review

The drafting pipeline prepares content.

It does not automatically publish anything.

Human review remains necessary before publishing.

## What I Practiced

I practiced designing a Python-based drafting workflow that can:

1. Read a structured content input.
2. Use one prompt template.
3. Generate the required post structure.
4. Create three versions of the same topic.
5. Keep the facts consistent.
6. Allow the final content to be reviewed manually.

## Expected Output

A working draft generator script and three versions of one topic:

- Technical version
- Beginner-friendly version
- Short version

## Self-Check

- [ ] Python drafting script works
- [ ] One prompt template is used
- [ ] Hook is generated
- [ ] 5–8 line body is generated
- [ ] Lesson is generated
- [ ] Optional CTA is generated
- [ ] Hashtags are generated
- [ ] Technical version created
- [ ] Beginner-friendly version created
- [ ] Short version created
- [ ] Facts checked against notes
- [ ] No exaggeration
- [ ] No automatic publishing

## Day 19 Result

The Social Media Assistant now has a drafting pipeline that can transform the same real project information into multiple post styles while keeping the underlying facts consistent.