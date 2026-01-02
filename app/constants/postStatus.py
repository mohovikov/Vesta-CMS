from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    MODERATION = "moderation"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"

    def __str__(self):
        return str(self.value)