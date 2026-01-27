from .agent import CodexAgent

class MarketingAgent(CodexAgent):
    """
    Agent specialized in content creation, SEO, and social media strategy.
    """
    def __init__(self):
        super().__init__()
        self.role = "Marketing Expert"

    def write_blog_post(self, topic: str, audience: str) -> str:
        """
        Generates a complete blog post optimized for SEO.
        """
        prompt = f"""
        TASK: Write a high-quality blog post.
        TOPIC: {topic}
        TARGET AUDIENCE: {audience}
        
        STRUCTURE:
        1. Catchy Title
        2. Introduction (Hook)
        3. Key Points (Subheadings)
        4. Conclusion
        5. Call to Action
        
        TONE: Professional, engaging, and authoritative.
        """
        return self.chat(prompt)

    def social_media_post(self, platform: str, content_context: str) -> str:
        """
        Generates a social media post for a specific platform.
        """
        prompt = f"""
        TASK: Write a {platform} post.
        CONTEXT: {content_context}
        
        REQUIREMENTS:
        - Appropriate length for {platform}.
        - Use emojis/hashtags if typical for {platform}.
        - Engaging hook.
        """
        return self.chat(prompt)
