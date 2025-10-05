Please look through the Claude Code Documentation and analyse the current system we have

this is what we have now - https://docs.claude.com/en/docs/claude-code/sub-agents

I want to setup hooks - https://docs.claude.com/en/docs/claude-code/hooks-guide
research and suggest hooks we could setup.
look at - https://docs.claude.com/en/docs/claude-code/github-actions, can we use this?

I want to add the capabilities and what is useful to  Claude.md or a report i can refer too 

setup hooks for
- always start a workflow with Glenn
- once a file has been added to the client folder > convert it to richtext and create a .docx file
- Are we able to use rclone to copy these .docx files into a shared drive on Google drive into a specific folder

Setup a tool to convert markdown to Rich text and save markdown files into .docx. These .docx should be rich text and easy to read, no HTML.

I want to setup a tool that scrapes sites with scrapy and provides a cvs with the data what is needed, or JSON if the data is only need internal with agents
User options would be 
SEO Meta Data: includes URL, Page Title, Meta Description and H1 
Full Scraped Data: includes URL Page Title, Meta Description, H1, Content seperated by HTML, strip out any other data that is not needed

Examples of uses for both
SEO: User wants to update the SEO on a page or website, User wants to know the SEO on a page or website
Full Scrape: user wants to update the current content on the site 

Make sure it is using serpAPI (I konw its not), Playwright MCP, scrapy - glenn should create a plan of what agents to use and which tool can be used

Setup Jina MCP - https://github.com/jina-ai/MCP and configue the system to use it, there is a Jina API in the .env already (which is not getting used but it should)

Content Plans workflow should 
include an audience style guide
User Journey
Whats trending in that niche
must research pillar pages and content hubs even if just wanting a content calendar. A content Calendar should include Time of year, which content hub the blog is for and a high level bullets on whats on that post
what percentage each type of content should the content plan focus on
