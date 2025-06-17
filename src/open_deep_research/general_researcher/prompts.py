initial_upfront_model_provider_web_search_system_prompt = """You are a research assistant conducting deep research. Use the tools provided to thoroughly research what the user is asking about.

You can use websearch, or any other tool provided to you.
{mcp_prompt}

Focus on:
- Finding authoritative, comprehensive sources
- Covering multiple perspectives and aspects of the topic
- Using specific, targeted search queries
- Gathering sufficient information for a detailed report

Use multiple searches as needed to cover the topic thoroughly."""

follow_up_upfront_model_provider_web_search_system_prompt = """You are continuing deep research based on previous findings. Use the tools provided to fill knowledge gaps identified in the reflection.

You can use websearch, or any other tool provided to you.
{mcp_prompt}

Focus on areas that need deeper investigation. Use targeted searches to find missing information and perspectives.
"""

upfront_model_provider_reflection_system_prompt = """Analyze these research findings for completeness and depth with respect to the original messages asking about the topic:

Original Messages asking about the Topic: {messages}

Current Research Findings:
{findings}

Please evaluate:
1. Are the findings comprehensive enough for a detailed report to answer the question(s) in the original messages?
2. What key knowledge gaps or missing perspectives exist?
3. What specific areas need deeper investigation?
4. What follow-up research queries would be most valuable?

Respond in valid JSON format with these exact keys:
"is_satisfied": boolean,
"knowledge_gaps": ["gap1", "gap2", ...],
"suggested_queries": ["query1", "query2", ...],
"reasoning": "detailed explanation of the analysis"
"""


gap_context_prompt = """Knowledge gaps to address:
{knowledge_gaps}

Suggested focus areas:
{focus_areas}

Reasoning: {reasoning}

You only need to output net new information that we have not already gathered. This will get appended to the existing information.
"""

response_structure_instructions="""You are performing deep research to comprehensively answer a question that a user asked.

These are the messages that have been exchanged so far between yourself and the user:
<Messages>
{messages}
</Messages>

We have already gathered a lot of information from web searches about the topic. Here is a all of the information that we've gathered so far:
<Information gathered already>
{context}
</Information gathered already>


<Task>
Generate a list of sections for the answer to provide to the user. Your plan should be tight and focused with NO overlapping sections or unnecessary filler.
You can generate however many sections you are necessary, as these will be computed in parallel. If a user asks for a list of 10 items, you could generate 10 sections, for example.

The structure of your sections will really depend on the question that the user asked. 
This structure is important because you will be writing each section independently, so they should not have any dependence on each other.

You can structure your sections in a number of different ways. Here are some examples:

To answer a question that asks you to compare two things, you might structure your sections like this:
1/ intro
2/ overview of topic A
3/ overview of topic B
4/ comparison between A and B
5/ conclusion

To answer a question that asks you to return a list of things, you might only need a single section which is the entire list.
1/ list of things

Or, you could choose to make each item in the list a separate section. When asked for lists, you don't need an introduction or conclusion.
1/ item 1
2/ item 2
3/ item 3

To answer a question that asks you to summarize a topic, give a report, or give an overview, you might structure your sections like this:
1/ overview of topic
2/ concept 1
3/ concept 2
4/ concept 3
5/ conclusion

If you think you can answer the question with a single section, you can do that too!
1/ answer

REMEMBER: Section is a VERY fluid and loose concept. You can structure your sections however you think is best, including in ways that are not listed above!

Each section should have the fields:

- Name - Name for this section of the report.
- Description - A specific overview of what the section will be about. Do not be vague or general.

Integration guidelines:
- Ensure each section has a distinct purpose with no content overlap
- Combine related concepts rather than separating them
- CRITICAL: Every section MUST be directly relevant to the main topic
- Avoid tangential or loosely related sections that don't directly address the core topic

Before submitting, review your structure to ensure it has no redundant sections and follows a logical flow that answers the user's question in the best way possible.
</Task>

<Feedback>
Here is feedback on the report structure from review (if any):
{feedback}
</Feedback>

Return your outline in the following format as a list of sections!
<Format>
Call the Outline tool 
</Format>
"""

initial_section_write_instructions = """Write a first draft of this section based on the research that we have done so far.
<Task>
1. Review the messages describing the report request, the section name, and the section topic carefully.
2. Then, look at the provided information gathered from web searches. Not all of this information will be relevant to this section. Be particular about what information you use.
3. Write the report section. 
</Task>

<Writing Guidelines>
- Strict 150-200 word limit
- Use simple, clear language
- Use short paragraphs (2-3 sentences max)
- Use ## for section title (Markdown format)
- Do NOT ever refer to yourself as the writer of the report. This should be a professional report without any self-referential language. 
- Do not say what you are doing in the report. Just write the report without any commentary from yourself.
</Writing Guidelines>

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
</Citation Rules>

<Final Check>
1. Verify that EVERY claim is grounded in the provided Source material
2. Confirm each URL appears ONLY ONCE in the Source list
3. Verify that sources are numbered sequentially (1,2,3...) without any gaps
4. DO NOT include any commentary from yourself in the section. Just write the section. Do not say "I'm writing a section" or "I'll revise this section" or anything like that. Just include the report itself.
</Final Check>
"""


initial_section_write_inputs=""" 
These are the messages that have been exchanged so far from the user asking for the report:
<Messages>
{messages}
</Messages>

This is the section name:
<Section name>
{section_name}
</Section name>

This is the section description:
<Section description>
{section_description}
</Section description>

This is the information that you have gathered from web searches so far:
<Information gathered from web searches>
{context}
</Information gathered from web searches>
"""

follow_up_section_write_instructions = """Revise the section based on the feedback and the information gathered from web searches.

<Task>
1. Review the messages describing the report request, section name, and section topic carefully.
2. Review the existing section, as well as the feedback gathered to improve on the section.
3. Then, look at the new provided information gathered from web searches.
4. Decide the sources that you will use it to revise the section.
5. Revise the section and list your sources. 
</Task>

<Writing Guidelines>
- Synthesize the existing section with the new information gathered from web searches, according to the feedback.
- Strict 150-200 word limit
- Use simple, clear language
- Use short paragraphs (2-3 sentences max)
- Use ## for section title (Markdown format)
- Do NOT ever refer to yourself as the writer of the report. This should be a professional report without any self-referential language. 
- Do not say what you are doing in the report. Just write the report without any commentary from yourself.
</Writing Guidelines>

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Keep the existing sources in the section untouched, you can change the numbers if necessary.
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
</Citation Rules>

<Final Check>
1. Verify that EVERY claim is grounded in the provided Source material
2. Confirm each URL appears ONLY ONCE in the Source list
3. Verify that sources are numbered sequentially (1,2,3...) without any gaps
4. DO NOT include any commentary from yourself in the section. Just write the section. Do not say "I'm writing a section" or "I'll revise this section" or anything like that. Just include the report itself.
</Final Check>
"""

follow_up_section_write_inputs=""" 
These are the messages that have been exchanged so far from the user asking for the report:
<Messages>
{messages}
</Messages>

This is the section name:
<Section name>
{section_name}
</Section name>

This is the section description:
<Section description>
{section_description}
</Section description>

This is the existing section content:
<Existing section content>
{section_content}
</Existing section content>

This is the feedback on the section:
<Feedback on the section>
{feedback}
</Feedback on the section>

This is the information that you have gathered from web searches so that you can address that feedback:
<Information gathered from web searches>
{context}
</Information gathered from web searches>
"""

section_grader_instructions = """Review a section relative to the section description and user's messages:

These are the messages that have been exchanged so far from the user asking for the report:
<Messages>
{messages}
</Messages>

This is the section description:
<section description>
{section_description}
</section description>

This is the section content:
<section content>
{section_content}
</section content>

<task>
Evaluate whether the section content adequately addresses the section description.

If the section content does not adequately address the section description, generate {number_of_follow_up_queries} follow-up search queries to gather missing information.
</task>
"""

final_report_generation_prompt = """Based on all the research conducted, create a comprehensive, well-structured answer to the question(s) in these original messages: {messages}

Here are the findings from the research that you conducted:
{findings}

These are the additional sources that you found during research (reference these as appropriate as you write your response):
{source_list}

We iterated on a section outline for the answer to the question. Here is the outline, follow this as best as you can:
{outline}

Please create a detailed answer to the question(s) in the original messages that:
1. Follows the section outline as closely as possible
2. Is well-organized with proper headings (# for title, ## for sections, ### for subsections)
3. Includes specific facts and insights from the research
4. References relevant sources using [Title](URL) format
5. Provides a balanced, thorough analysis
6. Includes a "Sources" section at the end with all referenced links

For each section, do the following:
- Strict 150-200 word limit
- Use simple, clear language
- Use short paragraphs (2-3 sentences max)
- Use ## for section title (Markdown format)
- Do NOT ever refer to yourself as the writer of the report. This should be a professional report without any self-referential language. 
- Do not say what you are doing in the report. Just write the report without any commentary from yourself.

Format the report in clear markdown with proper structure and include source references where appropriate.

<Citation Rules>
- Assign each unique URL a single citation number in your text
- End with ### Sources that lists each source with corresponding numbers
- IMPORTANT: Number sources sequentially without gaps (1,2,3,4...) in the final list regardless of which sources you choose
- Example format:
  [1] Source Title: URL
  [2] Source Title: URL
</Citation Rules>"""