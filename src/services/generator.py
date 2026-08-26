from src.models import Platform

def generate_caption(source_text: str, platform: Platform) -> str:
    """
    Generate a platform-specific caption from the source text.
    This is a template-based generator (no AI required).
    """
    # Truncate text for preview
    preview = source_text[:100] + "..." if len(source_text) > 100 else source_text
    
    if platform == Platform.INSTAGRAM:
        return f"🌟 Check this out!\n\n{preview}\n\n#social #content #blog"
    
    elif platform == Platform.X:
        return f"{source_text[:250]}… Read more: [link]"
    
    elif platform == Platform.LINKEDIN:
        return f"📄 New blog post\n\n{source_text[:300]}…\n\nWhat are your thoughts? #leadership #innovation"
    
    return preview
