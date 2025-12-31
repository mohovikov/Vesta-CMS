from enum import Enum

class PostStatus(str, Enum):
    MODERATION = "moderation"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"